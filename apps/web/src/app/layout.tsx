import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Prospecting Engine",
  description: "Flujo de investigación B2B basado en evidencia",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
