# ML Backend

An ML Backend is a Label Studio model service used for **semi-automated annotation**: it generates pre-labeling boxes for unannotated tasks, and annotators correct them by hand.

## Purpose

When an ML Backend is attached, pre-annotations are written into Label Studio as predictions and are visible in the annotation workbench. Annotators review and correct instead of drawing every box from scratch.

## Flow

1. **Register an ML Backend** — record its name, URL, and associated model (optional).
2. **Select it in the workbench** — use the dropdown next to the **Semi-automated annotation** button, or keep the default.
3. **Run pre-labeling** — predictions are written into Label Studio and shown in the annotation workbench.

## Prerequisites

- The ML Backend service must be reachable (inside the cluster or already exposed).
- When a model is associated, its pre-labeling results match that model's class space.

## FAQ

!!! question "Pre-labeling labels do not match?"

    The model's classes must be consistent with the annotation configuration.

!!! question "Service unhealthy?"

    The health check is a real HTTP probe against `/health`.

## Next steps

Register the model, select it in the annotation workbench, run semi-automated annotation, review by hand, then export for training. See [Annotations](annotations.md).
