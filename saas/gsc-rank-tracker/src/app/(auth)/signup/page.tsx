"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { Suspense } from "react";

const PLAN_LABELS: Record<string, string> = {
  free: "Free（無料）",
  starter: "Starter（$9/月）",
  pro: "Pro（$19/月）",
  agency: "Agency（$49/月）",
};

function SignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const plan = searchParams.get("plan") ?? "free";
  const supabase = createClient();

  const handleGoogleSignup = async () => {
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/api/auth/callback?plan=${plan}`,
        scopes:
          "https://www.googleapis.com/auth/webmasters.readonly openid email profile",
        queryParams: {
          access_type: "offline",
          prompt: "consent",
        },
      },
    });

    if (error) {
      setError("Googleサインアップに失敗しました: " + error.message);
      setLoading(false);
    }
  };

  const handleEmailSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (password.length < 8) {
      setError("パスワードは8文字以上で設定してください");
      setLoading(false);
      return;
    }

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/api/auth/callback?plan=${plan}`,
      },
    });

    if (error) {
      setError(
        error.message === "User already registered"
          ? "このメールアドレスは既に登録されています"
          : error.message
      );
      setLoading(false);
      return;
    }

    setSuccess(true);
  };

  if (success) {
    return (
      <div className="text-center p-8">
        <div className="text-5xl mb-4">📧</div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          確認メールを送信しました
        </h2>
        <p className="text-gray-600 text-sm mb-6">
          {email} に確認メールを送りました。
          <br />
          メール内のリンクをクリックしてアカウントを有効化してください。
        </p>
        <Link
          href="/login"
          className="text-brand-600 font-medium hover:underline"
        >
          ログインページへ →
        </Link>
      </div>
    );
  }

  return (
    <>
      {/* プラン表示 */}
      {plan !== "free" && (
        <div className="mb-6 p-3 bg-brand-50 border border-brand-200 rounded-xl text-center">
          <p className="text-brand-700 text-sm font-medium">
            選択中のプラン: {PLAN_LABELS[plan] ?? plan}
          </p>
          <p className="text-brand-600 text-xs mt-0.5">
            ※ 決済はアカウント作成後に設定できます
          </p>
        </div>
      )}

      {/* Googleサインアップ */}
      <button
        onClick={handleGoogleSignup}
        disabled={loading}
        className="w-full flex items-center justify-center gap-3 px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-700 font-medium hover:border-gray-300 hover:bg-gray-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg className="w-5 h-5" viewBox="0 0 24 24">
          <path
            fill="#4285F4"
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          />
          <path
            fill="#34A853"
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          />
          <path
            fill="#FBBC05"
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          />
          <path
            fill="#EA4335"
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          />
        </svg>
        Googleで登録（推奨 · GSC連携が簡単）
      </button>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-200" />
        </div>
        <div className="relative flex justify-center">
          <span className="bg-white px-4 text-gray-400 text-sm">または</span>
        </div>
      </div>

      {/* メール/パスワード登録 */}
      <form onSubmit={handleEmailSignup} className="space-y-4">
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            メールアドレス
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="you@example.com"
            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all"
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            パスワード
            <span className="text-gray-400 font-normal ml-2">（8文字以上）</span>
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            placeholder="••••••••"
            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 px-6 bg-brand-600 text-white rounded-xl font-semibold hover:bg-brand-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "登録中..." : "無料アカウントを作成"}
        </button>

        <p className="text-center text-xs text-gray-500">
          登録することで{" "}
          <Link href="/terms" className="underline">
            利用規約
          </Link>{" "}
          および{" "}
          <Link href="/privacy" className="underline">
            プライバシーポリシー
          </Link>{" "}
          に同意したものとみなされます
        </p>
      </form>
    </>
  );
}

export default function SignupPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* ロゴ */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2">
            <span className="text-3xl">📊</span>
            <span className="font-bold text-gray-900 text-xl">
              GSC Rank Tracker<span className="text-brand-600"> Pro</span>
            </span>
          </Link>
          <h1 className="text-2xl font-bold text-gray-900 mt-6 mb-2">
            無料アカウントを作成
          </h1>
          <p className="text-gray-600 text-sm">
            クレジットカード不要 · 設定5分で開始
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <Suspense fallback={<div className="text-center text-gray-500">読み込み中...</div>}>
            <SignupForm />
          </Suspense>
        </div>

        <p className="text-center text-gray-600 text-sm mt-6">
          すでにアカウントをお持ちの方は{" "}
          <Link
            href="/login"
            className="text-brand-600 font-medium hover:underline"
          >
            ログイン
          </Link>
        </p>
      </div>
    </div>
  );
}
