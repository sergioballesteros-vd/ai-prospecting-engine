# Commercial Red Team — fuentes y trazabilidad

Fecha de consulta: 23 de agosto de 2026. Todas las URLs eran públicas en la fecha de consulta. Este fichero distingue fuente primaria, evidencia de usuario y marketing de proveedor. Una ausencia en documentación pública se registra como `NOT FOUND`, nunca como prueba de inexistencia.

## Jerarquía usada

1. **Norma/fuente oficial:** BOE, AEAT, AEPD.
2. **Documentación primaria de producto:** página del fabricante, ayuda, ficha funcional, API o precio.
3. **Evidencia operativa:** vacantes, foros de soporte y reseñas atribuibles.
4. **Prensa/directorio:** útil para escala, propiedad o financiación; puede estar desactualizado.
5. **Comunidad:** útil para descubrir patrones y contraejemplos; no representativa.
6. **Marketing/caso de proveedor:** demuestra posicionamiento y claims, no resultados independientes.

## A. Wolters Kluwer A3

| ID | Fuente | Tipo | Qué respalda | Límite/sesgo |
|---|---|---|---|---|
| A01 | [a3ASESOR](https://www.wolterskluwer.com/es-es/solutions/a3asesor) | Primaria | Suite integrada fiscal/contable/laboral, ficha única, roles y procesos | No demuestra configuración real en un despacho |
| A02 | [a3doc](https://www.wolterskluwer.com/es-es/solutions/software-gestion-documental-a3doc) | Primaria | Gestión documental cloud, intercambio con cliente e integración A3 | No confirma chasing de faltantes |
| A03 | [Ficha a3doc](https://assets.contenthub.wolterskluwer.com/api/public/content/2458301-ficha-producto-a3doc-cloud-despacho-241420a5e2?v=c7ba5851) | Primaria/PDF | Clasificación automática, búsqueda, acciones, intercambio bidireccional | “Automática” no equivale a IA semántica |
| A04 | [a3ASESOR Ges](https://www.wolterskluwer.com/es-es/solutions/a3asesor-ges) | Primaria | Tareas, expedientes, documentos, costes y responsables | No confirma canal de entrada |
| A05 | [a3factura para asesorías](https://www.wolterskluwer.com/es-es/solutions/a3factura/asesorias) | Primaria | Flujo factura-cliente-contabilidad, adjuntos y proceso histórico | Centrado en facturación |
| A06 | [Conectia](https://www.wolterskluwer.com/es-es/solutions/conectia) | Primaria | Portal/API del ecosistema cloud | Cobertura de productos legacy no inequívoca |
| A07 | [a3HRgo](https://www.wolterskluwer.com/es-es/solutions/a3hrgo-para-asesorias) | Primaria | Portal empleado, documentación e integración con nómina | No cubre todo el workflow laboral |
| A08 | [a3innuva Portal del Empleado](https://www.wolterskluwer.com/es-es/solutions/a3innuva-portal-del-empleado-empresas) | Primaria | Altas, cambios, variables, ausencias, IT, permisos y trazabilidad | Producto para empresa/asesoría; adopción no probada |
| A09 | [a3ASESOR Nom](https://www.wolterskluwer.com/es-es/solutions/a3asesor-nom) | Primaria | Nómina, procesos masivos e integración con portal | Claims del fabricante |
| A10 | [Radiografía del despacho 2026](https://www.wolterskluwer.com/es-es/expert-insights/radiografia-del-despacho-profesional-2026) | Estudio de proveedor | 76,5% del sector con menos de 10 empleados | Metodología completa no visible en la página consultada |
| A11 | [Portal NEOS para asesorías](https://www.wolterskluwer.com/es-es/solutions/portalneos-asesorias) | Primaria | Sincronización de buzones, plazos y notificaciones oficiales | Demuestra que el workflow base ya tiene solución vertical |

## B. Sage

| ID | Fuente | Tipo | Qué respalda | Límite/sesgo |
|---|---|---|---|---|
| B01 | [Sage para asesorías](https://www.sage.com/es-es/asesorias-y-despachos/) | Primaria | Suite conectada, portal, automatización y colaboración | Marketing de fabricante |
| B02 | [Sage Despachos Connected](https://www.sage.com/es-es/software-asesorias-y-despachos/) | Primaria | Expedientes, tareas, cargas, peticiones, OCR, CRM y portales | No prueba uso/adopción |
| B03 | [Detalle funcional](https://www.sage.com/es-es/-/media/files/sagedotcom/spain/documents/pdf/generacion_despachos_profesionales.pdf) | Primaria/PDF | Módulos de gestión interna, laboral, contable y portal | Documento comercial |
| B04 | [Declaración de conectividad](https://www.sage.com/es-es/-/media/files/sagedotcom/spain/documents/pdf/certificados/declaracion_responsable_sagedespachosc_30-4-25.pdf) | Primaria/PDF | Office 365, OneDrive, bancos, portales y botón WhatsApp | Botón WhatsApp no es ingestión automática |
| B05 | [Partners tecnológicos](https://www.sage.com/es-es/partners/tech-partners/) | Primaria | Ecosistema de integración | No especifica todas las APIs por producto |
| B06 | [Portal del Empleado](https://www.sage.com/es-es/-/media/images/sagedotcom/spain/es-es/pdf/productos/sage%20200c%20laboral/new/sage200-laboral-modulo-portal-del-empleado.pdf) | Primaria/PDF | Datos, anticipos, vacaciones y autoservicio | Documento antiguo; funciones actuales pueden variar |
| B07 | [Sage Community: error en fecha crítica](https://communityhub.sage.com/es/sage-despachos-connected/f/gestion-interna/269467/error-sage-despachos/648597) | Usuario/soporte | Fallos y tiempo extra durante Renta | Caso individual no representativo |
| B08 | [Sage Notificaciones](https://www.sage.com/es-es/-/media/images/sagedotcom/spain/es-es/pdf/partner/catalogo%20isv/catalogo_isv_2020_15febrero.pdf?la=es-es) | Primaria histórica/PDF | Seguimiento desatendido de buzones AEAT/TGSS integrado con Sage | Documento antiguo; no usar para asegurar alcance actual |

## C. Holded, Bilky, Aplifisa, Cegid/Diez, Quipu y NCS

| ID | Fuente | Tipo | Qué respalda | Límite/sesgo |
|---|---|---|---|---|
| C01 | [Holded IA para asesorías](https://www.holded.com/es/ia-asesorias) | Primaria | Email-in, OCR/IA, clasificación, duplicados y revisión | Claims del proveedor |
| C02 | [Holded asesorías](https://www.holded.com/es/asesorias) | Primaria | Colaboración asesor-cliente | No confirma missing-doc chase |
| C03 | [Holded precios](https://www.holded.com/es/precios) | Primaria | Planes 15–199 €/mes y módulos | Precio de cartera de asesoría puede variar |
| C04 | [Holded API](https://www.holded.com/es/desarrolladores) | Primaria/técnica | API, claves, paginación y estado de webhooks | Capacidades cambian; fecha de consulta importa |
| C05 | [Holded integraciones](https://www.holded.com/es/integraciones) | Primaria | Zapier, Drive, Dropbox y ecommerce | Profundidad desigual |
| C06 | [Holded portal](https://help.holded.com/es/articles/9382835-acciones-disponibles-en-el-portal-del-cliente) | Ayuda primaria | Acciones visibles para el cliente | No es portal documental completo de asesoría |
| C07 | [Holded Trustpilot](https://es.trustpilot.com/review/holded.com) | Reseñas | Fricción de integraciones/soporte en casos recientes | Autoselección y casos individuales |
| C08 | [Bilky funciones](https://bilky.es/funcionalidades/) | Primaria | Portales, OCR/IA, CRM, roles, procesos, plazos | Marketing del proveedor |
| C09 | [Bilky integraciones](https://bilky.es/integraciones/) | Primaria | A3, Aplifisa y otras integraciones | No prueba calidad bidireccional |
| C10 | [Bilky precios 2026](https://bilky.es/tarifas-para-asesorias-2026/) | Primaria | 29,99/59,99/79,99 €/mes y módulos | Promociones/IVA pueden variar |
| C11 | [Bilky Trustpilot](https://es.trustpilot.com/review/bilky.es) | Reseñas | Valoración y experiencias de soporte/portal | 56 reseñas; mayoría antiguas/positivas |
| C12 | [Visma entra en Bilky](https://cadenaser.com/andalucia/2026/04/27/el-gigante-noruego-del-software-visma-entra-en-el-capital-de-la-malaguena-bilky-ser-malaga/) | Prensa | Escala declarada y respaldo competitivo | Cifras proceden en parte de las empresas |
| C13 | [ApliScan](https://www.aplifisa.com/asesorias/escanear-contabilizar-facturas/) | Primaria | Escaneo/PDF a asiento y archivo documental | No confirma IA general |
| C14 | [Aplifisa Fiscal](https://www.aplifisa.com/asesorias/programa-fiscal-aplifisa/) | Primaria | Obligaciones, avisos SMS/email y fiscal | No prueba chase de documentos |
| C15 | [Aplifisa teletrabajo](https://www.aplifisa.com/empresas-teletrabajo/) | Primaria | Doc3W, portal, tareas/expedientes y precios parciales | Página orientada a empresa |
| C16 | [Cegid ERP Despachos](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/) | Primaria | ERP 360, tareas, documentos, expedientes, proyectos y avisos | No detalla API de Diez |
| C17 | [Cegid Portal Asesor](https://www.cegid.com/ib/es/productos/software-programa-erp-asesorias-gestorias/portal-asesor/) | Primaria | Intercambio documental y estados | Claims del fabricante |
| C18 | [Cegid Profiture](https://www.cegid.com/ib/es/productos/programas-software-erp-bi-business-intelligence/) | Primaria | Capacidad, productividad y carga por cliente | No sustituye workflow operativo |
| C19 | [Diez Asesor móvil](https://play.google.com/store/apps/details?id=com.diezsoftware.asesormovil&hl=es) | Marketplace oficial | Foto/digitalización y DiezSCAN; actualización 2026 | Texto del editor, no prueba de uso |
| C20 | [ERPdiez Capterra](https://www.capterra.es/software/1023434/erpdiez) | Reseñas/directorio | 69 reseñas, precio inicial indicado y valoración | Datos agregados de tercero |
| C21 | [ERPdiez reviews](https://www.capterra.com/p/241303/ERPdiez/reviews/) | Reseñas | Petición de avisos/comunicación para evitar correo/WhatsApp | Una reseña no representa a todos |
| C22 | [Quipu asesorías](https://getquipu.com/es/despachos) | Primaria | Plataforma colaborativa y API | Precio de partner no público |
| C23 | [Quipu OCR/email-in](https://getquipu.com/es/digitalizar-facturas-asesorias) | Primaria | OCR/IA, email, duplicados, revisión humana | Claims de precisión del proveedor |
| C24 | [Quipu precios negocio](https://getquipu.com/es/despachos) | Primaria | 13–28 €/mes para negocio | No equivale a plan de asesoría completa |
| C25 | [Quipu para asesorías](https://getquipu.com/ca/assessories) | Primaria | Complemento a contabilidad, tareas, notificaciones y activación de clientes | Página en catalán y claims del proveedor |
| C26 | [NCS Asesoriaweb](https://www.ncs.es/emprendedores2018/index.htm) | Primaria histórica | Portal, archivo y automatización | Página antigua; no usada para afirmar estado completo 2026 |
| C27 | [NCS EFacturaE 2026](https://blog.ncs.es/novedades/ncs-efacturae-gestion-documental-mejoras/) | Primaria | Actividad y mejoras recientes | No cubre toda la suite |

## D. Competidores españoles directos

| ID | Fuente | Tipo | Claim relevante |
|---|---|---|---|
| D01 | [Recopila](https://www.myeficacia.com/) | Primaria | Campañas, magic link, recordatorios, estado y descarga organizada |
| D02 | [Archivum Cloud](https://archivumcloud.com/) | Primaria | Solicitud, revisión, comentarios, aprobación/rechazo, versiones y precios |
| D03 | [Escania](https://escania.es/) | Primaria | WhatsApp/Telegram, OCR/IA, clasificación, recordatorios y precios |
| D04 | [Escania DPA](https://escania.es/dpa) | Primaria/legal | Roles, subencargados y WhatsApp Business API declarados |
| D05 | [Previoo gestorías](https://previoo.io/previoo-gestorias/) | Primaria | Recordatorios, faltantes/errores y exportación A3/Sage/Wolters |
| D06 | [Taabolo asesorías](https://taabolo.com/sector/asesorias-y-gestorias) | Primaria | Ciclo completo, detección de pendientes y tarifa por uso/gestionada |
| D07 | [AccioGest precios](https://acciogest.com/precios/) | Primaria | 29/49/99 €, portal, WhatsApp, plazos, responsables y API |
| D08 | [Kabilio asesorías](https://www.kabilio.es/asesores/asesorias) | Primaria | Captura, IA, contabilidad e integración A3 |
| D09 | [Kabilio carga](https://help.kabilio.es/carga-de-documentos) | Ayuda primaria | Canales de carga de documentos |
| D10 | [Kabilio ronda](https://cincodias.elpais.com/companias/2025-11-05/la-espanola-kabilio-levanta-cuatro-millones-en-una-ronda-pre-seed-para-su-ia-de-automatizacion-de-procesos-contables-y-fiscales.html) | Prensa | Financiación, equipo y adopción declarada | Cifras de compañía/prensa |
| D11 | [OptimaTech](https://optimatech.es/) | Primaria | Oferta vertical a medida, incluido payroll intake, correo y mantenimiento |
| D12 | [Sergio Sallavera](https://sergiosallavera.es/automatizacion-asesorias/) | Primaria | Oferta de un solo consultor casi idéntica a la hipótesis |
| D13 | [ROXEX](https://roxex.es/sectores/gestorias) | Primaria | Portal, plazos, recordatorios y n8n/A3/Sage declarados |

## E. Competidores UE/internacionales

| ID | Fuente | Tipo | Claim relevante |
|---|---|---|---|
| E01 | [FileCollect](https://www.filecollect.io/) | Primaria | Checklist, enlace sin cuenta, reminders y entrega Drive |
| E02 | [FileCollect precios](https://www.filecollect.io/pricing) | Primaria | 0/19,99/49 € y API/webhooks/Zapier |
| E03 | [FileCollect DPA](https://www.filecollect.io/dpa) | Primaria/legal | DPA artículo 28 y tratamiento declarado |
| E04 | [Content Snare contables](https://contentsnare.com/industries/accounting/) | Primaria/marketing | Intake, approval, recordatorios, portal e integraciones |
| E05 | [Content Snare precios](https://contentsnare.com/pricing/) | Primaria | 35/71 USD mensual equivalente anual y enterprise |
| E06 | [Quire](https://withquire.com/) | Primaria | Recurring requests, magic links, SMS/email y QBO/Xero |
| E07 | [Quire precios](https://withquire.com/pricing/) | Primaria | 49/89 USD y capacidades por plan |
| E08 | [Financial Cents workflow](https://financial-cents.com/workflow-automation/) | Primaria | Requests, email-to-task, reminders, owners y recurring work |
| E09 | [Financial Cents precios](https://financial-cents.com/pricing/) | Primaria | Inicio 19 USD/mes solo y planes de equipo |
| E10 | [Financial Cents ayuda](https://help.financial-cents.com/en/articles/4213219-client-tasks-requests) | Ayuda primaria | Recordatorios email/SMS hasta completar |
| E11 | [TaxDome precios España/UE](https://help.taxdome.com/article/926-eu-br-taxdome-pricing-faq) | Ayuda primaria | 800 €/usuario/año en España; asiento mensual 90 € |
| E12 | [TaxDome capacidades](https://taxdome.com/pricing) | Primaria | Portal, organizers, workflow, omnicanal, reminders e IA |
| E13 | [TaxDome integraciones](https://help.taxdome.com/article/taxdome-integrations) | Ayuda primaria | Diferencias global/UE y DATEV |
| E14 | [Karbon clientes/workflow](https://karbonhq.com/solution/client-management) | Primaria | Requests, fechas, email, reminders y visibilidad |
| E15 | [Karbon precios](https://karbonhq.com/en-GB/pricing) | Primaria | 89 USD/usuario/mes anual para Business con reminders |
| E16 | [Glasscubes AI Assist](https://www.glasscubes.com/ai-assist/) | Primaria | Faltantes, reminders, estados y enlace sin contraseña |
| E17 | [Glasscubes precios](https://www.glasscubes.com/pricing/) | Primaria | Página de precio; crawl no permitió confirmar base completa |
| E18 | [Dext upload](https://help.dext.com/en/collections/878120-upload) | Ayuda primaria | Canales de carga y documentos |

## F. Dolor real, comportamiento y operación

| ID | Fuente | Tipo | Evidencia | Confianza |
|---|---|---|---|---|
| F01 | [Asesoría López García: auxiliar](https://es.linkedin.com/jobs/view/auxiliar-administrativo-at-asesor%C3%ADa-l%C3%B3pez-garc%C3%ADa-4411898079) | Vacante | Solicitud/seguimiento documental, email, archivo y soporte; 5 h/día | Alta en la tarea; URL hoy redirige por expiración |
| F02 | [Junior laboral con A3](https://es.linkedin.com/jobs/view/junior-laboral-con-a3-at-renlink-4416271802) | Vacante | Seguimiento documental persiste con A3; 20–25k € | Alta |
| F03 | [Mouni Partners](https://es.linkedin.com/jobs/view/finance-intern-becario-financiero-contable-at-mouni-partners-4440562655) | Vacante | Automatización propia + revisión OCR, discrepancias y tracking manual | Alta |
| F04 | [Randstad gestor documental](https://www.randstad.com/jobs/gestor-de-documentacion-de-clientes_madrid_46318313/) | Vacante | 25k €, solicitud de info, Excel y alto volumen | Media; sector más amplio |
| F05 | [Problema al reunir facturas](https://www.reddit.com/r/autonomos/comments/1tytfe9/problema_al_reunir_facturas/) | Comunidad España | Fragmentación, tres horas/trimestre, portal sin control; también contraejemplo de carpetas | Media-baja, muestra pequeña |
| F06 | [Chasing clients](https://www.reddit.com/r/Accounting/comments/1s715ta/how_do_you_get_clients_to_actually_send_you_what/) | Comunidad internacional | Seis horas/mes en 22 clientes y portal ignorado | Media-baja, no España |
| F07 | [Uso de portales](https://www.reddit.com/r/Accounting/comments/1ujwtac/do_clients_actually_use_client_portals/) | Comunidad internacional | Adopción heterogénea | Media-baja |
| F08 | [TaxDome portal opinion](https://www.reddit.com/r/taxdome/comments/1s4951r/unpopular_opinion_client_portals_have_made/) | Comunidad/cliente producto | Portal puede aumentar chase sin onboarding obligatorio | Media-baja |
| F09 | [Feedback de servicio](https://www.reddit.com/r/AutonomosES/comments/1vd28nx/feedback_de_servicio/) | Comunidad España | Advertencia de competencia y valor en documentos incompletos | Baja; autor validando producto |
| F10 | [Caso Glasscubes/Verallo](https://www.accountingweb.co.uk/community/industry-insights/why-client-portals-keep-failing-accountants-a-case-study-from-verallo) | Caso patrocinado | Portal antiguo poco usable y respuestas fragmentadas | Media-baja; patrocinio explícito |
| F11 | [Content Snare para contables](https://contentsnare.com/industries/accounting/) | Caso/marketing | Claim de 75% de reducción en administración | Baja como benchmark independiente |
| F12 | [Sage Community error](https://communityhub.sage.com/es/sage-despachos-connected/f/gestion-interna/269467/error-sage-despachos/648597) | Foro de usuario | Fallos en momento crítico y coste de tiempo | Media; caso individual |
| F13 | [Holded Trustpilot](https://es.trustpilot.com/review/holded.com) | Reseñas | Complejidad de integración y soporte | Media-baja |

## G. Regulación, seguridad y triggers

| ID | Fuente | Tipo | Claim relevante |
|---|---|---|---|
| G01 | [AEAT FAQ VERI*FACTU](https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/preguntas-frecuentes.html?faqId=2e0c77fe52572910VgnVCM100000dc381e0aRCRD) | Oficial | 1/1/2027 sociedades; 1/7/2027 resto cubierto |
| G02 | [RDL 15/2025](https://www.boe.es/buscar/doc.php?id=BOE-A-2025-24446) | BOE | Ampliación formal de plazos VERI*FACTU |
| G03 | [RD 1007/2023 consolidado](https://www.boe.es/buscar/act.php?id=BOE-A-2023-24840) | BOE | Requisitos SIF y fechas consolidadas |
| G04 | [RD 238/2026 factura electrónica B2B](https://www.boe.es/buscar/act.php?id=BOE-A-2026-7295) | BOE | Aplicación 12/24 meses desde orden ministerial; estados e interoperabilidad |
| G05 | [AEPD guía contratos de encargo](https://www.aepd.es/es/documento/guia-directrices-contratos.pdf) | Oficial | Contenido de contrato y obligaciones artículo 28 |
| G06 | [AEPD roles reales en ecosistemas](https://www.aepd.es/informes-y-resoluciones/criterios-juridicos-aepd/delimitacion-funcional-entre-responsable-y-encargado-tratamiento-ecosistemas-logisticos-y-tecnologicos) | Oficial | Sanciones cuando contrato y realidad del tratamiento divergen |
| G07 | [AEPD cloud para clientes](https://www.aepd.es/guias/guia-cloud-clientes.pdf) | Oficial | Contrato, subencargados y medidas adecuadas al riesgo | Guía antigua, principios vigentes |

## H. Fuentes de los nueve prospects

La reevaluación reutiliza la investigación pública detallada del 23 de agosto de 2026 y sólo cambia la lectura comercial.

| Prospect | Fuentes clave |
|---|---|
| Carsán | [web](https://www.carsangestion.es/), [contacto](https://www.carsangestion.es/contacto/), [aviso legal](https://www.carsangestion.es/aviso-legal/), [Empresia](https://www.empresia.es/empresa/carsan-gestion/) |
| Sialco | [web](https://sialco.es/), [portal](https://sialco.es/acceso-portal-sialco-asesores/), [Bilky de Sialco](https://sialco.bilky.es/), [Iberinform](https://www.iberinform.es/empresa/201516/sialco-asesores) |
| Guijarro y Ruiz | [web](https://guijarroyruizasesores.com/), [equipo](https://guijarroyruizasesores.com/quien-somos/), [BORME](https://www.boe.es/borme/dias/2022/05/27/pdfs/BORME-A-2022-100-28.pdf) |
| CDC | [web](https://cdcasesores.com/), [BORME](https://www.boe.es/borme/dias/2019/01/04/pdfs/BORME-A-2019-3-28.pdf), [Empresia](https://www.empresia.es/empresa/consulting-diaz-cordero-asesores-asociados/) |
| Del Amo | [web](https://delamoasesores.es/), [privacidad](https://delamoasesores.es/politica-de-privacidad/), [Informa](https://www.informa.es/directorio-empresas/Empresa_AMO-ASESORES.html) |
| Viaconta | [web](https://www.viaconta.es/), [BORME](https://www.boe.es/diario_borme/txt.php?id=BORME-A-2022-239-28), [LinkedIn empresa](https://es.linkedin.com/company/viaconta-consultoria-empresarial-sl) |
| Ibérica | [web](https://ibericadeasesoramiento.com/), [contacto](https://ibericadeasesoramiento.com/contactar/), [socios](https://ibericadeasesoramiento.com/socios-partners/) |
| Asesorus | [web](https://www.asesorus.es/), [equipo/stack](https://www.asesorus.es/equipo-asesorus/), [Holded](https://www.asesorus.es/holded-asesorus-gestion-contable-laboral/), [Informa](https://www.informa.es/directorio-empresas/Empresa_ASESORUS-INNOVACION-TECNOLOGICA.html) |
| Karma | [web](https://k-asesores.com/), [Formission en el pie](https://k-asesores.com/asesoria-laboral-madrid/), [BORME de extinción](https://www.boe.es/borme/dias/2017/03/02/pdfs/BORME-A-2017-43-28.pdf), [Formission](https://www.empresia.es/empresa/formission/) |

## I. Gaps que deben permanecer como gaps

- **FACT:** No se encontró pricing público completo de A3, Sage Despachos, Cegid ERP Despachos, Kabilio, OptimaTech, Sergio Sallavera, ROXEX o Glasscubes base. Se registra `UNKNOWN`; no se estima.
- **FACT:** No se encontró ingestión WhatsApp confirmada para a3doc, Bilky, Holded para asesorías, Aplifisa o Cegid/Diez. Un botón de WhatsApp, soporte por WhatsApp o envío de mensajes no prueba ingestión documental.
- **FACT:** No se encontró una encuesta española independiente reciente de horas de chasing, adopción de portal o WTP por tamaño de despacho.
- **FACT:** No se verificó dolor interno en ninguno de los nueve prospects. Todo pain statement individual sigue siendo hipótesis.
- **INFERENCE:** Estos gaps no son razones para vender; son preguntas de discovery.
