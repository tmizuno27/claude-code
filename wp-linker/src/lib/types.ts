// ---- WordPress types ----
export interface WPPost {
  id: number;
  title: { rendered: string };
  link: string;
  content: { rendered: string };
}

// ---- App domain types ----
export interface Site {
  id: string;
  name: string;
  url: string;
  rest_api_url: string;
  username: string;
  app_password: string;
  post_count?: number;
  last_analyzed?: string;
  created_at: string;
}

export interface LinkSuggestion {
  source_post_id: number;
  source_title: string;
  source_url: string;
  target_post_id: number;
  target_title: string;
  target_url: string;
  relevance_score: number;
  already_linked: boolean;
}

export interface AnalysisReport {
  id: string;
  site_id: string;
  created_at: string;
  total_posts: number;
  orphan_posts: number;
  suggestions_count: number;
  applied_count: number;
  suggestions: LinkSuggestion[];
}

export interface OrphanPost {
  post_id: number;
  title: string;
  url: string;
  incoming_links: number;
  outgoing_links: number;
}

export interface PostLinkStats {
  post_id: number;
  title: string;
  url: string;
  incoming_links: number;
  outgoing_links: number;
  linked_from: string[]; // titles of posts linking TO this post
  links_to: string[]; // titles of posts this post links TO
}
