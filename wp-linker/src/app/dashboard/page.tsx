import Dashboard from "@/components/Dashboard";
import { Link2 } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2 font-bold text-lg">
            <div className="w-7 h-7 bg-blue-600 rounded-lg flex items-center justify-center">
              <Link2 className="w-4 h-4 text-white" />
            </div>
            WP Linker
          </a>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span>Dashboard</span>
          </div>
        </div>
      </nav>
      <Dashboard />
    </div>
  );
}
