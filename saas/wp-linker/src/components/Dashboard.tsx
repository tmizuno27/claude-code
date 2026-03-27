"use client";

import { useState, useEffect } from "react";
import {
  Link2,
  AlertTriangle,
  CheckCircle,
  Loader2,
  ArrowRight,
  Globe,
  BarChart3,
  Zap,
  Trash2,
  History,
} from "lucide-react";
import { createClient } from "@/lib/supabase";
import type { LinkSuggestion, OrphanPost, PostLinkStats } from "@/lib/types";

interface SiteConfig {
  rest_api_url: string;
  username: string;
  app_password: string;
  site_name?: string;
}

interface SavedSite {
  id: string;
  name: string;
  url: string;
  rest_api_url: string;
  username: string;
  app_password: string;
}

interface AnalysisHistory {
  id: string;
  total_posts: number;
  orphan_count: number;
  suggestions_count: number;
  applied_count: number;
  coverage: number;
  created_at: string;
}

interface AnalysisData {
  total_posts: number;
  orphan_posts: OrphanPost[];
  post_stats: PostLinkStats[];
  suggestions: LinkSuggestion[];
  summary: {
    total_suggestions: number;
    orphan_count: number;
    coverage: number;
  };
}

export default function Dashboard({ userId }: { userId: string }) {
  const supabase = createClient();
  const [savedSites, setSavedSites] = useState<SavedSite[]>([]);
  const [currentSiteId, setCurrentSiteId] = useState<string | null>(null);
  const [site, setSite] = useState<SiteConfig>({
    rest_api_url: "",
    username: "",
    app_password: "",
  });
  const [connected, setConnected] = useState(false);
  const [testing, setTesting] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [applying, setApplying] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [error, setError] = useState("");
  const [applyResult, setApplyResult] = useState<string>("");
  const [tab, setTab] = useState<"analyze" | "history">("analyze");
  const [history, setHistory] = useState<AnalysisHistory[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Load saved sites on mount
  useEffect(() => {
    async function loadSites() {
      const { data } = await supabase
        .from("sites")
        .select("*")
        .order("created_at", { ascending: false });
      if (data && data.length > 0) {
        setSavedSites(data);
      }
    }
    loadSites();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function selectSavedSite(s: SavedSite) {
    setSite({
      rest_api_url: s.rest_api_url,
      username: s.username,
      app_password: s.app_password,
      site_name: s.name,
    });
    setCurrentSiteId(s.id);
    setConnected(true);
    loadHistory(s.id);
  }

  async function loadHistory(siteId: string) {
    setLoadingHistory(true);
    const { data } = await supabase
      .from("analyses")
      .select("id, total_posts, orphan_count, suggestions_count, applied_count, coverage, created_at")
      .eq("site_id", siteId)
      .order("created_at", { ascending: false })
      .limit(20);
    if (data) setHistory(data);
    setLoadingHistory(false);
  }

  async function testConnection() {
    setTesting(true);
    setError("");
    try {
      const res = await fetch("/api/sites/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(site),
      });
      const data = await res.json();
      if (data.success) {
        const siteName = data.site_name || site.rest_api_url;
        setSite((s) => ({ ...s, site_name: siteName }));

        // Save to Supabase
        const siteUrl = site.rest_api_url.replace(/\/wp-json\/wp\/v2\/?$/, "");
        // Check if site already exists
        const { data: existing } = await supabase
          .from("sites")
          .select("id")
          .eq("user_id", userId)
          .eq("rest_api_url", site.rest_api_url)
          .single();

        let saved: SavedSite | null = null;
        let saveErr = null;

        if (existing) {
          const result = await supabase
            .from("sites")
            .update({ name: siteName, url: siteUrl, username: site.username, app_password: site.app_password })
            .eq("id", existing.id)
            .select()
            .single();
          saved = result.data;
          saveErr = result.error;
        } else {
          const result = await supabase
            .from("sites")
            .insert({
              user_id: userId,
              name: siteName,
              url: siteUrl,
              rest_api_url: site.rest_api_url,
              username: site.username,
              app_password: site.app_password,
            })
            .select()
            .single();
          saved = result.data;
          saveErr = result.error;
        }

        if (!saveErr && saved) {
          setCurrentSiteId(saved.id);
          setSavedSites((prev) => {
            const filtered = prev.filter((s) => s.id !== saved.id);
            return [saved, ...filtered];
          });
          loadHistory(saved.id);
        }

        setConnected(true);
      } else {
        setError(data.error || "Connection failed");
      }
    } catch {
      setError("Network error");
    }
    setTesting(false);
  }

  async function runAnalysis() {
    setAnalyzing(true);
    setError("");
    setApplyResult("");
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...site, site_id: currentSiteId }),
      });
      const data = await res.json();
      if (data.success) {
        setAnalysis(data);
        // Select all suggestions by default
        const keys = new Set<string>(
          data.suggestions.map(
            (s: LinkSuggestion) => `${s.source_post_id}-${s.target_post_id}`
          )
        );
        setSelected(keys);
        if (currentSiteId) loadHistory(currentSiteId);
      } else {
        setError(data.error || "Analysis failed");
      }
    } catch {
      setError("Network error");
    }
    setAnalyzing(false);
  }

  async function applyLinks() {
    if (!analysis) return;
    setApplying(true);
    setError("");

    const toApply = analysis.suggestions.filter((s) =>
      selected.has(`${s.source_post_id}-${s.target_post_id}`)
    );

    try {
      const res = await fetch("/api/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...site, suggestions: toApply }),
      });
      const data = await res.json();
      if (data.success) {
        setApplyResult(
          `${data.updated} posts updated, ${data.errors} errors`
        );
      } else {
        setError(data.error || "Apply failed");
      }
    } catch {
      setError("Network error");
    }
    setApplying(false);
  }

  function toggleSuggestion(key: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  function toggleAll() {
    if (!analysis) return;
    if (selected.size === analysis.suggestions.length) {
      setSelected(new Set());
    } else {
      setSelected(
        new Set(
          analysis.suggestions.map(
            (s) => `${s.source_post_id}-${s.target_post_id}`
          )
        )
      );
    }
  }

  function disconnect() {
    setSite({ rest_api_url: "", username: "", app_password: "" });
    setCurrentSiteId(null);
    setConnected(false);
    setAnalysis(null);
    setSelected(new Set());
    setError("");
    setApplyResult("");
  }

  async function deleteSavedSite(siteId: string) {
    await supabase.from("sites").delete().eq("id", siteId);
    setSavedSites((prev) => prev.filter((s) => s.id !== siteId));
  }

  // ---- Connection form ----
  if (!connected) {
    return (
      <div className="max-w-lg mx-auto mt-12">
        {/* Saved sites */}
        {savedSites.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Your Sites</h3>
            <div className="space-y-2">
              {savedSites.map((s) => (
                <div
                  key={s.id}
                  className="bg-white rounded-xl border border-gray-200 p-4 flex items-center justify-between hover:border-blue-300 transition cursor-pointer"
                  onClick={() => selectSavedSite(s)}
                >
                  <div>
                    <p className="font-medium text-sm">{s.name}</p>
                    <p className="text-xs text-gray-500">{s.url}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteSavedSite(s.id);
                      }}
                      className="text-gray-400 hover:text-red-500 transition p-1"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <ArrowRight className="w-4 h-4 text-gray-400" />
                  </div>
                </div>
              ))}
            </div>
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200" /></div>
              <div className="relative flex justify-center text-xs"><span className="bg-gray-50 px-2 text-gray-500">or add new site</span></div>
            </div>
          </div>
        )}

        {/* Onboarding guide for first-time users */}
        {savedSites.length === 0 && (
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-2xl p-6">
            <h3 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
              <Zap className="w-5 h-5 text-blue-600" />
              Welcome! Let&apos;s set up your first site in 3 steps:
            </h3>
            <ol className="space-y-2 text-sm text-blue-800">
              <li className="flex items-start gap-2">
                <span className="font-bold text-blue-600 shrink-0">1.</span>
                Go to your WordPress dashboard &rarr; Users &rarr; Profile &rarr; scroll to &ldquo;Application Passwords&rdquo;
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold text-blue-600 shrink-0">2.</span>
                Create a new application password (name it &ldquo;WP Linker&rdquo;) and copy it
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold text-blue-600 shrink-0">3.</span>
                Enter your site URL, username, and the application password below
              </li>
            </ol>
            <p className="mt-3 text-xs text-blue-600">
              WP Linker uses read-only access. We never modify your content without your approval.
            </p>
          </div>
        )}

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-xl font-semibold">Connect WordPress Site</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                REST API URL
              </label>
              <input
                type="url"
                placeholder="https://yoursite.com/wp-json/wp/v2"
                value={site.rest_api_url}
                onChange={(e) =>
                  setSite((s) => ({ ...s, rest_api_url: e.target.value }))
                }
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <input
                type="text"
                placeholder="admin"
                value={site.username}
                onChange={(e) =>
                  setSite((s) => ({ ...s, username: e.target.value }))
                }
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Application Password
              </label>
              <input
                type="password"
                placeholder="xxxx xxxx xxxx xxxx xxxx xxxx"
                value={site.app_password}
                onChange={(e) =>
                  setSite((s) => ({ ...s, app_password: e.target.value }))
                }
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition"
              />
              <p className="mt-1 text-xs text-gray-500">
                WordPress &gt; Users &gt; Profile &gt; Application Passwords
              </p>
            </div>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              {error}
            </div>
          )}

          <button
            onClick={testConnection}
            disabled={
              testing || !site.rest_api_url || !site.username || !site.app_password
            }
            className="mt-6 w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-medium rounded-xl transition flex items-center justify-center gap-2"
          >
            {testing ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <ArrowRight className="w-4 h-4" />
            )}
            {testing ? "Connecting..." : "Connect & Test"}
          </button>
        </div>
      </div>
    );
  }

  // ---- Dashboard ----
  return (
    <div className="max-w-5xl mx-auto mt-8 px-4">
      {/* Site header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center">
            <CheckCircle className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-semibold">
              {site.site_name || "Connected"}
            </h2>
            <p className="text-sm text-gray-500">{site.rest_api_url}</p>
          </div>
        </div>
        <button
          onClick={disconnect}
          className="text-sm text-gray-500 hover:text-red-600 transition flex items-center gap-1"
        >
          <Trash2 className="w-4 h-4" />
          Disconnect
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 bg-gray-100 rounded-lg p-1 w-fit">
        <button
          onClick={() => setTab("analyze")}
          className={`px-4 py-2 rounded-md text-sm font-medium transition ${tab === "analyze" ? "bg-white shadow-sm text-gray-900" : "text-gray-500 hover:text-gray-700"}`}
        >
          <span className="flex items-center gap-1.5"><BarChart3 className="w-4 h-4" />Analyze</span>
        </button>
        <button
          onClick={() => { setTab("history"); if (currentSiteId && history.length === 0) loadHistory(currentSiteId); }}
          className={`px-4 py-2 rounded-md text-sm font-medium transition ${tab === "history" ? "bg-white shadow-sm text-gray-900" : "text-gray-500 hover:text-gray-700"}`}
        >
          <span className="flex items-center gap-1.5"><History className="w-4 h-4" />History</span>
        </button>
      </div>

      {/* History tab */}
      {tab === "history" && (
        <div className="bg-white rounded-xl border border-gray-200">
          <div className="p-5 border-b border-gray-100">
            <h3 className="font-semibold flex items-center gap-2">
              <History className="w-4 h-4 text-blue-600" />
              Analysis History
            </h3>
          </div>
          {loadingHistory ? (
            <div className="p-8 text-center text-gray-500"><Loader2 className="w-5 h-5 animate-spin mx-auto" /></div>
          ) : history.length === 0 ? (
            <div className="p-8 text-center text-gray-500 text-sm">No analysis history yet. Run your first analysis!</div>
          ) : (
            <div className="divide-y divide-gray-50">
              {history.map((h) => (
                <div key={h.id} className="px-5 py-4 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium">
                      {new Date(h.created_at).toLocaleDateString("ja-JP", { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}
                    </p>
                    <p className="text-xs text-gray-500 mt-0.5">
                      {h.total_posts} posts analyzed
                    </p>
                  </div>
                  <div className="flex items-center gap-4 text-xs">
                    <span className={`px-2 py-1 rounded-full ${h.orphan_count === 0 ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"}`}>
                      {h.orphan_count} orphans
                    </span>
                    <span className="px-2 py-1 rounded-full bg-blue-50 text-blue-700">
                      {h.suggestions_count} suggestions
                    </span>
                    <span className={`px-2 py-1 rounded-full font-medium ${h.coverage >= 80 ? "bg-emerald-50 text-emerald-700" : h.coverage >= 50 ? "bg-amber-50 text-amber-700" : "bg-red-50 text-red-700"}`}>
                      {h.coverage}% coverage
                    </span>
                    {h.applied_count > 0 && (
                      <span className="px-2 py-1 rounded-full bg-purple-50 text-purple-700">
                        {h.applied_count} applied
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Analyze tab */}
      {tab === "analyze" && !analysis && (
        <button
          onClick={runAnalysis}
          disabled={analyzing}
          className="w-full py-4 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-medium rounded-xl transition flex items-center justify-center gap-2 text-lg"
        >
          {analyzing ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing posts...
            </>
          ) : (
            <>
              <BarChart3 className="w-5 h-5" />
              Analyze Internal Links
            </>
          )}
        </button>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          {error}
        </div>
      )}

      {applyResult && (
        <div className="mt-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-700 text-sm flex items-center gap-2">
          <CheckCircle className="w-4 h-4 shrink-0" />
          {applyResult}
        </div>
      )}

      {/* Analysis results */}
      {tab === "analyze" && analysis && (
        <>
          {/* Summary cards */}
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <p className="text-sm text-gray-500 mb-1">Total Posts</p>
              <p className="text-3xl font-bold">{analysis.total_posts}</p>
            </div>
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <p className="text-sm text-gray-500 mb-1">Orphan Posts</p>
              <p className="text-3xl font-bold text-amber-600">
                {analysis.summary.orphan_count}
              </p>
              <p className="text-xs text-gray-400 mt-1">
                No incoming internal links
              </p>
            </div>
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <p className="text-sm text-gray-500 mb-1">Link Coverage</p>
              <p className="text-3xl font-bold text-emerald-600">
                {analysis.summary.coverage}%
              </p>
            </div>
          </div>

          {/* Orphan posts */}
          {analysis.orphan_posts.length > 0 && (
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-8">
              <h3 className="font-semibold text-amber-800 mb-3 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Orphan Posts ({analysis.orphan_posts.length})
              </h3>
              <p className="text-sm text-amber-700 mb-3">
                These posts have no incoming internal links. They are harder for
                search engines to discover.
              </p>
              <ul className="space-y-1">
                {analysis.orphan_posts.map((p) => (
                  <li
                    key={p.post_id}
                    className="text-sm text-amber-900 flex items-center gap-2"
                  >
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full shrink-0" />
                    <a
                      href={p.url}
                      target="_blank"
                      rel="noopener"
                      className="hover:underline"
                    >
                      {p.title}
                    </a>
                    <span className="text-amber-600 text-xs">
                      ({p.outgoing_links} outgoing)
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Link Map - all posts with their link stats */}
          {analysis.post_stats && analysis.post_stats.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 mb-8">
              <div className="p-5 border-b border-gray-100">
                <h3 className="font-semibold flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-blue-600" />
                  Internal Link Map ({analysis.post_stats.length} posts)
                </h3>
              </div>
              <div className="divide-y divide-gray-50">
                {analysis.post_stats.map((ps) => (
                  <div key={ps.post_id} className="px-5 py-3">
                    <div className="flex items-center justify-between mb-1">
                      <a
                        href={ps.url}
                        target="_blank"
                        rel="noopener"
                        className="text-sm font-medium hover:text-blue-600 truncate max-w-[500px]"
                      >
                        {ps.title}
                      </a>
                      <div className="flex items-center gap-3 text-xs shrink-0">
                        <span className={`px-2 py-0.5 rounded-full ${ps.incoming_links === 0 ? 'bg-red-100 text-red-700' : 'bg-emerald-50 text-emerald-700'}`}>
                          {ps.incoming_links} incoming
                        </span>
                        <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">
                          {ps.outgoing_links} outgoing
                        </span>
                      </div>
                    </div>
                    {(ps.linked_from.length > 0 || ps.links_to.length > 0) && (
                      <div className="text-xs text-gray-500 mt-1 space-y-0.5">
                        {ps.linked_from.length > 0 && (
                          <p>
                            <span className="text-gray-400">Linked from:</span>{" "}
                            {ps.linked_from.join(", ")}
                          </p>
                        )}
                        {ps.links_to.length > 0 && (
                          <p>
                            <span className="text-gray-400">Links to:</span>{" "}
                            {ps.links_to.join(", ")}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggestions */}
          <div className="bg-white rounded-xl border border-gray-200">
            <div className="flex items-center justify-between p-5 border-b border-gray-100">
              <h3 className="font-semibold flex items-center gap-2">
                <Link2 className="w-4 h-4 text-blue-600" />
                Link Suggestions ({analysis.suggestions.length})
              </h3>
              <div className="flex items-center gap-3">
                <button
                  onClick={toggleAll}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  {selected.size === analysis.suggestions.length
                    ? "Deselect All"
                    : "Select All"}
                </button>
                <button
                  onClick={applyLinks}
                  disabled={applying || selected.size === 0}
                  className="py-2 px-4 bg-emerald-600 hover:bg-emerald-700 disabled:bg-gray-300 text-white text-sm font-medium rounded-lg transition flex items-center gap-2"
                >
                  {applying ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Zap className="w-4 h-4" />
                  )}
                  Apply {selected.size} Links
                </button>
              </div>
            </div>

            <div className="divide-y divide-gray-50">
              {analysis.suggestions.map((s) => {
                const key = `${s.source_post_id}-${s.target_post_id}`;
                return (
                  <div
                    key={key}
                    className="flex items-center gap-4 px-5 py-3 hover:bg-gray-50 transition"
                  >
                    <input
                      type="checkbox"
                      checked={selected.has(key)}
                      onChange={() => toggleSuggestion(key)}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 text-sm">
                        <span className="font-medium truncate max-w-[200px]">
                          {s.source_title}
                        </span>
                        <ArrowRight className="w-3 h-3 text-gray-400 shrink-0" />
                        <span className="text-blue-600 truncate max-w-[200px]">
                          {s.target_title}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 shrink-0">
                      <div
                        className={`h-2 rounded-full ${
                          s.relevance_score > 50
                            ? "bg-emerald-400"
                            : s.relevance_score > 20
                            ? "bg-amber-400"
                            : "bg-gray-300"
                        }`}
                        style={{
                          width: `${Math.min(60, Math.max(12, s.relevance_score))}px`,
                        }}
                      />
                      <span className="text-xs text-gray-500 w-8 text-right">
                        {s.relevance_score}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Re-analyze button */}
          <div className="mt-6 text-center">
            <button
              onClick={runAnalysis}
              disabled={analyzing}
              className="text-sm text-blue-600 hover:text-blue-800 transition"
            >
              {analyzing ? "Analyzing..." : "Re-analyze"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
