var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/utils.js
var PLATFORM_PATTERNS = {
  tiktok: /(?:https?:\/\/)?(?:www\.|vm\.)?tiktok\.com\/.+/i,
  twitter: /(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/.+\/status\/\d+/i,
  instagram: /(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv)\/[\w-]+/i,
  youtube: /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)[\w-]+/i,
  facebook: /(?:https?:\/\/)?(?:www\.|m\.)?(?:facebook\.com|fb\.watch)\/.+/i
};
function detectPlatform(url) {
  for (const [platform, regex] of Object.entries(PLATFORM_PATTERNS)) {
    if (regex.test(url)) return platform;
  }
  return null;
}
__name(detectPlatform, "detectPlatform");
function isValidUrl(str) {
  try {
    const u = new URL(str);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}
__name(isValidUrl, "isValidUrl");
function browserHeaders(extra = {}) {
  return {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    ...extra
  };
}
__name(browserHeaders, "browserHeaders");
function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  };
}
__name(corsHeaders, "corsHeaders");
function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders()
    }
  });
}
__name(jsonResponse, "jsonResponse");
var rateLimitMap = /* @__PURE__ */ new Map();
function checkRateLimit(ip, maxRequests = 20, windowSec = 60) {
  const now = Date.now();
  let entry = rateLimitMap.get(ip);
  if (!entry || now > entry.resetAt) {
    entry = { count: 0, resetAt: now + windowSec * 1e3 };
    rateLimitMap.set(ip);
  }
  entry.count++;
  rateLimitMap.set(ip, entry);
  const allowed = entry.count <= maxRequests;
  return {
    allowed,
    remaining: Math.max(0, maxRequests - entry.count),
    resetAt: entry.resetAt
  };
}
__name(checkRateLimit, "checkRateLimit");
setInterval(() => {
  const now = Date.now();
  for (const [key, val] of rateLimitMap) {
    if (now > val.resetAt) rateLimitMap.delete(key);
  }
}, 5 * 60 * 1e3);
var SUPPORTED_PLATFORMS = [
  { id: "tiktok", name: "TikTok", domain: "tiktok.com", urlPattern: "https://www.tiktok.com/@user/video/1234" },
  { id: "twitter", name: "Twitter / X", domain: "x.com", urlPattern: "https://x.com/user/status/1234" },
  { id: "instagram", name: "Instagram", domain: "instagram.com", urlPattern: "https://www.instagram.com/reel/ABC123/" },
  { id: "youtube", name: "YouTube", domain: "youtube.com", urlPattern: "https://www.youtube.com/watch?v=abc123" },
  { id: "facebook", name: "Facebook", domain: "facebook.com", urlPattern: "https://www.facebook.com/watch/?v=1234" }
];

// src/extractors.js
function fail(platform, message) {
  return { success: false, platform, error: message };
}
__name(fail, "fail");
function ok(data) {
  return { success: true, ...data };
}
__name(ok, "ok");
async function fetchPage(url, extraHeaders = {}) {
  return fetch(url, {
    headers: browserHeaders(extraHeaders),
    redirect: "follow"
  });
}
__name(fetchPage, "fetchPage");
async function extractTikTok(url) {
  const platform = "tiktok";
  try {
    const oembedUrl = `https://www.tiktok.com/oembed?url=${encodeURIComponent(url)}`;
    const oembedRes = await fetchPage(oembedUrl);
    let title = null;
    let author = null;
    let thumbnail = null;
    if (oembedRes.ok) {
      const oembed = await oembedRes.json();
      title = oembed.title || null;
      author = oembed.author_name || null;
      thumbnail = oembed.thumbnail_url || null;
    }
    const pageRes = await fetchPage(url);
    if (!pageRes.ok) return fail(platform, `Failed to fetch page (HTTP ${pageRes.status})`);
    const html = await pageRes.text();
    let videoUrl = null;
    let duration = null;
    const rehydrationMatch = html.match(
      /<script[^>]*id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>([\s\S]*?)<\/script>/
    );
    if (rehydrationMatch) {
      try {
        const data = JSON.parse(rehydrationMatch[1]);
        const defaultScope = data?.__DEFAULT_SCOPE__;
        const videoDetail = defaultScope?.["webapp.video-detail"]?.itemInfo?.itemStruct || defaultScope?.["webapp.video-detail"]?.itemStruct;
        if (videoDetail) {
          videoUrl = videoDetail.video?.playAddr || videoDetail.video?.downloadAddr || null;
          duration = videoDetail.video?.duration || null;
          title = title || videoDetail.desc || null;
          author = author || videoDetail.author?.uniqueId || null;
          thumbnail = thumbnail || videoDetail.video?.cover || null;
        }
      } catch {
      }
    }
    if (!videoUrl) {
      const patterns = [
        /"playAddr"\s*:\s*"([^"]+)"/,
        /"downloadAddr"\s*:\s*"([^"]+)"/,
        /playAddr['"]\s*:\s*['"]([^'"]+)['"]/
      ];
      for (const p of patterns) {
        const m = html.match(p);
        if (m) {
          videoUrl = m[1].replace(/\\u002F/g, "/").replace(/\\u0026/g, "&");
          break;
        }
      }
    }
    if (!videoUrl) {
      const sigiMatch = html.match(
        /<script[^>]*id="SIGI_STATE"[^>]*>([\s\S]*?)<\/script>/
      );
      if (sigiMatch) {
        try {
          const sigi = JSON.parse(sigiMatch[1]);
          const items = sigi?.ItemModule;
          if (items) {
            const firstKey = Object.keys(items)[0];
            const item = items[firstKey];
            videoUrl = item?.video?.playAddr || item?.video?.downloadAddr || null;
            duration = duration || item?.video?.duration || null;
            title = title || item?.desc || null;
            author = author || item?.author || null;
          }
        } catch {
        }
      }
    }
    if (!videoUrl) {
      return ok({
        platform,
        title,
        author,
        thumbnail,
        video_url: null,
        quality: null,
        duration,
        note: "Metadata retrieved via oembed but video URL could not be extracted. TikTok may require authentication or have changed their page structure."
      });
    }
    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: "original",
      duration
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}
__name(extractTikTok, "extractTikTok");
async function extractTwitter(url) {
  const platform = "twitter";
  try {
    const normalized = url.replace("twitter.com", "x.com");
    const idMatch = normalized.match(/status\/(\d+)/);
    if (!idMatch) return fail(platform, "Could not extract tweet ID from URL");
    const tweetId = idMatch[1];
    const syndicationUrl = `https://cdn.syndication.twimg.com/tweet-result?id=${tweetId}&token=0`;
    const synRes = await fetchPage(syndicationUrl);
    let title = null;
    let author = null;
    let thumbnail = null;
    let videoUrl = null;
    let duration = null;
    if (synRes.ok) {
      try {
        const data = await synRes.json();
        title = data.text || null;
        author = data.user?.screen_name || null;
        const media = data.mediaDetails || [];
        for (const m of media) {
          if (m.type === "video" || m.type === "animated_gif") {
            thumbnail = m.media_url_https || null;
            const variants = m.video_info?.variants || [];
            const mp4s = variants.filter((v) => v.content_type === "video/mp4").sort((a, b) => (b.bitrate || 0) - (a.bitrate || 0));
            if (mp4s.length > 0) {
              videoUrl = mp4s[0].url;
            }
            duration = m.video_info?.duration_millis ? Math.round(m.video_info.duration_millis / 1e3) : null;
          }
        }
      } catch {
      }
    }
    if (!videoUrl) {
      const embedUrl = `https://platform.twitter.com/embed/Tweet.html?id=${tweetId}`;
      const embedRes = await fetchPage(embedUrl);
      if (embedRes.ok) {
        const html = await embedRes.text();
        const vidMatch = html.match(/https:\/\/video\.twimg\.com\/[^"'\s]+\.mp4[^"'\s]*/);
        if (vidMatch) {
          videoUrl = vidMatch[0].replace(/&amp;/g, "&");
        }
      }
    }
    if (!videoUrl) {
      return ok({
        platform,
        title,
        author,
        thumbnail,
        video_url: null,
        quality: null,
        duration,
        note: "Could not extract video URL. The tweet may not contain a video, or Twitter may have restricted access."
      });
    }
    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: "highest_available",
      duration
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}
__name(extractTwitter, "extractTwitter");
async function extractInstagram(url) {
  const platform = "instagram";
  try {
    const shortcodeMatch = url.match(/(?:p|reel|tv)\/([\w-]+)/);
    if (!shortcodeMatch) return fail(platform, "Could not extract shortcode from URL");
    const shortcode = shortcodeMatch[1];
    const embedUrl = `https://www.instagram.com/p/${shortcode}/embed/`;
    const res = await fetchPage(embedUrl);
    if (!res.ok) return fail(platform, `Failed to fetch embed page (HTTP ${res.status})`);
    const html = await res.text();
    let title = null;
    let author = null;
    let thumbnail = null;
    let videoUrl = null;
    const videoPatterns = [
      /"video_url"\s*:\s*"([^"]+)"/,
      /video_url['"]\s*:\s*['"]([^'"]+)['"]/,
      /<source\s+src="([^"]+)"\s+type="video\/mp4"/,
      /data-video-url="([^"]+)"/
    ];
    for (const p of videoPatterns) {
      const m = html.match(p);
      if (m) {
        videoUrl = m[1].replace(/\\u0026/g, "&").replace(/\\\//g, "/");
        break;
      }
    }
    const authorMatch = html.match(/"owner"\s*:\s*\{[^}]*"username"\s*:\s*"([^"]+)"/) || html.match(/data-owner-username="([^"]+)"/) || html.match(/@([\w.]+)/);
    if (authorMatch) author = authorMatch[1];
    const captionMatch = html.match(/"caption"\s*:\s*"([^"]*)"/) || html.match(/<meta[^>]*property="og:title"[^>]*content="([^"]*)"/) || html.match(/class="Caption"[^>]*>([^<]+)/);
    if (captionMatch) title = captionMatch[1];
    const thumbMatch = html.match(/"display_url"\s*:\s*"([^"]+)"/) || html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]+)"/) || html.match(/"thumbnail_src"\s*:\s*"([^"]+)"/);
    if (thumbMatch) thumbnail = thumbMatch[1].replace(/\\\//g, "/").replace(/\\u0026/g, "&");
    const sharedDataMatch = html.match(/window\.__additionalDataLoaded\s*\([^,]*,\s*(\{[\s\S]*?\})\s*\)/);
    if (sharedDataMatch && !videoUrl) {
      try {
        const sd = JSON.parse(sharedDataMatch[1]);
        const media = sd?.graphql?.shortcode_media || sd?.items?.[0];
        if (media) {
          videoUrl = media.video_url || null;
          title = title || media.edge_media_to_caption?.edges?.[0]?.node?.text || null;
          author = author || media.owner?.username || null;
          thumbnail = thumbnail || media.display_url || null;
        }
      } catch {
      }
    }
    if (!videoUrl) {
      return ok({
        platform,
        title,
        author,
        thumbnail,
        video_url: null,
        quality: null,
        duration: null,
        note: "Could not extract video URL. Instagram may require authentication or the post may not contain a video."
      });
    }
    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: "original",
      duration: null
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}
__name(extractInstagram, "extractInstagram");
async function extractYouTube(url) {
  const platform = "youtube";
  try {
    const idMatch = url.match(/(?:v=|shorts\/|youtu\.be\/)([\w-]{11})/);
    if (!idMatch) return fail(platform, "Could not extract video ID from URL");
    const videoId = idMatch[1];
    let title = null;
    let author = null;
    let thumbnail = null;
    let duration = null;
    let videoUrl = null;
    const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
    const oembedRes = await fetchPage(oembedUrl);
    if (oembedRes.ok) {
      const oembed = await oembedRes.json();
      title = oembed.title || null;
      author = oembed.author_name || null;
      thumbnail = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
    } else {
      thumbnail = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
    }
    const watchUrl = `https://www.youtube.com/watch?v=${videoId}`;
    const pageRes = await fetchPage(watchUrl);
    if (pageRes.ok) {
      const html = await pageRes.text();
      const playerMatch = html.match(
        /var\s+ytInitialPlayerResponse\s*=\s*(\{[\s\S]*?\});\s*(?:var|<\/script>)/
      );
      if (playerMatch) {
        try {
          const player = JSON.parse(playerMatch[1]);
          const details = player.videoDetails;
          if (details) {
            title = title || details.title || null;
            author = author || details.author || null;
            duration = details.lengthSeconds ? parseInt(details.lengthSeconds) : null;
            thumbnail = thumbnail || details.thumbnail?.thumbnails?.slice(-1)?.[0]?.url || null;
          }
          const formats = [
            ...player.streamingData?.formats || [],
            ...player.streamingData?.adaptiveFormats || []
          ];
          const combined = formats.filter((f) => f.mimeType?.startsWith("video/mp4") && f.url && f.audioQuality).sort((a, b) => (b.height || 0) - (a.height || 0));
          if (combined.length > 0) {
            videoUrl = combined[0].url;
          } else {
            const any = formats.filter((f) => f.url);
            if (any.length > 0) videoUrl = any[0].url;
          }
        } catch {
        }
      }
    }
    const embedVideoUrl = `https://www.youtube.com/embed/${videoId}`;
    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl || null,
      embed_url: embedVideoUrl,
      quality: videoUrl ? "highest_available" : null,
      duration,
      note: videoUrl ? void 0 : "Direct video URL may be signature-protected. Use the embed_url for embedding, or a dedicated YouTube client library for downloading."
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}
__name(extractYouTube, "extractYouTube");
async function extractFacebook(url) {
  const platform = "facebook";
  try {
    const pageRes = await fetchPage(url, {
      "sec-fetch-dest": "document",
      "sec-fetch-mode": "navigate"
    });
    if (!pageRes.ok) return fail(platform, `Failed to fetch page (HTTP ${pageRes.status})`);
    const html = await pageRes.text();
    let title = null;
    let author = null;
    let thumbnail = null;
    let videoUrl = null;
    let duration = null;
    const ogTitle = html.match(/<meta[^>]*property="og:title"[^>]*content="([^"]*)"/);
    if (ogTitle) title = ogTitle[1];
    const ogImage = html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]*)"/);
    if (ogImage) thumbnail = ogImage[1].replace(/&amp;/g, "&");
    const videoPatterns = [
      /"playable_url"\s*:\s*"([^"]+)"/,
      /"playable_url_quality_hd"\s*:\s*"([^"]+)"/,
      /"sd_src"\s*:\s*"([^"]+)"/,
      /"hd_src"\s*:\s*"([^"]+)"/,
      /hd_src\s*:\s*"([^"]+)"/,
      /sd_src\s*:\s*"([^"]+)"/
    ];
    for (const p of videoPatterns) {
      const m = html.match(p);
      if (m) {
        const candidate = m[1].replace(/\\\//g, "/").replace(/\\u0025/g, "%").replace(/&amp;/g, "&");
        if (!videoUrl || p.source?.includes("hd")) {
          videoUrl = candidate;
        }
      }
    }
    if (!videoUrl) {
      return ok({
        platform,
        title,
        author,
        thumbnail,
        video_url: null,
        quality: null,
        duration,
        note: "Could not extract video URL. Facebook heavily restricts scraping and may require authentication."
      });
    }
    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: "best_available",
      duration
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}
__name(extractFacebook, "extractFacebook");
var EXTRACTORS = {
  tiktok: extractTikTok,
  twitter: extractTwitter,
  instagram: extractInstagram,
  youtube: extractYouTube,
  facebook: extractFacebook
};
async function extract(platform, url) {
  const fn = EXTRACTORS[platform];
  if (!fn) return fail(platform, `No extractor for platform: ${platform}`);
  return fn(url);
}
__name(extract, "extract");

// src/index.js
var index_default = {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }
    if (request.method !== "GET") {
      return jsonResponse({ error: "Method not allowed" }, 405);
    }
    const ip = request.headers.get("cf-connecting-ip") || request.headers.get("x-forwarded-for") || "unknown";
    const maxReqs = parseInt(env.RATE_LIMIT_MAX || "20");
    const windowSec = parseInt(env.RATE_LIMIT_WINDOW_SEC || "60");
    const rateCheck = checkRateLimit(ip, maxReqs, windowSec);
    if (!rateCheck.allowed) {
      return jsonResponse(
        { error: "Rate limit exceeded", remaining: 0, retry_after_sec: Math.ceil((rateCheck.resetAt - Date.now()) / 1e3) },
        429
      );
    }
    const url = new URL(request.url);
    const path = url.pathname;
    if (path === "/" || path === "") {
      return jsonResponse({
        name: "Social Video API",
        version: "1.0.0",
        description: "Extract video download URLs from social media platforms by parsing public HTML pages.",
        endpoints: {
          "GET /download?url=<video_url>": "Extract video download URL",
          "GET /info?url=<video_url>": "Get video metadata without download URL",
          "GET /platforms": "List supported platforms"
        },
        rate_limit: `${maxReqs} requests per ${windowSec} seconds per IP`
      });
    }
    if (path === "/platforms") {
      return jsonResponse({ platforms: SUPPORTED_PLATFORMS });
    }
    if (path === "/download" || path === "/info") {
      const targetUrl = url.searchParams.get("url");
      if (!targetUrl) {
        return jsonResponse({ error: "Missing required parameter: url" }, 400);
      }
      if (!isValidUrl(targetUrl)) {
        return jsonResponse({ error: "Invalid URL format" }, 400);
      }
      const platform = detectPlatform(targetUrl);
      if (!platform) {
        return jsonResponse(
          { error: "Unsupported platform", supported: SUPPORTED_PLATFORMS.map((p) => p.id) },
          400
        );
      }
      const result = await extract(platform, targetUrl);
      if (path === "/info" && result.success) {
        const { video_url, ...meta } = result;
        return jsonResponse(meta);
      }
      return jsonResponse(result, result.success ? 200 : 422);
    }
    return jsonResponse({ error: "Not found" }, 404);
  }
};
export {
  index_default as default
};
//# sourceMappingURL=index.js.map
