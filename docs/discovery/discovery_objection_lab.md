# Discovery Objection Lab

Objetivo: usar objeciones como tests de hipótesis. La respuesta breve valida primero, pregunta por el último caso y permite cerrar sin proyecto.

| Objeción | Respuesta consultiva | Evidencia a buscar / salida |
|---|---|---|
| “A3 ya hace esto.” | “Puede ser. Prefiero comprobarlo antes de añadir nada. ¿Qué parte usasteis en el último cierre y qué quedó fuera?” | Configuración, adopción y excepciones. Si cubre el resultado: `EXISTING_STACK_SOLVES_IT`. |
| “Sage ya hace esto.” | “Entonces lo sensato es explotar Sage. ¿Podemos recorrer una petición real, su owner y el estado al cutoff?” | Activar/configurar; no competir por funciones. |
| “Bilky ya hace esto.” | “Bilky cubre mucho. ¿La cartera lo usa y las excepciones quedan visibles o seguís reconstruyéndolas fuera?” | Uso real y excepción residual; si no existe, cerrar. |
| “Ya tenemos portal.” | “Tenerlo es distinto de usarlo, pero puede estar totalmente resuelto. ¿Qué porcentaje/cohorte lo usó en el último cierre?” | Adopción observada, no licencia. |
| “Mis clientes no usan el portal.” | “Eso apunta a adopción, no necesariamente a software nuevo. ¿Qué intentasteis y qué canal usan de verdad?” | Posible servicio de adopción/configuración; respetar canales aprobados. |
| “Todo me llega por WhatsApp.” | “No propondría automatizar un WhatsApp personal sin control. ¿Es corporativo, quién accede y cómo llega la excepción al sistema?” | Si el único alcance es canal personal incontrolado: blocker de seguridad. |
| “No tenemos tanto problema.” | “Perfecto; no quiero crearlo. En el último cierre, ¿hubo recordatorios o reaperturas? Si fueron cero y es representativo, paramos.” | Número buyer-reported. `NO_PROBLEM` si no es recurrente. |
| “Somos muy pequeños.” | “El tamaño no prueba nada por sí solo. ¿Cuántas veces ocurre y qué consecuencia tiene? Si no justifica atención, no seguimos.” | Economía basada en baseline, no empleados. |
| “Prefiero contratar a alguien.” | “Puede ser la mejor alternativa. ¿Qué tareas asumiría y qué seguiría requiriendo criterio/ownership?” | Comparar coste, capacidad y resiliencia con datos del buyer. |
| “No quiero IA tocando nóminas.” | “Yo tampoco pondría IA a calcular o presentar nóminas. El límite sería visibilidad de excepciones con aprobación humana; si exige tocar cálculo, se descarta.” | Frontera de datos y seguridad. |
| “Por 30–80 € compro una herramienta.” | “Correcto; primero miraría esa herramienta. Sólo tendría sentido continuar si el problema es implantación o una excepción que no cubre.” | Probar sustituto barato; evitar defender precio prematuramente. |
| “No quiero cambiar cómo trabajan mis clientes.” | “Es una restricción válida. ¿Se puede mejorar el control interno sin forzarles otro canal? Si no, quizá no hay piloto seguro.” | Disposición real y límite de adopción. |
| “Ahora no es prioritario.” | “Entendido. ¿Es porque la consecuencia es baja o porque hay otra fecha mejor? Puedo cerrar el tema sin seguimiento.” | No fabricar urgencia; next action sólo si buyer lo pide. |
| “¿Qué haces tú exactamente?” | “Estoy validando si hay una excepción recurrente que vuestro stack no resuelve. Si existe, podría ayudar a medir y probar un flujo acotado; hoy quiero diagnosticar.” | Volver al caso real, no demo. |
| “¿Cuánto cuesta?” | “No tengo base para cotizar sin problema, baseline y alcance. Si llegamos a un piloto acotado, definiríamos precio y kill criteria antes de construir.” | No asumir €1k setup ni €200 MRR. |
| “Esto se arregla con disciplina.” | “Puede ser. ¿Qué cambio de disciplina se probó, quién lo sostiene y cómo mediremos un cierre?” | Alternativa válida; si funciona, stack/proceso resuelve. |
| “Es temporada, no pasa siempre.” | “Entonces separemos pico y recurrencia. ¿En cuántos de los últimos cierres ocurrió?” | Si no es repetible, no piloto; quizá medida estacional. |
| “No puedo compartir datos de empleados.” | “No necesito datos personales para discovery. Podemos trabajar con conteos y proceso; el piloto sólo avanzaría con límites de acceso aprobados.” | Minimización y seguridad. |

## Antipatrones

- Discutir con el buyer sobre lo que su software “debería” hacer.
- Responder a cada objeción con una función futura.
- Usar “IA” para elevar valor percibido.
- Convertir “interesante” en sponsor, baseline o willingness-to-pay.
- Dar precio antes de conocer frontera y consecuencia.
