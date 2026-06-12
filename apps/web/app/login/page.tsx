"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Zap } from "lucide-react";
import { apiLogin, apiRegister } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { refresh } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isRegister) {
        await apiRegister(email, password);
      } else {
        await apiLogin(email, password);
      }
      refresh();
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-cream px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 grid h-14 w-14 place-items-center rounded bg-espresso text-cream">
            <Zap size={24} />
          </div>
          <h1 className="text-2xl font-bold text-espresso">Action Engine</h1>
          <p className="mt-1 text-sm text-[#725D50]">Turn learning into execution.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 rounded border border-line bg-[#fffdf9] p-6 shadow-soft">
          <div>
            <label className="mb-1 block text-sm font-semibold text-espresso">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded border border-line px-3 py-2 text-sm focus:border-copper focus:outline-none"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-semibold text-espresso">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded border border-line px-3 py-2 text-sm focus:border-copper focus:outline-none"
              placeholder="At least 6 characters"
              minLength={6}
            />
          </div>

          {error && (
            <div className="rounded border border-[#E5A39C] bg-[#FFF1EF] p-3 text-sm text-[#8B1E18]">{error}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="focus-ring w-full rounded bg-espresso px-4 py-2.5 text-sm font-semibold text-cream hover:opacity-90 disabled:opacity-70"
          >
            {loading ? "Please wait..." : isRegister ? "Create Account" : "Login"}
          </button>

          <button
            type="button"
            onClick={() => { setIsRegister(!isRegister); setError(""); }}
            className="focus-ring w-full rounded border border-line px-4 py-2.5 text-sm font-semibold text-espresso hover:bg-[#f2e8dc]"
          >
            {isRegister ? "Already have an account? Login" : "No account? Create one"}
          </button>
        </form>
      </div>
    </main>
  );
}
