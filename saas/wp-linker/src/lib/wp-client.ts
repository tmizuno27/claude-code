/**
 * WordPress REST API client
 */

import type { WPPost } from "./types";

export class WPClient {
  private restApiUrl: string;
  private authHeader: string;

  constructor(restApiUrl: string, username: string, appPassword: string) {
    this.restApiUrl = restApiUrl.replace(/\/$/, "");
    this.authHeader =
      "Basic " + Buffer.from(`${username}:${appPassword}`).toString("base64");
  }

  private async request(path: string, options?: RequestInit) {
    const res = await fetch(`${this.restApiUrl}${path}`, {
      ...options,
      headers: {
        Authorization: this.authHeader,
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
    if (!res.ok) {
      const body = await res.text().catch(() => "");
      throw new Error(`WP API ${res.status}: ${body}`);
    }
    return res;
  }

  async testConnection(): Promise<{ name: string; url: string }> {
    const res = await fetch(this.restApiUrl.replace("/wp/v2", ""), {
      headers: { Authorization: this.authHeader },
    });
    if (!res.ok) throw new Error(`Connection failed: ${res.status}`);
    const data = await res.json();
    return { name: data.name, url: data.url };
  }

  async fetchAllPosts(): Promise<WPPost[]> {
    const allPosts: WPPost[] = [];
    let page = 1;

    while (true) {
      const params = new URLSearchParams({
        per_page: "100",
        status: "publish",
        page: String(page),
        _fields: "id,title,link,content",
      });

      const res = await this.request(`/posts?${params}`);
      const posts: WPPost[] = await res.json();

      if (!posts.length) break;
      allPosts.push(...posts);

      const totalPages = parseInt(
        res.headers.get("X-WP-TotalPages") ?? "1",
        10
      );
      if (page >= totalPages) break;
      page++;
    }

    return allPosts;
  }

  async updatePostContent(postId: number, newContent: string): Promise<void> {
    await this.request(`/posts/${postId}`, {
      method: "POST",
      body: JSON.stringify({ content: newContent }),
    });
  }
}
