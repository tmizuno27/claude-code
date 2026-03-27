import { NextRequest, NextResponse } from "next/server";
import { WPClient } from "@/lib/wp-client";
import { buildRelatedLinksHtml } from "@/lib/linker-engine";
import { createServerSupabaseClient } from "@/lib/supabase-server";
import type { LinkSuggestion } from "@/lib/types";

const LINK_SECTION_MARKER = "<!-- wp-linker-internal-links -->";

export async function POST(req: NextRequest) {
  try {
    // Authentication check
    const supabase = await createServerSupabaseClient();
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      return NextResponse.json(
        { error: "Authentication required" },
        { status: 401 }
      );
    }

    const { rest_api_url, username, app_password, suggestions } =
      (await req.json()) as {
        rest_api_url: string;
        username: string;
        app_password: string;
        suggestions: LinkSuggestion[];
      };

    if (!rest_api_url || !username || !app_password || !suggestions?.length) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    const client = new WPClient(rest_api_url, username, app_password);

    // Group suggestions by source post
    const grouped = new Map<number, LinkSuggestion[]>();
    for (const s of suggestions) {
      const list = grouped.get(s.source_post_id) ?? [];
      list.push(s);
      grouped.set(s.source_post_id, list);
    }

    // Fetch current content for each source post and apply links
    const posts = await client.fetchAllPosts();
    const results: { post_id: number; status: string }[] = [];

    for (const [postId, links] of grouped) {
      const post = posts.find((p) => p.id === postId);
      if (!post) {
        results.push({ post_id: postId, status: "not_found" });
        continue;
      }

      let content = post.content.rendered;

      // Remove existing wp-linker section
      const markerIdx = content.indexOf(LINK_SECTION_MARKER);
      if (markerIdx !== -1) {
        content = content.substring(0, markerIdx).trimEnd();
      }

      // Append new related links
      const relatedHtml = buildRelatedLinksHtml(
        links.map((l) => ({ title: l.target_title, url: l.target_url }))
      );
      content += relatedHtml;

      try {
        await client.updatePostContent(postId, content);
        results.push({ post_id: postId, status: "updated" });
      } catch (err) {
        results.push({
          post_id: postId,
          status: `error: ${err instanceof Error ? err.message : "unknown"}`,
        });
      }
    }

    return NextResponse.json({
      success: true,
      results,
      updated: results.filter((r) => r.status === "updated").length,
      errors: results.filter((r) => r.status.startsWith("error")).length,
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Apply failed" },
      { status: 500 }
    );
  }
}
