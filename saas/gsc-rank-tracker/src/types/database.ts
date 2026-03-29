export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string;
          email: string;
          plan: "free" | "starter" | "pro" | "agency";
          stripe_customer_id: string | null;
          gsc_access_token: string | null;
          gsc_refresh_token: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          email: string;
          plan?: "free" | "starter" | "pro" | "agency";
          stripe_customer_id?: string | null;
          gsc_access_token?: string | null;
          gsc_refresh_token?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          email?: string;
          plan?: "free" | "starter" | "pro" | "agency";
          stripe_customer_id?: string | null;
          gsc_access_token?: string | null;
          gsc_refresh_token?: string | null;
          updated_at?: string;
        };
      };
      sites: {
        Row: {
          id: string;
          user_id: string;
          domain: string;
          gsc_property_url: string;
          is_active: boolean;
          last_synced_at: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          domain: string;
          gsc_property_url: string;
          is_active?: boolean;
          last_synced_at?: string | null;
          created_at?: string;
        };
        Update: {
          domain?: string;
          gsc_property_url?: string;
          is_active?: boolean;
          last_synced_at?: string | null;
        };
      };
      keywords: {
        Row: {
          id: string;
          site_id: string;
          query: string;
          is_tracked: boolean;
          created_at: string;
        };
        Insert: {
          id?: string;
          site_id: string;
          query: string;
          is_tracked?: boolean;
          created_at?: string;
        };
        Update: {
          is_tracked?: boolean;
        };
      };
      rankings: {
        Row: {
          id: string;
          site_id: string;
          date: string;
          page_url: string;
          query: string;
          position: number;
          impressions: number;
          clicks: number;
          ctr: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          site_id: string;
          date: string;
          page_url: string;
          query: string;
          position: number;
          impressions: number;
          clicks: number;
          ctr: number;
          created_at?: string;
        };
        Update: {
          position?: number;
          impressions?: number;
          clicks?: number;
          ctr?: number;
        };
      };
      alerts: {
        Row: {
          id: string;
          site_id: string;
          alert_type: "position_drop" | "ctr_low" | "impressions_spike";
          threshold: number;
          notification_channels: {
            email?: boolean;
            slack_webhook?: string;
          };
          is_active: boolean;
          created_at: string;
        };
        Insert: {
          id?: string;
          site_id: string;
          alert_type: "position_drop" | "ctr_low" | "impressions_spike";
          threshold: number;
          notification_channels?: {
            email?: boolean;
            slack_webhook?: string;
          };
          is_active?: boolean;
          created_at?: string;
        };
        Update: {
          threshold?: number;
          notification_channels?: {
            email?: boolean;
            slack_webhook?: string;
          };
          is_active?: boolean;
        };
      };
      alert_logs: {
        Row: {
          id: string;
          alert_id: string;
          triggered_at: string;
          payload: Json;
        };
        Insert: {
          id?: string;
          alert_id: string;
          triggered_at?: string;
          payload: Json;
        };
        Update: Record<string, never>;
      };
    };
    Views: Record<string, never>;
    Functions: Record<string, never>;
    Enums: {
      plan_type: "free" | "starter" | "pro" | "agency";
      alert_type: "position_drop" | "ctr_low" | "impressions_spike";
    };
  };
};

// 便利な型エイリアス
export type User = Database["public"]["Tables"]["users"]["Row"];
export type Site = Database["public"]["Tables"]["sites"]["Row"];
export type Keyword = Database["public"]["Tables"]["keywords"]["Row"];
export type Ranking = Database["public"]["Tables"]["rankings"]["Row"];
export type Alert = Database["public"]["Tables"]["alerts"]["Row"];
export type AlertLog = Database["public"]["Tables"]["alert_logs"]["Row"];
export type PlanType = Database["public"]["Enums"]["plan_type"];
