# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
Oluwatofunmi Oyetan corpus: campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
    This is a RAG system that chunks corpus documents, builds a vector index, and answers user questions by retrieving the most relevant passages. 
    
    I used the campus_life corpus; typical questions ask about campus services, schedules, and student advice. Answers are grounded in the retrieved documents and include a filename evidence line (or the system will refuse with “I don't have enough information to answer that.” if no support is found). 
   
   To reproduce, run python app.py index then ask questions with python app.py ask "..." (a valid GEMINI_API_KEY is required for fresh generation).

## Chunking Strategy

**Chunk size:** 800 characters — corpus documents are short forum threads, so 800 chars keeps whole replies and short multi-reply threads together while limiting chunk scope.

**Overlap:** 120 characters — a modest overlap preserves sentence context across chunk boundaries and prevents cutting important phrases.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->
     ======================================================================
     Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::split_documents
     ======================================================================
     THREAD: Is a bike worth it for a 20 minute walk commute?

     --- reply 1 (14 votes) ---
     Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

     --- reply 2 (9 votes) ---
     Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

     --- reply 3 (22 votes) ---
     Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

     --- reply 4 (5 votes) ---
     If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.

     ======================================================================
     Chunk 2  |  source: thread_first_gen.txt#0  |  produced by: chunker.py::split_documents
     ======================================================================
     THREAD: Anything specific for first-generation students?

     --- reply 1 (33 votes) ---
     The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

     ======================================================================
     Chunk 3  |  source: thread_laptop_specs.txt#0  |  produced by: chunker.py::split_documents
     ======================================================================
     THREAD: How much laptop do I actually need for CS courses?

     --- reply 1 (31 votes) ---
     Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

     --- reply 2 (18 votes) ---
     Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

     --- reply 3 (12 votes) ---
     I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

     ======================================================================
     Chunk 4  |  source: thread_meal_plan_tier.txt#1  |  produced by: chunker.py::split_documents
     ======================================================================
     --- reply 1 (24 votes) ---
     Depends entirely on whether your building has a kitchen. Fenwick has kitchenettes, so people there go down a tier and cook two or three nights. Everywhere else, get the middle tier.

     --- reply 2 (19 votes) ---
     The highest tier only makes sense if you eat three meals a day in the halls every single day, which basically nobody does past October.

     --- reply 3 (11 votes) ---
     Remember you can only change it once and only in the first ten days. I waited and got stuck on a plan I didn't use.

     --- reply 4 (7 votes) ---
     Declining balance rolls within the semester but not between them. Spend it in December or lose it.

     ======================================================================
     Chunk 5  |  source: thread_printing.txt#0  |  produced by: chunker.py::split_documents
     ======================================================================
     THREAD: Is the printing quota enough?

     --- reply 1 (17 votes) ---
     For most people yes. $30 is about 600 pages black and white. It's the colour printing that eats it — eight times the cost per page.

     --- reply 2 (11 votes) ---
     Doesn't roll over between semesters. Print your readings in December rather than losing it.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
How much dollar does every student get for printing per semester
**Answer:**
Every student gets $30 of printing per semester.
Evidence: admin_printing_quota.txt
```
```

**Sample Answer**

**Question:** What are the walk-in hours for the health centre?

**Answer:** Walk-in hours for the health centre are 8:00 AM to 11:00 AM. 
Evidence: health_center.txt


**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|----------|------------|---------------|
| How much dollar does every student get for printing per semester | Yes |  0.2529 |
| What are the walk-in hours for the health centre | Yes |  0.1750 |
| What are the library hours during reading week | Yes |  0.4316 |
| The lab practical for phys 130 mechanics course is worth how many percent | Yes |  0.1932 |
| What is winter like | Yes |  0.4670 |
| What is the capital of Mongolia | No |  0.8246 |
| How do I change the oil in a diesel engine| No |  0.9340 |
| Who won the 1994 World Cup| No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache| No | 0.8442 |
| How do I write a for loop in Rust| No | 0.8960 |


 Yes, there is a gap — min_out_of_scope (0.8246) > max_in_corpus (0.4670).
 Relevance Cutoff (midpoint): (0.4670 + 0.8246)/2 ≈ 0.646.
This sits squarely in the gap and avoids false accepts while still answering in‑scope questions.


## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

1) Chunking function

- Asked: paragraph-first chunker; merge tiny paragraphs; fallback sliding window.
- Returned: draft that sometimes split mid-paragraph.
- Changed: implemented paragraph-first split and tiny-paragraph merge in `chunker.py`.

2) Grounding & evidence

- Asked: require answers cite filenames and refuse when unsupported.
- Returned: prompt draft + wrapper; inconsistent refusal/evidence formatting.
- Changed: added strict `GROUNDING_INSTRUCTION` in `generate.py` and updated `Sample Answer`.
<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk >90 words or <200 characters | 88 of 88 | 83/88 | 83/88 | 83/88 | MISSED |
| 5. Random sample of 5 chunks reads as a complete thought | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->
Full evidence: [`results/run_2026-10-04_2212_before.md`](results/run_2026-10-04_2212_before.md),
produced by `run_eval.py::main` (3 runs per question, caching off, `scorer.py::judge`
marking pass/fail) and `run_eval.py::check_out_of_scope` (the gate pass).

**Criterion 1** — retrieved chunk for "What are the library hours during reading
week" (distance 0.432), from `store.py::search`:

```
Library hours and where to actually sit

Open until 2am during term, until 10pm during reading week, which is backwards
and catches everyone out every single year.
```

The question's `expects` phrase is "Open until 10pm" — not a literal substring
of the chunk, but the chunk plainly contains the answer, which is the actual
test. All 5 questions had the answer in their top-5 retrieved chunks, and
retrieval is deterministic (same best distance all 3 runs), so this doesn't
move between runs.

**Criterion 2** — answer for "How much dollar does every student get for
printing per semester" (run 1 of 3), from `generate.py::answer_from_chunks`:

```
Every student gets $30 of printing per semester.

Evidence: admin_printing_quota.txt
```

All 15 answers (5 questions × 3 runs) named at least one source the same way.

**Criterion 3** — `run_eval.py::check_out_of_scope`, calling `gate.py::check`:

```
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

> Criteria 4 and 5 are about chunk quality, not question-answering, so
> `run_eval.py` doesn't measure them — it only calls `store.search`,
> `generate.answer_from_chunks`, and `gate.check`. The numbers below came from
> running `chunker.py::split_documents` directly. Chunking is deterministic
> (no model call), so there's one measurement, same as criterion 3.

**Criterion 4** — all 88 chunks from `chunker.py::split_documents` (via
`ingest.py::load_documents`): 1 chunk over 90 words, 4 chunks under 200
characters, 83/88 compliant. The 4 short ones are no longer split-off
titles — they're whole documents that are themselves under 200 characters,
so no merge rule can fix them without inventing content:

```
too long (>90 words): 1 ['housing_old_brewhouse.txt#0']
too short (<200 chars): 4 ['course_biol_160_exams.txt#0', 'course_hist_118_exams.txt#0',
                           'course_math_220_exams.txt#0', 'course_phys_130_exams.txt#0']

>>> course_phys_130_exams.txt (194 chars total)
'PHYS 130 Mechanics — assessment\n\nThree midterms, no final, plus a lab
practical. Not curved, but the lowest midterm is dropped.\n\nThe lab
practical is worth 20% and almost nobody prepares for it.'
```

**Criterion 5** — random sample of 5 chunks (`random.seed(42)`), from
`chunker.py::split_documents`:

```
===== money_textbooks.txt#0 (374 chars, 62 words)
Textbooks without paying full price

The library holds one copy of most required texts on two-hour reserve. For
courses where the text is used constantly that isn't enough, but for the
reading-light courses it's genuinely all you need.

The campus store price-matches, which is not advertised anywhere and you
have to ask at the counter with the other listing on your phone.

===== admin_wifi_and_accounts.txt#0 (283 chars, 48 words)
On the wifi and accounts

Your student account gives you campus wifi, printing, and a cloud drive with
unlimited storage that most people never discover. The account stays active
for six months after you graduate, and the cloud drive is purged at that
point without a second warning.

===== admin_dining_dollars.txt#0 (211 chars, 36 words)
On the dining dollars

Declining balance — what everyone calls dining dollars — rolls over from the
autumn semester to the spring, but not from spring to the following autumn.
Whatever is left in May disappears.

===== course_math_220.txt#0 (383 chars, 65 words)
MATH 220 Linear Algebra

I lived here my sophomore year. Format is chalk-and-talk lecture, weekly
problem sets marked for correctness. Assessment: two midterms and a
cumulative final. Curved to a b- median.

Expect 6 to 8 hours a week, almost all of it on problem sets.

The one piece of advice: the problem sets are the course; the lectures make
sense afterwards rather than during.

===== course_engl_205_workload.txt#0 (266 chars, 45 words)
Workload for ENGL 205 Writing for the Sciences

People keep asking so: 4 to 5 hours a week, mostly writing and rewriting.
That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because
you're learning the format.
```

All 5 read as complete thoughts, no sentence cut off at either end.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
