---
name: md2wechat
description: Convert Markdown to WeChat Official Account HTML. Use this whenever the user wants WeChat article conversion, local preview, draft upload, image upload, cover or infographic generation, image-post creation, writer-style drafting, AI trace removal, or capability/theme/provider/prompt inspection before running the workflow.
---

# MD to WeChat

Use `md2wechat` for WeChat Official Account article workflows:

- Convert Markdown into WeChat-compatible HTML.
- Inspect article metadata, readiness, and publish risks.
- Generate local preview artifacts.
- Upload article images or create WeChat drafts when explicitly requested.
- Generate covers, infographics, or other article images when explicitly requested.
- Create image-first posts instead of standard article drafts.
- Use writer-style or humanizer commands.
- Inspect live capabilities, providers, themes, prompts, and layout modules.

## Intent Routing

Choose the target workflow before running publish or upload actions.

- Use `inspect`, `preview`, and `convert` for standard WeChat article drafts, HTML conversion, metadata checks, or previews.
- Use `create_image_post` for image-first posts, multi-image posts, newspic-style posts, or when the user asks for an image-led social post rather than an HTML article draft.
- Do not route image-first post requests to `convert --draft` just because the source content is Markdown. A Markdown file can still be input to `create_image_post -m article.md`.
- Treat `convert --draft` and `create_image_post` as different publish targets.

## CLI Resolution

Resolve the executable before running workflow commands.

1. Try `md2wechat`.
2. On Windows/Codex, if `md2wechat` is not found or the PowerShell shim is blocked, try the npm `.cmd` shim:
   - `%APPDATA%\npm\md2wechat.cmd`
   - Common example: `C:\Users\<user>\AppData\Roaming\npm\md2wechat.cmd`
3. Do not use `md2wechat.ps1` on Windows when PowerShell execution policy blocks scripts.
4. If no installed CLI is available, fall back to `npx.cmd --yes @geekjourneyx/md2wechat`.
5. In Codex sandboxed shells, npm global directories or npm cache access may require an escalated shell command.
6. Treat live CLI output as the source of truth. Do not guess provider names, theme names, prompt names, models, or command flags from repository files alone.

When giving examples in this skill, `md2wechat` means the resolved executable from the steps above.

## Data Transfer Boundaries

Separate local-only actions from actions that may transmit content.

- Local-only by default: `inspect`, `preview`, and plain `convert --preview` without upload/draft flags.
- May transmit article text to configured services: `convert --mode ai`, API conversion modes, writer-style commands, and humanizer commands.
- May transmit images or files: `--upload`, `--draft`, `upload_image`, `download_and_upload`, `generate_image`, `generate_cover`, `generate_infographic`, and `create_image_post`.
- May publish or create remote state: `convert --draft`, `create_draft`, and `create_image_post`.

Run transfer actions only when the user explicitly asks for that operation and destination class. Draft creation, image-post creation, publishing, upload, and remote image generation require explicit user intent.

## Local-First AI Theme Workflow

For themes whose resolved theme type is `ai`, use a local-first workflow by default.

- Do not run remote AI conversion for AI themes unless the user explicitly allows external AI processing for the article text.
- Do not run `preview --mode ai`, `convert --mode ai`, or any command path that may implicitly send article text to a remote model for an AI theme by default.
- Treat the theme YAML as the output style specification, not as approval to transmit article text.
- Before converting an AI theme, look for a local converter script that implements the theme, such as `tools/generate_ocean_preview.py` for `ocean-calm-safe`, or a future `tools/generate_<theme>_preview.py` equivalent.
- If a local script exists, inspect it before use. Verify that it matches the theme requirements, uses inline styles, handles local images safely, preserves or implements image captions when required, and does not call remote AI, upload files, create drafts, or transmit article text.
- If the local script is correct, use it directly to generate the preview HTML.
- If the local script is missing or does not match the theme requirements, create or fix the local script first, then run it.
- For draft creation after a local AI-theme conversion, use the local HTML as the source of truth. Upload and replace images only after the user explicitly asks for draft creation or image upload.

## Defaults And Config

- Draft upload and publish-related actions require `WECHAT_APPID` and `WECHAT_SECRET`.
- Image generation may require provider config in `~/.config/md2wechat/config.yaml`.
- `convert` defaults to `api` mode unless the user explicitly asks for `--mode ai`.
- Check config in this order:
  1. `~/.config/md2wechat/config.yaml`
  2. environment variables such as `MD2WECHAT_BASE_URL`
  3. project-local `md2wechat.yaml`, `md2wechat.yml`, or `md2wechat.json`
- If the user asks to switch API domain, change `api.md2wechat_base_url` or `MD2WECHAT_BASE_URL`.
- Validate config before draft creation, upload, image-post creation, or publish-like actions.

## Discovery First

Run discovery before selecting a provider, theme, model, or prompt:

```bash
md2wechat version --json
md2wechat capabilities --json
md2wechat providers list --json
md2wechat themes list --json
md2wechat prompts list --json
md2wechat prompts list --kind image --json
md2wechat prompts list --kind image --archetype cover --json
```

Inspect a specific resource before using it:

```bash
md2wechat providers show openrouter --json
md2wechat providers show volcengine --json
md2wechat themes show ocean-calm --json
md2wechat prompts show cover-default --kind image --json
md2wechat prompts show cover-hero --kind image --archetype cover --tag hero --json
md2wechat prompts show infographic-victorian-engraving-banner --kind image --archetype infographic --tag victorian --json
md2wechat prompts render cover-default --kind image --var article_title='Example' --json
```

When choosing image presets, prefer `prompts show --json`, especially `primary_use_case`, `compatible_use_cases`, `recommended_aspect_ratios`, and `default_aspect_ratio`.

When choosing an image model, prefer `providers show <name> --json` and read `supported_models` before hard-coding `--model`.

## Core Commands

Configuration:

- `md2wechat config init`
- `md2wechat config show --format json`
- `md2wechat config validate`

Article conversion:

- `md2wechat inspect article.md`
- `md2wechat inspect article.md --json`
- `md2wechat preview article.md`
- `md2wechat preview article.md --json`
- `md2wechat convert article.md --preview`
- `md2wechat convert article.md -o output.html`
- `md2wechat convert article.md --title "New Title" --author "Author" --digest "Digest"`
- `md2wechat convert article.md --mode ai --theme ocean-calm --preview`
- `md2wechat convert article.md --draft --cover cover.jpg`

Image handling:

- `md2wechat upload_image photo.jpg`
- `md2wechat download_and_upload https://example.com/image.jpg`
- `md2wechat generate_image "A cute cat sitting on a windowsill"`
- `md2wechat generate_image --preset cover-hero --article article.md --size 2560x1440`
- `md2wechat generate_cover --article article.md`
- `md2wechat generate_infographic --article article.md --preset infographic-comparison`
- `md2wechat generate_infographic --article article.md --preset infographic-dark-ticket-cn --aspect 21:9`
- `md2wechat generate_infographic --article article.md --preset infographic-handdrawn-sketchnote`

Drafts and image posts:

- `md2wechat create_draft draft.json`
- `md2wechat test-draft article.html cover.jpg`
- `md2wechat create_image_post --help`
- `md2wechat create_image_post -t "Weekend Trip" --images photo1.jpg,photo2.jpg`
- `md2wechat create_image_post -t "Travel Diary" -m article.md`
- `md2wechat create_image_post -t "Test" --images a.jpg,b.jpg --dry-run`

Writing and humanizing:

- `md2wechat write --list`
- `md2wechat write --style dan-koe`
- `md2wechat write --style dan-koe --input-type fragment article.md`
- `md2wechat write --style dan-koe --cover-only`
- `md2wechat write --style dan-koe --cover`
- `md2wechat write --style dan-koe --humanize --humanize-intensity aggressive`
- `md2wechat humanize article.md`
- `md2wechat humanize article.md --intensity gentle`
- `md2wechat humanize article.md --intensity aggressive`
- `md2wechat humanize article.md --intensity authentic`
- `md2wechat humanize article.md --show-changes`
- `md2wechat humanize article.md -o output.md`

Humanizer intensity levels: `gentle`, `medium` default, `aggressive`, and `authentic`.

Use `authentic` when the goal is natural skilled human writing, concrete expression, stable tone, and no performative depth. Use other intensities when the goal is mostly AI-trace cleanup.

## Article Metadata Rules

For `convert`, metadata resolution is:

- Title: `--title` -> `frontmatter.title` -> first Markdown heading -> unnamed fallback.
- Author: `--author` -> `frontmatter.author`.
- Digest: `--digest` -> `frontmatter.digest` -> `frontmatter.summary` -> `frontmatter.description`.

CLI limits:

- `--title`: max 32 characters.
- `--author`: max 16 characters.
- `--digest`: max 128 characters.

Digest writing:

- Prefer explicit metadata when present: `digest`, then `summary`, then `description`.
- If no usable digest metadata exists, write a concise digest from the actual article content each time.
- Do not use a fixed digest template across articles.
- Do not invent claims, topics, outcomes, names, dates, or categories that are not supported by the article.
- Keep the digest within the CLI limit and make it useful as draft metadata, not body copy.

Draft behavior:

- If digest is empty when creating a draft, the draft layer generates one from article HTML content with a 120-character fallback.
- Creating a draft requires either `--cover` or `--cover-media-id`.
- `--cover` is a local image path for article drafts.
- `--cover-media-id` is for an existing WeChat permanent cover asset.
- Do not assume a WeChat image URL or `mmbiz.qpic.cn` URL can be reused as `thumb_media_id`.
- `--title`, `--author`, and `--digest` affect draft metadata, not necessarily visible body HTML.

Draft creation from local HTML:

- Use this path when the article HTML was generated locally, especially for local-first AI themes.
- Validate config before upload or draft creation.
- Upload local article images only after the user explicitly asks for upload or draft creation.
- After upload, rewrite every local `<img src="...">` in the HTML to the returned WeChat image URL.
- Verify that the final draft HTML has no remaining local image paths before creating the draft.
- Use a valid uploaded image `media_id` as `thumb_media_id`; do not use the WeChat image URL as `thumb_media_id`.
- Build a draft JSON with title, digest, content, `thumb_media_id`, and comment settings, then call `create_draft`.
- Write draft JSON as UTF-8 without BOM.
- Ensure JSON string fields remain strings; do not let shell serialization convert HTML content into an object.

## Preview Rules

- `inspect` is the source-of-truth command for resolved metadata, readiness, and checks.
- `preview` writes a standalone local HTML preview file. It does not write back to Markdown, upload images, or create drafts.
- `convert --preview` is the convert-path preview flag. It is not the same command as standalone `preview`.
- `preview --mode ai` is degraded confirmation only. Do not treat it as final AI-generated layout.
- Markdown images are only uploaded or replaced during `--upload` or `--draft`, not during plain preview commands.
- If a Markdown file has no document title and starts with a section heading, pass `--title` explicitly when converting or drafting.

## Layout Modules

Advanced layout modules use `layout` commands and `:::block` syntax.

- Discover modules with `md2wechat layout list --json`.
- Inspect a module with `md2wechat layout show <name> --json`.
- Render a module with `md2wechat layout render <name> --var key=value --json`.
- Validate block syntax with `md2wechat layout validate --file article.md --json`.
- Prefer a small number of modules. Use one module only when it materially improves attention, readability, memorability, or conversion.
- Do not assume layout modules work in every conversion mode. Verify current CLI capabilities and conversion output.

Useful discovery examples:

```bash
md2wechat layout list --serves attention --json
md2wechat layout show hero --json
md2wechat layout render hero --var eyebrow=DeepDive --var title="The Real Question" --json
md2wechat layout validate --file article.md --json
```

## Agent Rules

- Start with CLI resolution and discovery before committing to a provider, theme, prompt, or model.
- Prefer the confirm-first article flow: `inspect` -> `preview` -> `convert` or `--draft`.
- Use `--title`, `--author`, and `--digest` when the inferred metadata is wrong or incomplete.
- Prefer `generate_cover` or `generate_infographic` over raw `generate_image` when a bundled preset fits the task.
- If draft creation returns `45004`, check digest, summary, and description before assuming the body content is too long.
- If the user asks for AI conversion or style writing, be explicit that the workflow may call configured external model services.
- Do not create drafts, upload images, create image posts, publish, or generate remote images unless the user asked for that operation.
- Do not save or expose credentials. Use existing config or environment variables.

## Capabilities Summary

- Reads local Markdown files and local images.
- May download remote images when asked.
- May call external AI or image-generation services when configured and requested.
- May upload HTML, images, drafts, and image posts to WeChat when explicitly requested.
