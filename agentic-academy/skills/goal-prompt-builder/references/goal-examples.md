# Goal Examples

Load this file only when the user asks for examples or when adapting one of these exact patterns.

## Company Research From A Spreadsheet

```text
/goal Read the company list from [SOURCE SPREADSHEET OR EXCEL FILE]. Research every company in the list and create or update a Google Sheet called [OUTPUT SHEET NAME] with one completed row per company.

The work is done when:
- Every company from the source list has exactly one row in the output sheet.
- Each row includes: company name, website, what the company is, problem it solves, product it sells, who it serves, source links, confidence level, and unverifiable notes.
- Every factual claim has at least one source link.
- Any missing or unverifiable detail is marked clearly instead of guessed.
- You surface a final count: total companies in source list, total rows completed, total rows with unverifiable fields, and any companies skipped.

Do not:
- Invent company details, customer segments, products, traction, pricing, or metrics.
- Add companies that are not in the source list.
- Overwrite the original source sheet.
- Use unsourced social posts as the only evidence for a claim.

Only use or touch:
- The source spreadsheet or Excel file I provide.
- The output Google Sheet.
- Company websites, product pages, docs, pricing pages, reputable databases, and recent public sources.

If a check fails:
- If a company detail cannot be verified, search for a primary source first.
- If no reliable source exists, leave the field blank or mark it as unverified.
- If a company has the same name as another company, use the website or context from the source sheet to disambiguate.
- If the output row is incomplete, fix that row before moving on.

Stop when:
- All companies have been processed and the completion count matches the source list.
- Or stop after 40 turns and report what is finished, what is blocked, and which rows still need human judgment.
```

## Landing Page Build

```text
/goal Build a single-page responsive landing page as one self-contained index.html for the Claude Code Goal Kit. The offer is a free download: a folder with a completion-criteria template and 3 ready /goal recipes for research, writing, and landing pages. The page should help people make Claude finish long tasks without babysitting and capture an email in exchange for the kit.

Use these proof points in the page:
- Problem stats: 5 re-prompts before one long task is finished, 40 minutes spent supervising a single multi-step run, and 70% of runs stopping before the task meets the real definition of done.
- Credibility: [YOUR NAME] writes [YOUR PUBLICATION] for [AUDIENCE SIZE] readers, and the kit can be pasted in 60 seconds.
- Proof stats: re-prompts dropped from 5 to 1 after using the criteria template, 9 of 10 test runs finished to spec without a manual nudge, and 35 minutes of supervision time was recovered per run on average.

The work is done when:
- index.html exists and contains all required landing page sections in order: headline, problem, agitate, credibility, solution, proof, and CTA.
- The page includes a viewport meta tag and opens cleanly in a browser.
- The CTA is benefit-led and does not default to "Sign up" or "Submit".
- The Problem, Credibility, and Proof sections use the specific numbers provided above.
- You surface a section-by-section checklist proving each section is present.
- You surface 3 headline variants, the one you chose, and why it carries the emotional payoff.
- You surface the So-What chain for the core benefit: Feature -> Functional -> Financial -> Emotional.

Do not:
- Invent metrics, testimonials, customer numbers, revenue numbers, or performance claims beyond the numbers provided.
- Change the offer, price, audience, or promise unless those changes are clearly marked as suggestions.
- Hide missing proof behind vague language like "many," "lots," or "save time."
- Polish the page before fixing missing sections, broken layout, or weak proof.

Only use or touch:
- The landing page file you create.
- The source material I provide about the Claude Code Goal Kit offer, audience, and proof.
- Any local assets I explicitly provide.

If a check fails:
- If a required section is missing, add that section before editing the rest of the page.
- If a claim needs a number and no real number is provided, use a bracketed placeholder instead of inventing one.
- If the page does not render, fix the HTML or CSS and check again.
- If the CTA is generic, rewrite it around the benefit the reader gets after downloading the Claude Code Goal Kit.

Stop when:
- The page renders cleanly, all required sections are present, and the proof checklist is complete.
- Or stop after 15 turns and report what is finished, what still fails, and what needs human judgment.
```

## Newsletter Repurposing Queue

```text
/goal Repurpose every newsletter post in [SOURCE FOLDER OR SOURCE SHEET] into platform-specific social drafts. For each source newsletter, create 5 LinkedIn posts, 10 Substack Notes, and 3 Twitter threads.

The work is done when:
- Every source newsletter has exactly 18 outputs: 5 LinkedIn posts, 10 Substack Notes, and 3 Twitter threads.
- Each output is tagged with the source newsletter title, source file name, platform, output type, and draft number.
- LinkedIn posts are saved in [LINKEDIN OUTPUT FOLDER OR SHEET].
- Substack Notes are saved in [SUBSTACK NOTES OUTPUT FOLDER OR SHEET].
- Twitter threads are saved in [TWITTER OUTPUT FOLDER OR SHEET].
- You surface a completion table showing each source newsletter and the count of LinkedIn posts, Substack Notes, and Twitter threads created.
- You surface a final total: source newsletters processed, LinkedIn posts created, Substack Notes created, Twitter threads created, total outputs created, skipped sources, and failed outputs.

Do not:
- Merge two newsletter sources into one output.
- Create outputs that are not tied back to a source newsletter.
- Reuse the same hook across multiple outputs unless it is intentionally marked as a variation.
- Change the author's core argument or invent a new claim that was not in the source.
- Treat the same format rules as interchangeable across LinkedIn, Substack Notes, and Twitter.

Only use or touch:
- The source newsletters in the folder or sheet I provide.
- The output folders or sheets I specify.
- The platform rules I provide for LinkedIn, Substack Notes, and Twitter.

If a check fails:
- If a source newsletter has fewer than 5 LinkedIn posts, 10 Substack Notes, or 3 Twitter threads, create the missing outputs before moving on.
- If an output is not tagged to a source, add the source tag before counting it as complete.
- If an output does not match the platform rules, revise that output before creating more.
- If two outputs are too similar, rewrite one with a different angle.

Stop when:
- The completion table shows every source newsletter has 5 LinkedIn posts, 10 Substack Notes, and 3 Twitter threads.
- Or stop after 50 turns and report the completed sources, incomplete sources, failed outputs, and what needs human judgment.
```
