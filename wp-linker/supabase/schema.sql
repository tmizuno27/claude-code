-- WP Linker Database Schema
-- Run this in Supabase SQL Editor

-- Sites table: stores WordPress site connections
create table public.sites (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  name text not null,
  url text not null,
  rest_api_url text not null,
  username text not null,
  app_password text not null,
  post_count integer default 0,
  last_analyzed timestamptz,
  created_at timestamptz default now() not null
);

-- Analysis reports table
create table public.analyses (
  id uuid default gen_random_uuid() primary key,
  site_id uuid references public.sites(id) on delete cascade not null,
  user_id uuid references auth.users(id) on delete cascade not null,
  total_posts integer not null default 0,
  orphan_count integer not null default 0,
  suggestions_count integer not null default 0,
  applied_count integer not null default 0,
  coverage integer not null default 0,
  report jsonb not null default '{}',
  created_at timestamptz default now() not null
);

-- Row Level Security
alter table public.sites enable row level security;
alter table public.analyses enable row level security;

-- Users can only see their own sites
create policy "Users can view own sites"
  on public.sites for select
  using (auth.uid() = user_id);

create policy "Users can insert own sites"
  on public.sites for insert
  with check (auth.uid() = user_id);

create policy "Users can update own sites"
  on public.sites for update
  using (auth.uid() = user_id);

create policy "Users can delete own sites"
  on public.sites for delete
  using (auth.uid() = user_id);

-- Users can only see their own analyses
create policy "Users can view own analyses"
  on public.analyses for select
  using (auth.uid() = user_id);

create policy "Users can insert own analyses"
  on public.analyses for insert
  with check (auth.uid() = user_id);
