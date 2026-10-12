---
name: "outlier-check"
description: "Use when someone shares a viral or outlier short-form video (Reel, TikTok, Short) and asks whether to copy it, what to take from it, or how to use it for their own account. Gives a COPY / ADAPT / SKIP verdict and their next video, using Sandcastles data."
---

# Outlier Check

This skill answers one question: **should I copy this viral video, and if so, what exactly?**

Inputs: an outlier video URL and the user's own account (handle and platform). Optional: the goal of the next video (for example signups, leads or follows), and a credit cap. The default cap is 13.

Output: **one screen**, not a report. It has five blocks: Verdict, Is it typical?, Does it fit me?, What to take, and My next video. Receipts sit collapsed at the bottom.

## Why this exists

People see an outlier, copy the hook, and get nothing. The hook usually isn't what carried it.

Two findings from building this method:
- **One outlier was a fluke on its own channel.** A 2,254x Reel was built like that creator's flops, not like his hits. Copying it would have copied the exception.
- **What wins on one account can lose on another.** On creator A, lists won and single-idea videos flopped. On creator B the pattern was reversed. So every verdict needs two checks: is it typical for *them*, and does it fit *me*.

The method runs under the hood but stays honest:
- read the transcript, not the labels
- respect the noise floor
- lock the rules before measuring

## Data source: Sandcastles MCP only

If the Sandcastles tools aren't connected, say so and stop. Don't fall back to browsing; the method depends on this data.

- `analyze_video(url | video_uuid)` costs 1 credit for a new video and 0 if the video is already in the library. It always returns `still_analyzing`, so poll `get_video_details` every ~30 seconds until `analyzed: true`.
- `get_video_details(uuid)` returns metrics plus `analysis.narrative_structure.structure_sections[]`, which holds the transcript sentences with section start and end seconds.
- `get_channel_recap(channel, limit=50, lookback_days=365, platform)` returns at most 50 videos.
  - Its output can be too large to return inline and gets saved to a file. Parse that file with python or jq, and read all of it.
  - The `title` field often holds the full caption. Some creators put the whole script in their captions.
- `get_credit_usage()` reports the remaining credits.

### Trust rules (tested by analysing the same recording twice)

**Use as evidence:**
- transcript sentences
- big section boundaries
- views, likes, comments and publish date

**Treat as hypotheses only, never as findings:**
- topic, seed, summary and supporting evidence
- hook category, mad-lib and hook-alignment advice
- format labels
- middle section boundaries

These changed between two runs on identical content.

**Other rules:**
- **Proper nouns:** fact-check every name, study or date from a transcript before it goes into a script. Transcription errors land in different places on each run.
- **Outlier score:** Sandcastles' relative score. Always compute your own median views from the recap rows as the baseline.
- **Not available:** shares, saves, retention and on-screen text. Never claim anything about them.

## Procedure

Add a task list for these steps. Before spending any credits, tell the user the estimated credit cost in one line. Work in a scratch folder and keep every intermediate file, because they become the receipts.

### 1. Pull the outlier and both channels

1. Analyse the outlier, then get its details: views, outlier score, publish date, channel UUID and transcript.
2. Recap the outlier's channel ("theirs") and the user's channel ("mine"), each with limit 50 and lookback 365.
3. Compute the median views for each channel from the recap rows.
4. Note the date window each recap covers. The 50-video cap usually means about 6–8 weeks.

### 2. Lock the rules before reading any transcript

Write `00_locked_rules.md` with a timestamp before any transcript other than the outlier's is read. It contains everything in this step and the next two.

**Exclusions**, applied to both channels:
- rows with zero views (removed or unscraped)
- posts under 7 days old, because their views are still climbing
- pure promos or announcements with no teaching content
- reposts or duplicates of the outlier: same title or caption, or a matching transcript

Reposts are excluded from selection but used for the noise floor (step 3).

**Dedupe:** collapse re-cuts and reposts of any video (same caption, or a matching transcript) into one entry, keeping the higher score, before picking the top 3 and bottom 3.

**Selection on each channel:**
- the top 3 and bottom 3 eligible videos by outlier score, excluding the outlier itself
- ties go first to videos already analysed (0 credits), then to the most recent

**Same source on both sides:** score the outlier from the same source as the videos it is compared against. If a grid is classified from captions, classify the outlier from its caption too, and report both readings when they differ (for example a short spoken script with a 10-item list in the caption).

**Free shortcut:** if a creator's captions run to 80 words or more and read as the spoken script, classify their full eligible grid on M4 from the captions at no credit cost. Check that the caption labels match the transcript labels on the 6 analysed videos. If they disagree, drop the shortcut.

**Metrics.** Apply these literally:
- Sentence start times are interpolated by word count:
  `section_start + (words before the sentence in its section ÷ words in the section) × section duration`.
- **M1 · Seconds to first real value.** The start time of the first sentence that gives:
  - (a) a specific instruction the viewer could carry out,
  - (b) a claim carrying a reason, mechanism, fact or number, or
  - (c) a definition that states what X actually is.
  - These count as promises, not value: headlines or bare stances that restate the title ("X is a trap"), "It's called X" naming lines, "here's how" lines, setups, stories and credentials.
  - Also report the sentence index.
- **M2 · Who the opening is about.** Label every sentence that starts in 0–10s as VIEWER ("you", an imperative, or the viewer's situation), CREATOR (I/me/my, the creator's story or credentials) or NEUTRAL. The metric is the VIEWER share of the non-neutral sentences.
- **M3 · Instruction count.** Sentences that tell the viewer to do something specific and doable this week.
  - Don't count: generic exhortations, "examples would be…" lists, questions posed to the viewer, or comment-keyword CTAs.
  - A sentence that lists several actions counts once.
- **M4 · ONE or LIST.** ONE is a single thesis that every section serves. That includes one procedure whose steps belong to one method, and up to 2 supporting tips. LIST is 3 or more items that could each stand alone as their own video.

**Predictions.** Write down the expected direction for each metric on each channel. If the user has a theory, use theirs.

**Thresholds.** On a channel, a metric DISCRIMINATES if at least 5 of the 6 videos fall on the predicted side of a threshold set in advance. Defaults:
- M1: ≤5s
- M2: >50%
- M3: ≥3
- M4: ONE vs LIST

Record whether the result HELD, BROKE (4 or fewer of 6) or was NOISE.

### 3. Noise floor

- Reposts are the strongest evidence this skill has, and they outrank every metric. Apply these rules literally:
  - **Repost fluke:** the best repost of the outlier got under 20% of its views AND its own outlier score is below the channel's top-3 cutoff. The words didn't carry it.
  - **Repost proven:** a repost scored at or above the top-3 cutoff. The script travels.
  - **No reposts:** fall back to the metrics in steps 5 and 6.
- **Repeatable scripts:** on the outlier's channel, find any other script that scored at or above the top-3 cutoff on two or more posts. Name the best one in the verdict as the Reel worth studying instead.
- If a repost of the outlier exists, report `outlier views ÷ repost views`. That gap is distribution, not content. The repost's own outlier score is the content-adjusted signal.
- If the outlier's score is below the 90th percentile of eligible scores on its channel, it's a good day, not an outlier. Say so; the verdict is at most ADAPT.
- Never credit an assembly feature with a difference smaller than an observed noise floor.
- Record distribution triggers the transcript can't measure: a comment-keyword CTA ("Comment X and I'll send you…"), a list carried in the caption, an unusually high comment rate. Flag them as possible drivers; never score them.
- With 6 videos per channel, metrics can rule ideas out but can't prove rules. Say "pattern", never "law".

### 4. Blind scoring

For the outlier plus the 6 videos per channel:
1. Write the transcripts as `[start–end] sentence | sentence` lines under random IDs. Leave out titles, views and scores.
2. Precompute the first-10s sentences for M2.
3. Spawn **two independent rater subagents** with the rules file. Use the rater prompt below.

If you can't spawn subagents, score them yourself from the anonymised file only, and say so in the receipts.

- When raters disagree on a verdict-relevant metric, mark it SPLIT and don't use it.
- Never resolve a disagreement toward the hypothesis.

**Rater prompt:**

> You are a blind rater. Read only [rules file] and [transcripts file]. Don't search or open any other file. You know nothing about performance; don't guess. For each video return JSON: `m1_sentence` (exact text or NONE) with a one-line reason, `m2` (labels for the listed first-10s sentences), `m3_sentences` (exact texts) and `m3_count`, and `m4` (ONE/LIST) with a reason. Be strict and consistent across videos.

### 5. Is it typical? (theirs)

Reposts decide first (step 3): a repost fluke is FLUKE and a proven repost is TYPICAL, whatever the metrics say. Without reposts, use only the metrics that DISCRIMINATE on their channel:
- **TYPICAL:** the outlier sits on the top-3 side for most of them.
- **FLUKE:** the outlier sits on the bottom-3 side for most of them.
- **UNTESTED:** no metric discriminates, or there are fewer than 8 eligible videos.

### 6. Does it fit me? (mine)

Run the same scoring on my top 3 and bottom 3.

1. Find which metrics discriminate on **my** account, and in which direction.
2. Compare each mechanic of the outlier against my winners' side.
3. Also group my recap captions by opening phrase (for example "This is the…", "These are the N…", "The reason your…"). Report n, the median and the range for each group.
   - A hook template whose range runs from below 1x to well above it carries nothing on its own.
   - Openers whose median is below 1x count as evidence against using them.

### 7. Verdict

- **SKIP:** the outlier is a FLUKE on its own channel, however big the number. Also SKIP if every transferable mechanic conflicts with my winners. A SKIP can still say "its structure happens to match your winners". Then build the next video from my own winners, not from the outlier.
- **COPY:** TYPICAL on their channel, and its mechanics match my winners on every metric that discriminates on my account. Copy the *structure*; never the topic or the hook wording.
- **ADAPT:** everything in between. Take only the mechanics that my own data supports.

Also label the verdict **STRONG** (repost evidence, or 2+ metrics discriminating) or **WEAK** (one metric, or a borderline score), and say which evidence leads (`ledBy`). When reposts and metrics disagree, reposts win and the disagreement goes in the receipts.

### 8. What to take (3 moves at most)

Each move is a **mechanic**, phrased as an instruction. Examples: "Name one mechanism and land it by sentence 3" or "No 'I' before 10s; credentials after 20s".

- A move is never the outlier's topic, its claims or its exact hook.
- Each move carries a one-line receipt, for example "your top 3: all single ideas".

Also list up to 2 DISCARDs when they matter, for example "their 38% motivational close: your winners end on a short comment CTA".

### 9. My next video: the production brief

The founder's only questions after reading this block are "what do I film, and what do I say?" Answer both completely, so they can film today without asking anything.

1. **Topic.** One sentence, inside the territory my winners already own. Never the outlier's topic unless the verdict is COPY. Add one line on why it should work, with a receipt from my data.
2. **Format and setup.** The delivery my top 3 share (for example talking head to camera, green screen over a screenshot, walk-and-talk), the setting, and the target length. Read it from my top 3's covers and transcripts; Sandcastles' layout labels are hints only.
3. **Spoken hook.** The exact first line, in the opener family my data supports. Value lands by the time my winners deliver it.
4. **Copy hook.** The on-screen text on the first frame: 3 to 7 words, concrete, no jargon, and it must make the same promise as the spoken hook.
5. **Value structure.** Name its type (for example "one mechanism, proven twice", "myth then correction", "before and after"). State the promise the hook makes, then the sequence of beats. Each beat must depend on the one before, so leaving early feels like missing the payoff.
6. **Talking points.** 3 to 6 points in filming order, written in the second person, one line each. Someone should be able to film from these alone, without a teleprompter.
7. **Script.** Up to 6 beats. Each has a time range, the exact spoken line, and screen direction where the visual proves the point a second before the words say it.
   - Measure my speaking rate from my top video: transcript words ÷ seconds. Keep the total under 60 seconds and state the word count.
   - Put any credential or "I" line where my winners put it. Quote credentials only from my channel description or captions as returned by Sandcastles in this run. Never from memory, past chats or general knowledge, even if they look right. If none is available, write `[YOUR PROOF]` and say so in one line.
8. **Shot list.** Every clip to capture, as a checklist: the main to-camera take and its framing, each screen recording (what to open and what to click), any props or B-roll. Mark the shots the video can't work without.
9. **Caption and comment trigger.** The caption's first line, the comment keyword, and exactly what the DM delivers: a free asset tied to the video's mechanism, plus the user's goal if one was given (for example a tracked link). Don't use a sales CTA unless my data supports it.

Fact-check every number and name in the brief against the receipts.

## The screen

The page is a fixed template, so every run looks the same and reads like Instagram: real Reel covers in profile grids, the verdict as a post, and the next video as a production brief with a Reel storyboard. Never hand-write the page.

1. Write `data.json` in the scratch folder using the schema below. Use the raw Sandcastles `thumbnail` URLs (channel and video); the build script embeds them.
2. Run `python scripts/build_page.py data.json outlier-check.html` from this skill's folder.
3. Publish `outlier-check.html` as the page. If artifacts aren't available, give the user the HTML file and reply with the same five blocks in text.

Covers download from `storage.googleapis.com`. If the sandbox blocks that domain, the page falls back to tiles shaded by outlier score; tell the user once to add `storage.googleapis.com` under Settings → Capabilities → Additional allowed domains.

**Copy rules:** every line is one claim, no paragraphs. Headlines are the finding, not the section name. Numbers carry their unit (views, ×, seconds).

**Schema** (all fields required unless marked optional):

```
meta:     {account, goal, run (date), credits}
verdict:  {call: COPY|ADAPT|SKIP, confidence: STRONG|WEAK, ledBy (e.g. "reposts"), headline (one sentence), detail (one sentence)}
outlier:  {thumb, url, views, score, title, handle, avatar}
reposts:  optional {headline, ratio (e.g. "232×"), note, items: [{thumb, url, views, score, date, title}]}
theirs, mine: {
  handle, avatar, followers, median, reels (count), window (one line on the date range and what is highlighted),
  headline, line,
  grid:    every recap row, newest first: [{thumb, url, views, score, title, role: top|bottom|outlier|repost|""}],
  compare: exactly 7, ordered top 3, outlier, bottom 3: [{thumb, url, views, score, title (short name), role, label (the discriminating metric, e.g. "7 steps" or "ONE · 3.0s"), win (true if on the winners' side), blur (optional)}]
}
movesHeadline, moves: [{move, receipt}] (max 3), discards: [{what, why}] (max 2)
next:     {title, topic, why, format: {delivery, setting, length},
           spokenHook, copyHook, valueStructure: {type, promise, sequence: [beat names]},
           talkingPoints: [strings], shotList: [{shot, detail, mustHave: bool}],
           caption: {firstLine, keyword, delivers},
           facts: [short strings: words, seconds, rate],
           beats: [{time, line, screen, thumb (optional), blur (true for any outlier-creator cover)}]}
receipts: [{title, items: [strings]}] covering locked rules, predictions vs results, selection and exclusions, rater agreement, noise floor, fields used and ignored, credits, limits
sources:  [{label, url, views, score}] for every video measured
```

## Guardrails

- Tell the user the credit cost before spending, and stay within the cap. If a channel needs more, run with what the cap allows and mark it UNTESTED.
- Never show the outlier's channel in a public-facing script beat without blurring the face and handle, unless the user says they have permission.
- If the user's own account has fewer than 8 eligible videos, block 3 reads "Not enough history to test fit", and the verdict is at most ADAPT.
- Don't overclaim. Six videos can break a prediction but can't prove a rule. Say what broke as plainly as what held.
