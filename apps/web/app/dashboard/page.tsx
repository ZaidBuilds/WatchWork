"use client";

import { Activity, CheckCircle2, Lock, PlusCircle } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/shell";
import { ContentCard } from "@/components/content-card";
import { apiGet, type ContentItem, type PaginatedResponse } from "@/lib/api";

export default function DashboardPage() {
  const [data, setData] = useState<PaginatedResponse<ContentItem>>({ items: [], total: 0, offset: 0, limit: 6 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet<PaginatedResponse<ContentItem>>("/content?limit=6")
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const content = data.items;
  const ready = content.filter((item) => item.status === "ready").length;
  const active = content.filter((item) => item.status !== "failed").length;

  return (
    <AppShell>
      <header className="mb-6">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-copper">Execution cockpit</p>
        <h2 className="mt-2 text-3xl font-bold">Turn captured content into work done.</h2>
      </header>

      <section className="grid gap-3 sm:grid-cols-3">
        <Metric icon={<Activity size={18} />} label="Captured" value={data.total} />
        <Metric icon={<CheckCircle2 size={18} />} label="Plans ready" value={ready} />
        <Metric icon={<Lock size={18} />} label="Active queue" value={active} />
      </section>

      <section className="mt-6 rounded border border-line bg-[#fffdf9] p-5 shadow-soft">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="text-lg font-bold">Autonomous capture</h3>
            <p className="mt-1 max-w-2xl text-sm text-[#725D50]">
              Load the Chrome extension, open a YouTube learning video, and send it here without copying the link.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 rounded bg-[#F2E8DC] px-3 py-2 text-sm font-semibold">
            <PlusCircle size={17} />
            Extension inbox
          </div>
        </div>
      </section>

      <section className="mt-6">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-xl font-bold">Recent captures</h3>
          <Link href="/library" className="text-sm font-semibold text-copper">
            View library
          </Link>
        </div>
        {loading ? (
          <div className="grid gap-4 lg:grid-cols-2">
            {[1, 2].map((i) => (
              <div key={i} className="h-32 animate-pulse rounded border border-line bg-[#fffdf9]" />
            ))}
          </div>
        ) : content.length > 0 ? (
          <div className="grid gap-4 lg:grid-cols-2">
            {content.map((item) => (
              <ContentCard key={item.id} item={item} />
            ))}
          </div>
        ) : (
          <div className="rounded border border-dashed border-line p-8 text-center text-[#725D50]">
            No captures yet. Your first win is loading the extension and sending one high-value video.
          </div>
        )}
      </section>
    </AppShell>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: number }) {
  return (
    <div className="rounded border border-line bg-[#fffdf9] p-4 shadow-soft">
      <div className="mb-3 flex h-9 w-9 items-center justify-center rounded bg-espresso text-cream">{icon}</div>
      <p className="text-3xl font-bold">{value}</p>
      <p className="text-sm text-[#725D50]">{label}</p>
    </div>
  );
}
