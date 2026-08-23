# Discovery Quantification

Hoja para convertir relatos buyer-reported en una línea base auditable. Los campos vacíos permanecen vacíos: nunca equivalen a cero.

## Proveniencia

Por cada número registrar: valor o rango, unidad, periodo, persona, fecha y si es observado, aproximado o calculado.

| Tipo | Uso |
|---|---|
| `BUYER_REPORTED_OBSERVED` | Contado en un cierre, registro o ejemplo concreto |
| `BUYER_REPORTED_ESTIMATE` | Aproximación declarada por el buyer |
| `CALCULATED` | Aritmética reproducible sobre inputs buyer-reported |
| `MISSING` | Desconocido; no entra en fórmulas |

## Cierre laboral: inputs

| Campo | Unidad/periodo | Pregunta de control |
|---|---|---|
| Empresas en nómina | empresas/cierre | ¿Es toda la cartera o la cohorte estudiada? |
| Empleados procesados | empleados/cierre | Sólo si está disponible |
| Cutoff | fecha/hora | ¿Formal o real? |
| Adopción del portal | % o empresas | ¿Uso activo, no sólo licencia? |
| Empresas con recordatorio | empresas/cierre | Al menos un recordatorio manual |
| Recordatorios | mensajes/llamadas/emails por cierre | Contar acciones, no clientes |
| Minutos por recordatorio | minutos | Aproximación buyer-reported |
| Seguimiento total | minutos/cierre | Preferir tiempo medido si existe |
| Incompletas al cutoff | empresas/cierre | Definir “incompleta” |
| Cambios tardíos | cambios/cierre | Recibidos tras cutoff |
| Correcciones/reaperturas | casos/trimestre | Confirmar causa tardía/incompleta/ambigua |
| Personas involucradas | personas | No multiplicar horas automáticamente |
| Coste/hora | €/hora | Sólo si el buyer lo proporciona |
| Otras consecuencias | texto/importe | Riesgo, SLA, horas extra, error, demora |

## Cálculos permitidos

```text
derived_total_followup_minutes = manual_reminders * minutes_per_reminder
manual_followup_hours = total_followup_minutes / 60
estimated_monthly_followup_cost = manual_followup_hours * buyer_provided_hourly_cost
```

Usar `total_followup_minutes` medido antes que el derivado. Mostrar fórmula, inputs y unidad. Si falta cualquier input, el resultado es `MISSING`, no `0`.

Ejemplo válido: buyer informa 12 recordatorios, 5 minutos por recordatorio y 30 €/h. Resultado calculado: 60 min, 1 h y 30 €/mes. Ninguno de esos inputs se infiere del tamaño del despacho.

## Trabajo fuera de alcance: registro por ejemplo

| Campo | Descripción |
|---|---|
| Fecha y solicitud | Qué pidió el cliente y por qué canal |
| Incluido en cuota | Sí / no / ambiguo / no comprobado |
| Quién detectó el extra | Persona o rol |
| Aprobación y precio | Antes/después de ejecutar; quién aprobó |
| Valor estimado | Importe declarado por buyer |
| Valor facturado | Importe y fecha reales si existen |
| Demora | Días entre ejecución y factura |
| Resultado | Facturado, olvidado, absorbido, discutido |
| Fallo de proceso | Scope invisible, aprobación ausente, registro o handoff a facturación |

Para un periodo homogéneo:

```text
potential_absorbed_value = out_of_scope_estimated_value - out_of_scope_invoiced_value
```

No llamar “ingreso recuperable” al resultado sin validar que el cliente habría aprobado/pagado. Mantenerlo como potencial y conservar ejemplos.

## Baseline usable

Una baseline es usable cuando tiene: definición, cohorte, periodo, número o rango, fuente buyer-reported y responsable que puede repetir la medición. Si falta, resultado `MEASURE_FIRST`.

Plan mínimo de medición para un cierre: cohorte definida; contador de empresas con reminder; contador de acciones; minutos totales; incompletas al cutoff; cambios tardíos; reaperturas atribuibles; owner; fecha de revisión.

## Comparación de piloto

Definir antes del piloto exactamente la misma métrica pre/post. No aceptar “parece mejor”. Registrar efectos adversos, adopción y excepciones desplazadas a otro canal. El éxito no autoriza ampliar alcance sin una nueva decisión.
