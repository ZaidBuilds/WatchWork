import Link from "next/link";

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-cream px-4">
      <div className="grid h-16 w-16 place-items-center rounded bg-espresso text-cream">
        <span className="text-2xl font-bold">?</span>
      </div>
      <h1 className="mt-6 text-3xl font-bold">Page not found</h1>
      <p className="mt-2 max-w-md text-center text-[#725D50]">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link
        href="/dashboard"
        className="mt-6 rounded bg-espresso px-6 py-3 text-sm font-semibold text-cream hover:opacity-90"
      >
        Back to dashboard
      </Link>
    </main>
  );
}
