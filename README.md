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

**1. Unit 1: Claude wrote the chunking function from my notes and added a rule
I had not asked for.** I had decided on sentence boundaries, a ceiling, and 70
characters of overlap. The code that came back also folded any tail under 170
characters back into the previous chunk. I kept it, and it is why my ceiling
broke: at 400 the fold recreated five whole documents as single chunks up to
513 characters. I only caught it by sorting chunks by length and noticing the
five longest were all index #0. Testing three ceilings and working out that
the fold only protects the last chunk, never the middle ones, is in my
Chunking Strategy section. Taken unread, the code would have had me report
89 chunks and think it worked.

**2. Unit 1: Claude made a prediction that was wrong, and checking it
produced my real evidence.** It predicted that a laundry question aimed at
the six-subject `housing_old_brewhouse.txt` would retrieve badly. It scored
0.211, my best of the project, because a dedicated laundry file existed. So I
tested heating, which lives only in the mixed file, and got 0.363. That 0.152
gap is what my whole ceiling argument rests on. Test the claim, not the story.

**3. Unit 2: Claude coached; I ran and read.** Every number in the Unit 2
tables came from a command I ran or an answer I read in results/. Claude
explained what each criterion measured and where to look, and corrected me
once when I carried the scorer's fail into row 1. The fifteen answers, the
tallies, and every MET or MISSED are mine. The fix was my breakout room coach's input
not Claude's: Claude first suggested stemming in the judge, and I chose the
question reword after asking in class. Claude assembled README sections from
paragraphs already in notes.md or the chat, and I edited each before pasting.
It got one lesson wrong, saying I should have tested both chunk bounds before
choosing a ceiling when I had tested them three times, and the corrected
version is what appears above. It also fixed setup problems: wrong folder,
`return bool`, a truncated paste.

**4. Both units: grammar.** I wrote rough, Claude tightened, I went back over
it. The What This Does section is untouched.

---

# Unit 2

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Run: `results/run_2026-09-23_2048.md`, produced by `run_eval.py` calling `scorer.judge`. Before the question 1 reword. Scorer: 14/15.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk is under 170 characters or over 400 characters | 0 under 170, 0 over 400 | 177-420, 3 over 400 | 177-420, 3 over 400 | 177-420, 3 over 400 | MISSED |
| 5. For all of my 5 test questions, every fact in the answer must appear in one of the retrieved chunks | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Real output for question 1, all three runs, from `results/run_2026-09-23_2048.md`, produced by `run_eval.py` calling `scorer.judge`:

```
are there penalties for declaring my major late ? — run 1
Best distance: 0.2283 (passed the gate)
Sources retrieved: admin_declaring_a_major.txt, admin_pass_fail_option.txt
No, there is no penalty for declaring your major late.
Source: admin_declaring_a_major.txt

are there penalties for declaring my major late ? — run 2
Best distance: 0.2283 (passed the gate)
Sources retrieved: admin_declaring_a_major.txt, admin_pass_fail_option.txt
No, there are no penalties for declaring your major late. This information comes from admin_declaring_a_major.txt.

are there penalties for declaring my major late ? — run 3
Best distance: 0.2283 (passed the gate)
Sources retrieved: admin_declaring_a_major.txt, admin_pass_fail_option.txt
No, there is no penalty for declaring your major late.
Source: admin_declaring_a_major.txt
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | The same source document was retrieved on all three runs for every question, including question 1 run 2 where the scorer said fail. The criterion is about retrieval, not wording, and retrieval did not change. |
| 2 | Every answer names a source | MET | All 15 answers end with a Source: line naming a file. This comes from the "name the file" rule in GROUNDING_INSTRUCTION. |
| 3 | Gate stops out-of-corpus questions | MET | Read off run_eval's "gate refused 5 of 5" line. Identical across runs because the gate is deterministic, one number compared to 0.6, no model call. |
| 4 | No chunk under 170 or over 400 characters | MISSED | From `python app.py index`: 97 chunks, shortest 177, longest 420, three over 400. Same in all three columns because chunking happens once at index time, not per run. |
| 5 | Every fact in the answer appears in a retrieved chunk | MET | Read all 15 answers against the retrieved chunks. None stated a fact the chunk did not hold. "No penalties" in question 1 run 2 is the same fact as "no penalty", phrased differently, so it does not fail this criterion even though the scorer failed it. |

## Diagnoses

### Criterion 4 — three chunks over 400 (MISSED)

Stage: chunking, `chunker.py::split_documents`.

Mechanism: the chunker fills to the 300 ceiling and pushes the leftover into a
new chunk. When the leftover is under my 170 floor, the tail fold glues it back
on, recreating the whole document as one chunk over the ceiling. Worst case is
ceiling plus floor, 470; longest measured is 420. All three over 400 are whole
documents that split and reassembled.

Not fixed yet. The real fix is a chunker rewrite that merges undersized middle
chunks too, and re-indexing would move every distance I have measured.
Reported, not hidden.

### Question 1 run 2 — looked like a miss, was not

The scorer reported fail on this run, so I checked it against all five
criteria. None missed. The source document was retrieved (criterion 1), the
answer named it (criterion 2), and every fact in the answer was in the chunk
(criterion 5). "No penalties" is the same fact as "no penalty" in different
words.

Stage: scoring, `scorer.py::judge`. Mechanism: substring check, and "no
penalty" is not a substring of "no penalties". Retrieval was identical all
three runs. The only thing that moved was the model's wording, and my question
had the plural in it, so the model was echoing me.

A measurement miss, not a system miss. This is the one I chose to fix.

## The Improvement

**What I changed:** Reworded question 1 from "are there penalties for
declaring my major late?" to "is there any penalty for declaring my major
late?" Original kept as a comment in `questions.py` with the reason.

**Why I picked it:** The scorer is shared class code; my questions are mine.
One diagnosis, one change. My plural was handing the model the word it echoed
back, so removing it is the smallest fix that targets the actual mechanism.

## Run Log — After

Run: `results/run_2026-09-23_2200.md`, same pipeline. After the question 1 reword. Scorer: 15/15.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk is under 170 characters or over 400 characters | 0 under 170, 0 over 400 | 177-420, 3 over 400 | 177-420, 3 over 400 | 177-420, 3 over 400 | MISSED |
| 5. For all of my 5 test questions, every fact in the answer must appear in one of the retrieved chunks | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?** The scorer went from 14/15 to 15/15 and question 1's
distance dropped from 0.228 to 0.205. Every criterion verdict is identical
before and after; the change fixed the scorer's read of one question and
nothing else.

## What's Still Broken

**Criterion 4 — three chunks over 400.** The chunker produced three chunks
over 400. I could fix the chunker but chose not to because it is a rewrite
that moves every distance. Every cutoff and TOP_K decision in Unit 1 was
measured against the current chunks, so re-chunking means re-measuring all of
it. The real fix is merging undersized middle chunks as well as tails, or
splitting documents into roughly equal pieces instead of filling the front
greedily.

**Workload boilerplate.** The course workload files share boilerplate wording
and differ only in the course name and the hours. I tested it with
`python app.py retrieve "how heavy is the workload?"`. Both TOP_K slots came
back as workload files, PHYS 130 at 0.529 and CS 210 at 0.553, and the gate
passed it because 0.529 is under 0.6. The model would get two near identical
chunks about two different courses and no way to tell which one I meant. Part
of this is the question, which has no single right answer, and part is the
corpus, where a dozen documents match it about equally. Not fixed.

**Correct but incomplete answers.** Two of my Milestone 2 answers were correct
but skipped a figure that was sitting in the chunks. Criterion 5 cannot catch
this, because leaving a fact out is not the same as inventing one. A fourth
grounding rule telling the model to include specific numbers and deadlines
would help, but it works against the "be brief" rule already in there, so it
is a real tradeoff rather than a free improvement. Not done.

## What I'd Do Differently

**Criterion 5 is the one I'd rewrite.** It says every fact in the answer must
appear in a retrieved chunk, which catches invented facts and nothing else.
This unit showed me two correct answers that skipped a figure sitting in the
chunk, and criterion 5 passed them, because leaving a fact out is not the same
as putting one in. It also needs a person to decide what counts as a fact,
which I flagged in unit 1. Next time I would split it in two: keep the
no-invented-facts check as it is, and add a second check that the specific
figure or deadline in `expects` appears in the answer, which the scorer can
test without a judgment call. Same target, 5 of 5. Sharper, not looser.

Fix the chunker's logic before tuning its number. I tested three ceilings in
Unit 1 Milestone 3 and measured both bounds each time. At 400 and 300 the
ceiling broke, at 230 the floor broke. That told me no ceiling value could
satisfy criterion 4, because the fold only protects the last chunk of a
document and never the middle ones. I kept tuning the number anyway. Next
time, once the measurements show the knob cannot win, I stop turning it and
fix the algorithm, then tune.

Write the "why this target" for every criterion the day I write the
criterion. Criteria 1, 2 and 3 sat with empty placeholders for two weeks and I
had to rebuild the reasoning from my notes. It was all there, but it should
have been in criteria.md from the start.

Read my own question before I read the model's answer. The plural in "are
there penalties" is what the model echoed back. A question that hands the
model a word is a question that will sometimes get that word back, and my
`expects` string has to survive that.