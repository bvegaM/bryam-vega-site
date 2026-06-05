---
title: "From isolated contracts to orchestrated flows: Arazzo and the future of API governance"
description: "Arazzo bridges the gap between what OpenAPI documents and how APIs are actually used in production: business flows, inter-call dependencies, and governance over real sequences."
pubDate: 2026-06-04
tags: ["arazzo", "openapi", "api-governance", "workflows", "apidays"]
series: "APIs"
heroImage: "/images/blog/arazzo/arazzo-hero.png"
signature: "Bryam David Vega Moreno is a Senior Consultant at Thoughtworks"
draft: false
---

I had never heard of Arazzo until I attended [Frank Kilcommins](https://www.linkedin.com/in/frank-kilcommins/) session at Apidays New York 2026. Frank is one of the most active contributors at the OpenAPI Initiative, and in that talk he presented **version 1.1.0 of the Arazzo specification**, which among other things adds support for **AsyncAPI** —a step that extends Arazzo's reach beyond HTTP flows into event-driven architectures.

What hooked me wasn't the technology itself but the problem it solves. At some point in the talk, a phrase landed that articulated something I had felt but never been able to name: **the problem isn't that we don't have good API contracts; the problem is that contracts don't talk to each other.**

OpenAPI describes endpoints beautifully. It tells you what parameters a `POST /orders` accepts, what it responds, what errors it can return. But it says nothing about what happens **before** or **after**. It doesn't capture that you first need to authenticate, then search for the product, then add it to the cart, and only then create the order. That logic lives in developers' heads, in integration tests nobody reads, or worse: nowhere at all.

I left that talk wanting to understand Arazzo deeply. This article is the result of that research —and also a personal bet on giving more visibility to a standard I believe deserves a place in the conversation of any team working on API governance.

---

## The problem everyone has, but few can name

Think of the last time you integrated an API from a third party or another team. The OpenAPI contract was there. You could see the endpoints, the models, the error codes. And yet you still needed to:

- Read the narrative documentation to understand the order of calls.
- Ask someone on the producer team how the steps chained together.
- Write an integration test from scratch to validate the full flow.
- Repeat that exercise every time the contract changed.

This problem isn't minor in large organizations. At scale, it shows up like this:

**Business knowledge fragmentation.** The OpenAPI contract documents pieces. The real business flow —the sequence that produces value— lives in Slack conversations, outdated wikis, or directly in the consumer's code. When that flow changes, nobody documents it because there's no standard place to do so.

**Expensive and brittle end-to-end testing.** To test a real flow, someone has to build a test harness that chains multiple calls, manages tokens between steps, propagates IDs, and handles errors at intermediate points. That test code gets written once, never goes through governance review, and becomes technical debt.

**No way to detect breaking changes in flows.** OASDiff and similar tools detect incompatible changes in an individual contract. But if the producer renames the `orderId` field in the `POST /orders` response —the same field the consumer needs for the `GET /orders/{id}`— nobody connects the dots. The flow breaks in production.

**Duplication across every consumer.** Every team consuming the same API sequence implements its own version of the flow. If there are ten consumers, there are ten implementations of the same process, with ten different interpretations of what to do when step 2 fails.

---

## What Arazzo is and what it solves

**Arazzo** is an open specification from the [OpenAPI Initiative](https://www.openapis.org/) that lets you describe **workflows**: orchestrated sequences of API calls, with their dependencies, the data flow between steps, and the conditions for success or failure.

The core idea is simple: if OpenAPI describes the "what" of each endpoint, Arazzo describes the "how" of the flows that connect them.

Concretely, Arazzo solves problems that no individual OpenAPI can address:

- **Data flow between steps** — propagates outputs from one step as inputs to the next without the consumer having to infer it.
- **Explicit success criteria** — each step defines what response makes it valid, including business conditions (not just the HTTP status code).
- **Actions on success or failure** — the flow declares what to do if a step fails: retry, jump to another workflow, or abort with a specific output.
- **Multi-API orchestration** — a single file can reference contracts from multiple services and connect them in a coherent sequence.
- **Documented authentication flow** — the token is obtained in one step and reused in the following ones; no more guessing.
- **Reusable components** — common parameters, inputs, and actions are defined once and referenced from any workflow in the file.

<figure>
  <img src="/images/blog/arazzo/arazzo-structure.png" alt="Arazzo specification structure" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;" />
  <figcaption>Arazzo specification structure. Source: <a href="https://github.com/OAI/Arazzo-Specification/raw/main/images/Arazzo-Specification-Structure.png" target="_blank" rel="noopener">OAI/Arazzo-Specification</a></figcaption>
</figure>

The diagram summarizes the blocks that make up an Arazzo file and how they relate to each other:

**`info`** — File metadata: title, version, description. The same pattern you already know from OpenAPI.

**`sourceDescriptions`** — The list of external contracts this workflow will invoke. Each entry points to an OpenAPI or AsyncAPI file and assigns it a local name that steps will use to reference it. It's the bridge between the flow and the individual contracts.

**`workflow` (\*)** — The heart of the specification. There can be one or several workflows in the same file. Each workflow defines:
- `inputs` — The schema of the input data the workflow accepts as a starting point.
- `parameters` — Global parameters applicable to all steps in the workflow.
- `success actions` / `failure actions` — What to do when the workflow completes successfully or fails: redirect, execute another workflow, emit an output.
- `outputs` — The values the workflow exposes to the outside once completed.
- **`step` (\*)** — Each individual call within the workflow. A step can invoke an operation from a `sourceDescription` via `operationId`, or invoke another workflow in the same file via `workflowId`. This second option is key for modeling layers: a BFF workflow orchestrates high-level steps and delegates to a BL workflow containing the business logic. The BFF calls the BL as if it were just another step, receives its `outputs`, and continues. Each step has its own `parameters`, `successCriteria`, `success actions`, `failure actions`, and `outputs` that subsequent steps can consume.

**`components`** — Section to define reusable elements: `inputs`, `parameters`, `success actions`, and `failure actions` that can be referenced from multiple workflows or steps, avoiding repetition.

**`Criterion` / `Selector`** — The types that model success conditions: expressions that evaluate the HTTP status code, response body fields, or any JSONPath or XPath expression over a step's result.

**`Expression Type Object`** — The expression system that enables propagating data between steps using references like `$steps.login.outputs.token` or `$inputs.productId`.

**`Reusable Object`** — The reference mechanism (`$ref`) for pointing to elements defined in `components`.

---

## What Arazzo makes possible that wasn't before

With an Arazzo file as the source of truth, several things change:

**Flow documentation as a first-class artifact.** The flow is no longer a diagram in Confluence or a paragraph in the README. It's a versioned file, reviewable in a pull request, with the same lifecycle as the OpenAPI contract.

**Integration testing generated from the specification.** An Arazzo file defines the flow with enough precision to execute it directly against a real API or a mock, without anyone writing the test code from scratch. The flow is the test.

**Breaking change detection in sequences.** If the `id` field in the `POST /orders` response gets renamed to `orderId`, and that field is referenced in the next Arazzo step as `$steps.create-order.outputs.orderId`, the toolchain can detect that the flow is broken —not just that the individual contract changed.

**Reuse across consumers.** A producer team can publish the Arazzo alongside their OpenAPI. All consumers start from the same canonical flow. If the flow changes, it changes in one place.

---

## Demo: a credit card system with Arazzo

To make all of this concrete, I built a public GitLab repository that implements the workflows of a financial loyalty system:

**[api-labs1/api-arazzo/api-workflows](https://gitlab.com/api-labs1/api-arazzo/api-workflows)**

### The architecture

The system has two services, each with its own OpenAPI contract:

- **BFF Loyalty Financial** — the external layer the frontend consumes. Exposes the card, benefits, and discounts endpoints.
- **BL Loyalty Financial** — the internal database layer. The BFF calls it to fulfill each consumer request.

The Arazzo file defines **eight workflows** organized into three groups:

| Group | Client | Workflows |
|-------|--------|-----------|
| Consumer Journeys | Frontend | Cards → benefits · Cards → discounts |
| Consumer Workflows | Frontend | Get cards · Get benefits · Get discounts |
| BFF Internal | BFF | Delegate cards to BL · Delegate benefits · Delegate discounts |

The `sourceDescriptions` connects both contracts to the same Arazzo file:

```yaml
sourceDescriptions:
  - name: bff-loyalty-financial-information
    url: ../openapi/bff-loyalty-financial-information.yaml
    type: openapi
  - name: bl-loyalty-financial-information
    url: ../openapi/bl-loyalty-financial-information.yaml
    type: openapi
```

### The two consumer journeys

The most interesting workflows are the consumer journeys: two-step flows where the `card_id` extracted from the first step is automatically propagated to the second, without the consumer having to provide it explicitly.

**Flow 1 — cards → benefits**

```yaml
- workflowId: consumer-browse-card-benefits
  steps:
    - stepId: get-credit-cards
      operationId: bff-loyalty-financial-information.getCustomerCreditCards
      successCriteria:
        - condition: $statusCode == 200
          type: simple
      onFailure:
        - name: get-credit-cards-failed
          type: end
      outputs:
        first_card_id: $response.body#/credit_cards/0/card_id  # extracts the ID from step one

    - stepId: get-benefits-for-selected-card
      dependsOn:
        - get-credit-cards
      operationId: bff-loyalty-financial-information.getCardBenefits
      parameters:
        - name: card_id
          in: path
          value: $steps.get-credit-cards.outputs.first_card_id  # uses it here
      successCriteria:
        - condition: $statusCode == 200
          type: simple
      outputs:
        benefits: $response.body#/benefits

  outputs:
    card_id: $steps.get-credit-cards.outputs.first_card_id
    benefits: $steps.get-benefits-for-selected-card.outputs.benefits
```

**Flow 2 — cards → discounts**

The second journey is structurally identical in the first step. Only the second step's operation changes:

```yaml
- workflowId: consumer-browse-card-discounts
  steps:
    - stepId: get-credit-cards
      operationId: bff-loyalty-financial-information.getCustomerCreditCards
      outputs:
        first_card_id: $response.body#/credit_cards/0/card_id

    - stepId: get-discounts-for-selected-card
      dependsOn:
        - get-credit-cards
      operationId: bff-loyalty-financial-information.getCardDiscounts
      parameters:
        - name: card_id
          in: path
          value: $steps.get-credit-cards.outputs.first_card_id
      outputs:
        discounts: $response.body#/discounts

  outputs:
    card_id: $steps.get-credit-cards.outputs.first_card_id
    discounts: $steps.get-discounts-for-selected-card.outputs.discounts
```

That repetition of the first step across two different workflows is exactly the pattern that previously existed implicitly in each consumer separately. Arazzo makes it visible and named.

### Retry in the card retrieval workflow

The `consumer-get-credit-cards` workflow —a single step the frontend calls directly— shows how to declare a retry policy without anyone having to implement it in the client:

```yaml
onFailure:
  - name: bff-credit-cards-retry
    type: retry
    retryAfter: 1
    retryLimit: 3
    criteria:
      - condition: $statusCode >= 400
        type: simple
  - name: bff-credit-cards-failed
    type: end
```

Three retries with a one-second wait. The specification declares it; any compatible runtime or testing tool respects it.

### The BFF's internal workflows

The BFF also has its own documented workflows, showing exactly how it delegates each request to the business logic layer:

```yaml
- workflowId: bff-get-credit-cards
  steps:
    - stepId: call-bl-credit-cards
      operationId: bl-loyalty-financial-information.getCreditCardsFromDatabase
      parameters:
        - name: identification_number
          in: query
          value: $inputs.identification_number  # resolved by the BFF from the JWT
```

The `identification_number` is extracted by the BFF from the user's token. Without Arazzo, that logic lives only in the BFF's code and nobody else knows it happens. With Arazzo, it's part of the contract.

---

## Tools that shine alongside Arazzo

While researching, I found three tools that changed how I think about the lifecycle of an Arazzo workflow: one to render it, one to validate it, and one to run and debug it.

### Arazzo UI — visualize the flow as written

[Arazzo UI by Jentic](https://arazzo-ui.jentic.com/) takes your Arazzo file and renders it as an interactive flow diagram: you can see the steps, dependencies, inputs, and outputs, with nothing to install. It's the equivalent of Swagger UI but for workflows.

For teams just adopting Arazzo, this is key: the file stops being abstract YAML and becomes something anyone on the team can read and discuss.

### Spectral — governance over the Arazzo file

[Spectral](https://stoplight.io/open-source/spectral) is the most widely used linting tool in the OpenAPI ecosystem. And it works with Arazzo too.

While exploring the ecosystem, I noticed there was no public Spectral ruleset specifically for Arazzo. So as part of my exploration of this standard, **I created and published one**:

**[api-labs1/api-arazzo/spectral-rules](https://gitlab.com/api-labs1/api-arazzo/spectral-rules)**

The repository contains **116 validation rules** distributed across five rulesets:

| Ruleset | What it validates | Rules |
|---------|------------------|-------|
| **General** | Required fields across all Arazzo objects | 36 |
| **Governance** | Enums, mutual exclusivity, conditional requirements | 34 |
| **Naming** | Identifier patterns and casing conventions | 17 |
| **Expressions** | Runtime expression syntax (`$steps.*`, `$inputs.*`) | 11 |
| **Best Practices** | Opinionated quality recommendations | 18 |

To use it, simply reference the entry point from your own `.spectral.yaml`:

```yaml
extends:
  - "https://gitlab.com/api-labs1/api-arazzo/spectral-rules/-/raw/main/spectral-arazzo.yaml"
```

Then lint:

```bash
spectral lint credit-card-workflow.arazzo.yaml --ruleset .spectral.yaml
```

The repository includes ready-to-use templates for GitHub Actions and GitLab CI. The goal is for Arazzo to have the same level of executable governance we already have for OpenAPI: rules that block merges, not just recommendations in a wiki.

### Arazzo CLI — run and debug workflows locally

[arazzo-cli](https://strefethen.github.io/arazzo-cli/) is a command-line tool that executes Arazzo workflows directly against real APIs. No code generation, no manual Postman configuration.

What it makes possible:

- **Full flow execution** — resolves expressions, evaluates `successCriteria`, propagates outputs between steps.
- **DAG-based scheduling** — steps with no dependencies run in parallel automatically.
- **Detailed traces** — generates `trace.v1.json` artifacts with every request, response, criteria evaluation, and routing decision.
- **Deterministic replay** — re-execute a trace offline to debug without hitting the API again.
- **VS Code extension** — breakpoints, variable inspection, and watch expressions over the workflow.

To install from prebuilt binaries (Linux, macOS, Windows) or from source:

```bash
cargo install --git https://github.com/strefethen/arazzo-cli.git arazzo-cli --locked
```

And run the demo workflow:

```bash
arazzo-cli run credit-card-workflow.arazzo.yaml --workflow consumer-browse-card-benefits
```

The output is structured JSON, ready for CI.

---

## Why this matters for API governance

API governance has been, for years, focused on the individual contract: the OpenAPI that describes a service. That's necessary, but not sufficient.

APIs aren't used in isolation. They're used in sequences. Business value emerges from flows —from the combination of calls that produces a useful result. Documenting and governing only the individual contracts is like documenting a recipe's ingredients but never writing the cooking steps.

Arazzo formalizes the cooking steps.

When flows are first-class artifacts —versioned, reviewable, executable— things happen that don't occur with narrative documentation:

- **Breaking changes in flows are detectable** before they reach production.
- **Consumers start from a canonical source**, not from their own interpretation of the correct order.
- **Integration testing stops being handcrafted** and starts being derived from the specification.
- **Governance covers the sequence**, not just the endpoint.

---

## A young standard, a fast-growing ecosystem

Arazzo 1.0.0 was published by the OpenAPI Initiative in 2024. In less than two years it already has support in Speakeasy, Microcks, Redocly, and Portman.

The path Arazzo is tracing is the same one OpenAPI traveled: going from a team-by-team artisanal practice to a standard that tools understand. When that happens, governance stops being a manual process and becomes something the toolchain can execute.

What I find most promising is precisely that: it's not a vendor tool, it's an open standard. Any team can adopt it without locking into a platform, with the same interoperability advantages that OpenAPI already gave us for individual contracts.

---

## The thread that connects

In [API-First Flowline](/blog/api-first-flowline-ai-driven-spec-to-production/), I argued that API governance requires the OpenAPI contract to **block merges** —to be not just documentation, but a gate in the pipeline. The same logic applies to Arazzo: a flow that lives in a wiki is not governance; a flow that is a versioned artifact, validated in CI, and executed as a contract test, is.

The full picture then is: OpenAPI for contracts, Arazzo for flows, gates in the pipeline for both.

**Isolated contracts document what an API can do. Orchestrated flows document how APIs produce value together. Both need governance. Arazzo gives the second its first standard representation.**
