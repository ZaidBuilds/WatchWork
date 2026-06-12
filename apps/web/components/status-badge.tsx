import type { ContentItem } from "@/lib/api";

const statusStyle: Record<ContentItem["status"], string> = {
  pending: "bg-[#F2E8DC] text-espresso",
  transcribing: "bg-[#FCEAD8] text-[#8A4B20]",
  analyzing: "bg-[#FFE4DC] text-[#9A351F]",
  ready: "bg-[#E4F4E8] text-[#245B31]",
  failed: "bg-[#F9D8D5] text-[#8B1E18]",
};

export function StatusBadge({ status }: { status: ContentItem["status"] }) {
  return (
    <span className={`inline-flex rounded px-2 py-1 text-xs font-semibold ${statusStyle[status]}`}>
      {status}
    </span>
  );
}
