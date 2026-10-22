# Annotations

Annotations turn raw data into labeled training sets. Forge does not rebuild a
labeling tool: it integrates **Label Studio** (images, text and conversation)
and **CVAT** (video and tracking) as embedded workbenches, and adds a
self-built **ML Backend** that pre-labels with your own models. The intended
division of labor is *the machine labels first, a human reviews and corrects*.

In an internal run on 128 street-scene images (8 classes), one pre-labeling
pass produced 269 boxes on 75 images — about 59% of the images needed no boxes
drawn from scratch. Your savings depend on the model and scene; measure them
on a pilot batch.

## Task types

| Workbench | Tasks |
|---|---|
| Label Studio (images) | Object detection (rectangles), segmentation (polygons/masks), classification, keypoints, oriented boxes |
| Label Studio (text) | Text classification, named entities, generation/chat review |
| CVAT (video) | Object tracking across frames, keyframe interpolation, click-to-segment |

## Flow

1. **Create a project** — on the Annotations page, pick a dataset version and
   the task type; the project carries the label schema (the class list).
2. **Open the workbench** — the tool is embedded; images or text open
   directly, they are not copied (the workbench references presigned object
   URLs).
3. **Choose a pre-labeling model** — in the project header select a registered
   model version (detection/segmentation; SAM is offered separately in the
   video editor). The choice is remembered per project.
4. **Run semi-automated annotation** — the ML Backend predicts on the
   unlabeled tasks and writes predictions as editable drafts in the workbench.
5. **Review and correct** — a human confirms, fixes or discards each draft.
6. **Export** — the export becomes a new, immutable dataset version.

## Pre-labeling models

The ML Backend is model-agnostic; it routes by model family:

- **CNN models** (RT-DETR-style detectors, SAM for segmentation,
  classifiers) run through ONNX Runtime / Triton.
- **VLM models** (for example Qwen-VL / Florence-2) run through a
  vLLM-compatible OpenAI endpoint and turn prompts into labels or boxes —
  useful for irregular categories and zero-shot first passes.
- **Trained models loop back**: after a model is trained, selecting that model
  version for pre-labeling makes subsequent batches faster (the flywheel).

Suggestions below the project's confidence threshold are left unlabeled for a
human rather than inserted as noisy boxes. See [ML Backend](mlbackend.md) for
service registration and health.

## Video to training frames

CVAT labels video with tracks and keyframes; trainers consume frame images.
Forge provides a built-in **video frame-extraction** pipeline component:

```
CVAT export (tracks / keyframes / boxes)
   ──► extract at chosen fps / sampling (uniform or activity-based)
   ──► interpolate labels between keyframes
   ──► frame images + regenerated COCO/TXT labels
   ──► new dataset version (extracted once, reusable for many runs)
```

You do not extract frames by hand; the extraction runs as a preparation step,
and the extracted frames can be reused by later training runs.

## Review and quality

- Treat pre-labels as drafts: spot-check a sample before exporting, especially
  when the class list changed or the model is weak.
- Keep the model's class space identical to the project's label schema —
  mismatched classes are the usual reason predictions look empty or wrong.
- Export only reviewed work; the exported version is immutable and is what the
  trainer consumes.

## Export formats

| Data | Export |
|---|---|
| Images (detection / segmentation) | COCO, TXT (plus Label Studio JSON / CSV from the workbench) |
| Text classification | Plain JSONL (`text,label`) |
| Generation / chat | Sharegpt JSONL — directly usable by LLM-SFT training |
| Video | Frame images + COCO/TXT via the frame-extraction component |

## FAQ

!!! question "Pre-labeling returns nothing or is disabled?"
    A model version must be selected in the project header (and have weights
    available); the button is disabled until then. If predictions run but look
    empty, verify the model's classes match the project labels and lower the
    confidence threshold. A weak model returning few suggestions is normal on
    the first batch.

!!! question "Where does the export go?"
    It becomes a new dataset version (TXT/COCO for vision, JSONL for text),
    immediately selectable on the Training page.

!!! question "Labels and model classes disagree?"
    Re-export with an aligned label schema, or choose the model version trained
    on those same classes.

## Next steps

- [Training](training.md) — start a CV or LLM/VLM run from the exported
  version.
- [ML Backend](mlbackend.md) — register or troubleshoot the pre-labeling
  service.
- [Datasets](datasets.md) — how versions are stored and reused.
