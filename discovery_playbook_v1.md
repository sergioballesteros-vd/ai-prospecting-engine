# Discovery Playbook v1

Objetivo: descubrir la verdad del workflow en 20–30 minutos. No demostrar una idea, no enseñar una demo y no convertir una hipótesis en un hecho.

## Regla de evidencia

- `FACT`: información pública verificable. Sirve para preparar, no para atribuir dolor.
- `INFERENCE`: interpretación razonable de hechos públicos. Se presenta como posibilidad.
- `HYPOTHESIS`: afirmación que la conversación debe intentar matar.
- `BUYER_REPORTED`: hecho, ejemplo o número dicho por el comprador. Registrar literalmente, con fecha y persona.

Una respuesta como “a veces” no es una línea base. Una ausencia no es cero. Si el buyer no sabe, registrar `desconocido` y diseñar una medición.

## Apertura no comercial (2 min)

> Gracias por el tiempo. No traigo una demo. Estoy intentando entender cómo ocurre de verdad un cierre reciente, qué cubre ya vuestro software y dónde, si ocurre, queda trabajo fuera. Si no hay problema o A3/Sage ya lo resuelve, esa también es una buena conclusión.

Pedir permiso para tomar notas y confirmar el rol de la persona en el proceso.

## Flujo de 20–30 minutos

### 1. Contexto (2 min)

- ¿Qué parte del área laboral o de la gestión del despacho controlas tú?
- ¿Quién vive el proceso cada mes y quién decide cambiarlo?

Registrar sponsor potencial y workflow owner por separado. El interés de una persona sin autoridad u operación no cubre ambos papeles.

### 2. Workflow actual (3 min)

- “Llévame desde que pedís los cambios hasta que la nómina queda cerrada.”
- ¿Qué sistemas y canales intervienen realmente, no sólo los definidos en el procedimiento?

Construir una secuencia breve: entrada → validación → excepción → dueño → cierre.

### 3. Último caso real (4 min)

Prioridad absoluta: el cierre más reciente o un extra concreto de los últimos 30–90 días.

- ¿Qué ocurrió, en qué fecha y con qué cliente/cohorte?
- ¿Qué tuvo que hacer cada persona?
- ¿Qué quedó incompleto, tarde o ambiguo?

Evitar: “¿Os cuesta perseguir documentación?”. Preguntar: “En el último cierre, ¿cuántas empresas necesitaron al menos un recordatorio manual?”.

### 4. Software existente (3 min)

- ¿Qué parte cubre A3, Sage, Cegid, Aplifisa, Bilky u otra herramienta?
- ¿La función está contratada, configurada y adoptada?
- ¿Qué queda en correo, WhatsApp, teléfono o Excel?

Separar cuatro resultados: el stack ya resuelve; falta configuración; falta adopción; falta funcionalidad. Probar primero “A3/Sage/Bilky ya hace esto”.

### 5. Excepciones (3 min)

- ¿Qué convierte un caso normal en excepción?
- ¿Quién la detecta, quién la posee y cómo sabe el equipo que sigue abierta?
- ¿Existe una cola única o se reconstruye el estado desde varios canales?

### 6. Cuantificación (4 min)

Pedir números observados o aproximaciones explícitamente buyer-reported. Registrar rango si no hay exactitud. Nunca aportar un coste/hora propio.

- Cohorte, recordatorios, minutos, incompletas al corte, cambios tardíos, reaperturas.
- Para extras: casos, valor, facturación, demora y motivo de pérdida.

### 7. Consecuencia (2 min)

- ¿Qué pasó por llegar tarde/incompleto: retrabajo, riesgo, demora, llamada, reapertura o ingreso absorbido?
- ¿A quién le importó y por qué?

No convertir tiempo en dinero sin coste aportado por el buyer.

### 8. Workaround actual (2 min)

- ¿Cómo lo controláis hoy?
- ¿Qué se rompería si se retira el Excel, chat o persona que coordina?
- ¿Qué alternativa habéis probado y por qué se mantiene o abandonó?

### 9. Ownership (2 min)

- ¿Quién responde por el resultado mensual?
- ¿Quién mantiene el dato y resolvería excepciones en un piloto?

Sin workflow owner no hay piloto.

### 10. Disposición al cambio (2 min)

- Si el stack actual puede resolverlo, ¿preferís activarlo antes de añadir nada?
- ¿Qué hábito de clientes/equipo no estáis dispuestos a cambiar?
- ¿Qué condición haría que no mereciera continuar?

### 11. Calificación de piloto (3 min)

Sólo explorar cuando existen recurrencia, baseline, consecuencia y gap no resuelto razonablemente por el stack.

- ¿Se puede aislar un sistema, una cohorte y un cierre?
- ¿Quién patrocina, quién opera y qué métrica decide éxito?
- ¿Qué datos/canales quedan fuera y cuál es el kill criterion?

## Rama: cierre laboral

Capturar, cuando el buyer lo sepa: empresas y empleados procesados; cutoff; software; portal y adopción; canales reales; empresas con recordatorio; mensajes/llamadas/emails; minutos; incompletas al corte; cambios tardíos; correcciones/reaperturas; hojas laterales; dueño de la excepción; método para conocer el estado; capacidad del stack y naturaleza del gap.

La solución hipotética nunca calcula nóminas ni presenta a organismos. El resultado buscado sería una cola visible de excepciones antes del corte, usando primero el software pagado.

## Rama: trabajo fuera de alcance

Reconstruir un caso de los últimos 30–90 días: canal de solicitud → comprobación de cuota → aprobación y precio → ejecución → registro → facturación → revisión de rentabilidad.

Preguntar quién identifica extras, si se ejecuta antes de valorar, quién aprueba, cuánto tardó en facturarse y si quedó absorbido. Sólo usar `OUT_OF_SCOPE_WORK_CANDIDATE` con ejemplo buyer-reported.

## Cierres válidos

- `NO_PROBLEM`: agradecer y cerrar; no fabricar seguimiento.
- `EXISTING_STACK_SOLVES_IT`: recomendar activar/configurar y verificar un cierre.
- `MEASURE_FIRST`: acordar qué medir durante un cierre o 30–90 días.
- Candidato de hipótesis: segunda sesión con workflow owner.
- `PILOT_CANDIDATE`: pasar el hard gate de `pilot_candidate_handoff.md`; todavía no programar.
