import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Prospecting Engine",
  description: "Evidence-backed B2B company research workflow",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
