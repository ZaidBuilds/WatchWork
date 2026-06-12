export default function ContentDetailLoading() {
  return (
    <main className="min-h-screen bg-cream text-espresso">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-[#fffdf9] p-5 md:block">
        <div className="mb-8 flex items-center gap-3">
          <div className="h-10 w-10 animate-pulse rounded bg-[#E8DED3]" />
          <div className="space-y-2">
            <div className="h-3 w-20 animate-pulse rounded bg-[#E8DED3]" />
            <div className="h-5 w-28 animate-pulse rounded bg-[#E8DED3]" />
          </div>
        </div>
      </aside>
      <section className="md:pl-64">
        <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="mb-6 space-y-3">
            <div className="h-5 w-16 animate-pulse rounded bg-[#E8DED3]" />
            <div className="h-8 w-96 animate-pulse rounded bg-[#E8DED3]" />
            <div className="h-4 w-32 animate-pulse rounded bg-[#E8DED3]" />
          </div>
          <div className="grid gap-5 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="h-96 animate-pulse rounded border border-line bg-[#fffdf9]" />
            <div className="h-96 animate-pulse rounded border border-line bg-[#fffdf9]" />
          </div>
        </div>
      </section>
    </main>
  );
}
