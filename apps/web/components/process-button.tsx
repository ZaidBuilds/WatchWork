"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, WandSparkles } from "lucide-react";
import { apiPost, pollJob, type Job } from "@/lib/api";

export function ProcessButton({ contentId }: { contentId: string }) {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>("");
  const router = useRouter();

  async function process() {
    setLoading(true);
    setStatus("Submitting job...");

    try {
      const job = await apiPost<Job>(`/content/${contentId}/process`);
      setStatus("Processing transcript and generating plan...");

      await pollJob(
        job.id,
        (completedJob) => {
          if (completedJob.status === "failed") {
            setStatus(completedJob.error_message || "Processing failed.");
          } else {
            setStatus("Done!");
          }
          router.refresh();
          setLoading(false);
        },
        (errMsg) => {
          setStatus(errMsg);
          setLoading(false);
        },
      );
    } catch {
      setStatus("Failed to start processing.");
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-end gap-2">
      <button
        onClick={process}
        disabled={loading}
        className="focus-ring inline-flex items-center gap-2 rounded bg-espresso px-4 py-2 text-sm font-semibold text-cream disabled:opacity-70"
      >
        {loading ? <Loader2 size={16} className="animate-spin" /> : <WandSparkles size={16} />}
        {loading ? "Processing..." : "Generate plan"}
      </button>
      {status && <p className="text-xs text-[#725D50]">{status}</p>}
    </div>
  );
}
