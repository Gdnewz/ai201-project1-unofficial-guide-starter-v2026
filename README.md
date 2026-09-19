# The Unofficial Guide

Goodnews (Goody) Idowu — corpus: `campus_life`

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

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
chunks would eat two of my five retrieval slots. I also thought about 10, but
two words of carryover protect nothing. I got to 70 by elimination.

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

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     Milestone 5. -->

**1.**

**2.**

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