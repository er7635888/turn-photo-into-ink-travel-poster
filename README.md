# 水墨旅行照片海报 / Ink-Wash Travel Poster

把旅行、风景、建筑或日常照片转成横版中国水墨编辑海报，同时确保地点、日期、招牌、署名和描述都有明确证据。

Transform travel, landscape, architecture, or everyday photographs into horizontal Chinese ink-wash editorial posters while keeping every place name, date, sign, credit, and descriptive claim grounded in evidence.

[中文](#中文说明) · [English](#english-guide) · [查看案例 / View examples](references/examples.md)

---

## 中文说明

### 功能介绍

`turn-photo-into-ink-travel-poster` 是一个面向 ChatGPT 与 Codex 的 Agent Skill。它会：

- 保留原始照片中可识别的山体、建筑、水线、人物、船只和其他关键对象。
- 将照片融合进温暖的宣纸底纹，以干笔、墨晕、飞白和断裂纤维形成不规则边缘。
- 使用松绿、蓝灰、暖赭、炭黑和纸张米白构成克制的复古色彩。
- 在左上方建立书法标题、正文、地点标签和页脚日期的编辑层级。
- 从画面、经人工核验的 OCR、EXIF 元数据或用户明确提供的信息中建立“文案证据账本”。
- 拒绝根据外观猜测地点、日期、季节、天气、摄影师或景点名称。
- 逐字检查生成结果，移除错字、伪中文、可读的虚构印章和额外文字。

### 工作流程

1. 按原始分辨率检查照片。
2. 运行证据提取脚本，读取尺寸、格式和安全的 EXIF 字段。
3. 对 OCR 结果进行画面核验。
4. 建立视觉、OCR、EXIF 和用户输入证据账本。
5. 只使用有证据支持的文字。
6. 以原图为唯一场景参考生成水墨海报。
7. 检查场景一致性、对象数量和每一个可见字符。
8. 对不合格文字或伪印章进行局部修正。

### 安装方法

#### 方法一：使用 Codex Skill Installer

在 Codex 中调用：

```text
$skill-installer
```

然后要求它从以下仓库安装：

```text
https://github.com/er7635888/turn-photo-into-ink-travel-poster
```

#### 方法二：安装为用户级 Skill

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/er7635888/turn-photo-into-ink-travel-poster.git \
  "$HOME/.agents/skills/turn-photo-into-ink-travel-poster"
```

这会让 Skill 对当前用户的不同项目可用。

#### 方法三：安装为项目级 Skill

在项目根目录执行：

```bash
mkdir -p .agents/skills
git clone https://github.com/er7635888/turn-photo-into-ink-travel-poster.git \
  .agents/skills/turn-photo-into-ink-travel-poster
```

项目级安装适合把工作流和代码仓库一起维护。

#### ChatGPT 桌面端

独立 Skills 可在 ChatGPT 桌面端使用。打开侧边栏中的 **Skills** 查看可用技能。若你的版本或工作区没有提供直接的 GitHub 导入入口，可先使用上述 Codex 本地安装方式；面向他人分发时，官方推荐将 Skill 打包为 Plugin。

官方说明：[Build skills](https://learn.chatgpt.com/docs/build-skills)

### 依赖

证据提取脚本需要 Python 3 和 Pillow：

```bash
python -m pip install Pillow
```

可选 OCR 支持需要安装 Tesseract 及对应语言包。没有 OCR 时，仍可通过人工查看画面确认文字。

海报转换还需要宿主环境提供支持参考图编辑的图片生成工具。

### 使用方法

在 ChatGPT 中可通过 `@` 选择该 Skill；在 Codex CLI 或 IDE 扩展中可通过 `$` 或 `/skills` 调用。

示例提示词：

```text
@turn-photo-into-ink-travel-poster
把这张湖边照片做成横版宣纸水墨旅行海报。
保留山体、码头和两艘木舟；不要猜地点或日期。
所有文字必须来自画面、EXIF 或我明确提供的信息。
```

如果需要地点或日期，请明确提供：

```text
这是杭州西湖。请把“杭州西湖”作为小号地点标签，
标题仍然只描述画面，不添加季节、天气或摄影师署名。
```

### 运行证据提取脚本

```bash
python scripts/extract_photo_evidence.py input.jpg --output evidence.json
```

启用本地 OCR：

```bash
python scripts/extract_photo_evidence.py input.jpg \
  --output evidence.json \
  --ocr \
  --ocr-language chi_sim+eng
```

OCR 结果仅是候选文本，必须对照原图逐字确认。

### 示例

#### 1. 仅使用可见画面

| 原始照片 | 水墨海报 |
| --- | --- |
| ![湖泊、群山、码头和两艘木舟](assets/examples/01-lake-source.jpg) | ![远山临水双舟泊岸水墨海报](assets/examples/01-lake-poster.jpg) |

核准标题：`远山临水，双舟泊岸`。未添加地点、日期或署名。

#### 2. 使用用户确认的地点

| 原始照片 | 水墨海报 |
| --- | --- |
| ![柳岸湖面和一艘小舟](assets/examples/02-willow-lake-source.jpg) | ![带杭州西湖地点标签的水墨海报](assets/examples/02-willow-lake-poster.jpg) |

地点 `杭州西湖` 来自用户确认，而不是视觉猜测。

#### 3. 使用 EXIF 拍摄日期

| 原始照片 | 水墨海报 |
| --- | --- |
| ![竹林溪流与石桥](assets/examples/03-stone-bridge-source.jpg) | ![带EXIF日期的石桥水墨海报](assets/examples/03-stone-bridge-poster.jpg) |

页脚 `2025.04.18` 来自示例文件的 `DateTimeOriginal`。

#### 4. 使用经核验的招牌文字

| 原始照片 | 水墨海报 |
| --- | --- |
| ![同福茶馆木结构老街](assets/examples/04-teahouse-source.jpg) | ![保留同福茶馆招牌的水墨海报](assets/examples/04-teahouse-poster.jpg) |

`同福茶馆` 经原图逐字确认后才允许使用。

#### 5. 证据不足时省略事实字段

| 原始照片 | 水墨海报 |
| --- | --- |
| ![群山河流与竹筏](assets/examples/05-karst-source.jpg) | ![不含地点日期的山水竹筏海报](assets/examples/05-karst-poster.jpg) |

画面外观不能证明具体地点，因此成品省略地点、日期和摄影师信息。

### 目录结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── icon.svg
│   └── examples/
├── references/
│   ├── evidence-and-copy.md
│   └── examples.md
└── scripts/
    └── extract_photo_evidence.py
```

### 核心原则

> 宁可少写，也不编造。

示例只用于展示工作流，不能作为其他照片的地点、日期、对象或文案证据。

---

## English guide

### Features

`turn-photo-into-ink-travel-poster` is an Agent Skill for ChatGPT and Codex. It:

- Preserves recognizable mountains, buildings, waterlines, people, boats, and other identity-bearing objects.
- Blends the photograph into warm rice paper with dry-brush, ink-bloom, splatter, and broken-fiber edges.
- Uses a restrained palette of pine green, blue-gray, warm ochre, charcoal, and paper cream.
- Creates an editorial hierarchy for a calligraphic headline, supporting copy, place label, and optional date.
- Builds a copy-evidence ledger from visible pixels, visually verified OCR, EXIF metadata, and user-supplied facts.
- Refuses to guess locations, dates, seasons, weather, photographer credits, or attraction names.
- Audits every generated character and removes misspellings, pseudo-Chinese, invented readable seals, and stray text.

### Workflow

1. Inspect the source at original resolution.
2. Run the evidence extractor for dimensions, format, and safe EXIF fields.
3. Verify OCR candidates against the pixels.
4. Build a visual, OCR, EXIF, and user-input evidence ledger.
5. Approve only evidence-backed copy.
6. Generate the poster using the source as the sole scene reference.
7. Check scene fidelity, object counts, and every visible character.
8. Apply targeted corrections when text or seal-like marks fail review.

### Installation

#### Option 1: Codex Skill Installer

Invoke:

```text
$skill-installer
```

Then ask it to install the skill from:

```text
https://github.com/er7635888/turn-photo-into-ink-travel-poster
```

#### Option 2: User-level installation

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/er7635888/turn-photo-into-ink-travel-poster.git \
  "$HOME/.agents/skills/turn-photo-into-ink-travel-poster"
```

This makes the skill available across projects for the current user.

#### Option 3: Repository-level installation

Run from the project root:

```bash
mkdir -p .agents/skills
git clone https://github.com/er7635888/turn-photo-into-ink-travel-poster.git \
  .agents/skills/turn-photo-into-ink-travel-poster
```

Repository-level installation is useful when a team wants to version the workflow with a codebase.

#### ChatGPT desktop

Standalone skills are available in the ChatGPT desktop app. Open **Skills** in the sidebar to view available skills. If direct GitHub import is not exposed in your app or workspace, use a local Codex installation; for broader distribution, OpenAI recommends packaging reusable skills as plugins.

Official documentation: [Build skills](https://learn.chatgpt.com/docs/build-skills)

### Requirements

The evidence extractor requires Python 3 and Pillow:

```bash
python -m pip install Pillow
```

Optional OCR requires Tesseract and the relevant language packs. Without OCR, text can still be verified manually against the source.

Poster transformation also requires an image-generation tool that supports reference-image editing.

### Usage

In ChatGPT, select the skill with `@`. In Codex CLI or the IDE extension, use `$` or `/skills`.

Example prompt:

```text
@turn-photo-into-ink-travel-poster
Turn this lakeside photo into a horizontal rice-paper ink-wash travel poster.
Preserve the mountains, pier, and two wooden boats.
Do not guess the location or date.
Every visible word must come from the image, EXIF, or facts I explicitly provide.
```

When a location is known, provide it explicitly:

```text
This is Hangzhou West Lake. Use “杭州西湖” as a small place label.
Keep the headline visually descriptive and do not add a season,
weather claim, or photographer credit.
```

### Evidence extraction

```bash
python scripts/extract_photo_evidence.py input.jpg --output evidence.json
```

With local OCR:

```bash
python scripts/extract_photo_evidence.py input.jpg \
  --output evidence.json \
  --ocr \
  --ocr-language chi_sim+eng
```

OCR output is only a candidate transcription and must be checked character by character against the source image.

### Examples

The five before-and-after comparisons above cover:

1. Visible-scene-only copy.
2. A user-confirmed place name.
3. An EXIF-supported capture date.
4. A visually verified shop sign.
5. Omission of unsupported place, date, and credit fields.

See the complete evidence ledgers and execution notes in [references/examples.md](references/examples.md).

### Project structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── icon.svg
│   └── examples/
├── references/
│   ├── evidence-and-copy.md
│   └── examples.md
└── scripts/
    └── extract_photo_evidence.py
```

### Core principle

> Omit rather than invent.

Examples demonstrate workflow patterns only. Never reuse their locations, dates, objects, or copy as evidence for another photograph.
