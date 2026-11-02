---
description: "Foundry lab context and boundaries for guided engineering."
---

# Foundry Multi-Agent Lab

* Use the [knowledge base](../docs/README.md) and
  [source register](../docs/research/sources.md), checking current sources
  before decisions that depend on APIs, previews, quotas, or regions.
* The [demo use case](../docs/demo/use-case.md) is a proposal, not an
  approved requirement. Do not automatically adopt it for a new project.
* APIM and paths that require it are out of scope unless an explicit
  scope change is agreed with the user.
* For guided work, use the
  [Foundry AI Engineer](agents/foundry-ai-engineer.agent.md) role. Do not
  turn an analysis request, an approved plan, or general appreciation
  into authorization to implement or deploy.
* The tracking requested by the user belongs in
  [.copilot-tracking](../.copilot-tracking/README.md). Do not invent answers,
  approvals, or results, and do not overwrite decision history.
* Keep repository documents in English. Respond in English by default
  unless the user explicitly requests another language. Clearly label
  translations of historical user answers instead of presenting them
  as verbatim quotations.
* Do not put secrets, complete transcripts, or real data in tracking.
  Development agents are not the runtime agents of the Foundry solution.
