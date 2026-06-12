"use client";

import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { BookOpen, Gauge, LogOut, Menu, Settings, X, Zap } from "lucide-react";
import { useAuth } from "@/lib/auth-context";

const nav = [
  { href: "/dashboard", label: "Dashboard", icon: Gauge },
  { href: "/library", label: "Library", icon: BookOpen },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.replace("/login");
    }
  }, [user, loading, router]);

  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-cream">
        <p className="text-sm text-[#725D50]">Loading...</p>
      </main>
    );
  }

  if (!user) return null;

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  return (
    <main className="min-h-screen bg-cream text-espresso">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-[#fffdf9] p-5 md:block">
        <div className="mb-8 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded bg-espresso text-cream">
            <Zap size={20} />
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-copper">Zaidbuilds</p>
            <h1 className="text-xl font-bold">Action Engine</h1>
          </div>
        </div>
        <nav className="space-y-1">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded px-3 py-2 text-sm font-medium hover:bg-[#f2e8dc] ${
                pathname === item.href ? "bg-[#f2e8dc] font-semibold" : ""
              }`}
            >
              <item.icon size={18} />
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="mt-auto border-t border-line pt-4">
          <p className="mb-2 truncate text-xs text-[#725D50]">{user.email}</p>
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded px-3 py-2 text-sm font-medium text-[#8B1E18] hover:bg-[#FFF1EF]"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      <div className="fixed inset-x-0 top-0 z-40 flex items-center border-b border-line bg-[#fffdf9] px-4 py-3 md:hidden">
        <button onClick={() => setMobileOpen(!mobileOpen)} className="mr-3 p-1">
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
        <div className="flex items-center gap-2">
          <div className="grid h-8 w-8 place-items-center rounded bg-espresso text-cream">
            <Zap size={16} />
          </div>
          <span className="font-bold">Action Engine</span>
        </div>
      </div>

      {mobileOpen && (
        <div className="fixed inset-0 z-30 bg-black/20 md:hidden" onClick={() => setMobileOpen(false)} />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 border-r border-line bg-[#fffdf9] p-5 transition-transform duration-200 md:hidden ${
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="mb-8 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded bg-espresso text-cream">
            <Zap size={20} />
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-copper">Zaidbuilds</p>
            <h1 className="text-xl font-bold">Action Engine</h1>
          </div>
        </div>
        <nav className="space-y-1">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded px-3 py-2 text-sm font-medium hover:bg-[#f2e8dc] ${
                pathname === item.href ? "bg-[#f2e8dc]" : ""
              }`}
            >
              <item.icon size={18} />
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="mt-auto border-t border-line pt-4">
          <p className="mb-2 truncate text-xs text-[#725D50]">{user.email}</p>
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded px-3 py-2 text-sm font-medium text-[#8B1E18] hover:bg-[#FFF1EF]"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      <nav className="fixed inset-x-0 bottom-0 z-30 flex border-t border-line bg-[#fffdf9] md:hidden">
        {nav.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-1 flex-col items-center gap-1 py-3 text-xs font-medium ${
              pathname === item.href ? "text-copper" : "text-[#9D8B7F]"
            }`}
          >
            <item.icon size={20} />
            {item.label}
          </Link>
        ))}
      </nav>

      <section className="pb-20 pt-14 md:pl-64 md:pb-0 md:pt-0">
        <div className="mx-auto min-h-screen max-w-6xl px-4 py-6 sm:px-6 lg:px-8">{children}</div>
      </section>
    </main>
  );
}
