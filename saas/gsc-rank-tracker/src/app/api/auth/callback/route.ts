import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

export const GET = async (request: NextRequest) => {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const plan = searchParams.get("plan") ?? "free";

  if (!code) {
    return NextResponse.redirect(`${origin}/login?error=missing_code`);
  }

  const supabase = await createClient();
  const { data, error } = await supabase.auth.exchangeCodeForSession(code);

  if (error || !data.session) {
    console.error("Auth callback error:", error);
    return NextResponse.redirect(`${origin}/login?error=auth_failed`);
  }

  // Google OAuthの場合、GSCスコープのトークンを users テーブルに保存
  const providerToken = data.session.provider_token;
  const providerRefreshToken = data.session.provider_refresh_token;

  if (providerToken) {
    await supabase
      .from("users")
      .update({
        gsc_access_token: providerToken,
        gsc_refresh_token: providerRefreshToken ?? null,
      })
      .eq("id", data.session.user.id);
  }

  // プランがfree以外の場合はStripe決済ページへリダイレクト（Week 4で実装）
  if (plan !== "free") {
    return NextResponse.redirect(
      `${origin}/dashboard?welcome=true&plan=${plan}`
    );
  }

  return NextResponse.redirect(`${origin}/dashboard?welcome=true`);
};
