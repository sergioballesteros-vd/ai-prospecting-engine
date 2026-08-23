# Commercial Learning Loop

Objetivo: aprender entre conversaciones sin convertir una muestra pequeña en verdad de mercado ni modificar automáticamente Evidence Engine/FirstCustomerFit.

## Registro de aprendizaje

| Campo | Regla |
|---|---|
| Learning statement | Falsable y acotado: segmento, workflow, sistema |
| Conversaciones a favor | IDs de sesiones, no memoria agregada |
| Contradicciones | IDs y explicación; nunca borrar |
| Date range | Primera y última evidencia |
| Evidence type | `BUYER_REPORTED`, `FACT`, `INFERENCE` o `HYPOTHESIS` |
| Cohorte | Tamaño y criterio de inclusión |
| Confidence | Baja/media/alta con razón, no fórmula opaca |
| Implicación | Qué pregunta o experimento cambia; no scoring automático |
| Owner/review date | Quién revisa y cuándo |

## Hipótesis vivas a seguir

- Firmas con A3 raramente tienen el problema residual.
- El bottleneck es adopción de portal, no funcionalidad.
- Firmas de menos de cinco empleados no justifican piloto.
- La cuña laboral es más débil de lo esperado.
- El trabajo fuera de alcance aparece con mayor consecuencia económica.
- El buyer valora más riesgo/reapertura que tiempo.
- Un setup de €1k genera resistencia.
- €200/mes es aceptado o rechazado bajo condiciones concretas.
- Otro workflow aparece repetidamente.

Todas comienzan como `HYPOTHESIS`, incluso si parecen plausibles por investigación pública.

## Cadencia

### Después de cada llamada

1. Guardar una nueva sesión histórica, nunca editar la anterior.
2. Separar citas/hechos buyer-reported de interpretación.
3. Registrar outcome adverso y siguiente acción que reduce incertidumbre.
4. Añadir evidencia a un learning existente o crear uno provisional.

### Cada 5 conversaciones comparables

- Contar resultados y contradicciones por segmento/software, no sólo totales.
- Revisar si las preguntas fueron leading o faltó el workflow owner.
- Buscar evidencia contra la cuña favorita.
- Decidir: mantener pregunta, medir, estrechar segmento o matar hipótesis.

### Antes de cambiar oferta o scoring

Exigir conversaciones comparables, ejemplos reales, contradicciones explicadas y fechas recientes. Documentar una decisión humana separada. Nunca trasladar automáticamente outcomes de discovery a los pesos de producto.

## Scoreboard comercial

El dashboard muestra conexiones enviadas/aceptadas, conversaciones, discovery calls, resultados de discovery, candidatos, pilotos propuestos/pagados, setup y MRR. North Star: €900 MRR. Objetivo próximo: primer piloto pagado.

El volumen no es éxito. Interpretar junto a ratios y calidad: muchas conexiones con cero calls es un problema; muchas calls con `NO_PROBLEM` puede ser aprendizaje valioso; un `PILOT_CANDIDATE` sin gate completo no es pipeline ganado.

## Plantilla de revisión

```text
Periodo:
Conversaciones comparables:
Learning:
A favor (session IDs):
Contradicciones (session IDs):
Evidence types:
Qué aún no sabemos:
Confidence + razón:
Próximo test manual:
Decisión (sin cambio / medir / estrechar / matar):
```
