import Link from "next/link";
import { Clock, ExternalLink } from "lucide-react";
import type { ContentItem } from "@/lib/api";
import { StatusBadge } from "./status-badge";

export function ContentCard({ item }: { item: ContentItem }) {
  return (
    <article className="rounded border border-line bg-[#fffdf9] p-4 shadow-soft">
      <div className="flex gap-4">
        <div className="h-20 w-32 shrink-0 overflow-hidden rounded bg-[#eaded1]">
          {item.thumbnail_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={item.thumbnail_url} alt="" className="h-full w-full object-cover" />
          ) : null}
        </div>
        <div className="min-w-0 flex-1">
          <div className="mb-2 flex items-center justify-between gap-2">
            <StatusBadge status={item.status} />
            <a href={item.source_url} target="_blank" rel="noopener noreferrer" className="text-copper" aria-label="Open source">
              <ExternalLink size={16} />
            </a>
          </div>
          <Link href={`/content/${item.id}`} className="line-clamp-2 font-semibold hover:text-copper">
            {item.title || "Untitled capture"}
          </Link>
          <p className="mt-1 truncate text-sm text-[#725D50]">{item.channel_name || item.platform}</p>
          <p className="mt-3 flex items-center gap-1 text-xs text-[#8A7467]">
            <Clock size={14} />
            {new Date(item.created_at).toLocaleString()}
          </p>
        </div>
      </div>
    </article>
  );
}
