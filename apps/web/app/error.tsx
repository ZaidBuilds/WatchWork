"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Global error:", error);
  }, [error]);

  return (
    <main className="flex min-h-screen items-center justify-center bg-cream px-4">
      <div className="max-w-md text-center">
        <h2 className="text-xl font-bold text-espresso">Something went wrong</h2>
        <p className="mt-2 text-sm text-[#725D50]">
          {error.message || "An unexpected error occurred."}
        </p>
        <button
          onClick={reset}
          className="focus-ring mt-6 rounded bg-espresso px-4 py-2 text-sm font-semibold text-cream hover:opacity-90"
        >
          Try again
        </button>
      </div>
    </main>
  );
}
