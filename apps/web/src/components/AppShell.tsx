"use client";

import { BarChart3, Building2, FileSearch, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

const navItems = [
  { href: "/", label: "Investigación", icon: Search, exact: true },
  { href: "/companies", label: "Empresas", icon: Building2 },
  { href: "/campaigns", label: "Campañas", icon: Send },
  { href: "/opportunities", label: "Oportunidades", icon: Sparkles },
  { href: "/analytics", label: "Analítica", icon: BarChart3 },
];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <main className="shell">
      <aside className="sidebar">
        <Link className="brand" href="/">
          <FileSearch size={22} />
          <span>AI Prospecting Engine</span>
        </Link>
        <nav className="nav">
          {navItems.map(({ href, label, icon: Icon, exact }) => {
            const isActive = exact ? pathname === href : pathname.startsWith(href);
            return (
              <Link className={`navItem${isActive ? " active" : ""}`} href={href} key={href}>
                <Icon size={17} />
                {label}
              </Link>
            );
          })}
        </nav>
        <div className="operator">
          <span className="avatar">SB</span>
          <span>
            <strong>Sergio Ballesteros</strong>
            <small>Workspace interno</small>
          </span>
        </div>
      </aside>
      {children}
    </main>
  );
}
