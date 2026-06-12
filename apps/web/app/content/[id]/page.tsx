"use client";

import { notFound, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/shell";
import { ProcessButton } from "@/components/process-button";
import { StatusBadge } from "@/components/status-badge";
import { TaskList } from "@/components/task-list";
import { apiGet, type ContentDetail } from "@/lib/api";

export default function ContentDetailPage() {
  const params = useParams<{ id: string }>();
  const [detail, setDetail] = useState<ContentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFoundState, setNotFoundState] = useState(false);

  useEffect(() => {
    if (!params?.id) return;
    apiGet<ContentDetail>(`/content/${params.id}`)
      .then(setDetail)
      .catch(() => setNotFoundState(true))
      .finally(() => setLoading(false));
  }, [params?.id]);

  if (loading) {
    return (
      <AppShell>
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-48 rounded bg-[#f2e8dc]" />
          <div className="h-12 w-96 rounded bg-[#f2e8dc]" />
          <div className="grid gap-5 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="h-64 rounded border border-line bg-[#fffdf9]" />
            <div className="h-64 rounded border border-line bg-[#fffdf9]" />
          </div>
        </div>
      </AppShell>
    );
  }

  if (notFoundState || !detail) {
    return (
      <AppShell>
        <div className="rounded border border-dashed border-line p-16 text-center">
          <p className="text-lg font-bold">Content not found</p>
          <p className="mt-2 text-sm text-[#725D50]">This capture may have been removed.</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <StatusBadge status={detail.status} />
          <h2 className="mt-3 max-w-3xl text-3xl font-bold">{detail.title || "Untitled capture"}</h2>
          <p className="mt-2 text-[#725D50]">{detail.channel_name || detail.platform}</p>
        </div>
        {detail.status === "pending" || detail.status === "failed" ? <ProcessButton contentId={detail.id} /> : null}
      </div>

      {detail.error_message ? (
        <div className="mb-5 rounded border border-[#E5A39C] bg-[#FFF1EF] p-4 text-sm text-[#8B1E18]">
          {detail.error_message}
        </div>
      ) : null}

      <div className="grid gap-5 lg:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded border border-line bg-[#fffdf9] p-5 shadow-soft">
          <h3 className="text-lg font-bold">Source summary</h3>
          {detail.thumbnail_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={detail.thumbnail_url} alt="" className="mt-4 aspect-video w-full rounded object-cover" />
          ) : null}
          <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-[#725D50]">
            {detail.transcript_preview || "Transcript preview will appear after processing."}
          </p>
        </section>

        <section>
          {detail.plan ? (
            <div className="space-y-5">
              <div className="rounded border border-line bg-[#fffdf9] p-5 shadow-soft">
                <div className="mb-3 flex items-center justify-between">
                  <h3 className="text-lg font-bold">Execution plan</h3>
                  <span className="rounded bg-[#F2E8DC] px-3 py-1 text-sm font-bold">
                    {detail.plan.completion_pct}% complete
                  </span>
                </div>
                <p className="text-sm leading-6 text-[#725D50]">{detail.plan.summary}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {detail.plan.key_concepts.map((concept) => (
                    <span key={concept} className="rounded bg-[#FFE4DC] px-2 py-1 text-xs font-semibold">
                      {concept}
                    </span>
                  ))}
                </div>
              </div>
              <TaskList tasks={detail.plan.tasks} />
            </div>
          ) : (
            <div className="rounded border border-dashed border-line p-8 text-center text-[#725D50]">
              Generate the plan when the capture is ready.
            </div>
          )}
        </section>
      </div>
    </AppShell>
  );
}
