# Changelog

## 2026-10-12: v2.2, fixed page template with real Reel covers

WHAT: The page is now built from assets/template.html by scripts/build_page.py from a data.json the skill writes. Real Reel covers are embedded as data URIs, laid out like Instagram profile grids, a verdict post and a Reel storyboard.

WHY: Hand-written pages varied run to run and read as generic AI output. Users recognise their own platform's UI faster than charts.

WATCH FOR: Covers need storage.googleapis.com egress from the sandbox; without it the page falls back to shaded tiles. Pages with ~100 covers run about 2.4 MB.

## 2026-10-12: v2.1, fixes from the first fresh run

WHAT: Reposts lead the verdict when they exist. Re-cuts are deduped before selection. Outlier and comparison videos are scored from the same source. Comment-keyword CTAs and caption lists are flagged as possible drivers. Verdicts carry STRONG or WEAK. Credentials come only from the user's own channel, else [YOUR PROOF].

WHY: The first fresh run (a 213x Reel) reached a defensible SKIP but led with a single borderline metric, counted a re-cut twice, compared spoken scripts against captions, and invented a credential for the user.

WATCH FOR: STRONG still means six videos per side. Caption-vs-transcript disagreements will be common on creators who write long captions.

## 2026-10-12: v2, renamed to Outlier Check

WHAT: Replaced the teardown skill with the version built in the claude.ai conversation. Output is now a one-screen COPY / ADAPT / SKIP verdict with two checks: is the outlier typical of its creator's hits, and does it fit the user's account. Rules are locked before measuring and scored by two blind raters.

WHY: A pre-registered test across two creators showed the single-outlier teardown copies flukes: the 2,254x Reel was built like its creator's flops, and the structure that won for one creator lost for the other.

WATCH FOR: Six videos per channel can rule ideas out but cannot prove rules. The recap cap of 50 videos limits the window to about 6 to 8 weeks for daily posters. Blind raters need subagents; without them the skill self-scores and must say so in the receipts.

## 2026-10-11: Initial release

WHAT: Assembly Teardown skill, ported from the long-form YouTube reference-teardown method onto Sandcastles short-form data. Natural-experiment hunt checks the creator's own remakes first, then cross-creator twins.

WHY: Sandcastles' structure labels vary between runs, so the skill builds its own assembly map from timestamped transcripts. Same-creator remakes are the cleanest twins because audience and face are held constant.

WATCH FOR: `get_channel_recap` returns at most 50 videos, so for daily posters the lookback window may not reach an old original. Start from the outlier's URL so its remakes fall inside the window. Twins under a 3x gap can be distribution noise (an identical video posted twice did 74K and 44K).
