# Outlier Check

A Claude skill that answers one question: **should I copy this viral video, and if so, what exactly?**

Paste a viral Reel, TikTok or Short and your own account. Using live [Sandcastles](https://sandcastles.ai) data, it returns one screen: a **COPY / ADAPT / SKIP** verdict, the moves worth taking, and a beat sheet for your next video.

## Why

People see an outlier, copy the hook, and get nothing, because the hook usually isn't what carried it. Building this surfaced two findings that shape every verdict:

- **Outliers can be flukes on their own channel.** A 2,254x Reel was built like its creator's flops, not his hits. Copying it would have copied the exception.
- **What wins on one account can lose on another.** On one creator, lists won and single-idea videos flopped. On a second account, the exact opposite.

So the skill runs two checks before it borrows anything: is this outlier typical of *their* hits, and does its structure fit *your* winners?

## How it stays honest

- **Reads the transcript, not the labels.** The same recording analysed twice came back with different topics, hook templates and section splits. Labels are hints; transcripts are evidence.
- **Respects the noise floor.** The identical video, posted twice, did 2.4M and 202K. Gaps smaller than that are distribution, not content.
- **Locks the rules before measuring,** then scores anonymised transcripts with two blind raters. Disagreements are marked SPLIT, never resolved toward the hypothesis.

## Origin

A short-form port of the reference-teardown method I run on clients' long-form YouTube references before we script. Same laws, new data layer.

## Install

1. Connect the Sandcastles MCP to Claude: https://sandcastles.ai/mcp
2. Download this repo as a zip.
3. In claude.ai: Settings → Capabilities → Skills → Upload skill. Code execution must be on.
4. Add `storage.googleapis.com` under Settings → Capabilities → Additional allowed domains, so the page can show real Reel covers.

## Use

> Run the Outlier Check on [URL] for @yourhandle.

A full run costs up to 13 Sandcastles credits, and it tells you the cost before spending anything.

Built by [Diego Oliverio](https://diego-oliverio.com) with Claude.
