# Documentation index

Checkpoint date: **2026-08-23**. This index describes the current state; dated validation and research files preserve earlier hypotheses for traceability.

## What is this?

AI Prospecting Engine is currently a human-in-the-loop commercial validation system supporting:

```text
prospecting
→ evidence research
→ opportunity scoring
→ first-customer fit
→ manual outreach
→ discovery
→ qualification
→ pilot readiness
→ commercial pipeline/outcomes
```

It does not send outreach. Public research is evidence for a question, not proof of a buyer's internal problem.

## Current commercial objective

- **North Star:** €900 MRR.
- **Near-term objective:** first paid pilot.

## Current commercial hypothesis

The primary hypothesis is **monthly payroll-close exception control for Spanish advisory/accounting/payroll firms**. The offer is existing-stack-first: it should configure or reuse A3, Sage, Bilky, Aplifisa, Cegid/Diez, or the customer's approved collaboration tools before custom software is considered.

The safest delivery default is **Blueprint A0**:

```text
customer-owned intake
→ deterministic metadata checklist
→ narrow exception queue
→ named owner
→ human review
→ manual payroll handoff
```

Default boundaries: no ERP write-back, payroll calculation, autonomous legal decision, required LLM, or document storage.

The design-partner pricing hypothesis is **€1,000 setup + €200/month**. It is unvalidated and only compatible with a tightly bounded, configuration-led pilot.

The secondary hypothesis is **out-of-scope work: request → scope check → approval → execution → invoicing**. It remains a discovery hypothesis, not a product.

## Current funnel

Source: local persisted commercial database at this checkpoint.

| Metric | Current value |
|---|---:|
| Connection requests sent | 5 |
| Accepted | 0 |
| Conversations | 0 |
| Discovery calls | 0 |
| Pilot candidates | 0 |
| Paid pilots | 0 |
| Setup revenue | €0 |
| MRR | €0 / €900 |

## Decision gates

| Gate | Meaning |
|---|---|
| `COMMERCIAL_OUTREACH_READY` | The evidence, manual outreach process, boundaries, and initial queue are ready. It does not validate pain or authorize automated sending. |
| `DISCOVERY_SYSTEM_READY` | Buyer-reported discovery can be recorded, quantified, and qualified with safe outcomes including no problem, existing stack solves it, and measure first. It does not prove either wedge. |
| `PILOT_DELIVERY_READY` | A bounded, existing-stack-first pilot can be assessed and delivered after a real candidate passes the handoff and commercial approval. It does not authorize implementation on its own. |

## What not to build yet

- Universal ERP connectors.
- SaaS multitenancy.
- OCR engine or generic email classifier.
- Generic workflow builder or chatbot.
- WhatsApp automation platform.
- Payroll engine or legal decision agent.
- Customer mobile app or full CRM.
- Speculative integrations, write-back, or infrastructure.

## Documentation map

### Commercial — current operating material

- [Commercial operations status](commercial/commercial_ops_status.md) — canonical funnel details and unknowns.
- [First offer v2](commercial/first_offer_v2.md) — current unvalidated offer and pricing hypothesis.
- [Manual commercial playbook](commercial/commercial_playbook.md).
- [Commercial learning loop](commercial/commercial_learning_loop.md).
- [Outreach queue](commercial/tomorrow_outreach_queue.md) — **paused historical queue; do not send while the five current requests await evidence**.

### Discovery — current interview and qualification system

- [Discovery playbook](discovery/discovery_playbook_v1.md).
- [First-call cheatsheet](discovery/discovery_first_call_cheatsheet.md).
- [Decision tree](discovery/discovery_decision_tree.md).
- [Quantification](discovery/discovery_quantification.md).
- [Objection lab](discovery/discovery_objection_lab.md).
- [Simulations](discovery/discovery_simulations.md).
- [Discovery Engine implementation](discovery/discovery_engine_implementation.md).

### Pilot — current delivery-readiness material

- [Pilot candidate handoff](pilot/pilot_candidate_handoff.md) — hard prerequisite for implementation.
- [Pilot delivery lab](pilot/pilot_delivery_lab.md).
- [Architecture blueprints](pilot/pilot_architecture_blueprints.md).
- [Stack matrix](pilot/pilot_stack_matrix.md) and [stack recommendation](pilot/pilot_stack_recommendation.md).
- [Security checklist](pilot/pilot_security_checklist.md) and [implementation checklist](pilot/pilot_implementation_checklist.md).
- [Technical discovery questions](pilot/pilot_technical_discovery_questions.md).
- [Failure modes](pilot/pilot_failure_modes.md) and [economic kill criteria](pilot/pilot_economic_kill_criteria.md).
- [Vendor/source register](pilot/pilot_vendor_sources.md).

### Research — evidence and hypothesis evolution

- [Commercial red team](research/commercial_red_team.md) and [source register](research/commercial_red_team_sources.md).
- [Surviving wedges](research/surviving_wedges.md).
- [Madrid advisory deep research, 2026-08-23](research/madrid_advisory_deep_research_2026-08-23.md).
- Files prefixed `professional_services_` are **historical validation inputs** for the earlier generic intake/routing hypothesis. They are retained, not current positioning.

### Validation and technical

- [`validation/`](validation/) contains dated, **historical** Markdown reports and valuable JSON evidence snapshots. Rankings are reproducible evidence of earlier runs, not current outreach instructions.
- [Technical debt after market validation](technical/technical_debt_after_market_validation.md).

## Next action

Review the five LinkedIn connection requests already sent and wait for buyer-reported evidence. Record an acceptance, reply, or discovery outcome when it actually occurs.

Until new buyer evidence exists: **NO BUILD**.
