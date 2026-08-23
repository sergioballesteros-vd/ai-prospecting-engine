# Commercial Red Team — hipótesis de primer cliente

Fecha de verificación: 23 de agosto de 2026. Ámbito: despachos españoles pequeños y medianos de asesoría fiscal, contable y laboral. Investigación exclusivamente pública; no se contactó a nadie.

## Veredicto

**PIVOT.**

- **FACT:** El dolor de perseguir documentación y controlar expedientes incompletos existe. Lo muestran ofertas de trabajo de despachos que incluyen expresamente la solicitud y seguimiento de documentos, incluso con dominio de A3, y testimonios públicos de clientes que siguen repartiendo facturas entre correo, papel, Drive y portales ([Asesoría López García](https://es.linkedin.com/jobs/view/auxiliar-administrativo-at-asesor%C3%ADa-l%C3%B3pez-garc%C3%ADa-4411898079), [Junior laboral con A3](https://es.linkedin.com/jobs/view/junior-laboral-con-a3-at-renlink-4416271802), [hilo de autónomos](https://www.reddit.com/r/autonomos/comments/1tytfe9/problema_al_reunir_facturas/)).
- **FACT:** La solución genérica ya es una categoría muy concurrida. En España, Recopila, Archivum, Escania, Taabolo, AccioGest, Bilky y Previoo venden recogida, recordatorios, estados, OCR, WhatsApp o expedientes desde aproximadamente 19–100 €/mes; Taabolo ofrece incluso configuración gestionada por uso ([Recopila](https://www.myeficacia.com/), [Archivum](https://archivumcloud.com/), [Escania](https://escania.es/), [Taabolo](https://taabolo.com/sector/asesorias-y-gestorias), [AccioGest](https://acciogest.com/precios/), [Bilky](https://bilky.es/tarifas-para-asesorias-2026/)).
- **FACT:** Una boutique española, OptimaTech, publica literalmente los casos de uso “variables de nómina recogidas cada mes con formularios y recordatorios”, reclamación de documentación, clasificación de correo, integración con programas y mantenimiento continuo. Sergio Sallavera publica una oferta casi idéntica para pedir y clasificar documentos por WhatsApp/email sin cambiar el software del despacho ([OptimaTech](https://optimatech.es/), [Sergio Sallavera](https://sergiosallavera.es/automatizacion-asesorias/)).
- **FACT:** Los verticales tampoco se limitan al cálculo fiscal o laboral. A3, Sage, Cegid/Diez, Bilky, Aplifisa y Quipu tienen portales, gestión documental, tareas, responsables, plazos, OCR o integración en distintos grados. a3innuva Portal del Empleado permite introducir conceptos variables, absentismos e IT; Sage Despachos gestiona expedientes, tareas, cargas y peticiones de cliente ([a3innuva Portal](https://www.wolterskluwer.com/es-es/solutions/a3innuva-portal-del-empleado-empresas), [Sage Despachos](https://www.sage.com/es-es/software-asesorias-y-despachos/)).
- **INFERENCE:** Por tanto, “automatizamos lo manual antes y entre sistemas” no diferencia: describe una categoría, no una oferta. El hueco no es una función ausente universal, sino una implantación fallida, baja adopción o excepción específica que sólo puede demostrarse dentro de cada despacho.
- **HYPOTHESIS:** La única entrada razonable que sobrevive para un fundador solo es un servicio de diagnóstico e implantación sobre el stack ya pagado, limitado a un cierre mensual laboral y a sus excepciones fuera de canal. Debe morir si el despacho no acredita una línea base de seguimiento/retrabajo o si A3/Sage/Bilky ya resuelve el flujo al activarlo correctamente.

La hipótesis original de crear otra capa general de intake/chasing queda **matada**. El mercado vertical no queda descartado; queda condicionado a una oferta de implantación/adopción, no de software genérico nuevo.

## Cómo leer los resultados

Cada afirmación está marcada como:

- **FACT:** evidencia pública directa.
- **INFERENCE:** conclusión razonable derivada de hechos, todavía no validada por un comprador.
- **HYPOTHESIS:** supuesto que requiere discovery o piloto.

En las matrices:

- **CONFIRMED:** una fuente pública específica demuestra la capacidad.
- **PARTIAL:** existe una función próxima o limitada, pero no la capacidad completa.
- **NOT FOUND:** se buscó y no se encontró evidencia pública; no significa que no exista.
- **UNKNOWN:** la documentación pública no permite evaluarlo.

## 1. Software existente: ¿qué resuelve de verdad?

### 1.1 Intake, portal, persecución y workflow

| Ecosistema | Entrada/subida | Portal cliente/empleado | Recordatorio automático al cliente | Detección de documento faltante | Workflow/routing | Responsable/tarea | Plazos | Evidencia principal |
|---|---|---|---|---|---|---|---|---|
| Wolters Kluwer A3 / a3ASESOR / a3doc | CONFIRMED | CONFIRMED | NOT FOUND | NOT FOUND | CONFIRMED | CONFIRMED | PARTIAL | [a3ASESOR](https://www.wolterskluwer.com/es-es/solutions/a3asesor), [a3doc](https://www.wolterskluwer.com/es-es/solutions/software-gestion-documental-a3doc), [a3ASESOR Ges](https://www.wolterskluwer.com/es-es/solutions/a3asesor-ges) |
| Sage Despachos Connected | CONFIRMED | CONFIRMED | PARTIAL | NOT FOUND | CONFIRMED | CONFIRMED | CONFIRMED | [producto](https://www.sage.com/es-es/software-asesorias-y-despachos/), [detalle funcional](https://www.sage.com/es-es/-/media/files/sagedotcom/spain/documents/pdf/generacion_despachos_profesionales.pdf) |
| Holded para asesorías | CONFIRMED | CONFIRMED | PARTIAL | PARTIAL | CONFIRMED | CONFIRMED | PARTIAL | [IA para asesorías](https://www.holded.com/es/ia-asesorias), [asesorías](https://www.holded.com/es/asesorias), [portal](https://help.holded.com/es/articles/9382835-acciones-disponibles-en-el-portal-del-cliente) |
| Bilky | CONFIRMED | CONFIRMED | PARTIAL | PARTIAL | CONFIRMED | CONFIRMED | CONFIRMED | [funciones](https://bilky.es/funcionalidades/), [centro de ayuda](https://bilky.es/centro-de-ayuda/categoria/asesor/) |
| Aplifisa / TeamSystem | CONFIRMED | CONFIRMED | PARTIAL | NOT FOUND | CONFIRMED | PARTIAL | CONFIRMED | [fiscal](https://www.aplifisa.com/asesorias/programa-fiscal-aplifisa/), [teletrabajo/portales](https://www.aplifisa.com/empresas-teletrabajo/) |
| Cegid ERP Despachos / Diez | CONFIRMED | CONFIRMED | PARTIAL | NOT FOUND | CONFIRMED | CONFIRMED | CONFIRMED | [ERP Despachos](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/), [Portal Asesor](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/portal-asesor/), [Diez Asesor](https://play.google.com/store/apps/details?id=com.diezsoftware.asesormovil&hl=es) |
| Quipu | CONFIRMED | CONFIRMED | PARTIAL | PARTIAL | CONFIRMED | CONFIRMED | PARTIAL | [asesorías](https://getquipu.com/es/despachos), [OCR](https://getquipu.com/es/digitalizar-facturas-asesorias), [brochure](https://getquipu.com/wp-content/uploads/2021/11/09162427/brochure-ebook-asesorias-quipu.pdf) |

**FACT:** “PARTIAL” en recordatorios no debe convertirse en “el producto persigue automáticamente todos los documentos faltantes”. Holded confirma recordatorios de cobro, Aplifisa avisos de obligaciones y Bilky alertas/CRM; no se encontró una declaración pública inequívoca de que cada uno construya por sí solo una lista semántica de documentos esperados por cliente y detenga recordatorios al completarla.

**FACT:** a3doc clasifica automáticamente documentos generados por soluciones Wolters Kluwer, permite intercambio bidireccional, búsqueda y seguimiento de acciones. Eso no prueba OCR universal ni detección de faltantes en documentos entrantes ([ficha de a3doc](https://assets.contenthub.wolterskluwer.com/api/public/content/2458301-ficha-producto-a3doc-cloud-despacho-241420a5e2?v=c7ba5851)).

**FACT:** Sage sí documenta OCR de facturas, revisión interna, incidencias, expedientes, tareas, carga de trabajo y seguimiento de peticiones. Su botón de WhatsApp en la ficha de contacto no equivale a ingestión automática de documentos desde WhatsApp ([declaración funcional y conectividad](https://www.sage.com/es-es/-/media/files/sagedotcom/spain/documents/pdf/certificados/declaracion_responsable_sagedespachosc_30-4-25.pdf)).

### 1.2 Canales, inteligencia, integraciones y excepciones

| Ecosistema | Ingestión email | Ingestión WhatsApp | OCR | Clasificación IA | Integraciones/API | Trabajo entre sistemas | Gestión explícita de excepciones |
|---|---|---|---|---|---|---|---|
| Wolters Kluwer A3 / a3doc | NOT FOUND | NOT FOUND | PARTIAL | NOT FOUND | PARTIAL | PARTIAL | PARTIAL |
| Sage Despachos Connected | PARTIAL | PARTIAL | CONFIRMED | PARTIAL | CONFIRMED | CONFIRMED | CONFIRMED |
| Holded | CONFIRMED | NOT FOUND | CONFIRMED | CONFIRMED | CONFIRMED | PARTIAL | PARTIAL |
| Bilky | NOT FOUND | NOT FOUND | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | PARTIAL |
| Aplifisa / TeamSystem | PARTIAL | NOT FOUND | CONFIRMED | NOT FOUND | PARTIAL | PARTIAL | PARTIAL |
| Cegid ERP Despachos / Diez | PARTIAL | NOT FOUND | CONFIRMED | NOT FOUND | PARTIAL | CONFIRMED | PARTIAL |
| Quipu | CONFIRMED | NOT FOUND | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED | CONFIRMED |

**FACT:** Holded recibe documentos por correo, extrae y clasifica con OCR/IA y expone API, integraciones y Zapier; sus webhooks figuraban aún como futuros en su documentación pública revisada ([IA asesorías](https://www.holded.com/es/ia-asesorias), [API](https://www.holded.com/es/desarrolladores), [integraciones](https://www.holded.com/es/integraciones)).

**FACT:** Bilky conecta con A3ECO, A3ERP, A3innuva, Aplifisa y decenas de productos, además de OCR/IA y exportación contable ([integraciones](https://bilky.es/integraciones/)). En 2026 Visma entró en su capital; una noticia cifra más de 300.000 usuarios activos y miles de asesorías/pymes, lo que reduce la probabilidad de que sea un producto marginal ([Cadena SER](https://cadenaser.com/andalucia/2026/04/27/el-gigante-noruego-del-software-visma-entra-en-el-capital-de-la-malaguena-bilky-ser-malaga/)).

**FACT:** ApliScan convierte PDFs o escaneos en asientos y conserva copia documental; puede procesar PDFs con varias facturas. No se encontró API pública general para Aplifisa ni ingestión WhatsApp ([ApliScan](https://www.aplifisa.com/asesorias/escanear-contabilizar-facturas/)).

**FACT:** Cegid/Diez cubre tareas, tiempos, documentos, expedientes, proyectos, avisos y portal; Diez Asesor permite fotografiar facturas y trabajar con DiezSCAN. No se encontró una API pública inequívoca para Cegid ERP Despachos/Diez; no se extrapolaron APIs de otros productos Cegid ([Cegid ERP](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/), [Cegid Profiture](https://www.cegid.com/ib/es/productos/programas-software-erp-bi-business-intelligence/)).

**FACT:** Quipu permite carga móvil, arrastre y reenvío a un email dedicado, OCR/IA, detección de duplicados, validación humana, asignación de cuentas y API/Zapier. Es una capa explícitamente complementaria al programa contable y afirma trabajar con más de 1.000 asesorías en España ([OCR](https://getquipu.com/es/digitalizar-facturas-asesorias), [despachos](https://getquipu.com/es/despachos), [plataforma colaborativa](https://getquipu.com/ca/assessories)).

### 1.3 El golpe más fuerte a la tesis

- **FACT:** a3innuva Portal del Empleado ya permite alta de empleados, cambios de datos, vacaciones/permisos, absentismos, IT y conceptos variables, con trazabilidad ([a3innuva Portal](https://www.wolterskluwer.com/es-es/solutions/a3innuva-portal-del-empleado-empresas)).
- **FACT:** Sage Portal del Empleado cubre datos personales/bancarios, anticipos, vacaciones, ausencias y comunicación de incidencias, enlazado con nómina ([Sage Portal](https://www.sage.com/es-es/-/media/images/sagedotcom/spain/es-es/pdf/productos/sage%20200c%20laboral/new/sage200-laboral-modulo-portal-del-empleado.pdf)).
- **INFERENCE:** Incluso la cuña aparentemente más prometedora —variables de nómina antes del cálculo— no es un espacio vacío. Sólo sobrevive cuando los clientes no usan esos portales, la asesoría mezcla varios sistemas o las excepciones siguen fuera del circuito.
- **HYPOTHESIS:** El producto a vender no debe ser “otro formulario” sino el resultado “una cola única de excepciones laborales antes del corte, usando primero las funciones existentes”.

## 2. Competidores directos

### 2.1 España

| Competidor | Cliente objetivo y problema exacto | Precio público | Distribución e integraciones | Fortaleza | Limitación pública | ¿Mata la cuña? |
|---|---|---|---|---|---|---|
| [Recopila](https://www.myeficacia.com/) | Asesorías; campañas recurrentes de petición, enlace sin login, recordatorios y estado de pendientes | 19 €/mes de lanzamiento; verificar tarifa vigente antes de compra | Self-serve web; descarga organizada | Encaja casi palabra por palabra con chasing documental | Producto reciente; evidencia pública principalmente del proveedor | **Sí**, para petición/recordatorio genérico |
| [Archivum Cloud](https://archivumcloud.com/) | Profesionales; pedir, recibir, revisar, comentar, aprobar/rechazar, versionar y recordar | 29 €/mes; 59 €/mes ilimitado, con descuento anual publicado | SaaS directo | Flujo completo de dossier, no sólo almacenamiento | No se confirmó integración profunda con A3/Sage | **Sí**, para dossier genérico |
| [Escania](https://escania.es/) | Asesorías; facturas por WhatsApp/Telegram, OCR/IA, clasificación y recordatorios | 0 €; 9 €; 29 €/mes según clientes/documentos | WhatsApp Business, Telegram, exportación Excel a A3/Sage/Contaplus/DELSOL | Canal que el cliente ya usa y precio extremadamente bajo | Centrado en facturas; dependencia del canal y calidad de imagen | **Sí**, para intake de facturas por WhatsApp |
| [Previoo](https://previoo.io/previoo-gestorias/) | Gestorías; app cliente, documentos, recordatorios, faltantes/errores y exportación | Precio de asesoría no público; planes individuales 9,99–13,99 € | Exportación CSV a A3/Sage/Wolters | Combina captura, revisión y error/faltante | Precio y adopción B2B no transparentes | **Sí/Parcial** |
| [Taabolo](https://taabolo.com/sector/asesorias-y-gestorias) | Despachos; solicitud, datos, documentos, firma, pago, validación, subsanación, estados y avisos | 288 €/año + 0,99 €/gestión; gestionado 3,99 €/gestión | Portal multiidioma, colas, firma, pagos, OpenAI/Google | Cubre el expediente completo y ofrece operación gestionada | Coste variable por gestión; no prueba integración vertical profunda | **Sí**, para portal/workflow general y servicio gestionado |
| [AccioGest](https://acciogest.com/precios/) | Despachos; CRM, expedientes, portal, responsables, plazos, email/WhatsApp, rentabilidad | 29 €/mes (3 usuarios), 49 € (10), 99 € ilimitados | API e integraciones, WhatsApp, self-serve | Gran amplitud por precio y activación rápida | Claims del proveedor; profundidad de cada integración no publicada | **Sí**, para organización general |
| [Bilky](https://bilky.es/funcionalidades/) | Asesorías, empresas y empleados; portal, documentos, OCR/IA, CRM, plazos y procesos | 29,99; 59,99; 79,99 €/mes más módulos | 47 integraciones, A3 y Aplifisa | Producto español maduro, integrado y respaldado por Visma | No se encontró ingestión WhatsApp ni falta semántica universal | **Sí**, para portal/OCR/CRM; parcial para excepciones off-channel |
| [Quipu](https://getquipu.com/es/despachos) | Asesorías; colaboración, OCR, email-in, validación y conciliación | Planes negocio 13–28 €/mes; precio cartera/partner no público | API, Zapier, importación al contable | Adopción española y validación humana | No es un sistema completo de gestión del despacho | **Sí**, para factura/OCR; parcial para workflow transversal |
| [Kabilio](https://www.kabilio.es/asesores/asesorias) | Asesorías; email/Dropbox/portal, OCR/IA, contabilidad, bancos e integración A3 | Propuesta privada | A3Eco/A3Con y ecosistema propio | Integración contable fuerte y capital para crecer | Precio no público; foco más contable que expediente general | **Sí**, para automatización contable |
| [OptimaTech](https://optimatech.es/) | Gestorías y despachos; soluciones a medida de extracción, correo, plazos, documentación y variables de nómina | No público; proyecto cerrado + mantenimiento | Venta consultiva; Microsoft 365, APIs y programa del cliente | Oferta casi idéntica, vertical y con frontera humana | Sin casos/precios públicos verificables | **Sí**, para la oferta de servicio a medida |
| [Sergio Sallavera](https://sergiosallavera.es/automatizacion-asesorias/) | Asesorías; petición y clasificación por WhatsApp/email, Drive/hoja/gestor, piloto supervisado | No público | Consultoría directa | Un solo fundador puede vender exactamente el mismo pitch | Profundidad e integración no públicas | **Sí**, para diferenciación comercial |
| [ROXEX](https://roxex.es/sectores/gestorias) | Gestorías; portal, documentos, plazos, recordatorios y automatizaciones | No encontrado | n8n y menciones a A3/Sage | Orientación a implantación | Precio y casos verificables no encontrados | **Parcial** |

**FACT:** Los precios bajos no demuestran que todas estas herramientas funcionen bien; sí demuestran que un comprador puede comparar una propuesta de 450 €/mes con sustitutos funcionales de 20–100 €/mes.

**INFERENCE:** Una propuesta externa necesita justificar no “más funciones”, sino configuración, cambio de hábito, integración o una excepción cuyo coste exceda claramente el diferencial de precio.

### 2.2 UE e internacional con capacidad de entrar en España

| Competidor | Capacidad | Precio público | Integraciones/distribución | Riesgo para la cuña española |
|---|---|---|---|---|
| [FileCollect](https://www.filecollect.io/pricing) | Checklist sin cuenta, recordatorios, aprobación/rechazo, auto-renombrado y entrega directa a Google Drive | 19,99 €/mes Pro; 49 €/mes Team | Google Drive; API/webhooks/Zapier en Team; DPA y hosting UE declarados | **Alto:** producto simple, barato y preparado para RGPD |
| [Content Snare](https://contentsnare.com/pricing/) | Formularios, documentos, auto-save, recordatorios, aprobación/rechazo y portal sin cuenta | 35 USD/mes Basic anual; 71 USD Plus | XPM, FYI, OneDrive, SharePoint, Dropbox, Drive, Zapier/Make, API/webhooks | **Alto:** solución madura de intake profesional |
| [Quire](https://withquire.com/pricing/) | Peticiones mensuales, magic link, email/SMS, recordatorios y portal | 49 USD/mes hasta 25 clientes; 89 USD ilimitado | QBO, Xero, Drive, Dropbox, Notion, Zapier, Slack | **Alto** en producto; menor por falta de integración española hoy |
| [Financial Cents](https://financial-cents.com/pricing/) | Workflow contable, email a tarea, responsables, solicitudes, recordatorios email/SMS, portal y rentabilidad | Desde 19 USD/mes solo; planes de equipo por usuario | QBO y ecosistema internacional | **Alto:** cubre práctica completa, aunque localizado a otros mercados |
| [TaxDome](https://help.taxdome.com/article/926-eu-br-taxdome-pricing-faq) | CRM, organizers, solicitudes, recordatorios, workflow, omnicanal, documentos, IA y rentabilidad | España: 800 €/usuario/año a un año; 90 €/asiento mensual | Región UE, DATEV; integraciones globales limitadas por región | **Alto:** ya vende oficialmente en España/UE |
| [Karbon](https://karbonhq.com/en-GB/pricing) | Email integrado, tareas, solicitudes, responsables, fechas y recordatorios automáticos | Business 89 USD/usuario/mes anual; 99 USD mensual | Xero, QuickBooks y ecosistema anglosajón | **Medio-alto:** caro pero fuerte en firmas mayores |
| [Glasscubes](https://www.glasscubes.com/ai-assist/) | Enlaces sin contraseña, recordatorios, estados, IA para faltantes y workflows fiscales/laborales | La página pública consultada no permitió confirmar el precio base | Venta directa a contables UK; portal GDPR y onboarding | **Medio-alto:** producto especializado que puede localizarse |
| [Dext](https://help.dext.com/en/collections/878120-upload) | Captura desde app/email y extracción; en materiales UK también WhatsApp | Precio español no confirmado | Integraciones contables internacionales | **Medio:** amenaza en captura/OCR, menos en workflow de despacho español |

**FACT:** FileCollect incluye DPA, infraestructura UE y afirma no conservar los archivos, que pasan a Google Drive; cuesta 19,99 €/mes ([producto](https://www.filecollect.io/), [DPA](https://www.filecollect.io/dpa)). Esto debilita la idea de que RGPD por sí solo protege a un proveedor local de la competencia.

## 3. ¿El dolor es real o sólo marketing?

### 3.1 Evidencia de practicantes y operación real

- **FACT — fuerte:** Una asesoría de Tarragona que declara combinar herramientas digitales con procesos organizados buscó un auxiliar a cinco horas diarias para atención, archivo, correo y “solicitud y seguimiento de documentación de clientes” ([oferta](https://es.linkedin.com/jobs/view/auxiliar-administrativo-at-asesor%C3%ADa-l%C3%B3pez-garc%C3%ADa-4411898079)). La vacante está expirada hoy, pero el texto público rastreado demuestra la tarea.
- **FACT — fuerte:** Una vacante laboral que exige dominio avanzado de A3 incluye comunicación con clientes para solicitar y seguir documentación, atrasos, regularizaciones, AEAT/Seguridad Social y plazos; salario publicado 20–25k € ([vacante](https://es.linkedin.com/jobs/view/junior-laboral-con-a3-at-renlink-4416271802)). Es evidencia directa de que tener A3 no elimina el seguimiento.
- **FACT — fuerte:** Mouni Partners declara una plataforma propia sobre Holded que ya automatiza reporting, facturas y conciliación, pero contrata una persona para validar OCR, cuadrar bancos, perseguir incoherencias hasta su origen, revisar informes y mantener hojas de seguimiento ([vacante](https://es.linkedin.com/jobs/view/finance-intern-becario-financiero-contable-at-mouni-partners-4440562655)). La automatización desplaza trabajo hacia revisión/excepciones; no lo elimina.
- **FACT — media:** Una oferta de gestor documental en servicios profesionales paga 25.000 €/año para seguir clientes, solicitar información, registrar documentación y manejar alto volumen en Excel ([Randstad](https://www.randstad.com/jobs/gestor-de-documentacion-de-clientes_madrid_46318313/)). No es exclusivamente una asesoría fiscal, por lo que sólo prueba el patrón en servicios profesionales.
- **FACT — media:** Un hilo español de autónomos describe facturas repartidas entre correo, descargas, papel y Drive; un usuario tarda unas tres horas por trimestre, y otro dice que aun con portal de gestoría pierde control de lo ya enviado. Otro participante afirma que una estructura de carpetas le basta ([Reddit](https://www.reddit.com/r/autonomos/comments/1tytfe9/problema_al_reunir_facturas/)). La evidencia confirma heterogeneidad, no frecuencia poblacional.
- **FACT — media:** En una discusión internacional, una contable con 22 clientes afirma haber gastado seis horas en un mes persiguiendo documentos, con portal poco usado; otros participantes dicen que el problema es permanente o que debe imponerse el portal ([Reddit Accounting](https://www.reddit.com/r/Accounting/comments/1s715ta/how_do_you_get_clients_to_actually_send_you_what/)). Es transferible como patrón conductual, no como WTP española.
- **FACT — media:** Usuarios de portales contables declaran adopción desigual; algunos hablan de aproximadamente 50%, otros de adopción alta con onboarding estricto ([discusión](https://www.reddit.com/r/Accounting/comments/1ujwtac/do_clients_actually_use_client_portals/)). El canal no arregla por sí solo el comportamiento.
- **FACT — media:** Una reseña de ERPdiez pide avisos al cargar archivos y comunicación integrada para no depender de correo/WhatsApp, pese a valorar positivamente el software ([Capterra](https://www.capterra.com/p/241303/ERPdiez/reviews/)). Esto evidencia huecos de experiencia alrededor del portal, no ausencia de funciones básicas.
- **FACT — media:** Una publicación reciente de la comunidad Sage denuncia errores repetidos en fechas críticas de Renta, incertidumbre y tiempo adicional ([Sage Community](https://communityhub.sage.com/es/sage-despachos-connected/f/gestion-interna/269467/error-sage-despachos/648597)). El dolor es continuidad/excepción del sistema, no intake.
- **FACT — media:** Reseñas recientes de Holded señalan complejidad de integraciones y necesidad de soporte experto; son experiencias individuales, no una medición representativa ([Trustpilot](https://es.trustpilot.com/review/holded.com)).

### 3.2 Evidencia de proveedores, separada

- **FACT — marketing:** Content Snare afirma que cerca del 70% de firmas considera la recogida su mayor reto y presenta un caso con 75% menos tiempo administrativo; la cifra y el caso son del propio proveedor, no de un estudio independiente auditado ([página para contables](https://contentsnare.com/industries/accounting/), [artículo](https://contentsnare.com/request-files-from-clients/)).
- **FACT — marketing:** Glasscubes publica un caso de Verallo donde el portal anterior era poco usable y las respuestas llegaban por partes; es contenido patrocinado/soportado por el vendedor ([AccountingWEB](https://www.accountingweb.co.uk/community/industry-insights/why-client-portals-keep-failing-accountants-a-case-study-from-verallo)).
- **FACT — marketing:** OptimaTech, Recopila, Escania y otros describen exactamente el caos de correo/WhatsApp/faltantes. Es evidencia de que los vendedores ven demanda, no prueba de resultados o WTP ([OptimaTech](https://optimatech.es/), [Recopila](https://www.myeficacia.com/), [Escania](https://escania.es/)).

### 3.3 Lo que no se pudo demostrar

- **FACT:** No se encontró una encuesta española independiente y reciente que cuantifique horas mensuales de chasing por tamaño de despacho, porcentaje de clientes fuera de portal, coste de errores o presupuesto disponible.
- **FACT:** No se encontró evidencia pública de que los nueve prospects hayan perdido plazos, documentos o dinero por estos workflows.
- **INFERENCE:** El dolor es creíble y repetido, pero su intensidad y urgencia son distribuciones, no una propiedad del sector.
- **HYPOTHESIS:** La única validación comercial válida es una línea base del despacho: número de recordatorios, expedientes incompletos al corte, minutos de revisión, correcciones y retrasos.

## 4. Ataque A–J

| Ataque | Clasificación | Conclusión adversa |
|---|---|---|
| A. El vertical ya resuelve suficiente | **FATAL** para la cuña genérica | Portales, tareas, OCR, responsables, plazos y variables laborales están confirmados en A3/Sage/Bilky/Cegid/Quipu. Los point tools completan chasing y faltantes por 20–100 €/mes. |
| B. No pagarán a un proveedor externo | **SERIOUS** | Sí existen boutiques externas, pero no publican ventas/precios verificables. El buyer puede preferir soporte del proveedor, partner certificado o una herramienta barata. |
| C. Integrar por 3–4,5k € es antieconómico | **SERIOUS**; fatal en 1–5 empleados | El setup compite con productos ya integrados y puede consumir margen en legacy, permisos, pruebas y soporte. Sólo cuadra con un proceso crítico y reusable. |
| D. 450 €/mes no es realista | **SERIOUS** | Equivale a 4,5–22 veces los point tools españoles. Necesita ahorro/evitación demostrable y mantenimiento real, no “soporte”. |
| E. El dolor no es urgente | **SERIOUS** | La recogida trimestral se tolera y es estacional. Laboral, notificaciones y cierres tienen plazos, pero la urgencia debe ligarse a un incidente o corte concreto. |
| F. Los pequeños tienen dolor pero no presupuesto | **SERIOUS** | El 76,5% de despachos tiene menos de 10 empleados; el mercado dominante es pequeño y tiene sustitutos baratos ([Wolters Kluwer, barómetro 2026](https://www.wolterskluwer.com/es-es/expert-insights/radiografia-del-despacho-profesional-2026)). |
| G. Los grandes lo construyen o compran enterprise | **SERIOUS** | Mouni construyó sobre Holded; firmas mayores pueden comprar Karbon/TaxDome/Kabilio o asignar equipo interno. Procurement y seguridad elevan el coste de venta. |
| H. El comportamiento del cliente vuelve frágil la automatización | **SERIOUS** | Portales no usados, fotos borrosas, respuestas parciales y mensajes fuera de canal crean excepciones. Magic links/WhatsApp reducen fricción, no garantizan cumplimiento. |
| I. RGPD/seguridad/compliance hacen inviable al proveedor | **MANAGEABLE** | Exigen contrato de encargado, medidas, subencargados, minimización y trazabilidad; proveedores baratos ya publican DPA/hosting UE. Es coste y barrera de confianza, no veto absoluto ([AEPD](https://www.aepd.es/es/documento/guia-directrices-contratos.pdf), [FileCollect DPA](https://www.filecollect.io/dpa)). |
| J. La oferta es demasiado genérica | **FATAL** | Competidores españoles usan casi las mismas palabras y algunos cubren el proceso end-to-end. No hay razón pública para elegir esta oferta sin un workflow, stack, resultado y frontera concretos. |

### Notas de red team

**A — FACT:** AccioGest publica expedientes, portal, responsables, recordatorios, WhatsApp y API desde 29 €/mes; Taabolo publica faltantes, subsanaciones y automatización por 24 €/mes más uso ([AccioGest](https://acciogest.com/precios/), [Taabolo](https://taabolo.com/sector/asesorias-y-gestorias)). Esto no prueba calidad, pero sí sustituibilidad.

**B — INFERENCE:** El servicio externo sólo gana si hace el trabajo que el despacho no quiere/can’t do: configurar, migrar hábitos, probar, medir y mantener excepciones. Una construcción desde cero añade riesgo sin una ventaja pública.

**C/D — INFERENCE:** Con precio bajo de software, el comprador comparará el fee con “activar Bilky/A3/Sage” o contratar soporte. El setup debe incluir un entregable irreversible a favor del cliente —mapa, plantillas, reglas, baseline y documentación— aunque el piloto pare.

**E/H — FACT:** Las discusiones de usuarios muestran dos extremos: clientes que no usan portal y despachos que lo vuelven obligatorio. El resultado depende tanto de política de servicio y onboarding como de automatización ([portal adoption](https://www.reddit.com/r/Accounting/comments/1ujwtac/do_clients_actually_use_client_portals/), [TaxDome discussion](https://www.reddit.com/r/taxdome/comments/1s4951r/unpopular_opinion_client_portals_have_made/)).

**I — FACT:** La AEPD exige que la realidad del tratamiento coincida con los roles y contrato del artículo 28; en 2026 publicó un criterio sobre sanciones cuando el contrato no reflejaba la operación real ([AEPD](https://www.aepd.es/informes-y-resoluciones/criterios-juridicos-aepd/delimitacion-funcional-entre-responsable-y-encargado-tratamiento-ecosistemas-logisticos-y-tecnologicos)).

## 5. Realidad de precio

### 5.1 Anclas observables

- **FACT:** Herramientas focalizadas: aproximadamente 19–99 €/mes según Recopila, FileCollect, Archivum, Escania, AccioGest, Bilky y Taabolo.
- **FACT:** Suites internacionales: TaxDome cuesta 800 €/usuario/año en España a un año; Karbon Business, que incluye recordatorios automáticos, publica 89 USD/usuario/mes anual ([TaxDome UE](https://help.taxdome.com/article/926-eu-br-taxdome-pricing-faq), [Karbon](https://karbonhq.com/en-GB/pricing)).
- **FACT:** A3, Sage, Cegid y Kabilio no muestran en las páginas revisadas un precio comparable completo; no se inventa.
- **FACT:** Una vacante española de perfil laboral con A3 publica 20–25k € y otra de gestión documental 25k €/año. No equivalen al coste empresa ni a WTP, pero sirven para entender que el trabajo consume personal real ([A3 laboral](https://es.linkedin.com/jobs/view/junior-laboral-con-a3-at-renlink-4416271802), [Randstad](https://www.randstad.com/jobs/gestor-de-documentacion-de-clientes_madrid_46318313/)).

### 5.2 Coste mensual equivalente del primer año

| Opción | Equivalente mensual año 1 | Horas/mes para recuperar a 20 €/h | a 30 €/h | a 40 €/h |
|---|---:|---:|---:|---:|
| 1.000 € setup + 200 €/mes | 283 € | 14,2 | 9,4 | 7,1 |
| 2.000 € + 300 €/mes | 467 € | 23,4 | 15,6 | 11,7 |
| 3.000 € + 450 €/mes | 700 € | 35,0 | 23,3 | 17,5 |
| 4.500 € + 450 €/mes | 825 € | 41,3 | 27,5 | 20,6 |
| 5.000 € + cuota custom | 417 € + cuota | Fórmula: (417 + cuota) / 20 | / 30 | / 40 |

**HYPOTHESIS:** Los valores de 20/30/40 €/h son sensibilidad matemática, no costes laborales observados ni WTP. Cada buyer debe introducir su coste completo y el valor de riesgo/capacidad.

### 5.3 Encaje por tamaño

Leyenda: **PLAUSIBLE** = puede superar un filtro económico si el dolor está medido; **CONDITIONAL** = exige evidencia fuerte; **UNLIKELY** = no hay base pública para esperarlo.

| Tamaño del despacho | 1k + 200 | 2k + 300 | 3k + 450 | 4,5k + 450 | 5k + custom |
|---|---|---|---|---|---|
| 1–5 empleados | CONDITIONAL | UNLIKELY | UNLIKELY | UNLIKELY | UNLIKELY |
| 5–15 | PLAUSIBLE como primer piloto | PLAUSIBLE si ahorra 12–24 h/mes o reduce riesgo | CONDITIONAL | UNLIKELY | UNLIKELY salvo integración crítica |
| 15–50 | PLAUSIBLE, posiblemente barato | PLAUSIBLE | PLAUSIBLE con sponsor y métrica | CONDITIONAL/PLAUSIBLE si cruza equipo | CONDITIONAL para integración/security |
| 50+ | Económico pero puede ser demasiado pequeño para procurement | Económico pero poco estratégico | PLAUSIBLE económicamente | PLAUSIBLE económicamente | PLAUSIBLE económicamente, venta mucho más difícil |

**INFERENCE:** El sweet spot de un fundador solo no es 1–5: es 5–15 empleados con un responsable accesible, varios clientes laborales, stack conocido y sin equipo tecnológico interno. 15–50 puede pagar más, pero suben las expectativas de seguridad, continuidad e integración.

**HYPOTHESIS:** Para el primer caso, 1.000 € + 200 €/mes es el único precio que reduce suficientemente el riesgo del comprador sin regalar el trabajo. El precio estándar posterior debe ser 2.000 € + 300 €/mes sólo después de demostrar una línea base y un resultado repetible. 450 €/mes debe reservarse para dos o más equipos/centros o un workflow con integración y mantenimiento real.

## 6. Trigger regulatorio: útil, pero no una cuña en sí

- **FACT:** VERI*FACTU será obligatorio el 1 de enero de 2027 para contribuyentes del Impuesto sobre Sociedades y el 1 de julio de 2027 para el resto de obligados cubiertos ([AEAT](https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/preguntas-frecuentes.html?faqId=2e0c77fe52572910VgnVCM100000dc381e0aRCRD), [BOE](https://www.boe.es/buscar/doc.php?id=BOE-A-2025-24446)).
- **FACT:** El Real Decreto 238/2026 desarrolló la factura electrónica B2B; su aplicación efectiva se cuenta desde la futura orden ministerial: 12 meses para más de 8 M€ y 24 meses para el resto ([BOE, disposición final cuarta](https://www.boe.es/buscar/act.php?id=BOE-A-2026-7295)).
- **INFERENCE:** Estos cambios crean conversaciones y migraciones, pero benefician primero a A3/Sage/Cegid/Holded/Quipu, que ya venden adaptación. “Te preparo para Verifactu” no diferencia.
- **HYPOTHESIS:** El trigger útil es una migración o implantación concreta que haya dejado clientes fuera de canal, no la norma abstracta.

## 7. Implicaciones para los nueve prospects

Los estados comparan contra el orden de investigación previo. No se añade una lista nueva.

| Prospect | Estado | Por qué cambia | Condición para discovery |
|---|---|---|---|
| Carsán Gestión | **UNCHANGED** | 14 empleados, tres oficinas y A3 CON dan volumen y stack conocido, pero A3 ya cubre mucho y no existe dolor probado ([web](https://www.carsangestion.es/), [contacto](https://www.carsangestion.es/contacto/)). | Preguntar por una excepción concreta entre sedes/canales y A3, no por “automatización documental”. |
| Sialco Asesores | **LOWER** | Su portal Bilky nuevo ofrece documentos, CRM, alertas e integraciones a precio bajo; proponer otra capa sería redundante ([portal](https://sialco.es/acceso-portal-sialco-asesores/), [Bilky](https://bilky.es/funcionalidades/)). | Sólo si puede medir clientes fuera del portal o una excepción no cubierta. |
| Guijarro y Ruiz | **UNCHANGED** | La recogida física y dos oficinas siguen siendo un workflow visible, pero productos sin login/WhatsApp abaratan la solución y el tamaño/presupuesto no están claros ([web](https://guijarroyruizasesores.com/)). | Confirmar frecuencia, trazabilidad y horas antes de hablar de precio. |
| CDC Asesores | **HIGHER** | Si los 200+ clientes siguen activos, un ciclo laboral/fiscal puede tener volumen; buyer directo y stack no publicado. La cifra debe validarse ([web](https://cdcasesores.com/)). | Elegir un solo corte recurrente y medir recordatorios/expedientes incompletos. |
| Del Amo Asesores | **LOWER** | Tres empleados y <300k € de facturación estimada hacen difícil competir con software de 20–80 €/mes; el dolor visible no prueba presupuesto ([web](https://delamoasesores.es/)). | Sólo piloto low-risk si reconoce ≥10 h/mes o riesgo concreto. |
| Viaconta | **HIGHER** | Dos oficinas, teléfonos por área y operación laboral permiten probar routing/cierre con buyer accesible; no hay stack público que descarte la hipótesis ([web](https://www.viaconta.es/)). | No asumir silos: medir un expediente que cruce canales o áreas. |
| Ibérica de Asesoramiento | **LOWER** | Buyer claro, pero no hay señal de cambio, volumen, software ni dolor; el intake genérico ya no basta ([web](https://ibericadeasesoramiento.com/)). | Sólo si una conversación revela un proceso recurrente y cuantificable. |
| Asesorus | **LOWER** | Holded Gold Partner, Bilky, Aplifisa/Aon y capacidad de implantación interna aumentan sustitución e internalización ([equipo](https://www.asesorus.es/equipo-asesorus/), [Holded](https://www.asesorus.es/holded-asesorus-gestion-contable-laboral/)). | Sólo una excepción sofisticada entre sistemas; mala opción para primer caso. |
| Karma Asesores | **DISQUALIFIED** | La antigua Karma Asesores SL está extinguida; la marca parece operar con Formission SL y no hay buyer/rol público inequívoco ([BORME](https://www.boe.es/borme/dias/2017/03/02/pdfs/BORME-A-2017-43-28.pdf), [web](https://k-asesores.com/asesoria-laboral-madrid/)). | No invertir discovery comercial hasta resolver entidad, decisor y tamaño. |

Nuevo orden sólo entre estos nueve: **CDC, Carsán, Viaconta, Guijarro y Ruiz, Sialco, Del Amo, Ibérica, Asesorus, Karma**. Es un orden para aprendizaje, no una predicción de compra.

## 8. Decisión operativa final

### Lo que se abandona

- **FACT/DECISION:** No ofrecer “recogida documental + recordatorios + clasificación + routing” como una solución general.
- **FACT/DECISION:** No construir portal, OCR, bot de WhatsApp ni middleware A3/Sage antes de una venta.
- **FACT/DECISION:** No cobrar 3–4,5k € de setup por un flujo que pueda configurarse en Bilky, AccioGest, Taabolo, FileCollect o el vertical ya comprado.

### Lo que se prueba

- **HYPOTHESIS:** ICP: despacho independiente de 5–15 empleados, con área laboral, A3/Sage/Cegid/Aplifisa/Bilky ya contratado, sin equipo técnico interno y con un corte mensual que todavía recibe cambios por más de un canal.
- **HYPOTHESIS:** Buyer: socio director + responsable laboral; el primero controla presupuesto y el segundo conoce excepciones, plazos y retrabajo.
- **HYPOTHESIS:** Workflow: variables/cambios laborales antes del cierre de nómina, limitado a solicitud, completitud, recordatorio, excepción, propietario y entrega humana al sistema de nómina.
- **HYPOTHESIS:** Oferta: configurar primero el stack existente y añadir sólo el mínimo puente externo imprescindible; un cierre, una cohorte, una línea base, sin decisiones autónomas ni escritura directa en nómina.
- **HYPOTHESIS:** Piloto: 30 días; éxito si reduce al menos 30% los recordatorios manuales o el tiempo de seguimiento frente a la línea base acordada, sin aumentar correcciones y manteniendo aprobación humana. El 30% no es benchmark de mercado: es un umbral de prueba que el buyer debe aceptar o sustituir.
- **HYPOTHESIS:** Precio de entrada: 1.000 € setup + 200 €/mes; precio estándar futuro: 2.000 € + 300 €/mes tras evidencia repetible. No prometer 450 €/mes en microdespachos.
- **HYPOTHESIS:** Objección principal: “A3/Bilky/Sage ya lo hace”. Respuesta: “Entonces no hay proyecto. Primero comprobamos si el flujo ya comprado cubre el cierre; sólo intervenimos sobre la adopción o la excepción medible.”

El detalle ejecutable está en `first_offer_v2.md`; el ranking en `surviving_wedges.md`; el inventario completo de fuentes y sus sesgos en `commercial_red_team_sources.md`.
