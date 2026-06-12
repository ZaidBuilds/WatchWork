"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/shell";
import { SettingsForm } from "./settings-form";
import { apiGet } from "@/lib/api";

type Settings = {
  gatekeeper_enabled: boolean;
  gatekeeper_threshold: number;
};

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings>({ gatekeeper_enabled: false, gatekeeper_threshold: 70 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet<Settings>("/settings")
      .then(setSettings)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <AppShell>
      <header className="mb-6">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-copper">Settings</p>
        <h2 className="mt-2 text-3xl font-bold">Control the execution pressure.</h2>
      </header>
      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-12 rounded border border-line bg-[#fffdf9]" />
          <div className="h-12 rounded border border-line bg-[#fffdf9]" />
        </div>
      ) : (
        <SettingsForm initial={settings} />
      )}
    </AppShell>
  );
}
