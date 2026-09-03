# The Illustrated Guide to Using AI
## How Luma Learned to Get Things Done

A simple map for professionals and leaders who need a shared language.

---

Once upon a time there was a little question named Luma.

She was a simple question.
She had one wish and a tiny lantern of curiosity.

She lived in a crowded chat booth, where answers arrived like paper airplanes…
and then blew away.

Every time Luma came back, nobody remembered her.
The booth could talk.
It could not *do*.

Luma wished for a place where questions could grow into work.

---

### The Great Library Lion — LLM

One morning a vast, gentle lion padded out of a library the size of a mountain.
His mane was made of pages.

“Hello, little question. I am Leo,” he said.
“I am a Large Language Model. I have read so many stories that I can help you start almost any one.”

Luma asked for a picnic plan.
Leo wrote a beautiful picnic plan.
Then he sat very still.

The plan was words.
The picnic was not packed.

An LLM is a large language model: a general-purpose thinking engine that reads your words and writes useful words back. It is wonderful at explaining, drafting, summarizing, and planning. By itself, it does not fetch your calendar, open your files, or pack the sandwiches.

---

### The Busy Serving Kitchen — vLLM

Behind Leo’s library was a kitchen that never slept.
An octopus named Vee wore eight oven mitts and danced between stoves.

“Leo is the cook,” said Vee.
“I am the serving kitchen. When many questions arrive at once, I line them up, share the ovens fairly, and send answers out hot.”

Luma watched dozens of lanterns get fed at the same time.
Nobody waited forever.
Nobody burned the soup.

vLLM is a serving kitchen for models you host yourself. It batches many requests and manages memory so one cook can feed a crowd. Most people talking to a frontier model are not in Vee’s kitchen. Those lions are too big for one stove: their layers are spread across four or five huge ships, the recipes are compiled into tensors, and almost no waiters (CPU work) run around between plates. You meet vLLM when you call a cluster that chose that kitchen — not when you open a chat box to a frontier model.

---

### The Pocket Mouse — SLM

A mouse popped from Luma’s pocket.
“I’m Scout,” she squeaked.
“I don’t know every story in the mountain. I know enough for the path right here. I run on a little lamp. I am quick. I am quiet. I can work when the mountain library is far away.”

Luma put Scout on her shoulder.
Some jobs needed the lion.
Some jobs needed the mouse.

A Small Language Model (SLM) is a compact model. It uses less power and memory, often runs on a laptop or phone, and is best at focused everyday tasks. You choose an SLM when “good, fast, and nearby” beats “enormous and far away.”

---

### The Neighborhood Shopkeeper — SDM

On a side street stood a tiny shop with one perfect window.
A raccoon named Dom sold only maps of *this* neighborhood.

“I am a Specialized Domain Model,” said Dom.
“I do not bake cakes. I do not sail ships. Ask me which alley has the bakery, and I will not guess.”

Luma asked about the bakery alley.
Dom answered in one breath.

An SDM is a specialized (or domain) model: trained or tuned for one kind of work — medicine notes, legal clauses, warehouse codes, one company’s voice. Narrow on purpose. Sharp on purpose.

---

### The Backpack — Agents

“Talking is only the first step,” said a kind captain at the harbor.
Captain Context wore a coat of pockets.

“If you want the picnic to happen, you must become an Agent.”

Captain Context buckled a backpack onto Luma.
Inside were tools: a key, a pencil, a looking-glass, a tiny boat.

“An agent does not only answer,” said the captain.
“An agent *acts*. It may look something up, write a file, send a note, check the result, and try again.”

Luma stood taller.
She was still a question.
Now she was a question that could work.

An AI agent is a model wrapped in permission to use tools. It plans a step, does the step, sees what happened, and continues until the job is done or it must ask a human.

---

### The Harbor Crew — Supervisors and Crews

On a bigger job the captain did not send Luma alone.
He climbed onto a crate marked SUPERVISOR and pointed.

“One backpack can pack a basket,” he said.
“A picnic for the whole dock needs a crew. I assign. I check. I stop the work when it is good enough. You do not let every lantern invent the plan.”

A mouse checked the list.
A raccoon read the map.
A sparrow wrote the invitation.
Luma held the lantern.

Teams usually work this way: a supervisor (sometimes called a boss or orchestrator) directs specialist agents. A crew is not a pile of chat windows. It is a small company with a captain.

---

### The Recipe Shelf — Skills

In the harbor workshop stood a shelf of slim folders.
Each folder had a name on the spine:
*How to Pack a Picnic.*
*How to Write a Kind Letter.*
*How to Check a List Twice.*

“These are Skills,” said Scout.
“You do not memorize every recipe. You open the right folder when the job matches.”

Luma opened *How to Pack a Picnic.*
It told her the order: check weather, pick food, pack cold things last, leave a note.

Skills are reusable playbooks for agents — short instructions, checklists, and sometimes little scripts. The agent loads a skill when the task matches, instead of inventing the procedure from scratch every time.

---

### The Safety Rigging — Harnesses

The harbor wind grew strong.
Captain Context clipped Luma into a climbing harness of soft ropes, bells, and clips.

“This is the Harness,” said the captain.
“It holds your tools. It watches your steps. It keeps notes. It stops you at the cliff edge. The lion is strong. The harness keeps the strength useful.”

The bells rang if Luma wandered.
The ropes brought her back to the dock.

A harness is the runtime around an agent: the loop runner, the tool permissions, the logs, the tests, the memory, the budgets, and the stop rules. A model without a harness is a conversation. A model with a harness can finish work.

---

### The Universal Dock — MCP

Along the pier were sockets of every color.
A calendar plug.
A mailbox plug.
A map plug.
A toolbox plug.

A sign read: **MCP — Model Context Protocol**
Underneath, in smaller letters: *the polite way to plug things in.*

“Before MCP,” said Vee, “every tool spoke a private language.”
“Now a dock is a dock. Clip in. The agent can see what the tool can do.”

Luma plugged the picnic calendar into the dock.
The dock introduced itself: *I can read events. I can add events.*

MCP is an open standard that lets models talk to tools and data sources through one kind of connection. Instead of a custom adapter for every app, an MCP server offers tools and resources in a shared shape.

---

### The Garden Path — Loops

Behind the workshop was a round garden path with four stones:

1. THINK
2. ACT
3. LOOK
4. AGAIN

Luma walked it with her picnic.

THINK: I need apples.
ACT: She used a tool to check the pantry.
LOOK: No apples.
AGAIN: She walked to Dom’s street, then packed the basket.

Around and around, not forever — until the basket was ready, or the harness rang the dinner bell.

A loop is the heartbeat of an agent. The model reasons, calls a tool, observes the result, and decides the next step. Loop engineering is deciding when to continue, when to retry, when to ask a person, and when to stop.

---

### Other Friends at the Harbor

**Context Window** — Luma’s satchel. It only holds so many pages at once. When it is full, old pages must be folded away. When satchels grew to about 200,000 pages, stuffing a few fetched scraps in first became less useful than just looking things up.

**Memory** — jars of glowing beads on a shelf. Some beads last for one afternoon. Some last for seasons.

**Vector store** — a map cabinet on the dock. You keep notes nearby and search them directly. The old pelican trick (RAG) made you fetch pages with the *same* embedding the model used to tokenize, which was fussy and is largely left behind.

**Tools** — hammers, keys, and looking-glasses. Skills teach *how*. Tools *do*.

**Guardrails** — a painted fence along the cliff. Kind, firm, not optional.

**Human-in-the-loop** — a grown-up on the dock. For big choices, Luma waves. The grown-up waves back.

**Crews** — other lanterns with their own backpacks, plus a supervisor who assigns and checks. One packs food. One checks the weather. One writes the invitation.

---

### Home

Together they packed the picnic.
Leo helped with the poem on the invitation.
Vee served everyone quickly.
Scout kept the list on Luma’s shoulder.
Dom pointed to the bakery alley.
Skills kept the order of operations.
The harness kept the path safe.
MCP plugged in the calendar.
The loop walked until the work was done.

Luma still asked questions.
Now her questions could grow into days that actually happened.

Luma had found her harbor.

And she lived usefully ever after.

The end.
