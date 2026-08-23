# Pilot Candidate Handoff

Hard gate entre discovery y trabajo técnico. “Suena interesante”, un readiness alto o una clasificación de candidato no autorizan código.

## Checklist obligatoria

| Gate | Evidencia requerida | Estado |
|---|---|---|
| Sponsor | Nombre, cargo, autoridad y compromiso explícito | ☐ |
| Workflow owner | Persona que opera/resuelve excepciones y participará | ☐ |
| Un sistema | Producto y versión/entorno; no multi-ERP | ☐ |
| Una cohorte | Lista/definición y tamaño; datos mínimos | ☐ |
| Un cierre mensual | Fecha, cutoff y ventana de observación | ☐ |
| Baseline | Métricas, periodo, fuente buyer-reported y owner | ☐ |
| Mapa actual | Entrada → validación → excepción → owner → cierre | ☐ |
| Canal aprobado | Corporativo, accesos y reglas; no WhatsApp personal | ☐ |
| Datos y seguridad | Categorías, minimización, retención, ubicación y responsables | ☐ |
| Límites de acceso | Qué puede leer/escribir; credenciales y revocación | ☐ |
| Métrica de éxito | Definición, baseline, target y método de medida | ☐ |
| Kill criteria | Daño, adopción, coste, calidad o fecha que detienen | ☐ |
| Implementation owner | Responsable del lado cliente y de Sergio | ☐ |
| Fecha objetivo | Inicio, revisión y cierre del experimento | ☐ |

## Frontera innegociable v1

- No cálculo ni modificación de nóminas.
- No presentación ante organismos.
- Toda acción sensible requiere aprobación humana.
- Sin contacto automatizado a clientes ni outreach.
- Sin integración multi-ERP ni datos fuera de la cohorte.
- El stack existente se configura/prueba primero cuando puede cubrir el resultado.

## Documento de handoff

Antes de estimar trabajo, dejar en una página: problema buyer-reported; último caso; baseline; función existente probada; gap; alcance dentro/fuera; flujo y owner; datos/canales; éxito/kill; riesgos; precio/condiciones si el buyer los acepta; incógnitas.

## Decisión

- Cualquier gate esencial vacío → volver a `MEASURE_FIRST` o candidato de hipótesis.
- Stack suficiente → `EXISTING_STACK_SOLVES_IT`.
- Requisito inseguro/no reducible → `DISQUALIFIED`.
- Todos los gates, límites y decisión comercial explícitos → autorizar diseño técnico separado. Aún no implica despliegue.
