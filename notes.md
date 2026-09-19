PROJECT 1, UNIT 1: WHAT I LEARNED

Goodnews (Goody) Idowu

Corpus: campus\_life





=============================================================================

PART 1: MILESTONES 1 AND 2

=============================================================================





WHERE I GOT STUCK AND HOW I GOT OUT



Setup.



My first pip command failed because I used single quotes. Windows cmd does not

understand single quotes, so it read the whole thing as a filename. Double

quotes fixed it. Then I created my virtual environment in my home folder

instead of the project folder and tried to run app.py from there, so Python

could not find the file. The lesson is that cmd has no idea where my project is

unless I cd into it first, and the venv should live beside the code it serves.



Thinking the terminal was a chat box.



I typed questions like "what are good dining halls?" straight at the prompt and

got "not recognized as an internal or external command." Every line I type

there is read as a program name. Questions only reach my system through

python app.py ask "...". I also ran ask"how hard..." with no space, and argparse

read the whole thing as one unknown command name.



Thinking questions.py fed the ask command.



I edited questions.py, re ran ask, and saw identical output. I assumed I needed

to restart the terminal. Neither was true. The ask command takes its question

from the command line and never opens questions.py. That file is only read by

run\_eval.py in unit 2. On top of that, repeated questions were being served

from cache, so the output was byte for byte identical anyway.





WHERE MY QUESTIONS WENT WRONG



My first five questions came from topics I personally cared about. Three of

them were refused outright and one cleared the gate but still could not be

answered.



&#x20; change major        0.593   answered, but about declaring, not changing

&#x20; meal plan tier      0.454   gate opened, model refused

&#x20; commuting           0.663   refused

&#x20; roommate            0.625   refused

&#x20; reworded major      0.601   refused



The reworded major question is the one that taught me the most. It is the same

question as the first one, asked slightly differently, and it moved from 0.593

to 0.601. Those two numbers sit on opposite sides of the 0.6 cutoff, so one got

answered and one got refused. Eight thousandths of a difference, and nothing

about the meaning changed. Distance is sensitive to phrasing in ways that have

nothing to do with what I meant.



I then asked about credits and majors and got 0.513, comfortably under the

cutoff, and the model still told me the documents did not discuss changing a

major. That was the second big lesson. A good distance score means the

retrieved chunks are about the same topic as my question. It does not mean the

answer is in them. No cutoff can separate those two cases, because lowering the

threshold enough to catch it would also throw away good questions scoring

0.497.





HOW I GOT BACK ON TRACK



I stopped picking a topic and hoping a document covered it. I listed the

documents folder, read files, and wrote a question for each file I had actually

read. That one change fixed everything.



&#x20; declaring late      0.228   contains "no penalty"

&#x20; grade appeal        0.305   contains "returned"

&#x20; meal plan changes   0.271   contains "first ten"

&#x20; pass/fail deadline  0.274   contains "week eight"

&#x20; study abroad aid    0.295   contains "travels with"



Topic first questions gave me a 0.59 to 0.72 spread. Document first questions

gave me 0.23 to 0.31. Same system, same corpus, same day.





WHAT I LEARNED ABOUT THE EXPECTS FIELD



I got this wrong four separate ways before it clicked. The expects string is

checked as a substring of the answer, so it has to be short and it has to be

something the answer cannot phrase around.



First I wrote whole sentences copied from the documents. No model answer

reproduces a sentence word for word, so those could only fail.



Then I used "pass/fail" as the anchor for a question that already contained the

words pass/fail. Any answer would echo it back, so the check could never fail.

A test that always passes is measuring nothing.



Then I anchored on facts that were in the same document but were not the answer

to the question I asked. I asked whether I could skip my instructor when

appealing a grade, and anchored on "fifteen days," which is a deadline. The

system answered the process question correctly and never mentioned a deadline.

The document held both facts, but a question only pulls out one of them.



I also lost a match on "sciences" versus "science," because substring matching

cares about plurals and capital letters.





WHAT I FOUND OUT ABOUT MY CHUNKS



My index reported 88 documents producing 88 chunks, which means fallback\_split

had not split anything. One chunk equalled one document. Sizes ran from 178 to

549 characters, averaging 317.



I compared two documents. admin\_meal\_plan\_changes.txt is about 195 characters

and covers one subject, changing your meal plan tier, with three related facts.

housing\_old\_brewhouse.txt is 563 characters and covers six separate subjects:

the building history, the rooms, its character, the heating, the laundry, and

the noise.



Then I measured what that costs. Both of these are facts about the same

building, asked the same way.



&#x20; laundry at Old Brewhouse   0.211

&#x20; heating at Old Brewhouse   0.363



Laundry has its own dedicated file. Heating exists only inside the six subject

file. The gap is 0.152. A dining hall document also showed up in the top five

results for a question about dorm heating, which is the retriever scraping for

anything when nothing matches strongly.



Both answers were still correct. What a mixed chunk costs is margin, not

correctness. Margin matters because of the 0.593 and 0.601 result. A question

landing at 0.211 survives a bad rewording. One landing at 0.363 has less room

to move.



I want to be honest about the limit of this evidence. It came from a 563

character file. It proves that large multi subject files cost margin. It does

not prove that mixing begins at exactly 400. I picked 400 as my judgment of

where mixing starts, and Milestone 3 would show me whether that was the right

place. What I could see before running anything was only file sizes on disk,

which is not the same as chunk lengths. The real measurements are in Part 2.





WHY MY FLOOR IS 170



Nothing in the corpus was under 188 characters at that point, so the floor did

nothing on day one. It starts working once fallback\_split is replaced, because

it controls what the new chunker is allowed to produce. I saw why this matters

when I printed a chunk from the advice\_threads corpus. It held a question and

four replies, and the replies referred back to each other. One of them reads

"Counterpoint, I sold mine." Split per reply, that piece is retrievable and

completely meaningless.





WHY MY FIFTH CRITERION IS 5 OF 5



Twice I watched the system get chunks that were topically close, that did not

hold the answer, and refuse instead of inventing something. It could have

produced an answer about changing majors from the graduation requirements

document. It did not. I am protecting behaviour I have observed rather than

behaviour I hope for.



I set it at 5 of 5 rather than 4 of 5 because an invented fact is the failure I

cannot see from the outside. A retrieval miss is obvious, I get a refusal or a

clearly wrong document. A fabricated fact looks exactly like a correct answer.

So there is no reason to accept even one.





WHAT I KNOW IS STILL WEAK



Criteria 1 and 5 need a person to make a judgment call. Criterion 1 needs

someone to decide whether a chunk contains the answer, and criterion 5 needs

someone to decide what counts as a separate fact. Criteria 2, 3 and 4 are

mechanical and anyone would score them the same way. If asked how I would count

a fact, I would count each claim that could be true or false on its own.



Also, my corpus has no documents on changing majors, commuting, or transit, so

those early questions were never winnable no matter how I worded them.



And my run logs live in results/, which is deliberately not ignored by git,

because they are the evidence that the test actually ran.





=============================================================================

PART 2: MILESTONE 3, THE CHUNKER

=============================================================================





WHAT THE STARTER WAS DOING



The starter cuts fixed 800 character windows with overlap and ignores where

sentences end. My longest document is 563 characters, so it never reached 800

and never split anything. 88 documents, 88 chunks. The summary line looked fine

until I realised it meant the chunker had done no work at all.



The guide calls that a bug outright, and points out the same chunker turns

city\_guides into 51 chunks from 14 documents, and produces a 2 character chunk

on advice\_threads from a document that did not divide evenly. Same code, three

different failures depending on the corpus.





WHAT I CHANGED



Split on sentence boundaries. Accumulate sentences until the next one would

push past a ceiling, then start a new chunk carrying 70 characters from the end

of the previous one. Fold a leftover tail under 170 characters back into the

chunk before it.





MISTAKE 1: I CONFUSED TWO FILES



I pasted chunker.py and called it config.py. They are different files.

chunker.py holds the logic, config.py holds the numbers the logic reads. The

lines like chunk\_size = config.CHUNK\_SIZE are READING a value, not setting one.

I tried to edit the wrong file.





MISTAKE 2: I THOUGHT THE FLOOR CAME FROM THE GUIDE



I nearly changed my 170 floor to make the numbers work. It is not in the guide

at all. It came from criterion 4, which I wrote myself. The criteria page says

changing a criterion earns credit only when the criterion was broken, meaning

it measured the wrong thing. Missing the number is the case where the target

stays exactly where it is. Mine is measurable and I am failing it, so it stays.





MISTAKE 3: I CONFUSED THE CONFIG KNOB WITH THE CRITERION



Lowering CHUNK\_SIZE is not the same as changing criterion 4. The criterion says

no chunk over 400. The knob is what the chunker aims at. Aiming at 300 keeps

every chunk well under 400, so lowering the knob is a design choice and does

not touch the criterion at all.





WHAT I MEASURED



&#x20; Ceiling 400    89 chunks   average 313   shortest 177   longest 513

&#x20; Ceiling 300    97 chunks   average 292   shortest 177   longest 420

&#x20; Ceiling 230   123 chunks   average 244   shortest  88   longest 378



At 400, five documents split and were immediately reassembled. The five longest

chunks were all index #0, meaning single chunks: innisfree\_hall 513,

morrow\_house 458, calder\_annexe 427, cs\_340 424, fenwick\_court 422. Every one

of them is a whole document that had been split and glued back together.





THE MECHANISM, IN PLAIN WORDS



The chunker fills a chunk up to the ceiling and puts what is left into a new

one. If a document is comfortably longer than the ceiling, the leftover is big

enough to stand alone and the document splits. If a document is only slightly

longer, the leftover is tiny, and my fold glues it back on, which recreates the

whole document as one chunk that is over the ceiling.



So the worst case is roughly ceiling plus floor. At 400 that is 570 and I

measured 513. At 300 that is 470 and I measured 420.





WHY 230 DID NOT WORK EITHER



Ceiling plus floor would be exactly 400, so I expected it to satisfy the

criterion. The longest did drop to 378. But the shortest fell to 88, well under

my floor.



The reason is that my fold only protects the LAST chunk of a document. It never

checks the ones in the middle. At a ceiling of 230 the budget for later chunks

is 160, and a chunk closes the moment the next sentence will not fit. So a

chunk holding 88 characters closes and gets emitted when the next sentence is

150 characters long. Nothing catches it.



So the smaller the ceiling, the more often one long sentence forces an early

close, and the more undersized middle chunks appear.





WHAT I SETTLED ON AND WHY



300\. The floor holds at 177, nine documents actually split instead of one, and

only three chunks exceed my 400 ceiling. None of the three settings satisfies

both bounds, because this algorithm cannot. Fixing it properly means merging

undersized middle chunks as well as tails, which I did not do in this unit.



Whether the system works is not graded in this unit. What is graded is whether

the README describes the system I actually built. So I am reporting the

conflict rather than hiding it.





READING THE FIVE CHUNKS



All five passed the self containment test. The reason is that every document in

this corpus opens with a heading line naming its subject, and a heading has no

ending punctuation, so my sentence splitter keeps it attached to the text that

follows. That was not deliberate when I wrote the rule, but it is what makes

the chunks answerable. Strip the heading off the BIOL 160 chunk and it reads

"9 to 11 hours a week" with no way to tell of what.



Two problems I noticed, and both come from the corpus rather than my code.



Chunks 2 and 3 are near duplicates in wording. Both course workload files use

the same boilerplate sentences and differ only in the course name and the

hours. A general workload question will match a dozen of these about equally

and fill all five retrieval slots with near identical text.



Chunk 4 opens with "Adding to what people have said about The Ridgeway Café,"

which leans on a conversation that is not in the chunk. It carries hard facts

so it survives, but it is the closest of the five to failing.





STILL OPEN GOING INTO MILESTONE 4



More chunks means each of my five retrieval slots carries less text, so the

model gets less total context. That is worth watching when I tune retrieval and

the cutoff.



My five test questions were all measured against the OLD chunking, at 88 chunks

of one document each. Now that the corpus is 97 chunks, those distances may

have moved. I should re run them before I set the cutoff.



=============================================================================
PART 3: MILESTONES 4 AND 5, RETRIEVAL AND THE CUTOFF
=============================================================================


RE RUNNING MY FIVE QUESTIONS AFTER RE CHUNKING

I said at the end of Part 2 that I should re run my five questions, because
the corpus went from 88 chunks to 97 and the old distances might have moved.

They did not move at all. 0.228, 0.305, 0.271, 0.274, 0.295, identical to
before.

The reason is that all five of my questions point at short admin documents,
and none of those is anywhere near 300 characters, so none of them split. Only
the nine long documents changed, and none of my questions is about those. If I
had written questions about Old Brewhouse or Innisfree Hall the numbers would
probably have moved.

Worth remembering: a corpus level change does not automatically show up in my
measurements. It only shows up if my questions touch the part that changed.


WHAT RETRIEVAL WAS ACTUALLY RETURNING

app.py retrieve prints the chunks with their distances, which ask does not. I
ran all five through it.

  Question                    #1       #2      #3      #4      #5
  meal plan mid-semester      0.271    0.542   0.566   0.591   0.599
  grade appeal                0.305    0.667   0.681   0.720   0.755
  pass/fail deadline          0.274    0.441   0.525   0.598   0.599
  study abroad aid            0.295    0.638   0.692   0.764   0.772

The answer was at position 1 every single time. The drop from 1 to 2 is
enormous in every case. Positions 2 through 5 all sit between 0.44 and 0.77,
which is the same band my out of scope questions land in. They are noise.

For the meal plan question, what was actually in slots 2 through 5 was a
review of the burger at Verrill Street Grill, a post about dining dollars, and
a post about campus jobs. None of them about meal plan tiers. They came back
because they share the words dining and food with my question.

Two of those five slots were both Verrill Street Grill, one document that my
new chunker had split into two chunks. So one document was taking two slots.
That is the crowding I was worried about when I picked my overlap number.


WHY I SET TOP_K TO 2

My data on its own would say 1. The answer was never below position 1.

I did not go to 1 because five questions is a small sample, and all five are
ones I wrote on purpose to aim at documents I had read. That is the best case,
not the typical case. If a future question has its answer at position 2 and I
only retrieve 1, the model gets nothing useful and refuses a question my
corpus can actually answer. That is a worse failure than carrying one extra
chunk.

So 2. Position 2 has never been needed across five questions, and everything
from position 2 down scores in the same range as questions the corpus cannot
answer at all.

It also made answers cheaper. The meal plan question used 538 tokens at TOP_K
5 and 310 at TOP_K 2, and the answer did not lose a single detail. It actually
read better, because it led with a direct no.

TOP_K takes effect immediately. No re indexing needed.


SETTING THE CUTOFF

  In corpus                                     Out of scope
  declaring major late        0.228             capital of Mongolia      0.825
  meal plan mid-semester      0.271             ibuprofen dosage         0.844
  pass/fail deadline          0.274             1994 World Cup           0.886
  study abroad aid            0.295             for loop in Rust         0.896
  grade appeal                0.305             diesel oil change        0.934

Worst in corpus 0.305. Best out of scope 0.825. A gap of 0.52 with nothing in
it. The guide says most corpora land between 0.45 and 0.75, so my whole gap is
wider than the range they expect the answer to be in.

The starter's 0.6 already sat in the middle of my gap, so I measured and left
it. Moving it would have been changing a number for the sake of changing it.

The honest reading is that the clean separation says my questions are good,
not that my system is good. My first set of questions, picked by topic instead
of by document, landed at 0.593, 0.601, 0.625, 0.663 and 0.716. Those sit
right inside this gap. With that set the cutoff would have been genuinely hard
to place and I would have had to accept losing some real questions.

Out of scope questions cost nothing to run. A refusal never reaches the model,
so it is 0 model calls every time.


THE GROUNDING INSTRUCTION WAS ALREADY THERE

Milestone 4 asks for a grounding instruction as a second layer. I went looking
in generate.py and found GROUNDING_INSTRUCTION already written. It says use
only the documents, say you do not have enough information if they do not
cover it, name the file, and be brief.

That explains two things I had already seen without understanding why. The
credits question cleared the gate at 0.513 and the model still refused, which
was this instruction, not luck. And criterion 2, every answer names a source,
passes because of the third rule in it.

app.py ask "..." --show-prompt prints exactly what gets sent. Worth running
once. Seeing the retrieved chunks laid out as Documents: with the question
underneath made it obvious that retrieval, not the model, decides what an
answer can possibly be based on.

The clearest evidence it works: the meal plan prompt included the Verrill
Street Grill burger review, and the model ignored it completely and answered
only from the meal plan document.

Something I considered and did not do: adding a fourth rule telling the model
to include specific numbers and deadlines. Two of my Milestone 2 answers were
correct but skipped a figure that was sitting in the chunks. That rule would
work against the "be brief" rule already in there, so it is a real tradeoff
rather than a free improvement. Candidate for Unit 2.


THE TWO LAYERS, AND WHAT NEITHER CATCHES

  The gate   catches questions where nothing is close.       Mongolia, 0.825.
  The prompt catches questions where things are close but
             the answer is not there.                        credits, 0.513.

Neither catches an answer that is correct but incomplete. That is a third
thing, and it is what my fifth criterion is really testing.


WHAT I AM CARRYING INTO UNIT 2

Three chunks still break my own 400 ceiling. Reported, not hidden. The real
fix is merging undersized middle chunks as well as tails, or splitting
documents into roughly equal pieces instead of filling the front greedily.

The course workload files share boilerplate wording. A general question like
"how heavy is the workload?" will match a dozen of them about equally. With
TOP_K 2 that means both my slots could fill with near identical text about two
different courses. I have not tested that.

Criteria 1 and 5 need a human judgment call. 2, 3 and 4 are mechanical.

Unit 2 wants three runs per criterion through run_eval.py, verdicts against
the targets I already set rather than new ones, a diagnosis per miss naming
both the stage and the mechanism, one improvement tied to a specific
diagnosis, and an honest answer on whether it helped.

Caching is off during evaluation. run_eval.py passes cache=False, so three
runs are three real answers rather than one answer three times.
