---
title: "SkDD: When the Skill Transcends the Spec"
description: "A methodology that emerged from real team experience — and how it extends Spec-Driven Development rather than replacing it."
pubDate: 2026-05-02
tags: ["skdd", "ai-engineering", "methodology", "team-architecture"]
series: "IA"
heroImage: "/images/blog/skdd/skdd_phases.svg"
draft: false
---


## It Started With a Jira Board

The first visible shift happened on a Jira card for a new internal endpoint.

The ticket was straightforward: add an OpenAPI contract entry, run Spectral validation, and check for breaking changes. Normally that would begin with a fresh spec. This time, someone wrote a `SKILL.md` with the exact workflow instead. The agent ran it, the output was correct, and the team moved on.

That ticket made visible something that had been forming for weeks. There was no meeting where someone said "let's drop the spec here." It happened organically.

We had started with Spec-Driven Development (SDD): defining requirements, writing structured markdown specs, feeding them to the AI coding agent. The process worked. For a specific slice of work — repetitive, well understood, technical — we noticed something else: nobody was reading the spec afterward. The agent consumed it once, generated the code, and the spec stayed static: never updated, never referenced again.

When someone proposed dropping the spec for these cases, the pushback was real. Specs are traceability. Specs are onboarding. Specs are what you show an auditor. All legitimate concerns. What we landed on, after enough rounds of disagreement, was simple: the trace does not disappear; it changes form. Instead of a `spec.md` that describes what we want, we write a `SKILL.md` that encodes what we know how to do. The skill *is* the artifact. If a new engineer wants to see how documentation is produced, they can read the skill. If an audit asks what the agent did, the skill is the record. Traceability survives; ceremony does not.

So we stopped writing specs for that category of work. We started writing `SKILL.md` files instead — instructions that are reusable, executable, and callable by any agent in any session. We applied them to document generation, API boilerplate, vulnerability detection, and similar flows. The output was the same. The friction was gone.

That was the moment I realized we had shifted methodologies without naming the shift.

**The uncomfortable truth:** if your team already knows how to do something, writing a spec solely so the AI can parse it is not planning; it is ceremonial bureaucracy.

---

## Someone Else Was Observing the Same Thing

**SkDD already had a name before I wrote this.** In March 2026, Zak El Fassi published an article formalizing the pattern: **Skills-Driven Development (SkDD)** — how capabilities accumulate in a repo when you treat repeatable know-how as a first-class artifact. He arrived at it as an indie builder, watching his own stack of skills grow. He had to rename it from SDD because Spec-Driven Development already owned that acronym.

The rename fits. The `sk-` prefix is ubiquitous: `sk-ant-` API keys, `SKILL.md` files, `skillforge` invocations. The methodology is named after its own primitive.

I had observed the same pattern from a different angle — a backend architecture team, not a solo builder. Two independent paths to the same insight. When two unrelated contexts converge on the same structure, it is less likely to be taste or tooling fashion and more likely to reflect how agent-assisted work is actually settling in.

Zak explores SkDD from the perspective of individual productivity and capability accumulation. This post looks at the same idea through a team lens: *when* does SkDD excel, *when* is another approach better, and *what* lightweight structure helps a group apply it without sprawl?

---

## What SkDD Actually Is

SkDD's core primitive is the `SKILL.md` file: a plain markdown document that encodes not *what you want*, but *what you know how to do*. Any agent that can read those files can execute them. They persist across sessions, models, and codebases.

The methodology has one governing question:

> *Should this become a Skill?*

If yes — you capture it. If no — you build and move on.

What accumulates over time is not documentation. Not specs. **Capability** — executable procedure the team can hand to an agent without re-deriving context each time. The repo gets more capable because every repeated process that clears the bar becomes something reusable.

As Zak puts it: *"Specification is ephemeral. Skills are durable."*

That contrast is directionally right, but in teams durability is relative, not absolute. A skill that works for one major version of a framework may need refactoring at the next. What actually endures is the *pattern of capture*: the habit of noticing when repeated work deserves to be codified.

Zak describes three types of skills:
- **Operational** — callable, discrete, reusable. Does one thing well.
- **Meta** — creates other skills. A toolmaker that makes toolmakers.
- **Composed** — chains multiple skills into a pipeline that is itself a skill.

These types nest freely. A composed skill can invoke a meta-skill mid-run. The compounding is real: each layer removes friction for the next run and for the next person who picks up the repo.

---

## The Shape of the Methodology: One Gate, Then a Loop

What the team experience added to the pattern was structure. SDD has it. GitHub's spec-kit spells out a sequence — often **Constitution** (project principles and constraints), then **Specify → Plan → Tasks → Implement**, sometimes with a **Clarify** pass where ambiguity is high. Each phase yields an artifact that constrains the next. Humans review at checkpoints so intent and implementation stay aligned.

SkDD merits the same rigor, but not the same shape. SDD stays linear because intent has to settle before implementation. SkDD is **a gate followed by a loop**: the hard part is deciding what earns codification; everything after that is iteration.

![SkDD Gate and Loop](/images/blog/skdd/skdd_phases.svg)

The gate is **Observe**. Before anything else, someone has to look at a process and decide whether it earns the right to be codified. Is it truly repetitive? Is it well understood enough to encode without ambiguity? Does it require business judgment that is not settled yet? If the answer does not clear the gate, you do not capture it — you build once the SDD way (spec, alignment, implement) and revisit later. A one-off migration with unclear rollback criteria, for example, is a poor first candidate for a skill: the judgment work still lives in people's heads.

If the gate clears, four activities follow in a loop:

**Capture** — write the `SKILL.md`. Encode what you know how to do, not what you want to happen. Instructions, context, expected output.

**Execute** — the agent invokes the skill. The process runs without rebuilding context from scratch.

**Refine** — the skill improves with each execution. Edge cases are handled, instructions sharpen, and the team's collective knowledge crystallizes into the file.

**Compose** — skills invoke other skills. Pipelines form. A vulnerability scanner feeds a remediation skill; a documentation skill feeds a review skill. The system becomes more capable than any single skill — and the team spends less time re-explaining the same glue code.

The loop is mechanical; the gate is judgment. Flatten them into one linear checklist and you quietly delete the most important step.

---

## Why The Gate Matters

Tools like `skill-creator` can generate a `SKILL.md` automatically. That sounds like acceleration. In practice, it is a bypass.

`skill-creator` jumps straight to **Capture**. It assumes the gate has already been cleared. No one has decided whether this process *deserves* to be a skill. No one has asked: is this truly repetitive? Is it well understood enough to codify? Does it add capability or only noise?

The result is **skill sprawl** — a repository full of skills nobody asked for, duplicating each other, encoding processes that were not ready. Over time the skill set becomes a maintenance burden. The ratio of useful skills to noise drops. Engineers stop trusting the registry. The methodology that was supposed to compound capability starts compounding mess instead. Without the gate, who is accountable for saying "no" to the next auto-generated file?

![Skill Sprawl vs Curated Skills](/images/blog/skdd/skill_sprawl.svg)

The gate prevents that. It is the moment of human judgment that decides whether something earns codification. Remove it and you strip the intelligence from the methodology.

---

## Keeping the Gate Honest: Team Structure Around Skills

The gate relies on human judgment, so it scales the way judgment scales: through ownership and lightweight process, not gut feel alone. A few practices keep it honest at team scale.

**Each skill needs explicit ownership.** The simplest model mirrors `CODEOWNERS`: one primary owner accountable for correctness and one backup for continuity. Without that, skills drift into everyone's-and-no-one's territory — and stale skills erode trust in the whole catalog the same way stale specs do.

**Review needs criteria, not just approval.** A skill review should ask: is the process actually repetitive, are the preconditions explicit, are the outputs testable, and does this duplicate an existing skill? That keeps the catalog curated instead of turning into a second pile of abandoned docs.

**Approval levels should match operational risk.** For low-risk internal automation, senior engineer review suffices. For skills that touch compliance, contracts, or cross-team interfaces, include the relevant domain owner before merge.

**When the gate is contested, default to repetition.** Two senior engineers can reasonably disagree on whether something deserves a skill now or later. The lightweight rule that worked for us: if the process has repeated at least twice and no new business decision appears on the third run, capture it as a skill and refine from real usage.

SkDD scales when governance stays lightweight yet explicit. The goal is not bureaucracy; it is preserving judgment while capability compounds.

---

## Where SkDD Shines

SkDD is the right choice when:

- The process is **repetitive** — it will run again, probably many times
- The process is **instructive** — it can be encoded as clear steps without ambiguity
- The process does not require **business definition** — no stakeholder must decide *what* should happen (only inputs and constraints are known) before the agent starts
- The skill is **autonomous** — it does not depend on external contracts or cross-team agreements

Documentation generation. Test scaffolding. Vulnerability scanning. API boilerplate creation. Code migration pipelines. These are SkDD territory.

---

## A Concrete Example: API-First Endpoint Creation

Let me walk through a real case.

In an API-First team, every new endpoint follows the same path: a stakeholder describes what they need, the team creates the contract in OpenAPI, validates it against Spectral rules, and checks for breaking changes. Same choreography, endpoint after endpoint — yet each ticket is treated like a greenfield design review.

**With spec-kit** — one of the most widely adopted SDD workflows — that process often starts with a `constitution.md`: project-wide constraints, architectural commitments, validation principles. Used well, a constitution captures things no linter can. For a workflow this mechanical — same rules, same structure, same flow — the constitution becomes friction without payoff. Nothing in it crosses a team boundary. Nothing in it requires alignment beyond the team that already wrote the rules. The ceremony is paying for an audience that is not in the room.

Here is the same process through the gate and the loop:

![SkDD API-First Endpoint Example](/images/blog/skdd/skdd_api_example.svg)

**The gate clears (Observe).**
The team notices that every new endpoint follows the exact same pattern. Same Spectral rules. Same structure. Same validation flow. Nobody is making a new business decision each time; they are executing the same process repeatedly. That recognition is the signal: *this deserves to be a skill.*

**Capture.**
A `SKILL.md` gets written. It encodes the instructions: take the endpoint description, generate the OpenAPI contract entry, validate against Spectral rules, verify for breaking changes — steps the agent can follow every time.

**Execute.**
The stakeholder states what they need, perhaps in a small `.md` file or a single message. The skill takes over: create, validate, and check the contract. What used to be Specify → Plan → Tasks → Implement collapses into one invocation.

**Refine.**
Over time, the skill sharpens. A new Spectral rule lands. A versioning edge case gets handled. Retros and code review feed back into the file until "what a good endpoint looks like" is encoded where the next agent will read it.

**Compose.**
The endpoint-creation skill chains into others: contract generation feeds a controller-scaffolding skill, which then feeds an auto-documentation skill. The pipeline grows incrementally.

The intent — *"we need an endpoint that does X"* — still comes from the stakeholder. What changes is how you turn that intent into a valid, compliant, production-ready contract: that path becomes a skill, so you do not owe a full spec cycle on every identical ticket.

---

## Where SkDD Needs a Partner

SkDD works best alongside SDD when:

- The process needs **someone to decide what should happen first** — business logic, domain rules, or edge cases that are not understood yet
- There are **multiple integrations** — each with its own contract, team, and rhythm
- **Intent must be visible** outside the repo — to auditors, product owners, compliance
- The output **crosses an organizational boundary** — consumed by other teams, not only reused inside the squad that wrote the skill

In these cases, the skill arrives *after* the spec, not instead of it. Someone has to define what the system should do before the agent can be trusted to do it on repeat — which is exactly the handoff from SDD-shaped work to SkDD-shaped work.

---

## The Real Relationship: Not Alternatives, But Phases

This is the claim I want to leave you with:

**SDD and SkDD are not competing methodologies. They are sequential phases of the same build loop.**

SDD answers: *What should this system do, and why?*
SkDD answers: *Now that we know, how do we run that well every time without re-litigating the same steps?*

The **Implement** phase of SDD is often the birthplace of a SkDD skill. Once the spec has defined intent and the first implementation exists, the team *knows how to do it*. That knowledge can be captured. From that point forward, repetition is handled by the skill — not by re-specifying from scratch.

| | SDD | SkDD |
|---|---|---|
| **Starting point** | Intent is unclear | Process is understood |
| **Primary artifact** | Specification | SKILL.md |
| **Human role** | Define what should happen | Decide if it deserves a skill |
| **Value** | Alignment across stakeholders | Accumulated capability |
| **Risk** | Specs go stale — written, then orphaned | Skills proliferate — captured without judgment |

![SDD vs SkDD Decision Flow](/images/blog/skdd/sdd_vs_skdd.svg)

---

## A Practical Guide: Which One Do You Need?

Ask yourself one question before starting any task:

> *Does someone need to decide what this should do before the agent starts?*

**Yes** → Start with SDD. Write the spec, define intent, get alignment. After implementation, ask whether it warrants becoming a skill.

**No** → Start with SkDD. Run it through the gate. If it clears: capture, execute, refine, compose.

**Rule of thumb:** if you are reaching for a spec because the template says so, pause. If you are reaching for `skill-creator` because it is fast, pause. Match the method to the work — not the other way around.

The mistake teams make is applying SDD to everything out of habit and SkDD to everything out of speed. Both are wrong.

---

## What This Is Really About

We are at a point where AI agents can execute almost anything, provided they are told how. Execution is rarely the bottleneck anymore. **Judgment** is: what to codify, when to spell intent out in a spec, and when the team already knows enough to encode a skill and move on.

The danger is not picking the wrong methodology. It is skipping the choice. Teams write three-hour specs for work they have solved a hundred times because the workflow expects a spec. Or they point `skill-creator` at every recurring task because that feels like acceleration. Both failures share one root: nobody stopped at the gate to ask whether the work belonged to SDD's territory or SkDD's.

SkDD is not a substitute for thinking. It is a way to ensure that once your team has thought something through properly, you do not have to repeat the same thinking on every identical run. The spec does not disappear; it simply stops being the answer to every question.

Use SDD when the work demands it. Use SkDD when the work does not.

The methodology should match the nature of the work, not the other way around.

---

*Bryam David Vega Moreno is a Senior Consultant at Thoughtworks*
