import { browserHeaders, fetchWithRetry } from './utils.js';

// ─── Helper ────────────────────────────────────────────────────

function fail(platform, message) {
  return { success: false, platform, error: message };
}

function ok(data) {
  return { success: true, ...data };
}

/**
 * Fetch a URL with browser-like headers and retry/timeout support.
 */
async function fetchPage(url, extraHeaders = {}) {
  return fetchWithRetry(url, {
    headers: browserHeaders(extraHeaders),
    redirect: 'follow',
  });
}

// ─── TikTok ────────────────────────────────────────────────────

export async function extractTikTok(url) {
  const platform = 'tiktok';

  try {
    // 1) Try oembed first (reliable for metadata)
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

    // 2) Fetch the actual page to find video URL
    const pageRes = await fetchPage(url);
    if (!pageRes.ok) return fail(platform, `Failed to fetch page (HTTP ${pageRes.status})`);

    const html = await pageRes.text();

    // Look for video URL in __UNIVERSAL_DATA_FOR_REHYDRATION__
    let videoUrl = null;
    let duration = null;

    const rehydrationMatch = html.match(
      /<script[^>]*id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>([\s\S]*?)<\/script>/
    );
    if (rehydrationMatch) {
      try {
        const data = JSON.parse(rehydrationMatch[1]);
        // Navigate the nested structure to find video play URL
        const defaultScope = data?.__DEFAULT_SCOPE__;
        const videoDetail =
          defaultScope?.['webapp.video-detail']?.itemInfo?.itemStruct ||
          defaultScope?.['webapp.video-detail']?.itemStruct;

        if (videoDetail) {
          videoUrl = videoDetail.video?.playAddr || videoDetail.video?.downloadAddr || null;
          duration = videoDetail.video?.duration || null;
          title = title || videoDetail.desc || null;
          author = author || videoDetail.author?.uniqueId || null;
          thumbnail = thumbnail || videoDetail.video?.cover || null;
        }
      } catch {
        // JSON parse failed, continue with other methods
      }
    }

    // Fallback: look for video URL patterns in the HTML
    if (!videoUrl) {
      const patterns = [
        /"playAddr"\s*:\s*"([^"]+)"/,
        /"downloadAddr"\s*:\s*"([^"]+)"/,
        /playAddr['"]\s*:\s*['"]([^'"]+)['"]/,
      ];
      for (const p of patterns) {
        const m = html.match(p);
        if (m) {
          videoUrl = m[1].replace(/\\u002F/g, '/').replace(/\\u0026/g, '&');
          break;
        }
      }
    }

    // Fallback: SIGI_STATE
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
          // ignore
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
        note: 'Metadata retrieved via oembed but video URL could not be extracted. TikTok may require authentication or have changed their page structure.',
      });
    }

    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: 'original',
      duration,
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}

// ─── Twitter / X ───────────────────────────────────────────────

export async function extractTwitter(url) {
  const platform = 'twitter';

  try {
    // Normalize to x.com
    const normalized = url.replace('twitter.com', 'x.com');

    // Extract tweet ID
    const idMatch = normalized.match(/status\/(\d+)/);
    if (!idMatch) return fail(platform, 'Could not extract tweet ID from URL');
    const tweetId = idMatch[1];

    // 1) Try syndication API (publicly accessible)
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

        // Look for video in mediaDetails
        const media = data.mediaDetails || [];
        for (const m of media) {
          if (m.type === 'video' || m.type === 'animated_gif') {
            thumbnail = m.media_url_https || null;
            const variants = m.video_info?.variants || [];
            // Pick highest bitrate mp4
            const mp4s = variants
              .filter((v) => v.content_type === 'video/mp4')
              .sort((a, b) => (b.bitrate || 0) - (a.bitrate || 0));
            if (mp4s.length > 0) {
              videoUrl = mp4s[0].url;
            }
            duration = m.video_info?.duration_millis
              ? Math.round(m.video_info.duration_millis / 1000)
              : null;
          }
        }
      } catch {
        // parse failed
      }
    }

    // 2) Fallback: try embed page
    if (!videoUrl) {
      const embedUrl = `https://platform.twitter.com/embed/Tweet.html?id=${tweetId}`;
      const embedRes = await fetchPage(embedUrl);
      if (embedRes.ok) {
        const html = await embedRes.text();
        const vidMatch = html.match(/https:\/\/video\.twimg\.com\/[^"'\s]+\.mp4[^"'\s]*/);
        if (vidMatch) {
          videoUrl = vidMatch[0].replace(/&amp;/g, '&');
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
        note: 'Could not extract video URL. The tweet may not contain a video, or Twitter may have restricted access.',
      });
    }

    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: 'highest_available',
      duration,
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}

// ─── Instagram ─────────────────────────────────────────────────

export async function extractInstagram(url) {
  const platform = 'instagram';

  try {
    // Extract shortcode
    const shortcodeMatch = url.match(/(?:p|reel|tv)\/([\w-]+)/);
    if (!shortcodeMatch) return fail(platform, 'Could not extract shortcode from URL');
    const shortcode = shortcodeMatch[1];

    // Fetch embed page (publicly accessible)
    const embedUrl = `https://www.instagram.com/p/${shortcode}/embed/`;
    const res = await fetchPage(embedUrl);
    if (!res.ok) return fail(platform, `Failed to fetch embed page (HTTP ${res.status})`);

    const html = await res.text();

    let title = null;
    let author = null;
    let thumbnail = null;
    let videoUrl = null;

    // Extract video URL from embed page
    const videoPatterns = [
      /"video_url"\s*:\s*"([^"]+)"/,
      /video_url['"]\s*:\s*['"]([^'"]+)['"]/,
      /<source\s+src="([^"]+)"\s+type="video\/mp4"/,
      /data-video-url="([^"]+)"/,
    ];

    for (const p of videoPatterns) {
      const m = html.match(p);
      if (m) {
        videoUrl = m[1].replace(/\\u0026/g, '&').replace(/\\\//g, '/');
        break;
      }
    }

    // Extract metadata
    const authorMatch = html.match(/"owner"\s*:\s*\{[^}]*"username"\s*:\s*"([^"]+)"/) ||
      html.match(/data-owner-username="([^"]+)"/) ||
      html.match(/@([\w.]+)/);
    if (authorMatch) author = authorMatch[1];

    const captionMatch = html.match(/"caption"\s*:\s*"([^"]*)"/) ||
      html.match(/<meta[^>]*property="og:title"[^>]*content="([^"]*)"/) ||
      html.match(/class="Caption"[^>]*>([^<]+)/);
    if (captionMatch) title = captionMatch[1];

    const thumbMatch = html.match(/"display_url"\s*:\s*"([^"]+)"/) ||
      html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]+)"/) ||
      html.match(/"thumbnail_src"\s*:\s*"([^"]+)"/);
    if (thumbMatch) thumbnail = thumbMatch[1].replace(/\\\//g, '/').replace(/\\u0026/g, '&');

    // Also try the shared data JSON
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
        // ignore
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
        note: 'Could not extract video URL. Instagram may require authentication or the post may not contain a video.',
      });
    }

    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: 'original',
      duration: null,
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}

// ─── YouTube ───────────────────────────────────────────────────

export async function extractYouTube(url) {
  const platform = 'youtube';

  try {
    // Extract video ID
    const idMatch = url.match(/(?:v=|shorts\/|youtu\.be\/)([\w-]{11})/);
    if (!idMatch) return fail(platform, 'Could not extract video ID from URL');
    const videoId = idMatch[1];

    let title = null;
    let author = null;
    let thumbnail = null;
    let duration = null;
    let videoUrl = null;

    // 1) oembed for metadata (very reliable)
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

    // 2) Fetch watch page to look for streaming data
    const watchUrl = `https://www.youtube.com/watch?v=${videoId}`;
    const pageRes = await fetchPage(watchUrl);

    if (pageRes.ok) {
      const html = await pageRes.text();

      // Look for ytInitialPlayerResponse
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

          // Try to get streaming URLs (often signature-protected)
          const formats = [
            ...(player.streamingData?.formats || []),
            ...(player.streamingData?.adaptiveFormats || []),
          ];

          // Prefer mp4 with both audio+video
          const combined = formats
            .filter((f) => f.mimeType?.startsWith('video/mp4') && f.url && f.audioQuality)
            .sort((a, b) => (b.height || 0) - (a.height || 0));

          if (combined.length > 0) {
            videoUrl = combined[0].url;
          } else {
            // Any format with direct URL
            const any = formats.filter((f) => f.url);
            if (any.length > 0) videoUrl = any[0].url;
          }
        } catch {
          // JSON parse error
        }
      }
    }

    // YouTube embed URL as fallback reference
    const embedVideoUrl = `https://www.youtube.com/embed/${videoId}`;

    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl || null,
      embed_url: embedVideoUrl,
      quality: videoUrl ? 'highest_available' : null,
      duration,
      note: videoUrl
        ? undefined
        : 'Direct video URL may be signature-protected. Use the embed_url for embedding, or a dedicated YouTube client library for downloading.',
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}

// ─── Facebook ──────────────────────────────────────────────────

export async function extractFacebook(url) {
  const platform = 'facebook';

  try {
    // Fetch the page
    const pageRes = await fetchPage(url, {
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
    });
    if (!pageRes.ok) return fail(platform, `Failed to fetch page (HTTP ${pageRes.status})`);

    const html = await pageRes.text();

    let title = null;
    let author = null;
    let thumbnail = null;
    let videoUrl = null;
    let duration = null;

    // Extract og:title
    const ogTitle = html.match(/<meta[^>]*property="og:title"[^>]*content="([^"]*)"/) ;
    if (ogTitle) title = ogTitle[1];

    // Extract og:image
    const ogImage = html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]*)"/);
    if (ogImage) thumbnail = ogImage[1].replace(/&amp;/g, '&');

    // Look for video URL patterns in the page
    const videoPatterns = [
      /"playable_url"\s*:\s*"([^"]+)"/,
      /"playable_url_quality_hd"\s*:\s*"([^"]+)"/,
      /"sd_src"\s*:\s*"([^"]+)"/,
      /"hd_src"\s*:\s*"([^"]+)"/,
      /hd_src\s*:\s*"([^"]+)"/,
      /sd_src\s*:\s*"([^"]+)"/,
    ];

    for (const p of videoPatterns) {
      const m = html.match(p);
      if (m) {
        const candidate = m[1].replace(/\\\//g, '/').replace(/\\u0025/g, '%').replace(/&amp;/g, '&');
        // Prefer HD
        if (!videoUrl || p.source?.includes('hd')) {
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
        note: 'Could not extract video URL. Facebook heavily restricts scraping and may require authentication.',
      });
    }

    return ok({
      platform,
      title,
      author,
      thumbnail,
      video_url: videoUrl,
      quality: 'best_available',
      duration,
    });
  } catch (e) {
    return fail(platform, `Extraction error: ${e.message}`);
  }
}

// ─── Dispatcher ────────────────────────────────────────────────

const EXTRACTORS = {
  tiktok: extractTikTok,
  twitter: extractTwitter,
  instagram: extractInstagram,
  youtube: extractYouTube,
  facebook: extractFacebook,
};

export async function extract(platform, url) {
  const fn = EXTRACTORS[platform];
  if (!fn) return fail(platform, `No extractor for platform: ${platform}`);
  return fn(url);
}
