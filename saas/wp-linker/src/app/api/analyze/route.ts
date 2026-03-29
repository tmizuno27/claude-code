import { NextRequest, NextResponse } from "next/server";
import { WPClient } from "@/lib/wp-client";
import { analyzeInternalLinks } from "@/lib/linker-engine";
import { createServerSupabaseClient } from "@/lib/supabase-server";

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

    const { rest_api_url, username, app_password, site_id } = await req.json();

    if (!rest_api_url || !username || !app_password) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    const client = new WPClient(rest_api_url, username, app_password);
    const posts = await client.fetchAllPosts();

    if (posts.length === 0) {
      return NextResponse.json(
        { error: "No published posts found" },
        { status: 404 }
      );
    }

    const result = analyzeInternalLinks(posts, 3);

    const summary = {
      total_suggestions: result.suggestions.length,
      orphan_count: result.orphanPosts.length,
      coverage: Math.round(
        ((result.totalPosts - result.orphanPosts.length) /
          result.totalPosts) *
          100
      ),
    };

    // Save analysis to Supabase if user is authenticated and site_id provided
    let analysis_id: string | null = null;
    if (site_id) {
      try {
          const { data: saved } = await supabase
            .from("analyses")
            .insert({
              site_id,
              user_id: user.id,
              total_posts: result.totalPosts,
              orphan_count: summary.orphan_count,
              suggestions_count: summary.total_suggestions,
              applied_count: 0,
              coverage: summary.coverage,
              report: {
                orphan_posts: result.orphanPosts,
                post_stats: result.postStats,
                suggestions: result.suggestions,
              },
            })
            .select("id")
            .single();
          if (saved) analysis_id = saved.id;
      } catch {
        // Non-critical: continue even if save fails
      }
    }

    return NextResponse.json({
      success: true,
      analysis_id,
      total_posts: result.totalPosts,
      orphan_posts: result.orphanPosts,
      post_stats: result.postStats,
      suggestions: result.suggestions,
      summary,
    });
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : "Analysis failed";
    // Classify WP API auth errors as 401 for better UX
    const status =
      message.includes("401") || message.toLowerCase().includes("unauthorized")
        ? 401
        : 500;
    return NextResponse.json({ error: message }, { status });
  }
}
