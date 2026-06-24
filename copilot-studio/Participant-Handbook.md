# M+AI+CE Hackathon — Participant Handbook
### Build an AI agent with Microsoft Copilot Studio

Welcome! Over the next few weeks you'll build a working AI agent in **Microsoft Copilot Studio** that solves a real Mace problem. No deep coding required — if you can describe a process and write a clear instruction, you can build an agent.

This handbook is everything you need: the challenge, how to set up, what "good" looks like at each tier, the rules, and how you'll be judged. Keep the companion **Getting Started with Copilot Studio** guide open while you build.

---

## 1. The challenge

> **Build a Copilot Studio agent that solves a genuine Mace pain point.**

It's an **open brief** — pick a problem you or your team actually face. The best entries solve something real, not something invented for the hackathon.

**Example problem spaces** (inspiration, not a checklist):
- **Document & standards compliance** — an agent that answers questions about a standard or checks a document against it.
- **RFI / query triage** — an agent that takes an incoming query, classifies it, and routes or answers it.
- **Bid & proposal assistant** — drafts boilerplate, finds reusable content, answers "what do we usually say about X?"
- **Onboarding & policy Q&A** — a new-starter or policy assistant grounded in the right documents.
- **Health & safety guidance** — an agent that answers H&S questions from approved sources.
- **Programme knowledge agent** — a single place to ask questions about a programme's documents and processes.

Pick something with a clear user and a clear "before/after." If a colleague would say *"I'd use that"* — you've got a good idea.

---

## 2. What you'll actually do

You'll **build and demonstrate** your agent inside Copilot Studio. 

> **Important:** This hackathon is **build-only — you will not publish your agent.** We don't currently hold the licences to deploy to Teams, websites, or other channels. That's by design and it's completely fine: **you'll demo live in the Copilot Studio Test pane**, which shows your agent working end-to-end. Nothing goes live, and no data leaves Mace's environment.

If the judges see something worth taking further, the follow-on decision about licences and deployment is for the business — your job is to prove the value.

---

## 3. Getting set up

1. You'll build in a **free Copilot Studio trial or a Power Platform developer environment**. The organisers will tell you the exact, approved sign-in route — **use that one** (don't create random tenants or use production).
2. Sign in with the account the organisers specify and open Copilot Studio.
3. Follow the **Getting Started with Copilot Studio** guide (companion document) to create your first agent in about 15 minutes.

**Teams:** 2–4 people. Mixed skills welcome — a process expert + someone who likes building is a great combination.

---

## 4. The build tiers

Three tiers, so everyone can take part and finish with something they're proud of. **Aim for the tier that's realistic for your team — a polished Bronze beats a broken Gold.** Full tickable checklists are in Section 5.

| Tier | In one line |
|------|-------------|
| 🥉 **Bronze** | A **knowledge-grounded agent** that answers accurately from Mace documents you give it. |
| 🥈 **Silver** | Bronze **plus** custom logic — the agent captures input and performs a real check, decision or routing in a natural conversation. |
| 🥇 **Gold** | Silver **plus** it's **connected** — calls a Power Automate flow / connector / action, does multi-step work, and reads or writes data. |

---

## 5. Tier checklists

### 🥉 Bronze — Knowledge-grounded agent
- [ ] Agent created with a clear **name and description** aimed at a real Mace problem
- [ ] At least **one knowledge source** added (uploaded documents, a SharePoint site, or a website)
- [ ] Agent gives **accurate, grounded answers** from that knowledge (with citations where available)
- [ ] At least **two custom topics** with sensible trigger phrases (e.g. a guided "help me with…" path)
- [ ] A clear **greeting / "what I can help with"** opening and a sensible **fallback** for unknown questions
- [ ] Works end-to-end in the **Test pane**

### 🥈 Silver — Workflow agent *(everything in Bronze, plus)*
- [ ] **Captures user input** with questions, entities and variables, and uses it later in the conversation
- [ ] At least one topic performs a **real check, decision or routing** (e.g. validate a value, branch on conditions, triage a request)
- [ ] Generative answers are grounded in Mace docs with **clear agent instructions** (good system prompt)
- [ ] Handles **unhappy paths** gracefully (missing info, "I don't know", off-topic questions)
- [ ] The conversation **feels natural**, not just a rigid menu

### 🥇 Gold — Connected agent *(everything in Silver, plus)*
- [ ] Calls an **action** — a Power Automate flow, a connector, or a custom/REST action
- [ ] **Multi-step orchestration** — the agent chains topics/actions, or uses generative orchestration to choose them
- [ ] **Reads or writes data** somewhere (Dataverse, SharePoint, Excel, an API) — sample/dev data is fine
- [ ] **Robust error handling** on the action (no result, timeout, failure → a sensible message, not a crash)
- [ ] A short note on **how it could be operationalised** (what licences / connections a live version would need)

---

## 6. How you'll be judged

| Criterion | Weight | What we're looking for |
|-----------|:------:|------------------------|
| **Functionality** | 40% | Does it work, and does it actually solve the problem? |
| **Innovation** | 30% | Originality and ambition of the idea. |
| **Build quality & reusability** | 20% | Is it well-built? Could Mace genuinely use it? |
| **Presentation** | 10% | A clear, confident demo and pitch. |

Judging is on a **live demo in the Copilot Studio Test pane**. Tier matters less than impact — a brilliantly useful Bronze can beat a half-working Gold.

---

## 7. The rules

- **Original work** — build it during the hackathon. Bringing existing documents/knowledge to ground your agent is encouraged.
- **Use sample or non-sensitive data only.** Do **not** put confidential, personal, or client-restricted Mace data into trial/dev environments. If in doubt, anonymise it or make up realistic examples.
- **Stay in the approved environment** the organisers give you. No production tenants.
- **Build-only** — you're not publishing. Demo in the Test pane.
- **Version control is optional.** If your team wants a backup or history, you can **export your agent as a Power Platform solution (.zip)** and commit it to Git — but it's not required and not marked.
- **Ask for help** — using the community channel and office hours is encouraged, not cheating.

---

## 8. Timeline

| When | What |
|------|------|
| **Week 0** | Launch, brief, team formation, environment set-up |
| **Weeks 1–2** | Build sprint — with office hours and the community channel |
| **Week 3** | **Demo day** — live demos in the Test pane |
| **Week 3** | Executive showcase + recognition |

*(Exact dates will be confirmed by the organisers.)*

---

## 9. Demo day

- **5-minute live demo** in the Copilot Studio Test pane, followed by a few minutes of Q&A.
- Show the **problem**, then the agent **solving it** in a real conversation — including one "unhappy path" if you can.
- **Tip:** record a short backup screen-capture of your agent working, in case of live gremlins.
- Close with one line on **the impact** if Mace adopted it.

---

## 10. Support

- **Community channel (Teams):** ask questions any time — someone will help.
- **Office hours:** live drop-in sessions during the build sprint (times in the channel).
- **This handbook + the Getting Started guide** answer most setup questions.

---

## 11. FAQ

**Do I need to know how to code?**
No. Copilot Studio is low-code. Bronze and most of Silver need no code at all. Gold may involve a Power Automate flow or connector, but that's still low-code.

**I can't publish my agent — does that hurt my chances?**
Not at all. Everyone is in the same boat. You demo in the Test pane, which shows the full experience.

**Which environment do I use?**
The free trial / developer environment the organisers specify. Don't use a production tenant.

**Can I use real Mace documents and data?**
Use **non-sensitive** material only — public standards, sample documents, anonymised or made-up data. Never confidential or personal data.

**Do we have to use Git?**
No — it's optional. If you want a backup, export your agent as a solution (.zip) and commit it. It isn't judged.

**What if my idea is "too simple"?**
A simple agent that genuinely helps someone is a strong entry. Solve a real problem well.

**How big should the team be?**
2–4 people. Pair a process/subject expert with someone who enjoys building.

---

*Good luck — we can't wait to see what you build.*
*M+AI+CE Hackathon · Mace Digital*
