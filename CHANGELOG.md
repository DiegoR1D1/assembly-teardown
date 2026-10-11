# Changelog

## 2026-10-11: Initial release

WHAT: Assembly Teardown skill, ported from the long-form YouTube reference-teardown method onto Sandcastles short-form data. Natural-experiment hunt checks the creator's own remakes first, then cross-creator twins.

WHY: Sandcastles' structure labels vary between runs, so the skill builds its own assembly map from timestamped transcripts. Same-creator remakes are the cleanest twins because audience and face are held constant.

WATCH FOR: `get_channel_recap` returns at most 50 videos, so for daily posters the lookback window may not reach an old original. Start from the outlier's URL so its remakes fall inside the window. Twins under a 3x gap can be distribution noise (an identical video posted twice did 74K and 44K).
