---
title: "SkDD: When the Skill Transcends the Spec"
description: "A methodology that emerged from real team experience — and how it extends Spec-Driven Development rather than replacing it."
pubDate: 2026-05-02
tags: ["skdd", "ai-engineering", "methodology", "team-architecture"]
series: "Skill-Driven Development"
heroImage: "/images/blog/skdd/skdd_phases.svg"
draft: false
---


## It Started With a Jira Board

At some point, my team stopped writing specs for certain tasks.

Not intentionally. There was no meeting where someone said "let's drop the spec here." It happened organically. We had started with Spec-Driven Development (SDD) — defining requirements, writing structured markdown specs, feeding them to the AI coding agent. The process worked. But for a specific category of tasks — repetitive, well-understood, technical — we noticed something: nobody was reading the spec afterward. The agent consumed it once, generated the code, and the spec sat static, never updated, never referenced again.

So we stopped writing them.

Instead, we started writing `SKILL.md` files. Instructions. Reusable, executable, callable by any agent in any session. Document generation. API process creation. Vulnerability detection. The output was the same. The friction was gone.

That was the moment I realized we had shifted methodologies without naming the shift.

Here's the uncomfortable truth I'll come back to: **if your team already knows how to do something, writing a spec just so the AI understands it isn't planning. It's ceremonial bureaucracy.**

---

## Someone Else Was Observing the Same Thing

In March 2026, Zak El Fassi published an article formalizing exactly this pattern. He called it **SkDD — Skills-Driven Development**. He arrived at it from his own experience as an indie builder, watching capabilities accumulate in his repo over time. He had to rename it from SDD because Spec-Driven Development already claimed that acronym.

The rename is accurate. The `sk-` prefix is everywhere: `sk-ant-` API keys, `SKILL.md` files, `skillforge` invocations. The methodology is named after its own primitive.

I had observed the same pattern from a different angle — a backend architecture team, not a solo builder. Two independent paths to the same insight. That kind of convergence means something: this isn't a personal preference or a tool quirk. It's a real shift in how teams work with AI agents.

Zak explores SkDD from the lens of individual productivity and capability accumulation. This post explores it from the lens of a team — where the questions that emerge are slightly different: *when* does SkDD shine, *when* does something else serve better, and *what structure does a team need to apply it well?*

---

## What SkDD Actually Is

SkDD has one core primitive: the `SKILL.md` file. A plain markdown document that encodes not *what you want*, but *what you know how to do*. Any agent that reads files can execute it. It persists across sessions, models, and codebases.

The methodology has one governing question:

> *Should this become a Skill?*

If yes — you capture it. If no — you build and move on.

What accumulates over time is not documentation. Not specs. **Capability.** The repo becomes progressively more capable because every repeated process gets codified into something reusable.

As Zak puts it: *"Specification is ephemeral. Skills are durable."*

Zak describes three types of skills:
- **Operational** — callable, discrete, reusable. Does one thing well.
- **Meta** — creates other skills. A toolmaker that makes toolmakers.
- **Composed** — chains multiple skills into a pipeline that is itself a skill.

These types nest freely. A composed skill can invoke a meta-skill mid-run. The compounding is real.

---

## SkDD as a Methodology With Phases

What the team experience added to the pattern was structure: **SkDD with explicit phases**.

SDD has them. The spec-kit workflow from GitHub defines it clearly:

**Specify → Plan → Tasks → Implement**

Each phase produces an artifact that constrains and guides the next. There's a chain of accountability from intent to implementation. Human review at each checkpoint ensures alignment.

SkDD deserves the same rigor. From real team experience, the natural flow is:

![SkDD Five Phases](/images/blog/skdd/skdd_phases.svg)

**1. Observe**
Recognize that a process is repetitive, well-understood, and doesn't require business definition. This is the most important phase — and the one most likely to be skipped.

**2. Capture**
Write the `SKILL.md`. Encode what you know how to do, not what you want to happen. Instructions, context, expected output.

**3. Execute**
The agent invokes the skill. The process runs without rebuilding context from scratch.

**4. Refine**
The skill improves with each execution. Edge cases get handled. Instructions sharpen. The team's collective knowledge crystallizes.

**5. Compose**
Skills invoke other skills. Pipelines form. A vulnerability scanner feeds a remediation skill. A documentation skill feeds a review skill. The system becomes more capable than any individual skill.

---

## The Danger of Skipping Phase One

Tools like `skill-creator` can generate a `SKILL.md` automatically. That sounds like acceleration. In practice, it's a risk.

`skill-creator` jumps directly to **Capture**. It skips **Observe** entirely. No one has decided whether this process *deserves* to be a skill. No one has asked: is this truly repetitive? Is it well-understood enough to codify? Does it add to the repo's capability or just its noise?

The result is **skill sprawl** — a repository full of skills nobody requested, duplicating each other, encoding processes that weren't ready to be skills yet.

![Skill Sprawl vs Curated Skills](/images/blog/skdd/skill_sprawl.svg)

The most important phase in SkDD is not Capture. It's **Observe**. It's the moment of human judgment that decides whether something earns the right to be codified. Remove that phase and you remove the intelligence from the methodology.

---

## Where SkDD Shines

SkDD is the right choice when:

- The process is **repetitive** — it will run again, probably many times
- The process is **instructive** — it can be encoded as clear steps without ambiguity
- The process doesn't require **business definition** — no stakeholder needs to decide *what* should happen before the agent starts
- The skill is **autonomous** — it doesn't depend on external contracts or cross-team agreements

Documentation generation. Test scaffolding. Vulnerability scanning. API boilerplate creation. Code migration pipelines. These are SkDD territory.

---

## A Concrete Example: API-First Endpoint Creation

Let me walk through a real case.

In an API-First team, every new endpoint follows the same path: a stakeholder describes what they need, the team creates the contract in OpenAPI, validates it against Spectral rules, and checks for breaking changes. Repeat for every endpoint.

**With spec-kit** — one of the most widely adopted SDD workflows — this process started with a `constitution.md`: defining structure, constraints, and validation rules before the agent could start. The problem: Spectral already had those rules. The constitution was re-declaring what the toolchain already knew. The process was verbose for something the toolchain had already resolved.

Here's what the same process looks like through the five SkDD phases:

![SkDD API-First Endpoint Example](/images/blog/skdd/skdd_api_example.svg)

**1. Observe**
The team notices that every new endpoint follows the exact same pattern. Same Spectral rules. Same structure. Same validation flow. Nobody is making a new business decision each time — they're executing the same process repeatedly. That recognition is the signal: *this deserves to be a skill.*

**2. Capture**
A `SKILL.md` gets written. It encodes the instructions: take the endpoint description, generate the OpenAPI contract entry, validate against Spectral rules, verify for breaking changes. No constitution. No ceremony. Just instructions the agent can follow every time.

**3. Execute**
The stakeholder describes what they need — maybe in a simple `.md` file, maybe in a single message. The skill takes it from there. The contract gets created, validated, and checked. What used to be Specify → Plan → Tasks → Implement is now one invocation.

**4. Refine**
Over time, the skill sharpens. A new Spectral rule gets added. A versioning edge case gets handled. The team's collective knowledge about what a good endpoint looks like crystallizes into the skill itself.

**5. Compose**
The endpoint creation skill chains into others: contract generation feeds a controller scaffolding skill, which feeds an auto-documentation skill. The pipeline builds itself incrementally.

The intent — *"we need an endpoint that does X"* — still comes from the stakeholder. That part doesn't disappear. But the process of turning that intent into a valid, compliant, production-ready contract? That's a skill now. It doesn't need a spec every time.

---

## Where SkDD Needs a Partner

SkDD works best alongside SDD when:

- The process requires **someone to decide what should happen first** — business logic, domain rules, edge case handling that isn't yet understood
- There are **multiple integrations** — each with its own contract, team, and rhythm
- The **intent needs to be visible** to stakeholders outside the repo — auditors, product owners, compliance teams
- The skill would cross an **organizational boundary** — where the output isn't just reused by the same team but consumed by others

In these cases, the skill arrives *after* the spec, not instead of it. Someone has to define what the system should do before the agent can be trusted to do it repeatedly.

---

## The Real Relationship: Not Alternatives, But Phases

This is the claim I want to make clearly:

**SDD and SkDD are not competing methodologies. They are sequential phases of the same build loop.**

SDD answers: *What should this system do, and why?*
SkDD answers: *Now that we know — how do we make sure it runs well every time?*

The **Implement** phase of SDD is often the birthplace of a SkDD skill. Once the spec has defined intent and the first implementation exists, the team now *knows how to do it*. That knowledge can be captured. From that point forward, repetition is handled by the skill — not by re-specifying from scratch.

| | SDD | SkDD |
|---|---|---|
| **Starting point** | Intent is unclear | Process is understood |
| **Primary artifact** | Specification | SKILL.md |
| **Human role** | Define what should happen | Decide if it deserves a skill |
| **Value** | Alignment across stakeholders | Accumulated capability |
| **Risk** | Drift between spec and code | Skill sprawl without Observe |

![SDD vs SkDD Decision Flow](/images/blog/skdd/sdd_vs_skdd.svg)

---

## A Practical Guide: Which One Do You Need?

Ask yourself one question before starting any task:

> *Does someone need to decide what this should do before the agent starts?*

**Yes** → Start with SDD. Write the spec. Define intent. Get alignment. Then, once implemented, ask if it deserves to become a skill.

**No** → Start with SkDD. Observe. Capture. Execute. Refine. Compose.

The mistake teams make is applying SDD to everything out of habit, and applying SkDD to everything out of speed. Both are wrong. The methodology should match the nature of the work.

---

## Why This Matters Now

We're in a moment where AI agents can execute almost anything — if you tell them how. The bottleneck is no longer execution. It's *judgment*: knowing what to codify, when to define intent explicitly, and when to trust that the team already knows enough to just build a skill.

Here's what nobody in SDD circles wants to admit: nobody defines what "simple" actually means. And while nobody defines it, teams end up writing three-hour specs for repetitive processes they've already solved a hundred times — specs nobody will read again, that only existed to birth the code, and then die in the repo.

SkDD isn't a replacement for thinking. It's a way to make sure that when your team thinks through something once, you never have to think through it again. The spec doesn't disappear — it just stops being the answer to every question.

Use SDD when the work demands it. Use SkDD when the work doesn't.

The methodology should match the nature of the work, not the other way around.

---

*Bryam David Vega Moreno is a Senior Consultant at Thoughtworks*
