# Evidence and copy protocol

## Evidence ledger

Create a compact internal ledger before drafting:

| ID | Candidate fact or phrase | Source type | Source detail | Confidence | Allowed use |
| --- | --- | --- | --- | --- | --- |
| V1 | Directly visible subject/relationship | visual | Describe the pixels | high/medium | descriptive copy |
| O1 | Exact visible characters | OCR + visual check | Bounding area and transcription | high only | exact transcription |
| E1 | Capture time or GPS | EXIF | Exact field and raw value | high/medium | factual metadata |
| U1 | User-provided wording or fact | user | Exact supplied text | high | as authorized |

Do not add an item for an inference such as a guessed city, landmark, season, mood, ownership, purpose, or event.

## Source precedence

1. User-confirmed exact wording or correction
2. Visually confirmed text in the image
3. Standard EXIF fields extracted from the original file
4. Directly visible non-text content
5. Meaningful user-authored filename metadata

Conflicts require a question. Do not silently choose the most convenient source.

## Allowed transformations

- Compress visible nouns and relationships into a headline without adding facts.
- Reorder user-provided words for layout only when meaning stays unchanged.
- Format a supported date in another unambiguous format.
- Round GPS coordinates for display while retaining the correct hemisphere.
- Translate supported copy only when the user requests or clearly expects that language; preserve names conservatively.

## Forbidden transformations

- Converting GPS into a place name without a reliable lookup or confirmation
- Guessing a landmark from shape or scenery
- Converting file modification time or upload time into capture time
- Expanding an abbreviation, partial OCR result, or cropped sign by guessing
- Adding poetic claims about memory, history, silence, healing, time, weather, or local culture unless directly supported by visible content or user text
- Inventing an English travel label such as “Xiamen Travel”
- Inventing a readable seal or studio signature

## Safe copy examples

For an image visibly containing mountains, a body of water, a pier, and boats, safe phrases include:

- `山水相望`
- `舟泊岸边`
- `远山临水，近舟泊岸。`

These examples are reusable only when those subjects and relationships are actually visible. A location name or date remains prohibited without separate evidence.

## Missing evidence behavior

- If the user asked only for the style, omit unsupported factual fields and proceed.
- If the user explicitly wants a location/date/credit and the source lacks it, ask one focused question or ask for the original file with metadata.
- If only a flattened screenshot is available, state internally that original EXIF may have been stripped and do not substitute the screenshot timestamp.

## Final text audit

List every visible output string, then attach its ledger IDs. If any string lacks an ID, remove it. Inspect image-generated typography character by character; approximate glyphs and decorative pseudo-text fail the audit.
