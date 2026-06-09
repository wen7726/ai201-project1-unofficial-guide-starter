# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---
I chose student-generated housing and apartment reviews as my domain. This knowledge is valuable because official apartment websites usually describe amenities, pricing, and location, but they do not clearly explain residents' real experiences with noise, parking, maintenance, safety, management, roommate issues, or move-out problems. These experiences are scattered across Reddit threads, apartment review sites, and informal online discussions, making them difficult to search in one place.


## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
Review-based chunks. Each chunk is one complete review or comment section.

**Overlap:**
No fixed overlap. Because the documents are structured as separate reviews, each review is treated as a self-contained unit. I preserve the document header metadata in each chunk so the chunk still includes source, URL, and topic context.

**Reasoning:**
My corpus is made of short review-style comments rather than long articles or handbooks. A fixed character splitter initially produced weak chunks and sentence fragments, so I changed the approach to split by review markers such as Review 1:, Review 2:, etc. This keeps each chunk focused on one resident experience and makes retrieval more precise. I also filter out very short reviews under 120 characters because they usually do not contain enough context to support useful retrieval or grounded generation.

---

## Retrieval Approach


<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
sentence-transformers/all-MiniLM-L6-v2

**Top-k:**
5 chunks per query

**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it runs locally, is free to use, and is fast enough for a small student project. If this system were deployed for real users, I would compare embedding models based on retrieval accuracy, latency, cost, context length, multilingual support, and performance on informal housing-review language. I would also consider whether a larger embedding model improves semantic matching enough to justify higher compute cost.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |What do residents say about noise complaints? |Residents recommend documenting complaints, contacting management, encouraging neighbors to complain, and collecting evidence such as times or videos. |
| 2 |What problems do residents mention about maintenance? |Residents mention slow maintenance responses, poor management, delayed repairs, and frustration with corporate apartment management. |
| 3 |What do residents say about parking? |Residents describe parking as limited, difficult during busy times, and sometimes connected to safety or ticketing concerns. |
| 4 |What advice do people give about moving out for the first time? |People recommend making checklists, preparing basic household items, buying essentials, and expecting nervousness during the transition. |
| 5 |Which apartment has the best swimming pool? |The system should say it does not have enough information if the retrieved documents do not discuss swimming pools. |





---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some reviews are very short and may not contain enough semantic context for retrieval. To reduce this risk, I filter out reviews under 120 characters and preserve source/topic metadata in each chunk.
2. Housing reviews often mix multiple topics in one comment, such as maintenance, safety, parking, and management. This may cause retrieval to return partially relevant chunks. I will inspect retrieved chunks and distance scores during evaluation to decide whether each result is accurate, partially accurate, or inaccurate.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---
Raw .txt documents in data/raw/
          ↓ 
Document Ingestion: Python pathlib file reader
          ↓ 
Cleaning: whitespace cleanup and basic text normalization
          ↓ 
Chunking: review-based splitting by Review markers
          ↓ 
Embedding: sentence-transformers/all-MiniLM-L6-v2      
          ↓ 
Vector Store: ChromaDB persistent local database
          ↓ 
Retrieval: top-k semantic similarity search 
          ↓ 
Generation: Groq llama-3.3-70b-versatile with grounded prompt 
          ↓ 
Interface: Gradio web UI


## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will use ChatGPT to help implement the ingestion and review-based chunking pipeline. I will provide my Documents section, Chunking Strategy section, and sample raw document format. I expect it to produce Python functions for loading .txt files, splitting documents by review markers, filtering short reviews, and preserving source metadata. I will verify the output by running python ingest.py, checking the total chunk count, and manually reading sample chunks to make sure they are complete and readable.
**Milestone 4 — Embedding and retrieval:**
I will use ChatGPT to help implement embedding and retrieval with sentence-transformers and ChromaDB. I will provide my Retrieval Approach section and Architecture diagram. I expect it to produce code that embeds chunks, stores them in a persistent ChromaDB collection, and retrieves the top 5 chunks with source metadata. I will verify the output by testing at least three evaluation questions and checking whether the retrieved chunks are actually relevant.
**Milestone 5 — Generation and interface:**
I will use ChatGPT to help connect retrieval to Groq generation and a Gradio interface. I will provide my grounding requirement, expected answer format, and source attribution requirement. I expect it to produce code that answers only from retrieved context and displays both the generated answer and source list. I will verify it by asking both in-scope questions and an out-of-scope question to confirm the system refuses when the documents do not contain enough information.