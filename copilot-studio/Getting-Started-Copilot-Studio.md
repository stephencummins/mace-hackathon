# Getting Started with Microsoft Copilot Studio
### A hands-on guide for M+AI+CE Hackathon participants

This walks you from zero to a working agent. You can reach a solid **Bronze** in about 30–45 minutes. Keep this open while you build.

> **A note on labels:** Copilot Studio updates often, so a button might be named slightly differently from what's written here. The *concepts* are stable — look for the nearest equivalent, and ask in the community channel if you're stuck.

---

## Step 1 — Get access (5 min)

1. Go to **copilotstudio.microsoft.com** and sign in with **the account the organisers told you to use**.
2. Start the **free trial** or select the **developer environment** the organisers have set up. *Use the approved route — not a production tenant.*
3. You'll land in the Copilot Studio home page, where your agents live.

> **Don't put confidential or personal data into this environment.** Use public, sample, or anonymised material only.

---

## Step 2 — Create your agent (5 min)

1. Choose **Create** → **New agent**.
2. Give it a **name** and a **description** in plain English — describe its job, e.g. *"Helps Mace staff check whether a document name follows our naming convention, and answers questions about the standard."* Copilot Studio uses this description, so make it specific.
3. Pick the **language** and confirm. Your agent opens in the authoring canvas.

**The canvas has three things you'll use most:**
- **Knowledge** — what the agent knows.
- **Topics** — scripted conversation paths.
- **Actions / Tools** — things the agent can *do* (flows, connectors).
- **Test pane** (usually right-hand side) — chat with your agent live. This is where you'll demo.

---

## Step 3 — Add knowledge (Bronze) (10 min)

This is what makes your agent useful immediately.

1. Open **Knowledge** → **Add knowledge**.
2. Add one or more of:
   - **Upload files** (PDF, Word, etc.) — e.g. a standard, a policy, sample documents.
   - A **SharePoint** site or document library.
   - A **public website**.
3. Wait for it to finish processing.
4. In the **Test pane**, ask a question only your document could answer. You should get a **grounded answer with a citation**.

✅ **Bronze milestone:** your agent answers accurately from your documents.

> **Tip:** Good knowledge beats clever prompting. Curate a few high-quality, relevant documents rather than dumping everything in.

---

## Step 4 — Shape the conversation with topics (Bronze→Silver) (10 min)

**Topics** are conversation paths triggered by what the user says.

1. Open **Topics**. You'll see system topics (Greeting, Fallback, etc.).
2. Edit the **Greeting** so it explains what the agent helps with.
3. **Create a new topic** (e.g. "Check a document name"):
   - Add **trigger phrases** — different ways a user might ask ("check my file name", "is this named correctly?").
   - Add **message** nodes for what the agent says.
   - Add a **Question** node to capture input from the user.

✅ **Bronze milestone (topics):** at least two custom topics with sensible triggers + a clear greeting.

---

## Step 5 — Capture input and add logic (Silver) (15 min)

This is where the agent starts to *do* something.

1. In a topic, add a **Question** node and store the answer in a **variable**. Use **entities** to capture structured things (a number, a date, a choice).
2. Add a **Condition** node to branch on that input — e.g. *if the name matches the pattern → "✅ valid"; otherwise → "⚠️ here's what's wrong."*
3. Use the variable in later messages so the conversation feels personal and responsive.
4. Give your agent good **instructions** (the system prompt / agent instructions area) — tell it its role, tone, and what to do when it doesn't know.

✅ **Silver milestone:** the agent captures input and performs a real check, decision, or routing — and handles "I don't know" gracefully.

> **Tip:** Test the *unhappy paths* — what happens with a blank answer, a weird question, or something off-topic? Judges love an agent that fails gracefully.

---

## Step 6 — Connect an action (Gold) (time varies)

Actions let the agent reach beyond conversation — into data and systems.

1. Open **Actions / Tools** → **Add an action**.
2. Choose one:
   - A **Power Automate flow** you build (e.g. parse a document, look something up, write a row).
   - A **prebuilt connector** (SharePoint, Excel, Dataverse, etc.).
   - A **custom / REST action** if you're comfortable.
3. **Pass variables in** from the conversation and **use what comes back** in the agent's reply.
4. Add **error handling** — what does the agent say if the flow fails, times out, or returns nothing? (Don't let it crash silently.)

✅ **Gold milestone:** the agent calls an action, does multi-step work, reads/writes data, and handles failure cleanly.

> **Tip:** Keep the flow small and reliable. One solid action that works every time beats three flaky ones.

---

## Step 7 — Test, iterate, polish

- Use the **Test pane** constantly — every change, re-test.
- Turn on **conversation tracing** (if available) to see *why* the agent did what it did.
- Tighten your **agent instructions** and **trigger phrases** based on what goes wrong.
- Trim anything that doesn't serve the demo.

---

## Step 8 — (Optional) Save a version with Git

Entirely optional and **not judged** — but if your team wants a backup or history:

1. In the **Power Platform admin / solutions** area, add your agent to a **solution**.
2. **Export the solution** as a `.zip`.
3. Commit that `.zip` to your team's Git repo.

That's your versioned snapshot. (You can re-import it into another environment later.)

---

## Step 9 — Prepare your demo

You're demoing in the **Test pane** — no publishing needed.

- Script a tight **5-minute walkthrough**: the problem → the agent solving it live → one unhappy path → the impact.
- Have **realistic sample inputs** ready to paste.
- **Record a backup** screen-capture in case the live demo misbehaves.
- Practise once against the clock.

---

## Quick troubleshooting

| Problem | Try this |
|---------|----------|
| Agent won't answer from my docs | Check the knowledge source finished processing; ask a question only that doc answers; make sure generative answers are enabled. |
| It ignores my topic | Add more varied trigger phrases; check another topic isn't catching it first. |
| Variable is empty later | Confirm the Question node saved to the variable, and you're referencing the right variable name. |
| Action/flow errors | Test the Power Automate flow on its own first; check inputs match; add an error branch. |
| Answers are vague or wrong | Improve the agent instructions; curate better knowledge; be specific about its role and limits. |

---

## The 30-minute Bronze sprint (if you're short on time)

1. Create agent with a clear description. *(5 min)*
2. Add 2–3 good documents as knowledge. *(10 min)*
3. Test that it answers from them. *(5 min)*
4. Edit the greeting + add one custom topic. *(10 min)*

That's a demoable Bronze. Build up from there.

---

*Stuck? The community channel and office hours are there for exactly this.*
*M+AI+CE Hackathon · Mace Digital*
