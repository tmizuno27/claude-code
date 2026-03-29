import { notFound, redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

type Props = {
  params: Promise<{ id: string }>;
};

export default async function SiteDetailPage({ params }: Props) {
  const { id } = await params;
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // サイト情報取得（所有権チェック）
  const { data: site } = await supabase
    .from("sites")
    .select("*")
    .eq("id", id)
    .eq("user_id", user.id)
    .single();

  if (!site) notFound();

  // 最新30日の上位10キーワード
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const { data: topKeywords } = await supabase
    .from("rankings")
    .select("query, position, impressions, clicks, ctr, date")
    .eq("site_id", id)
    .gte("date", thirtyDaysAgo.toISOString().split("T")[0])
    .order("impressions", { ascending: false })
    .limit(20);

  // サマリー計算
  const summary = topKeywords?.reduce(
    (acc, r) => ({
      totalClicks: acc.totalClicks + r.clicks,
      totalImpressions: acc.totalImpressions + r.impressions,
      avgPosition:
        acc.count === 0
          ? r.position
          : (acc.avgPosition * acc.count + r.position) / (acc.count + 1),
      count: acc.count + 1,
    }),
    { totalClicks: 0, totalImpressions: 0, avgPosition: 0, count: 0 }
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4 h-16">
            <Link
              href="/dashboard"
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              ← ダッシュボード
            </Link>
            <span className="text-gray-300">|</span>
            <h1 className="font-bold text-gray-900">{site.domain}</h1>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                site.is_active
                  ? "bg-green-100 text-green-700"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              {site.is_active ? "● 監視中" : "停止中"}
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* サマリーカード */}
        {summary && summary.count > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              {
                label: "総クリック数",
                value: summary.totalClicks.toLocaleString(),
                sub: "過去30日",
              },
              {
                label: "総表示回数",
                value: summary.totalImpressions.toLocaleString(),
                sub: "過去30日",
              },
              {
                label: "平均CTR",
                value: `${((summary.totalClicks / summary.totalImpressions) * 100).toFixed(2)}%`,
                sub: "過去30日",
              },
              {
                label: "平均順位",
                value: summary.avgPosition.toFixed(1),
                sub: "過去30日",
              },
            ].map((stat) => (
              <div
                key={stat.label}
                className="bg-white rounded-2xl border border-gray-200 p-5"
              >
                <p className="text-xs text-gray-500 mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                <p className="text-xs text-gray-400 mt-1">{stat.sub}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-gray-200 p-10 text-center">
            <div className="text-4xl mb-3">⏳</div>
            <h3 className="font-bold text-gray-900 mb-2">データ取得待ち</h3>
            <p className="text-gray-600 text-sm">
              初回データ取得は翌日AM3:00（JST）に実行されます。
              <br />
              しばらくお待ちください。
            </p>
          </div>
        )}

        {/* キーワード一覧テーブル */}
        {topKeywords && topKeywords.length > 0 && (
          <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
              <h2 className="font-bold text-gray-900">
                上位キーワード（過去30日）
              </h2>
              <span className="text-xs text-gray-500">
                {topKeywords.length}件表示
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    {["キーワード", "平均順位", "クリック数", "表示回数", "CTR"].map(
                      (h) => (
                        <th
                          key={h}
                          className="px-4 py-3 text-left text-xs font-medium text-gray-500"
                        >
                          {h}
                        </th>
                      )
                    )}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {topKeywords.map((kw) => (
                    <tr key={`${kw.query}-${kw.date}`} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 max-w-xs truncate">
                        {kw.query}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                            kw.position <= 3
                              ? "bg-green-100 text-green-700"
                              : kw.position <= 10
                                ? "bg-yellow-100 text-yellow-700"
                                : "bg-gray-100 text-gray-600"
                          }`}
                        >
                          {kw.position.toFixed(1)}位
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">
                        {kw.clicks.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">
                        {kw.impressions.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={
                            kw.ctr < 0.02
                              ? "text-red-600 font-medium"
                              : "text-gray-700"
                          }
                        >
                          {(kw.ctr * 100).toFixed(2)}%
                          {kw.ctr < 0.02 && (
                            <span className="ml-1 text-xs">⚠️</span>
                          )}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* アラート設定へのリンク */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-gray-900 mb-1">
                順位急落アラートを設定
              </h3>
              <p className="text-sm text-gray-600">
                順位が急落したら即メール通知。見逃しゼロのSEO監視。
              </p>
            </div>
            <Link
              href={`/dashboard/sites/${id}/alerts`}
              className="px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium hover:bg-brand-700 transition-colors"
            >
              アラートを設定 →
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
