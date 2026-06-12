"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/shell";
import { ContentCard } from "@/components/content-card";
import { apiGet, type ContentItem, type PaginatedResponse } from "@/lib/api";

export default function LibraryPage() {
  const [items, setItems] = useState<ContentItem[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const limit = 20;

  useEffect(() => {
    apiGet<PaginatedResponse<ContentItem>>(`/content?offset=0&limit=${limit}`)
      .then((data) => {
        setItems(data.items);
        setTotal(data.total);
        setOffset(data.items.length);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  async function loadMore() {
    setLoadingMore(true);
    try {
      const data = await apiGet<PaginatedResponse<ContentItem>>(`/content?offset=${offset}&limit=${limit}`);
      setItems((prev) => [...prev, ...data.items]);
      setOffset((prev) => prev + data.items.length);
    } catch {}
    setLoadingMore(false);
  }

  return (
    <AppShell>
      <header className="mb-6">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-copper">Library</p>
        <h2 className="mt-2 text-3xl font-bold">Captured learning assets</h2>
        <p className="mt-1 text-sm text-[#725D50]">{total} total captures</p>
      </header>

      {loading ? (
        <div className="grid gap-4 lg:grid-cols-2">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-28 animate-pulse rounded border border-line bg-[#fffdf9]" />
          ))}
        </div>
      ) : (
        <>
          <div className="grid gap-4 lg:grid-cols-2">
            {items.map((item) => (
              <ContentCard key={item.id} item={item} />
            ))}
          </div>

          {items.length === 0 ? (
            <div className="rounded border border-dashed border-line p-8 text-center text-[#725D50]">
              The library fills automatically from the browser extension.
            </div>
          ) : offset < total ? (
            <div className="mt-6 text-center">
              <button
                onClick={loadMore}
                disabled={loadingMore}
                className="focus-ring rounded border border-line bg-[#fffdf9] px-6 py-2 text-sm font-semibold text-espresso hover:bg-[#f2e8dc] disabled:opacity-70"
              >
                {loadingMore ? "Loading..." : "Load more"}
              </button>
            </div>
          ) : null}
        </>
      )}
    </AppShell>
  );
}
