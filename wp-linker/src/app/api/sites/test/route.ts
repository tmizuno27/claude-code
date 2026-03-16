import { NextRequest, NextResponse } from "next/server";
import { WPClient } from "@/lib/wp-client";

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
