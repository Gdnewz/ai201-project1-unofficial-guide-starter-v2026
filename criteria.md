# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

---my five questions are the best case. with 0.23-0.31 distance so all are expected to hit. I wrote questions after reading the file that answers it. The slack is for questions I didn't write that should hit but might not because they weren't tailored

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

---The generate.py has a GROUNDING_INSTRUCTION that has rules:  use only the documents, say you do not have enough information if they do not cover it, name the file, and be brief. The "name the file" rule is what makes every answer name the source. When the model follows the second rule and refuses, the refusal names no file, so the answer would miss criterion 2

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---There was a clean gap. By worst in-corpus 0.305, best out-of-scope 0.825, cutoff 0.6. The gate checks the best distance to the cutoff for the model to even be called, the clean separation says my questions are good, not that my system is good. So a question i did not write could land closer to the cutoff, and the 4 of 5 leaves room for that

## 4. Something about your chunks

 No chunk is under 170 characters or over 400 characters 

**Why this target:**
no chunk is under 170 characters because nothing in the corpus is currently under 188, so the floor is of no use currently. The floor controls what the chunker is allowed to produce. Looking at the advice-thread chunk, the individual replies reference things said earlier, so splitting per reply would produce pieces nobody could answer from.
the chunk should not be above 400 because the 563 character file I inspected covered six subjects and scored 0.15 worse on a fact buried inside it. I set the ceiling below it, at the point where I'd expect mixing to start.


---

## 5. Your choice

For all of my 5 test questions, every fact in the answer must appear in one of the retrieved chunks.


**Why this target:**
It must be 5 of 5 because a system that invents facts one time in five is arguably worse than one that refuses more often. I saw the system decline to answer from chunks that were close, in terms of topics, but didn't hold the answer. 


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
