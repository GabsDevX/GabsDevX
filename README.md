<div align="center">
  <img src="powv-logo.webp" alt="PoWV Protocol" width="560" />
  <br />
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=28&duration=4000&pause=1000&color=22D3EE&center=true&vCenter=true&width=680&height=60&lines=Cyber-Physical+Systems+Architect;Security+%26+Evidence+Engineering;Founder+of+PoWV+Protocol" alt="Cyber-Physical Systems Architect · Security & Evidence Engineering · Founder of PoWV Protocol" width="680" />
</div>

## Gabriel de Almeida Santos Silva

Founder and architect of **PoWV Protocol**. I design and build systems that turn physical events (a weight, a measurement, a custody handover) into attributable, verifiable digital evidence, from the serial port of an industrial instrument to an auditable record.

> A signature can show that a record is intact. It cannot show that the physical event happened as recorded. PoWV keeps those two claims separate, and I design every layer around that distinction.

## Engineering capabilities

| Area | What I have built | Evidence |
| --- | --- | --- |
| **Physical integration** | Serial acquisition from a commercial weighing instrument, host-side normalization, delivery to an ESP32 receiver | [Bench record, Sep 2026](https://github.com/powvprotocol-org/powv-scale-edge-integration/blob/main/docs/integration-module/experimental-record.md) |
| **Applied cryptography** | Edge signing and verification, canonical serialization, hash-chained audit records, Merkle aggregation, key-rotation tooling | [Lab status](https://github.com/powvprotocol-org/powv-lab-status) |
| **Security engineering** | Threat-driven hardening: replay and duplicate control, idempotent delivery, fail-closed verification, tamper detection, evidence admissibility levels | [Nov 2026 engineering update](https://github.com/powvprotocol-org/powv-lab-status/blob/main/status/2026-11-software-engineering-update.md) |
| **Verification & testing** | 343 automated tests in CI on two Python versions; cross-language conformance test vectors | [Nov 2026 engineering update](https://github.com/powvprotocol-org/powv-lab-status/blob/main/status/2026-11-software-engineering-update.md) |
| **Data & backend** | Flask services, durable SQLite audit store, append-only Postgres audit mirror with outbox retry | Private repository, available under NDA |
| **Architecture & governance** | Product architecture, trust boundaries, disclosure policy, IP governance | [Documentation](https://powv-protocol.gitbook.io/powv-protocol-docs/) |

## How the system fits together

```mermaid
flowchart LR
    A["Physical instrument<br/>scale · sensor"] -->|serial capture| B["Edge capture<br/>normalize · identify"]
    B -->|signed evidence| C["Gateway<br/>verify · replay control"]
    C --> D["Audit store<br/>hash chain · Merkle"]
    D --> E["Independent verification<br/>admissibility outcome"]
    E -.->|planned| F["Ledger anchoring<br/>institutional systems"]
```

## Explore PoWV

A map of where things are. Each link goes to the primary record, not a summary.

| If you want to know… | Go to |
| --- | --- |
| **What PoWV is and the problem it addresses** | [Overview](https://powv-protocol.gitbook.io/powv-protocol-docs/overview) · [The Problem](https://powv-protocol.gitbook.io/powv-protocol-docs/the-problem) |
| **How the architecture works** | [Architecture](https://powv-protocol.gitbook.io/powv-protocol-docs/architecture) · [Evidence Model](https://powv-protocol.gitbook.io/powv-protocol-docs/verifiable-evidence/evidence-model) |
| **What has actually been demonstrated** | [Project Status](https://powv-protocol.gitbook.io/powv-protocol-docs/project-status) · [Lab Status records](https://github.com/powvprotocol-org/powv-lab-status) · [Bench record, Sep 2026](https://github.com/powvprotocol-org/powv-scale-edge-integration/blob/main/docs/integration-module/experimental-record.md) |
| **The products and their maturity** | [Product Portfolio](https://powv-protocol.gitbook.io/powv-protocol-docs/product-proposals/) · [Maturity and Availability](https://powv-protocol.gitbook.io/powv-protocol-docs/product-proposals/maturity) |
| **Where PoWV's role ends (RWA, tokenization, custody)** | [Trust Boundaries](https://powv-protocol.gitbook.io/powv-protocol-docs/product-proposals/trust-boundaries) |
| **Use cases and the market test** | [Use Cases](https://powv-protocol.gitbook.io/powv-protocol-docs/use-cases) · [Commercial strategy and candidate pilots](https://github.com/powvprotocol-org/powv-investment-and-governance/blob/main/docs/09-commercial-strategy/README.md) · [Rail sandbox](https://github.com/powvprotocol-org/powv-investment-and-governance/blob/main/docs/09-commercial-strategy/RAIL_SANDBOX.md) |
| **Investment thesis, costs and funding scenarios** | [Investment & Governance](https://github.com/powvprotocol-org/powv-investment-and-governance) · [R&D cost model](https://github.com/powvprotocol-org/powv-investment-and-governance/blob/main/docs/06-financial-model/TECHNOLOGY_CAPITAL_FORMATION.md) · [Capital roadmap](https://github.com/powvprotocol-org/powv-investment-and-governance/blob/main/docs/10-capital-roadmap/README.md) |
| **Economic finality and dispute research** | [Economic Finality & Dispute Governance](https://github.com/powvprotocol-org/protocol-economic-finality) |
| **Security, disclosure and IP** | [Threat Model](https://powv-protocol.gitbook.io/powv-protocol-docs/security/threat-model) · [Disclosure Boundary](https://powv-protocol.gitbook.io/powv-protocol-docs/security/disclosure-boundary) · [IP Policy](https://github.com/powvprotocol-org/powv-governance-and-docs/blob/main/TRADE_SECRET_POLICY.md) · [Report a vulnerability](https://github.com/powvprotocol-org/powv-embedded-security) |
| **Research essays** | [Research & Theses](https://powv-protocol.gitbook.io/powv-protocol-docs/research-and-theses) · [Substack](https://powvprotocol.substack.com/) |

<details>
<summary><strong>How I work</strong></summary>

- **Evidence before claims.** Every public statement links to a dated record, and its limits are written next to the result.
- **Separate what is verified from what is assumed.** Integrity, physical accuracy and key custody are reported as three different things.
- **Fail closed.** Inconsistent or incomplete evidence is held for review, never silently accepted.
- **Reproducibility.** Pinned dependencies, CI on every change, and conformance tests that a second implementation must pass.
- **AI-assisted, human-directed.** I use AI coding tools as accelerators. Architecture, security decisions, review and acceptance remain mine.

</details>

<details>
<summary><strong>Status and roadmap</strong></summary>

| Stage | Status |
| --- | --- |
| Laboratory proof of concept: bench capture and selected software validation (Sep 2026) | Complete |
| Engineering hardening: audit integrity, conformance, admissibility (Nov 2026, experimental) | In progress |
| Physical bench test of the signed capture path | Next |
| Hardware secure element for device identity | Planned |
| Controlled industrial pilot | Planned |

No product is commercially available yet.

</details>

## Stack

<p>
  <img src="https://skillicons.dev/icons?i=python,c,ts,js,react,vite,flask,sqlite,postgres,supabase,linux,git,githubactions,powershell,vscode&perline=15" alt="Python, C, TypeScript, JavaScript, React, Vite, Flask, SQLite, PostgreSQL, Supabase, Linux, Git, GitHub Actions, PowerShell, VS Code" />
</p>

<p>
  <img src="https://img.shields.io/badge/ESP32-E7352C?style=flat-square&logo=espressif&logoColor=white" alt="ESP32" />
  <img src="https://img.shields.io/badge/Serial_instrument_capture-334155?style=flat-square" alt="Serial instrument capture" />
  <img src="https://img.shields.io/badge/Digital_signatures-0F766E?style=flat-square" alt="Digital signatures" />
  <img src="https://img.shields.io/badge/Merkle_trees-334155?style=flat-square" alt="Merkle trees" />
  <img src="https://img.shields.io/badge/Secure_element-planned-6B7280?style=flat-square" alt="Secure element planned" />
</p>

## Activity

<p align="center">
  <img height="160" src="https://github-readme-stats.vercel.app/api?username=GabsDevX&show_icons=true&count_private=true&hide_border=true&theme=github_dark" alt="GitHub stats" />
  <img height="160" src="https://streak-stats.demolab.com?user=GabsDevX&hide_border=true&theme=github-dark-blue" alt="GitHub streak" />
</p>

## Contact

<p>
  <a href="mailto:gabriel@powvprotocol.com"><img src="https://img.shields.io/badge/Email-0F766E?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://www.powvprotocol.com"><img src="https://img.shields.io/badge/Website-18181B?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website" /></a>
  <a href="https://www.linkedin.com/in/gabriel-protocolpowv/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://www.linkedin.com/company/powv-protocol/"><img src="https://img.shields.io/badge/PoWV_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="PoWV Protocol on LinkedIn" /></a>
  <a href="https://www.youtube.com/@GabrielProtocolPowv"><img src="https://img.shields.io/badge/YouTube-DC2626?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" /></a>
  <a href="https://orcid.org/0000-0002-3415-4484"><img src="https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
</p>

**gabriel@powvprotocol.com** · Open to technical walkthroughs, research partnerships and pilot discussions. Confidential material is shared under NDA.

<sub>© 2025–2026 Gabriel de Almeida Santos Silva · PoWV Protocol™ · All rights reserved. Rights holder and IP terms: <a href="https://github.com/powvprotocol-org/powv-governance-and-docs/blob/main/TRADE_SECRET_POLICY.md">Trade Secret and IP Policy</a>.</sub>

<div align="center">
  <img src="https://raw.githubusercontent.com/GabsDevX/GabsDevX/output/github-contribution-grid-snake-dark.svg" alt="Contribution activity" width="100%" />
</div>
