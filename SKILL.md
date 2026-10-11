---
name: assembly-teardown
description: Tear down a short-form outlier by how it was ASSEMBLED, not how it was packaged, using live Sandcastles data. Finds "natural experiments" (videos with the same hook or topic and very different results), diffs their value structure, sequencing and retention beats to isolate what actually carried the winner, then rules BORROW, ADAPT or DISCARD and hands back a beat sheet for the user's own video. Use when the user says "tear this down", "why did this blow up", "what actually made this work", "assembly teardown", or pastes a Reel, TikTok or Short URL.
---

# Assembly Teardown

Short-form port of my YouTube reference-teardown skill, which I run on client references. Same laws, new data source.

The belief it runs on: the DNA of high-performing content is how the information is assembled and delivered. Packaging is the entry fee. Most people see an outlier, copy the hook and the caption, and get nothing, because the hook was not what carried it. This skill watches the content so you do not stop at the package.

Requires the Sandcastles MCP. Every number, hook and transcript line must come from a tool call. Never invent one.

## Laws

1. **A score tells you something worked, not what.** The multiple is the entry ticket. The finding is which layer produced it.
2. **The natural experiment settles it.** Two videos with the same package and very different results are an A/B test someone already ran. Find one before reasoning.
3. **Format is not value structure.** Format is the delivery (talking head, green screen, voiceover B-roll, skit). Value structure is what fills it (listicle, story, myth-bust, tutorial, case study). Sequencing is the order of reveal. Read all three separately.
4. **Topic or mechanic sets the evidence bar.** Taking a topic needs at least three INDEPENDENT creators overperforming on it. Taking a mechanic (a structure, a sequence, a device) only has to fit the user's account.
5. **No private data is visible.** Short-form retention curves are private. Every retention read here is a prediction from the assembly, labelled as one.
6. **Read the transcript, not the label.** Sandcastles' format types and section splits are AI summaries and vary between runs: the same video posted twice came back as "tutorial" with 5 sections and "breakdown_explainer" with 4. Build the assembly map yourself from `transcript_sentences` and each section's `start_second` / `end_second`. Treat Sandcastles' labels as hints.
7. **Respect the noise floor.** The identical video posted twice, 23 seconds apart, did 74K and 44K. A gap under 3x between twins can be distribution luck. Only call it a natural experiment when the gap is well beyond that, and say how far.

## Step 0. The user's account

Use the handle, niche and goal (followers, leads, sales or awareness) if the user gave them. Ask once only for what is missing. Call `get_channel_recap` on their handle, passing `platform` when known. That is THE BASELINE.

## Step 1. The outlier

If the user gave a URL: try `get_video_details` first, and only call `analyze_video` (1 credit) if it comes back without an analysis. Otherwise use `search_my_videos` and take the strongest performer relative to its own creator's median. Call `get_channel_recap` on the creator so the multiple is measured against THEIR median.

## Step 2. Gate 1: package or assembly?

From `get_video_details`, note its `spoken_hook_madlib`, format, narrative structure and topic.

Hunt the natural experiment, cleanest source first:

1. **The creator's own remakes.** Call `get_channel_recap` on the creator with `lookback_days` 365 and `limit` 50, and look for videos on the same topic. Same creator, same audience, same face: the only thing left to differ is the assembly. A repost of the identical recording is not a twin; it is a repeatability check.
2. **Other creators.** Run `search_all_videos` with the topic as the query, and `top_hooks` (scope all) to find other videos using the same hook madlib.

Pull 2 to 4 twins whose package matches (same madlib or same topic and format) but whose multiple is far lower. `get_video_details` on each.

Rule which layer carried it:
- **Package**: the twins underperform even with the same assembly, or the hook is the only difference.
- **Assembly**: same package, different assembly, different result. This is the answer more often than the multiple suggests.
- **Creator**: no twin explains the gap and the creator's own audience is the engine. Does not transfer.

Put the outlier and its twins in one table: creator, multiple, madlib, format, value structure.

## Step 3. Gate 2: what was it built for?

Read the CTA (comment keyword, follow, link, none), the offer behind it and the narrative structure. Awareness, followers, leads or sales. Flag any mismatch with the user's goal.

## Step 4. The assembly map

Beat by beat from the analysis and transcript, for the outlier and its best twin side by side:

- **Value structure** and whether it is a forced sequence (each beat depends on the last) or a leavable list.
- **Sequencing**: what is withheld, and when it is paid.
- **Retention beats**, tagged with these codes only:
  HOLD: `HOOK_CONFIRM` (first line pays off the visual stop), `OPEN_LOOP`, `PAYOFF`, `RE_HOOK`, `PATTERN_INTERRUPT`, `PROOF`, `BOOKEND`
  LEAK: `PROMISE_DIVERGENCE`, `CONFUSION`, `FLUFF`, `BARE_SEAM`
- **Format fit**: does the delivery match how this niche already consumes?

Then the diff: the 1 to 3 assembly differences that best explain the gap between the outlier and its twin.

## Step 5. Gate 3 and the ledger

Max 8 rows. Each row states the mechanism, not the artifact (if it names the outlier's topic, it is not abstracted yet), labels itself MECHANIC or TOPIC, and gets a verdict:

- **BORROW**: transfers as is.
- **ADAPT**: the mechanism transfers, the execution changes. Say what changes for this account.
- **DISCARD**: belongs to the creator, mismatches the goal, or rests on an advantage the user does not have.

Then **what this video does not teach**: the creator's audience, face, budget, trend window or luck.

## Output

One artifact, white background, blue accents:

1. Baseline strip: the user's handle, median views, goal.
2. The natural experiment: outlier vs twins table, with the verdict on which layer carried it.
3. The assembly map, outlier and twin side by side, beats tagged HOLD or LEAK.
4. The ledger.
5. **Your beat sheet**: the user's next video, built on every BORROW and ADAPT row: hook line, format, value structure, sequence of beats with the retention job of each, CTA matched to their goal.
6. Sources: every tool call used.
