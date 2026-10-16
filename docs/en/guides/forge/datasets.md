# Datasets

Datasets are the starting point of every Forge workflow: upload images, keep every upload as a version, then annotate or train against that version.

## Flow

1. **Create a dataset** — fill in the name and description and choose the format (COCO / YOLO).
2. **Upload data** — upload individual images or a ZIP archive. The archive is extracted and ingested asynchronously; follow the progress on the Dataset Versions page.
3. **Work with versions** — every upload produces a new version. Historical versions are retained and can be switched back to.

## Prerequisites

- Dataset images must be jpg / jpeg / png.
- Images inside the ZIP may sit in the archive root or in an `images/` subdirectory.

## FAQ

!!! question "How do I prepare labeled training data?"

    Finish labeling in the annotation workbench, then use **Export** to generate the YOLO format. Training picks it up automatically.

!!! question "How are version numbers incremented?"

    A new version is created automatically every time you upload images.

## Next steps

- **Annotate** — open the [Annotations](annotations.md) page, pick this dataset, and create an annotation project.
- **Train directly** — or pick the dataset on the [Training](training.md) page and start a training run.
- **First run?** Follow the end-to-end [Getting started](getting-started.md) walkthrough.
