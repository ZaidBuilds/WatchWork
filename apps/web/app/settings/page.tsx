import { SettingsForm } from "./settings-form";
import { AppShell } from "@/components/shell";
import { apiGet } from "@/lib/api";

type Settings = {
  gatekeeper_enabled: boolean;
  gatekeeper_threshold: number;
};

export default async function SettingsPage() {
  const settings = await apiGet<Settings>("/settings").catch(() => ({
    gatekeeper_enabled: false,
    gatekeeper_threshold: 70,
  }));

  return (
    <AppShell>
      <header className="mb-6">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-copper">Settings</p>
        <h2 className="mt-2 text-3xl font-bold">Control the execution pressure.</h2>
      </header>
      <SettingsForm initial={settings} />
    </AppShell>
  );
}
