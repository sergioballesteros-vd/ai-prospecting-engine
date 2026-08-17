"use client";

import { FileSearch, Save, Search, Send, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { createCampaign } from "@/lib/api";

export default function NewCampaignPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setError(null);
    setIsSubmitting(true);
    try {
      const campaign = await createCampaign({
        name: String(data.get("name") || ""),
        country: String(data.get("country") || ""),
        city_or_region: String(data.get("city_or_region") || ""),
        industries: String(data.get("industries") || "")
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        employee_min: numberOrNull(data.get("employee_min")),
        employee_max: numberOrNull(data.get("employee_max")),
        opportunity_id: 1,
        target_company_count: Number(data.get("target_company_count") || 20),
      });
      router.push(`/campaigns/${campaign.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo crear la campaña");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <FileSearch size={22} />
          <span>AI Prospecting Engine</span>
        </div>
        <nav className="nav">
          <Link className="navItem" href="/">
            <Search size={17} />
            Investigación
          </Link>
          <Link className="navItem active" href="/campaigns">
            <Send size={17} />
            Campañas
          </Link>
          <Link className="navItem" href="/opportunities">
            <Sparkles size={17} />
            Oportunidades
          </Link>
        </nav>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Nueva campaña</h1>
            <p>Ejemplo: empresas de formación en Madrid, 10-150 empleados.</p>
          </div>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        <form className="campaignForm" onSubmit={submit}>
          <label>
            <span>Nombre</span>
            <input name="name" defaultValue="Empresas de formación en Madrid" required />
          </label>
          <label>
            <span>País</span>
            <input name="country" defaultValue="Spain" required />
          </label>
          <label>
            <span>Ciudad / región</span>
            <input name="city_or_region" defaultValue="Madrid" required />
          </label>
          <label>
            <span>Industrias</span>
            <input name="industries" defaultValue="training companies" required />
          </label>
          <label>
            <span>Empleados mín.</span>
            <input name="employee_min" type="number" defaultValue="10" />
          </label>
          <label>
            <span>Empleados máx.</span>
            <input name="employee_max" type="number" defaultValue="150" />
          </label>
          <label>
            <span>Número de empresas objetivo</span>
            <input name="target_company_count" type="number" min="1" max="100" defaultValue="20" />
          </label>
          <label>
            <span>Hipótesis de oportunidad</span>
            <input value="Sales Operations Automation" disabled />
          </label>
          <button type="submit" disabled={isSubmitting}>
            <Save size={16} />
            Crear campaña
          </button>
        </form>
      </section>
    </main>
  );
}

function numberOrNull(value: FormDataEntryValue | null) {
  if (!value) return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}
