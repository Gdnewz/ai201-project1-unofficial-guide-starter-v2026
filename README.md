# The Unofficial Guide

Goodnews (Goody) Idowu — corpus: `campus_life`

---

# Unit 1

## What This Does

I picked the campus_life corpus, which has 88 short posts about one fictional
university that were written by students rather than the administration,
covering admin rules like deadlines and the pass/fail option, workload and exam
notes for nine courses, reviews of each dining hall, and write-ups of each dorm
down to laundry costs and the noise levels. The voice is people informing
everyone what they wish they had known, which is where the Unofficial Guide
name comes from.

My system answers specific factual questions about that campus, for example,
when the deadline to declare a course pass/fail falls or how noisy it gets in
Innisfree Hall. It searches and finds the posts closest to the question, only
answers from them, names the sources, and says it does not have enough
information rather than creating facts when nothing is close enough.

## Chunking Strategy

**Chunk size:** 300 characters (a ceiling, not a fixed width)
**Overlap:** 70 characters

I split on sentence boundaries instead of at a fixed character count. The
documents in `campus_life` are short and written in full sentences, so cutting
through the middle of one leaves a fragment that cannot answer anything. I saw
this clearly in the `advice_threads` corpus. One chunk there held a question
and four replies, and the replies referred back to each other. One of them
reads "Counterpoint, I sold mine." Split per reply, that piece is retrievable
and completely meaningless.

Sentences have whatever length they have, so 300 is a ceiling I accumulate
toward, not an exact size. The chunker adds one sentence at a time and closes
the chunk when the next one would push it past 300. If the leftover tail is
under 170 characters, it gets folded back into the chunk before it. That is
what stops me producing the kind of fragment the starter produces on
`advice_threads`, where a document that did not divide evenly left a 2
character chunk.

For overlap I picked 70 because that is roughly one short sentence. It carries
context across a boundary without duplicating a meaningful share of the chunk.
I first thought about 200, but that is half the ceiling I started with, so
every chunk would be mostly a copy of the one before it, and two near identical
chunks would eat two of my retrieval slots. I also thought about 10, but two
words of carryover protect nothing. I got to 70 by elimination.

**I changed my mind twice while doing this.**

I started with a ceiling of 400, because I had measured what mixing costs.
`housing_old_brewhouse.txt` is 563 characters and covers six different
subjects: the building history, the rooms, its character, the heating, the
laundry, and the noise. I asked two questions about that same building. Laundry
has its own dedicated file and scored 0.211. Heating only exists inside the six
subject file and scored 0.363. That is a gap of 0.152, and that is what a mixed
chunk costs me.

Both answers were still correct, so what I am losing is margin, not
correctness. Margin matters because earlier I asked the same question two
slightly different ways and got 0.593 and 0.601. Those sit on opposite sides of
the 0.6 cutoff, so one was answered and one was refused.

At a ceiling of 400 I got 89 chunks from 88 documents. Only one document
actually split. Five documents split and then got put back together, because
the leftover tail came out under my 170 floor and my fold glued it back on.
That recreates the whole document as one chunk, and that chunk is over the
ceiling. My longest was 513 characters, which breaks my own criterion.

The reason is simple once you see it. A document only slightly longer than the
ceiling leaves a tiny leftover. Worst case, the chunk ends up at about the
ceiling plus the floor.

At 300 I got 97 chunks. Nine documents split, the shortest chunk was 177 and
the longest came down to 420. Three chunks still go over my 400 ceiling.

I also tried 230, since ceiling plus floor would then be exactly 400. That
fixed the top and broke the bottom. The longest dropped to 378, but the
shortest fell to 88, which is well under my floor. The reason is that my fold
only protects the last chunk of a document and never checks the ones in the
middle. With a smaller budget, one long sentence can force a chunk to close
early and nothing catches it.

So I settled on 300. The floor holds at 177, nine documents actually split
instead of one, and only three chunks go over the ceiling. None of the three
settings satisfies both of my bounds, because this algorithm cannot do it. To
fix it properly I would have to merge undersized middle chunks as well as
tails, and I did not do that in this unit. I am writing it down rather than
hiding it, because I set both bounds before I had a chunker and the data showed
me they do not both hold.

## Sample Chunks

Produced by `chunker.py::split_documents` at chunk size 300, overlap 70.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for BIOL 160 Cell Biology

People keep asking so: 9 to 11 hours a week, the heaviest first-year course by reputation. That's real time, not optimistic time. It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 3** — source: `course_math_220_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for MATH 220 Linear Algebra

People keep asking so: 6 to 8 hours a week, almost all of it on problem sets. That's real time, not optimistic time. It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely. Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall_noise.txt#0` — produced by: `chunker.py::split_documents`

```
Noise levels in Innisfree Hall

Asked about this a lot so writing it down. Moderate; the building is l-shaped and the short wing is much quieter. If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.
```

All five of these stand on their own. The reason is that every document in this
corpus starts with a heading line that names its subject, and a heading has no
ending punctuation, so my sentence splitter keeps it attached to the text that
follows. I did not plan that when I wrote the rule, but it is what makes these
chunks answerable. Take the heading off chunk 2 and it reads "9 to 11 hours a
week, the heaviest first-year course by reputation" with no way to tell what
course that is.

Two things I noticed reading them, and both come from the corpus rather than my
code. Chunks 2 and 3 are near duplicates in wording. Both say "People keep
asking so:", both say "That's real time, not optimistic time," and both end
with the same front-loaded sentence. Only the course name and the hours change.
So a general question like "how heavy is the workload?" will match a dozen of
these about equally and fill all five of my slots with near identical text.

Chunk 4 is the weakest of the five. It opens with "Adding to what people have
said about The Ridgeway Café," which leans on a conversation that is not in the
chunk. It still carries hard facts, so it passes, but it is the closest one to
failing.

## Sample Answer

**Question:** can i upgrade my meal plan mid-semester?

**Answer:**

```
  (best distance 0.271, cutoff 0.6)

No, you cannot upgrade your meal plan mid-semester. Meal plan tier changes can
only be made once, during the first ten days of the semester, after which the
plan is locked (admin_meal_plan_changes.txt).

Sources retrieved: admin_meal_plan_changes.txt, dining_verrill_street_grill.txt
```

Worth noting what the second retrieved chunk was. `dining_verrill_street_grill.txt`
is a review of the burger and the Friday evening wait times, and it has nothing
to do with meal plan tiers. It came back at 0.542 because it shares the words
dining and food with my question. The model ignored it completely and answered
only from the first chunk, which is the grounding instruction doing its job.

**How many chunks I retrieve:** 2 (TOP_K in config.py, down from 5)

I ran all five of my questions through `app.py retrieve` and looked at where
the answer sat and where the distances jumped.

| Question | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| meal plan mid-semester | **0.271** | 0.542 | 0.566 | 0.591 | 0.599 |
| grade appeal | **0.305** | 0.667 | 0.681 | 0.720 | 0.755 |
| pass/fail deadline | **0.274** | 0.441 | 0.525 | 0.598 | 0.599 |
| study abroad aid | **0.295** | 0.638 | 0.692 | 0.764 | 0.772 |

The answer was at position 1 every time, and the drop to position 2 is huge in
every case. Positions 2 through 5 all sit between 0.44 and 0.77, which is the
same band my out-of-scope questions land in. They are noise.

My data alone would say 1, but five questions is a small sample and all five
are ones I wrote on purpose to point at documents I had read. That is the best
case, not the typical one. If a future question has its answer at position 2
and I only retrieve 1, the model gets nothing useful and refuses a question my
corpus can actually answer. I picked 2 because position 2 has never been needed
across five questions, and everything from position 2 down scores in the same
range as questions the corpus cannot answer at all.

It also made the answers cheaper. The meal plan question used 538 tokens at
TOP_K 5 and 310 at TOP_K 2, and the answer did not lose a single detail.

**My relevance cutoff:** 0.6 (THRESHOLD in config.py, unchanged)

| Question | In corpus? | Best distance |
|---|---|---|
| are there penalties for declaring my major late? | yes | 0.228 |
| can i upgrade my meal plan mid-semester? | yes | 0.271 |
| when is the deadline to declare a course pass/fail? | yes | 0.274 |
| does my financial aid package travel with me? | yes | 0.295 |
| can i appeal my grade without passing through my instructor? | yes | 0.305 |
| What is the capital of Mongolia? | no | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| Who won the 1994 World Cup? | no | 0.886 |
| How do I write a for loop in Rust? | no | 0.896 |
| How do I change the oil in a diesel engine? | no | 0.934 |

My worst in-corpus question is 0.305 and my best out-of-scope question is
0.825. That is a gap of 0.52 with nothing at all in it. The guide says most
corpora land between 0.45 and 0.75, so anything in that whole range would
separate my two groups perfectly. The starter's 0.6 already sits in the middle
of my gap, so I measured and left it where it was rather than moving a number
for the sake of moving it.

I do not think the clean separation says my system is good. It says my
questions are good. My first set of questions, the ones I picked by topic
instead of by document, landed at 0.593, 0.601, 0.625, 0.663 and 0.716. Those
sit right inside this gap, and with that set the cutoff would have been
genuinely hard to place. Rewriting the questions to aim at documents is what
made the gap clean.

There is also one thing no cutoff can fix, and I hit it in Milestone 2. I asked
whether I could change my major without enough credits and got 0.513, well
under the cutoff, and the model still said the documents did not discuss it.
The chunks were about the right topic but did not hold the answer. Lowering the
threshold far enough to catch that would also throw away good questions scoring
0.497. That is why my fifth criterion exists: the gate catches the clear
misses, the grounding instruction catches the near ones.

## How I Used AI

**1. I asked Claude to write the chunking function from my notes, and it added
a rule I had not asked for.**

I had already decided on sentence boundaries, a ceiling, and 70 characters of
overlap, and I asked for code that did that. What came back also included a
tail-fold rule: if the leftover piece at the end of a document was under 170
characters, glue it back onto the chunk before it. I had not asked for that. It
was Claude's way of handling the 2 character chunk problem the guide mentions
on `advice_threads`.

I kept it, but it is the reason my ceiling broke. At a ceiling of 400 that fold
fired on five documents, glued each tail back on, and recreated whole documents
as single chunks of up to 513 characters, over my own 400 limit. I only found
it because I sorted my chunks by length and noticed the five longest were all
index #0, meaning nothing had actually split.

What I changed was not the code but my understanding of the tradeoff. I tested
three ceilings, found that 230 fixed the top and broke the bottom, and worked
out that the fold only protects the last chunk of a document and never the ones
in the middle. That is written up in my Chunking Strategy section. If I had
taken the code without reading it I would have reported 89 chunks and thought
my chunker worked.

**2. Claude made a prediction about my corpus and it was wrong, and finding
that out is what produced my actual evidence.**

I was trying to decide my ceiling. `housing_old_brewhouse.txt` is 563
characters and covers six subjects, and Claude predicted that asking about the
laundry cost buried inside it would retrieve badly, because a chunk covering
six things matches no single question strongly.

I ran it and got 0.211, my best distance of the whole project. The prediction
was wrong, because there is a dedicated `housing_old_brewhouse_laundry.txt`
that did the work instead.

So I tested the case with no dedicated file. Heating is mentioned only inside
the six subject document, and it scored 0.363. Same building, same question
style, a gap of 0.152. That number is the evidence my whole ceiling argument
rests on, and I would not have it if the first prediction had been right.

What I took from this is to test the claim rather than the story. The
explanation sounded convincing both times. Only one of them was measurable.

**3. I used Claude to tidy up the grammar of this README.**

The measurements, the decisions and the reasoning in here are mine, out of my
own terminal. I wrote them up rough and had Claude clean up the grammar and
tighten the wording, then went back over it. I am saying so because it would be
odd to have a section about how I used AI that did not mention the AI I used on
the section itself. The What This Does section is my own writing, untouched.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

## The Improvement

**What I changed:**

**Why I picked it:**

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

## What's Still Broken

## What I'd Do Differently