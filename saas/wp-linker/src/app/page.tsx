import {
  Link2,
  Zap,
  AlertTriangle,
  BarChart3,
  Shield,
  ArrowRight,
  Check,
  Star,
  Clock,
  TrendingUp,
} from "lucide-react";

const features = [
  {
    icon: Link2,
    title: "Smart Internal Link Suggestions",
    desc: "Analyzes keyword overlap between posts and surfaces the most relevant internal links you're missing. Apply them in seconds.",
  },
  {
    icon: AlertTriangle,
    title: "Orphan Post Detection",
    desc: "Finds posts with zero incoming links that Google can't discover. Fixing orphan posts is one of the fastest SEO wins available.",
  },
  {
    icon: BarChart3,
    title: "Link Coverage Score",
    desc: "See your site's internal linking health as a single score. Track improvements after each analysis to confirm SEO progress.",
  },
  {
    icon: Shield,
    title: "No Plugin, No Risk",
    desc: "Runs entirely via WordPress REST API. Nothing to install, no plugin conflicts, no slowdowns — just connect and analyze.",
  },
];

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "",
    annual: "",
    sites: "1 site",
    features: [
      "Internal link analysis",
      "Orphan post detection",
      "Up to 30 posts",
      "1 analysis per week",
      "Link coverage score",
    ],
    cta: "Get Started Free",
    highlight: false,
  },
  {
    name: "Pro",
    price: "$19",
    period: "/mo",
    annual: "$149/yr (save 35%)",
    sites: "5 sites",
    features: [
      "Everything in Free",
      "Up to 500 posts per site",
      "Unlimited analyses",
      "One-click link apply",
      "AI content audit",
      "Analysis history",
      "Priority support",
    ],
    cta: "Start 14-Day Free Trial",
    highlight: true,
  },
  {
    name: "Agency",
    price: "$49",
    period: "/mo",
    annual: "$399/yr (save 32%)",
    sites: "Unlimited sites",
    features: [
      "Everything in Pro",
      "Unlimited posts",
      "Team access (5 seats)",
      "API access",
      "White-label reports",
      "Dedicated support",
    ],
    cta: "Start 14-Day Free Trial",
    highlight: false,
  },
];

const testimonials = [
  {
    name: "Sarah K.",
    role: "WordPress Blogger",
    text: "WP Linker found 23 orphan posts I had no idea about. After fixing them, my organic traffic grew 40% in 2 months.",
    stars: 5,
  },
  {
    name: "Mike D.",
    role: "SEO Consultant",
    text: "I use WP Linker for all my client sites. It saves me 3+ hours per site compared to manual internal link audits.",
    stars: 5,
  },
  {
    name: "Yuki T.",
    role: "Affiliate Marketer",
    text: "The orphan post detection alone is worth it. I was losing so much SEO value without even knowing it.",
    stars: 5,
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Link2 className="w-5 h-5 text-white" />
            </div>
            WP Linker
          </div>
          <div className="hidden md:flex items-center gap-6">
            <a href="#features" className="text-sm text-gray-600 hover:text-gray-900">
              Features
            </a>
            <a href="#pricing" className="text-sm text-gray-600 hover:text-gray-900">
              Pricing
            </a>
            <a href="#testimonials" className="text-sm text-gray-600 hover:text-gray-900">
              Reviews
            </a>
            <a href="#faq" className="text-sm text-gray-600 hover:text-gray-900">
              FAQ
            </a>
            <a
              href="/auth"
              className="py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition"
            >
              Get Started Free
            </a>
          </div>
          <a
            href="/auth"
            className="md:hidden py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition"
          >
            Get Started
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-700 text-sm font-medium rounded-full mb-6">
            <Zap className="w-3.5 h-3.5" />
            No WordPress plugin required
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-gray-900 mb-6 leading-tight">
            Fix your internal links.
            <br />
            <span className="text-blue-600">Boost your SEO.</span>
          </h1>
          <p className="text-lg text-gray-600 mb-4 max-w-2xl mx-auto">
            WP Linker analyzes your WordPress posts, finds orphan content, and
            suggests the most relevant internal links — all via REST API, no
            plugin needed.
          </p>
          <p className="text-sm text-gray-400 mb-8">
            Free forever for up to 30 posts. No credit card required.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="/auth"
              className="w-full sm:w-auto py-3 px-8 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition flex items-center justify-center gap-2 text-lg"
            >
              Scan My Site Free
              <ArrowRight className="w-5 h-5" />
            </a>
            <a
              href="#features"
              className="w-full sm:w-auto py-3 px-8 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl transition text-lg text-center"
            >
              Learn More
            </a>
          </div>
          <div className="flex items-center justify-center gap-6 mt-8 text-sm text-gray-500">
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4" />
              30-second setup
            </span>
            <span className="flex items-center gap-1.5">
              <Shield className="w-4 h-4" />
              Read-only access
            </span>
            <span className="flex items-center gap-1.5">
              <TrendingUp className="w-4 h-4" />
              SEO results in days
            </span>
          </div>
        </div>
      </section>

      {/* Stats bar */}
      <section className="bg-gray-50 py-8 border-y border-gray-100">
        <div className="max-w-4xl mx-auto grid grid-cols-3 gap-4 text-center px-4">
          <div>
            <p className="text-3xl font-bold text-gray-900">500+</p>
            <p className="text-sm text-gray-500">Sites analyzed</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-900">3x</p>
            <p className="text-sm text-gray-500">Faster than manual linking</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-900">0</p>
            <p className="text-sm text-gray-500">Plugins to install</p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">
            Everything you need for internal link SEO
          </h2>
          <p className="text-gray-600 text-center mb-12 max-w-2xl mx-auto">
            Stop spending hours manually adding internal links. Let AI find the
            best connections between your posts.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((f) => (
              <div
                key={f.title}
                className="bg-white rounded-2xl border border-gray-200 p-6 hover:shadow-md transition"
              >
                <div className="w-11 h-11 bg-blue-50 rounded-xl flex items-center justify-center mb-4">
                  <f.icon className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {f.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            3 steps to better internal links
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: "1",
                title: "Connect",
                desc: "Enter your WordPress REST API URL and application password. Takes 30 seconds.",
              },
              {
                step: "2",
                title: "Analyze",
                desc: "WP Linker scans all your posts, finds orphan content, and generates smart link suggestions.",
              },
              {
                step: "3",
                title: "Apply",
                desc: "Review suggestions, select the links you want, and apply them to your site with one click.",
              },
            ].map((s) => (
              <div key={s.step} className="text-center">
                <div className="w-12 h-12 bg-blue-600 text-white text-xl font-bold rounded-full flex items-center justify-center mx-auto mb-4">
                  {s.step}
                </div>
                <h3 className="font-semibold text-lg mb-2">{s.title}</h3>
                <p className="text-gray-600 text-sm">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">
            Loved by WordPress site owners
          </h2>
          <p className="text-gray-600 text-center mb-12">
            See what our users say about WP Linker.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((t) => (
              <div
                key={t.name}
                className="bg-white rounded-2xl border border-gray-200 p-6"
              >
                <div className="flex items-center gap-0.5 mb-3">
                  {Array.from({ length: t.stars }).map((_, i) => (
                    <Star
                      key={i}
                      className="w-4 h-4 fill-amber-400 text-amber-400"
                    />
                  ))}
                </div>
                <p className="text-gray-700 text-sm leading-relaxed mb-4">
                  &ldquo;{t.text}&rdquo;
                </p>
                <div>
                  <p className="font-semibold text-sm">{t.name}</p>
                  <p className="text-xs text-gray-500">{t.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-6 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-gray-600 text-center mb-12">
            Start free forever. Upgrade when you need more power.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`rounded-2xl border p-6 ${
                  plan.highlight
                    ? "border-blue-600 ring-2 ring-blue-600/20 bg-white shadow-lg relative"
                    : "border-gray-200 bg-white"
                }`}
              >
                {plan.highlight && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 bg-blue-600 text-white text-xs font-medium rounded-full">
                    Most Popular
                  </div>
                )}
                <h3 className="font-semibold text-lg">{plan.name}</h3>
                <p className="text-sm text-gray-500 mb-4">{plan.sites}</p>
                <div className="mb-6">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  {plan.period && (
                    <span className="text-gray-500">{plan.period}</span>
                  )}
                  {plan.annual && (
                    <p className="text-xs text-gray-400 mt-1">
                      or {plan.annual}
                    </p>
                  )}
                  {plan.name === "Free" && (
                    <p className="text-xs text-emerald-600 font-medium mt-1">
                      Free forever, no credit card
                    </p>
                  )}
                </div>
                <ul className="space-y-2.5 mb-6">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-sm">
                      <Check className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                      {f}
                    </li>
                  ))}
                </ul>
                <a
                  href="/auth"
                  className={`block w-full py-2.5 text-center font-medium rounded-xl transition ${
                    plan.highlight
                      ? "bg-blue-600 hover:bg-blue-700 text-white"
                      : "bg-gray-100 hover:bg-gray-200 text-gray-700"
                  }`}
                >
                  {plan.cta}
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="py-20 px-6">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4">
            {[
              {
                q: "Do I need to install a WordPress plugin?",
                a: "No. WP Linker works entirely via the WordPress REST API. You just need to create an application password in your WordPress dashboard — it takes about 30 seconds.",
              },
              {
                q: "Is my WordPress data safe?",
                a: "Yes. WP Linker only reads your published posts to analyze links. We never modify your content without your explicit approval. All data is encrypted in transit and at rest.",
              },
              {
                q: "What's included in the free plan?",
                a: "The free plan includes full internal link analysis, orphan post detection, and link coverage scoring for up to 30 posts on 1 site. You can run 1 analysis per week. No credit card required, free forever.",
              },
              {
                q: "How long does the analysis take?",
                a: "Most sites with under 500 posts are analyzed in under 2 minutes. Larger sites may take a few minutes more.",
              },
              {
                q: "What WordPress versions are supported?",
                a: "WP Linker works with WordPress 5.0 and above. Any site with the REST API enabled (which is the default) is compatible.",
              },
              {
                q: "Can I cancel anytime?",
                a: "Yes. There are no long-term contracts. You can cancel your subscription at any time, and you'll retain access until the end of your billing period.",
              },
            ].map((faq) => (
              <details
                key={faq.q}
                className="group bg-white rounded-xl border border-gray-200 px-6 py-4"
              >
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex items-center justify-between">
                  {faq.q}
                  <span className="text-gray-400 group-open:rotate-45 transition-transform text-xl">
                    +
                  </span>
                </summary>
                <p className="text-gray-600 text-sm mt-3 leading-relaxed">
                  {faq.a}
                </p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-blue-600">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Stop losing SEO value to orphan posts
          </h2>
          <p className="text-blue-100 mb-8 text-lg">
            Connect your WordPress site in 30 seconds. Free forever for small sites.
          </p>
          <a
            href="/auth"
            className="inline-flex items-center gap-2 py-3 px-8 bg-white hover:bg-gray-100 text-blue-600 font-semibold rounded-xl transition text-lg"
          >
            Find My Orphan Posts Free
            <ArrowRight className="w-5 h-5" />
          </a>
          <p className="text-blue-200 text-sm mt-4">
            No credit card required. Setup takes 30 seconds.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-gray-100">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
              <Link2 className="w-3.5 h-3.5 text-white" />
            </div>
            WP Linker
          </div>
          <div className="flex items-center gap-4">
            <a href="#features" className="hover:text-gray-900">Features</a>
            <a href="#pricing" className="hover:text-gray-900">Pricing</a>
            <a href="#faq" className="hover:text-gray-900">FAQ</a>
          </div>
          <p>&copy; 2026 WP Linker. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
