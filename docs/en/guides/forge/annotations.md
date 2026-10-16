# Annotations

Annotations turn an image dataset into labeled training data. Forge embeds Label Studio as the annotation workbench and supports semi-automated pre-labeling through an ML Backend.

## Flow

1. **Create an annotation project** — select a dataset and an annotation task type (detection / segmentation / classification, etc.).
2. **Open the annotation workbench** — Label Studio is embedded; annotate each image with bounding boxes, polygons, and so on.
3. **Semi-automated annotation** — click **Semi-automated annotation** and optionally choose an ML Backend (model) to pre-label the unannotated tasks.
4. **Review and export** — finished annotations can be exported as COCO / YOLO / Label Studio JSON / CSV.

## Prerequisites

- A dataset with uploaded images.
- Semi-automated annotation needs a usable ML Backend — register one on the ML Backend page, or use the default service. See [ML Backend](mlbackend.md).

## FAQ

!!! question "Pre-labeling returns nothing?"

    Confirm the selected model's classes match the annotation configuration. A weak model producing low-confidence predictions is normal.

!!! question "Where does the export go?"

    The export produces a new dataset in YOLO format, which can be selected directly on the Training page.

## Next steps

After exporting, create a training task on the [Training](training.md) page — the data loop closes automatically.

**First run?** Follow the end-to-end [Getting started](getting-started.md) walkthrough.
