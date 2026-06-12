"use client";

import { useState } from "react";
import { Save } from "lucide-react";
import { apiPatch } from "@/lib/api";

type Settings = {
  gatekeeper_enabled: boolean;
  gatekeeper_threshold: number;
};

export function SettingsForm({ initial }: { initial: Settings }) {
  const [settings, setSettings] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function save() {
    setSaving(true);
    setError(null);
    try {
      const updated = await apiPatch<Settings>("/settings", settings);
      setSettings(updated);
      setSaved(true);
      window.setTimeout(() => setSaved(false), 1800);
    } catch {
      setError("Failed to save settings. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="max-w-xl rounded border border-line bg-[#fffdf9] p-5 shadow-soft">
      <label className="flex items-center justify-between gap-4">
        <span>
          <span className="block font-bold">Gatekeeper mode</span>
          <span className="mt-1 block text-sm text-[#725D50]">
            Block new captures until active plans hit the required completion level.
          </span>
        </span>
        <input
          type="checkbox"
          checked={settings.gatekeeper_enabled}
          onChange={(event) => setSettings((current) => ({ ...current, gatekeeper_enabled: event.target.checked }))}
          className="h-5 w-5 accent-copper"
        />
      </label>

      <div className="mt-6">
        <label className="mb-2 flex items-center justify-between text-sm font-semibold">
          Completion threshold
          <span>{settings.gatekeeper_threshold}%</span>
        </label>
        <input
          type="range"
          min="10"
          max="100"
          step="5"
          value={settings.gatekeeper_threshold}
          onChange={(event) =>
            setSettings((current) => ({ ...current, gatekeeper_threshold: Number(event.target.value) }))
          }
          className="w-full accent-copper"
        />
      </div>

      {error && (
        <div className="mt-4 rounded border border-[#E5A39C] bg-[#FFF1EF] p-3 text-sm text-[#8B1E18]">{error}</div>
      )}

      <button
        onClick={save}
        disabled={saving}
        className="focus-ring mt-6 inline-flex items-center gap-2 rounded bg-espresso px-4 py-2 text-sm font-semibold text-cream disabled:opacity-70"
      >
        <Save size={16} />
        {saving ? "Saving..." : saved ? "Saved" : "Save settings"}
      </button>
    </section>
  );
}
