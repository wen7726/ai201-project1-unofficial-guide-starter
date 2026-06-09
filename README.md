# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---
This project focuses on student-generated housing and apartment reviews. The goal of the system is to make informal housing knowledge searchable through retrieval-augmented generation (RAG). Official apartment websites usually describe amenities, pricing, and location, but they rarely explain residents' actual experiences with noise, parking, maintenance, safety, management quality, roommate conflicts, or move-out problems.

This knowledge is valuable because students and renters often rely on scattered Reddit posts, apartment review sites, and online discussions to make housing decisions. These experiences are difficult to search in one place, especially when users want direct answers to natural-language questions such as “What do residents say about maintenance?” or “Which apartments are noisy at night?”

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | housing|noise complaint | data/raw/housing_noise_complaints.txt|
| 2 | apartment|maintenance complaints |data/raw/housing_maintenance_complaints.txt |
| 3 |moving |first time moving out experiences |data/raw/housing_moveout_experiences.txt|
| 4 |housing review|general apartment experience A |data/raw/housing_apartment_a.txt |
| 5 |housing review | general apartment experience B |data/raw/housing_apartment_b.txt |
| 6 |housing review |general apartment experience C |data/raw/housing_apartment_c.txt | 
| 7 |student housing |dorm condition |data/raw/housing_dorm_reviews.txt|
| 8 |student advice |roommate advice|data/raw/housing_roommate_advice.txt |
| 9 |housing review |parking availability|data/raw/housing_parking_reviews.txt |
| 10 |housing review |safety concerns |data/raw/housing_safety_reviews.txt |
---
## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
Review-based chunks. Each chunk corresponds to one complete review or discussion response.

**Overlap:**
Review-based chunks. Each chunk corresponds to one complete review or discussion response.

**Why these choices fit your documents:**
My corpus consists mostly of short review-style comments and Reddit discussions rather than long documents. Initially, I experimented with fixed character chunking, but this produced fragmented chunks and incomplete sentences that weakened retrieval quality. I changed the strategy to split documents using review markers such as Review 1: and Review 2:. This approach produced cleaner, self-contained chunks focused on one topic or experience.

Before chunking, I removed unnecessary formatting artifacts and preserved source metadata such as topic, URL, and source labels inside each chunk. I also filtered out very short reviews under 120 characters because they often lacked enough semantic information for useful retrieval.

**Final chunk count:**
31 chunks across 10 source documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
sentence-transformers/all-MiniLM-L6-v2

**Production tradeoff reflection:**
I selected all-MiniLM-L6-v2 because it is lightweight, free, runs locally, and performs well for semantic similarity search on short natural-language reviews. For a production deployment, I would compare larger embedding models based on retrieval accuracy, multilingual support, latency, and cost. I would also evaluate whether domain-specific embedding models perform better on informal housing-review language and Reddit-style discussions.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt instructs the model:
     “Answer the question using ONLY the provided context. If the context does not contain enough information, say ‘I don't have enough information from the provided documents.’”

This grounding instruction prevents the model from relying on general knowledge outside the retrieved chunks.

The retrieved chunks are concatenated into a context block and passed directly into the prompt alongside the user’s question. Only retrieved chunks are included in generation.
**How source attribution is surfaced in the response:**
Source attribution is handled programmatically rather than relying on the LLM to invent citations. After retrieval, the system collects the source file names from the retrieved metadata and displays them alongside the generated response in the Gradio interface.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |What do residents say about noise complaints? |Residents recommend documenting complaints and contacting management |System summarized documenting noise, contacting management, and encouraging neighbors to complain |Relevant |Accurate |
| 2 |What problems do residents mention about maintenance? |Residents describe slow maintenance response and poor management |Residents descibe slow maintenance response and poor management |System said it did not have enough information from the documents |Partially relevant |Inaccurate 
| 3 |What do residents say about the parking? |Residents mention limited parking and safety concerns |System said it did not have enough information from the documents |Off target |Inaccurate |
| 4 |What advice do people give about moving out for the first time? |People recommend preparing essentials, making checklists, and researching locations |System returned roommate-related advice about routines and shared living |Partially relevant |Partially accurate |
| 5 |Which apartment has the best swimming pool? |The system should refuse because the documents do not discuss swimming pools |System correctly refused and said it did not have enough information |Relevant |Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
“What advice do people give about moving out for the first time?”
**What the system returned:**
The system returned roommate advice about budgeting, routines, quiet hours, and shared living instead of focusing on moving-out preparation.
**Root cause (tied to a specific pipeline stage):**
This failure occurred during retrieval. The embedding model retrieved semantically related roommate-advice chunks because both topics involve independent living, comfort, routines, and housing preparation. Since the retrieved chunks were only partially relevant, the generation stage produced a partially accurate answer that drifted away from the intended topic.
**What you would change to fix it:**
I would improve retrieval quality by increasing the number of move-out examples in the corpus and experimenting with hybrid search (semantic + keyword search). I would also test larger embedding models or metadata filtering to better separate roommate-related discussions from moving-out experiences.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning document helped structure the implementation into clear stages: ingestion, chunking, retrieval, and generation. Writing the chunking strategy before coding made it easier to recognize that fixed character chunking was not appropriate for short review-style documents. The evaluation plan also helped identify retrieval weaknesses early instead of assuming the system worked correctly.
**One way your implementation diverged from the spec, and why:**
My original plan proposed fixed-size chunking with overlap, but during implementation I changed to review-based chunking. The fixed character approach produced fragmented chunks and incomplete sentences that weakened semantic retrieval. Because my documents were short Reddit-style reviews instead of long articles, review-based chunking produced cleaner and more meaningful retrieval results.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I provided my chunking strategy, sample raw review documents, and project requirements for handling short review-style text.

- *What it produced:*
The AI initially produced a fixed character chunking function using chunk size and overlap.

- *What I changed or overrode:*
I replaced the fixed character splitter with review-based chunking because the original approach created fragmented chunks and incomplete sentences that hurt retrieval quality.

**Instance 2**

- *What I gave the AI:*
I provided my retrieval architecture, embedding model choice, and requirement for grounded generation with source attribution.

- *What it produced:*
The AI generated retrieval code using ChromaDB and a Groq-based generation pipeline connected to a Gradio interface.

- *What I changed or overrode:*
I modified the generation prompt to explicitly refuse unsupported questions and added programmatic source attribution instead of relying on the model to generate citations itself.