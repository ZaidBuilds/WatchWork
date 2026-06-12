import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: "WatchWork — Turn Learning Into Execution",
    template: "%s | WatchWork",
  },
  description: "Turn saved YouTube learning content into tracked execution plans. Capture videos, generate AI-powered action plans, and track your progress.",
  keywords: ["productivity", "learning", "YouTube", "action plans", "task management", "AI"],
  authors: [{ name: "Zaidbuilds" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "WatchWork",
    title: "WatchWork — Turn Learning Into Execution",
    description: "Turn saved YouTube learning content into tracked execution plans.",
  },
  twitter: {
    card: "summary_large_image",
    title: "WatchWork — Turn Learning Into Execution",
    description: "Turn saved YouTube learning content into tracked execution plans.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  themeColor: "#FAF7F2",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
      <body className={inter.className}>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
