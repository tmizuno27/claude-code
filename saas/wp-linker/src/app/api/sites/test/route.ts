import { NextRequest, NextResponse } from "next/server";
import { WPClient } from "@/lib/wp-client";
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

    const { rest_api_url, username, app_password } = await req.json();

    if (!rest_api_url || !username || !app_password) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    const client = new WPClient(rest_api_url, username, app_password);
    const info = await client.testConnection();

    return NextResponse.json({
      success: true,
      site_name: info.name,
      site_url: info.url,
    });
  } catch (error: unknown) {
    const message =
      error instanceof Error
        ? `${error.message}${error.cause ? ` (cause: ${error.cause})` : ""}`
        : "Connection failed";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
