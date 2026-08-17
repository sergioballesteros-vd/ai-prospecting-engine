"use client";

import { Plus } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Company, listCompanies } from "@/lib/api";

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listCompanies()
      .then(setCompanies)
      .catch((err) => setError(err instanceof Error ? err.message : "No se pudieron cargar las empresas"))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <AppShell>
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Empresas</h1>
            <p>Listado de empresas creadas o descubiertas, con acceso a su cronología.</p>
          </div>
          <Link className="secondaryButton" href="/">
            <Plus size={16} />
            Investigar dominio
          </Link>
        </header>
        {error ? <div className="notice error">{error}</div> : null}
        <section className="panel">
          <div className="panelHeader">
            <div>
              <h2>Empresas registradas</h2>
              <p>Ordenadas por creación reciente desde la API.</p>
            </div>
            <span>{companies.length}</span>
          </div>
          <div className="rankedList">
            {companies.map((company) => (
              <Link className="campaignRow" href={`/companies/${company.id}`} key={company.id}>
                <span>
                  <strong>{company.name}</strong>
                  <small>
                    {company.domain} · {company.city ?? "Ciudad desconocida"} ·{" "}
                    {company.industry ?? "Industria desconocida"}
                  </small>
                </span>
                <span>{company.country ?? "País desconocido"}</span>
                <span className="status live">Cronología</span>
              </Link>
            ))}
            {!companies.length && !isLoading ? (
              <div className="empty">Todavía no hay empresas. Investiga un dominio para crear la primera.</div>
            ) : null}
            {isLoading ? <div className="empty">Cargando empresas...</div> : null}
          </div>
        </section>
      </section>
    </AppShell>
  );
}
