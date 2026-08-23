# Discovery Decision Tree

Esta lógica está separada de Evidence Engine y FirstCustomerFit. Un score alto no puede convertir un blocker fatal en piloto.

```text
¿El requisito implica cálculo de nómina, filing, canal personal no controlado o alcance inseguro?
├─ Sí → DISQUALIFIED
└─ No
   ¿El buyer confirma un problema recurrente mediante un último caso real?
   ├─ No, confirma que no ocurre → NO_PROBLEM
   ├─ Desconocido → MEASURE_FIRST
   └─ Sí
      ¿El stack actual lo resuelve con configuración razonable?
      ├─ Sí → EXISTING_STACK_SOLVES_IT
      └─ No / gap de adopción o funcionalidad
         ¿Existe baseline usable?
         ├─ No / desconocida → MEASURE_FIRST
         └─ Sí
            ¿Qué workflow está respaldado por buyer-reported evidence?
            ├─ Cierre laboral → LABOR_CLOSE_CANDIDATE
            ├─ Extra con ejemplo 30–90 días → OUT_OF_SCOPE_WORK_CANDIDATE
            └─ Otro patrón → OTHER_WORKFLOW_SIGNAL
               ¿Sponsor + owner + alcance acotado/seguro?
               ├─ No → conservar candidato y resolver blocker
               └─ Sí, para una de las dos hipótesis → posible PILOT_CANDIDATE
```

## Assessment 0–2

Puntuar frecuencia, baseline, consecuencia, gap de stack, autoridad, participación del owner, simplicidad, disposición, seguridad y repetibilidad. `0` ausente, `1` débil/desconocido, `2` confirmado. Toda dimensión exige una razón textual.

El total máximo es 20 y sirve para ver qué está confirmado, no como umbral autónomo. No usarlo en FirstCustomerFit.

## Blockers fatales

- `EXISTING_STACK_SOLVES_IT`: activar/configurar antes de construir.
- `NO_USABLE_BASELINE`: medir primero.
- `NO_CONFIRMED_SPONSOR`: no hay autoridad para piloto.
- `NO_WORKFLOW_OWNER`: no hay responsable operativo.
- `UNSAFE_REQUIREMENT`: descalificar o rediseñar frontera.
- `NON_RECURRING_OR_UNCONFIRMED`: no hay problema repetible confirmado.
- `PILOT_NOT_BOUNDED_SAFE`: reducir a un sistema, cohorte y cierre.

## Frontera obligatoria del piloto

- Un workflow, un sistema de nómina, una cohorte y un cierre mensual.
- Aprobación humana; sin cálculo de nómina ni presentación pública.
- Canal corporativo aprobado; no WhatsApp personal incontrolado.
- Sin multi-ERP ni expansión “ya que estamos”.
- Métrica de éxito, kill criteria, owner y fecha acordados antes de trabajo técnico.

## Interpretación de resultados

`NO_PROBLEM` y `EXISTING_STACK_SOLVES_IT` son resultados exitosos del discovery. `MEASURE_FIRST` es un experimento de medición, no una propuesta encubierta. `PILOT_CANDIDATE` sólo abre el handoff; no autoriza código ni presupone willingness-to-pay.
