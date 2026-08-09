---
name: turn-photo-into-ink-travel-poster
description: Transform an uploaded travel, landscape, architecture, or everyday photograph into a horizontal Chinese ink-wash editorial travel poster with warm rice-paper texture, irregular ink-bleed photo edges, restrained vintage color, calligraphic hierarchy, seal-like accents, and evidence-grounded copy. Use when the user asks to make a photo look like a Chinese ink painting, 宣纸水墨旅行海报, 国风摄影海报, ink-wash editorial poster, or a style matching a reference that combines a preserved photograph with Chinese editorial typography. Enforce that every factual word, place, date, label, and descriptive line comes only from visible image content, OCR, embedded metadata, or text explicitly supplied by the user; never invent or guess copy.
---

# Turn Photo Into Ink Travel Poster

Create one finished bitmap poster from the user's source photo. Preserve recognizable scene geometry and identity while translating its presentation into a quiet Chinese ink-wash travel editorial.

## Workflow

1. Inspect the source at original detail. Record visible subjects, scene relationships, readable text, orientation, and safe negative-space areas.
2. Run `scripts/extract_photo_evidence.py INPUT --output evidence.json`. Treat OCR as unverified until visually checked against the pixels.
3. Build a copy evidence ledger using `references/evidence-and-copy.md`. Add user-supplied facts verbatim and label their source.
   Read `references/examples.md` when choosing copy levels, resolving a missing-evidence case, or adapting the layout to a common photo type.
4. Decide whether the poster can be completed without questions:
   - Continue when all requested proper nouns, dates, and captions are supported.
   - Ask for only the missing fact when the user explicitly expects unsupported factual copy.
   - Omit an optional field when evidence is absent. Never fill space with a guess.
5. Draft the exact text before image generation. Every clause must map to one or more ledger entries. Prefer short literal or modestly poetic observations grounded in visible content.
6. Use the image-generation/editing tool with the source photo as a reference. Supply the exact approved text in the prompt and explicitly forbid any other legible characters.
7. Inspect the output at original detail. Verify scene fidelity, spelling, dates, place names, and that no stray pseudo-text appeared. Regenerate or edit until every visible character is correct.
8. Return the generated image and briefly state which evidence sources were used for the copy. Do not expose internal chain-of-thought.

## Non-negotiable copy rules

- Never identify a location from visual resemblance alone.
- Never turn the current date, filename timestamp, upload time, or tool time into the photo date.
- Use EXIF `DateTimeOriginal` only as a capture date; preserve uncertainty and timezone limits.
- Use GPS coordinates only as coordinates unless a reliable geocoder or user confirmation supplies a place name.
- Treat filenames and folder names as weak metadata. Use them only when clearly user-authored and semantically meaningful; otherwise ask.
- Transcribe OCR only after visual confirmation. Preserve uncertain characters as omitted text, not a best guess.
- Do not invent a seal inscription, brand, attraction name, travel label, quotation, weather, season, emotion, itinerary, or photographer credit.
- Descriptive copy may mention only directly visible content and relationships, such as “山影临水，泊船近岸.” Do not imply hidden facts or specific identities.
- If image generation produces unreadable or extra glyphs, remove them or regenerate. Pseudo-Chinese is a failed output.

## Visual specification

- Default to a 4:3 horizontal composition unless the user specifies another ratio.
- Preserve the main photograph across roughly the lower two-thirds to four-fifths of the canvas.
- Place it on a warm ivory, lightly fibrous rice-paper background with subtle age variation; avoid heavy grunge.
- Fade the photograph into paper through organic dry-brush, ink-bloom, splatter, and broken-fiber edges. Keep edges irregular, never a rectangular frame.
- Retain the original mountains, buildings, waterline, people, boats, and other identity-bearing shapes. Do not add or remove landmarks or objects unless asked.
- Reduce saturation, soften contrast, and bias colors toward muted pine green, blue-gray, warm ochre, charcoal, and paper cream. Keep selective source color only where compositionally useful.
- Reserve generous blank paper around text. Use a large black brush-script headline at upper left, small restrained body copy below it, and optional small factual metadata at lower right.
- Use one muted cinnabar accent: a dot, underline, or abstract seal-like mark. A seal may be decorative and non-legible; never place invented readable characters inside it.
- Keep typography editorial and calm. Do not imitate a living artist or reproduce a distinctive brand mark.

## Copy hierarchy

Use only the levels supported by evidence:

1. Headline: 6–18 Chinese characters, grounded in the dominant visible subjects. A literal description is safer than a factual title.
2. Supporting copy: zero to three short lines, each directly traceable to visible content or supplied text.
3. Side label: optional place or theme only when supported.
4. Footer: optional capture date and location only when supported by EXIF, reliable metadata, or user confirmation.

Dropping a level is always better than fabricating it. If only visible content is available, a valid poster can contain a descriptive headline and no footer.

## Generation prompt contract

Include all of the following in the editing prompt:

- “Use the attached photo as the sole scene reference; preserve its recognizable composition and objects.”
- The visual specification above, adapted to the source orientation.
- A `TEXT TO RENDER EXACTLY` block containing every allowed string and its placement.
- “Do not add any other letters, numbers, signatures, seals with readable characters, logos, captions, or pseudo-text.”
- “All visible text must be crisp, correctly written, and exactly match the supplied strings.”

If exact text rendering remains unreliable, create or edit the artwork without text and add the approved copy through a deterministic typography-capable editor. Never accept near-miss glyphs.

## Quality gate

Before delivery, confirm all answers are yes:

- Does the result remain unmistakably the same scene?
- Are all added factual claims supported by the evidence ledger?
- Does every visible character exactly match the approved copy?
- Are unsupported place names, dates, credits, and seals absent?
- Are the paper, ink edge, muted palette, and spacious editorial hierarchy present?
- Is there no watermark, hallucinated object, random mark that resembles writing, or accidental border?

Read `references/evidence-and-copy.md` whenever the poster contains any text. Use the bundled script for every locally accessible source image.
Use `references/examples.md` as patterns, never as a source of facts for the user's image.
