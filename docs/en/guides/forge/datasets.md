# Datasets

Datasets are the starting point of every Forge workflow. A dataset is a
**versioned container**: every upload and every annotation export creates a
new, immutable version, and every training, optimization or evaluation job
references one exact version. That is what makes every model reproducible.

## Dataset formats

Choose the format that matches the model family:

| Format | Used for | Contents |
|---|---|---|
| **COCO** | CV detection / segmentation | Images + a COCO `annotations.json` |
| **YOLO** | CV training | Images + YOLO labels + `data.yaml` |
| **ImageNet** | Image classification | Per-class folder layout |
| **LLM-SFT** | LLM / VLM fine-tuning | A sharegpt-style JSONL corpus; VLM datasets additionally carry an `images/` folder |
| **JSONL** | Text corpora | One sample per line (plain text, `{text}`, `{data}` or sharegpt conversations) |

`llm-sft` and `imagenet` versions are directly selectable for training. A
raw COCO upload is converted for the trainer automatically (a `data.yaml` is
generated); YOLO produced by an annotation export needs no conversion at all.

A sharegpt line looks like this and feeds the LLM/VLM trainers directly:

```json
{"conversations": [{"from": "human", "value": "Describe this image."},
                   {"from": "gpt", "value": "A blue circle on a red background."}]}
```

## Create and upload

1. On the **Datasets** page, create a dataset with a name, description and
   format.
2. Upload individual images or a **ZIP archive**. Images may sit at the
   archive root or in an `images/` subdirectory.
3. The archive is extracted and ingested **asynchronously** — follow progress
   in the version list. Each successful ingest becomes a new retained version.
4. Pre-staged corpora (for example an LLM-SFT JSONL plus an `images/`
   directory already placed in object storage) can be registered from their
   S3 prefix without a browser upload.

Accepted image types are jpg / jpeg / png. Bulk bytes go to the S3-compatible
object store; the workbench and trainers receive short-lived presigned URLs
instead of file copies.

## Versioning rules

- Every upload increments the version; old versions are retained and remain
  selectable. Versions are never mutated.
- An annotation **export** (COCO/YOLO for vision, JSONL for text) is itself a
  new dataset version, so a model is always traceable to the exact labels it
  learned from.
- Switch between versions when creating a job; the rest of the pipeline does
  not change.
- The version records its file counts (images and annotation files), format,
  size and origin (upload, export, S3 reconciliation).

## How versions feed the factory

```
upload images ──► v1 (raw)
annotate + export ──► v2 (YOLO / JSONL, training-ready) ──► training
new field images ──► v3 ──► annotate gaps ──► v4 ──► retrain
```

## FAQ

!!! question "How do I prepare labeled training data?"
    Label the images in the [annotation workbench](annotations.md), then use
    **Export**. Vision projects export COCO/YOLO; text-classification exports
    plain JSONL; generation/chat projects export sharegpt JSONL. The result is
    a new dataset version the training page can select immediately.

!!! question "How are version numbers incremented?"
    Automatically, once per finalized upload or export. You cannot overwrite a
    version.

!!! question "Can a dataset mix images and text?"
    VLM corpora do exactly that: an `llm-sft` JSONL references files in an
    accompanying `images/` directory. For pure vision use COCO/YOLO/ImageNet;
    for pure text use JSONL/LLM-SFT without images.

## Next steps

- Label the data on the [Annotations](annotations.md) page, or
- Start a [Training](training.md) run directly on a training-ready version.
- Set up pre-labeling first? See [ML Backend](mlbackend.md).
