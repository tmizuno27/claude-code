import { redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

export default async function DashboardPage() {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  // ユーザーのサイト一覧を取得
  const { data: sites } = await supabase
    .from("sites")
    .select("*")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false });

  // ユーザー情報取得
  const { data: userData } = await supabase
    .from("users")
    .select("plan, gsc_access_token")
    .eq("id", user.id)
    .single();

  const hasGscConnected = !!userData?.gsc_access_token;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <span className="text-xl">📊</span>
              <span className="font-bold text-gray-900">
                GSC Rank Tracker<span className="text-brand-600"> Pro</span>
              </span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                {user.email}
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-brand-100 text-brand-700 capitalize">
                {userData?.plan ?? "free"}
              </span>
              <form action="/api/auth/signout" method="POST">
                <button
                  type="submit"
                  className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                >
                  ログアウト
                </button>
              </form>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* GSC未連携の場合の案内 */}
        {!hasGscConnected && (
          <div className="mb-8 p-6 bg-amber-50 border border-amber-200 rounded-2xl flex items-start gap-4">
            <span className="text-2xl">🔗</span>
            <div className="flex-1">
              <h3 className="font-bold text-amber-900 mb-1">
                Google Search Consoleを接続してください
              </h3>
              <p className="text-amber-700 text-sm mb-4">
                GSCアカウントを接続するとデータの自動取得が始まります。
                Googleアカウントでログインするとそのまま連携できます。
              </p>
              <Link
                href="/login"
                className="inline-flex items-center px-4 py-2 bg-amber-600 text-white rounded-lg text-sm font-medium hover:bg-amber-700 transition-colors"
              >
                Googleアカウントで再ログイン →
              </Link>
            </div>
          </div>
        )}

        {/* サイトが0件の場合 */}
        {sites?.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🌐</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              最初のサイトを追加しましょう
            </h2>
            <p className="text-gray-600 mb-8 max-w-md mx-auto">
              監視したいサイトのGSCプロパティURLを追加すると、
              毎日自動でデータを取得・保存します。
            </p>
            <Link
              href="/dashboard/sites/new"
              className="inline-flex items-center px-6 py-3 bg-brand-600 text-white rounded-xl font-semibold hover:bg-brand-700 transition-colors"
            >
              + サイトを追加
            </Link>
          </div>
        ) : (
          <>
            {/* サイト一覧 */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">管理サイト一覧</h2>
              <Link
                href="/dashboard/sites/new"
                className="inline-flex items-center px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium hover:bg-brand-700 transition-colors"
              >
                + サイトを追加
              </Link>
            </div>

            <div className="grid gap-4">
              {sites?.map((site) => (
                <div
                  key={site.id}
                  className="bg-white rounded-2xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-xl bg-brand-100 flex items-center justify-center text-2xl">
                        🌐
                      </div>
                      <div>
                        <h3 className="font-bold text-gray-900">{site.domain}</h3>
                        <p className="text-sm text-gray-500">{site.gsc_property_url}</p>
                        <p className="text-xs text-gray-400 mt-0.5">
                          {site.last_synced_at
                            ? `最終同期: ${new Date(site.last_synced_at).toLocaleString("ja-JP")}`
                            : "まだ同期されていません"}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          site.is_active
                            ? "bg-green-100 text-green-700"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {site.is_active ? "● 監視中" : "停止中"}
                      </span>
                      <Link
                        href={`/dashboard/sites/${site.id}`}
                        className="px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        詳細を見る →
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {/* プランアップグレードバナー（freeユーザー） */}
        {userData?.plan === "free" && (sites?.length ?? 0) >= 1 && (
          <div className="mt-8 p-6 bg-gradient-to-r from-brand-600 to-brand-700 rounded-2xl text-white">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-lg mb-1">
                  Starterプランへアップグレード
                </h3>
                <p className="text-brand-200 text-sm">
                  3サイト管理・無期限保存・メールアラートが月$9で利用可能
                </p>
              </div>
              <Link
                href="/settings/billing"
                className="shrink-0 px-5 py-2.5 bg-white text-brand-700 rounded-xl font-semibold text-sm hover:bg-brand-50 transition-colors"
              >
                アップグレード →
              </Link>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
