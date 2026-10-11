# Assembly Teardown

A Claude skill that tears down a short-form outlier by how it was **assembled**, not how it was packaged, using live [Sandcastles](https://sandcastles.ai) data.

Most people see a viral video, copy the hook, and get nothing, because the hook usually isn't what carried it. This skill finds a natural experiment (the same creator or the same hook, wildly different results), diffs how each video was assembled beat by beat, and hands back a beat sheet for your next video built on what actually worked.

It's a short-form port of the reference-teardown method I run on clients' long-form YouTube references. Same laws, new data layer.

## What it does

1. **Finds the natural experiment.** It checks the creator's own remakes first, then other creators using the same hook or topic. Same package, different result means the assembly carried it.
2. **Reads what the video was built for** (awareness, followers, leads or sales) against your goal.
3. **Maps both assemblies beat by beat** from the timestamped transcripts: value structure, what's withheld and when it pays off, and every retention beat, tagged HOLD or LEAK.
4. **Rules every finding** BORROW, ADAPT or DISCARD, plus what doesn't transfer (their audience, face, timing).
5. **Hands back a beat sheet** for your account's next video.

## Example

On Sean Johnson's (@intentionally_) luck Reels: the original did 2.4M views (2,254x his average). His own remake on the same topic, set and length did 13.9K. The winner delivered its first piece of value at 0:03; the remake made viewers wait until 0:41. The topic didn't carry it. The assembly did.

## Install

1. Connect the Sandcastles MCP to Claude: https://sandcastles.ai/mcp
2. Download this repo as a zip (or zip the folder containing `SKILL.md`).
3. In claude.ai: Settings → Capabilities → Skills → Upload skill.

## Use

> Use the assembly-teardown skill on this Reel: [URL]. My account is @handle, niche is [one line], goal is [followers / leads / sales / awareness].

Built by [Diego Oliverio](https://diego-oliverio.com).
