# Changelog

## 2026-10-12: v2, renamed to Outlier Check

WHAT: Replaced the teardown skill with the version built in the claude.ai conversation. Output is now a one-screen COPY / ADAPT / SKIP verdict with two checks: is the outlier typical of its creator's hits, and does it fit the user's account. Rules are locked before measuring and scored by two blind raters.

WHY: A pre-registered test across two creators showed the single-outlier teardown copies flukes: the 2,254x Reel was built like its creator's flops, and the structure that won for one creator lost for the other.

WATCH FOR: Six videos per channel can rule ideas out but cannot prove rules. The recap cap of 50 videos limits the window to about 6 to 8 weeks for daily posters. Blind raters need subagents; without them the skill self-scores and must say so in the receipts.

## 2026-10-11: Initial release

WHAT: Assembly Teardown skill, ported from the long-form YouTube reference-teardown method onto Sandcastles short-form data. Natural-experiment hunt checks the creator's own remakes first, then cross-creator twins.

WHY: Sandcastles' structure labels vary between runs, so the skill builds its own assembly map from timestamped transcripts. Same-creator remakes are the cleanest twins because audience and face are held constant.

WATCH FOR: `get_channel_recap` returns at most 50 videos, so for daily posters the lookback window may not reach an old original. Start from the outlier's URL so its remakes fall inside the window. Twins under a 3x gap can be distribution noise (an identical video posted twice did 74K and 44K).
