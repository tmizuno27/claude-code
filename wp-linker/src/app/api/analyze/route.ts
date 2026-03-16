import { NextRequest, NextResponse } from "next/server";
import { WPClient } from "@/lib/wp-client";
import { analyzeInternalLinks } from "@/lib/linker-engine";

export async function POST(req: NextRequest) {
  try {
    const { rest_api_url, username, app_password } = await req.json();

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

    return NextResponse.json({
      success: true,
      total_posts: result.totalPosts,
      orphan_posts: result.orphanPosts,
      suggestions: result.suggestions,
      summary: {
        total_suggestions: result.suggestions.length,
        orphan_count: result.orphanPosts.length,
        coverage: Math.round(
          ((result.totalPosts - result.orphanPosts.length) /
            result.totalPosts) *
            100
        ),
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Analysis failed" },
      { status: 500 }
    );
  }
}
