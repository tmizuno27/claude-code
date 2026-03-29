"use client";

import { createClient } from "@/lib/supabase";
import { LogOut } from "lucide-react";

export default function LogoutButton() {
  const supabase = createClient();

  async function handleLogout() {
    await supabase.auth.signOut();
    window.location.href = "/";
  }

  return (
    <button
      onClick={handleLogout}
      className="text-gray-500 hover:text-red-600 transition flex items-center gap-1"
    >
      <LogOut className="w-4 h-4" />
      Logout
    </button>
  );
}
