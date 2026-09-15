---
title: KaryoAI
emoji: 🧬
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8501
pinned: false
license: other
license_name: dan36karyo
license_link: LICENSE
tags:
  - cytogenetics
  - karyotype
  - chromosome-analysis
  - bioinformatics
  - computer-vision
  - image-segmentation
  - research
short_description: Research-only chromosome segmentation & karyotyping
---

# KaryoAI

**Research prototype. Not a diagnostic device.** Every output here is a draft for review by a qualified cytogeneticist.

## What this does

Upload a Giemsa-stained chromosome spread image and get back:

- a segmented, annotated image identifying candidate chromosome objects
- a **draft** karyogram layout for visual review — not a confirmed karyotype
- a structured JSON result and Markdown report

This demo runs the classical (non-neural) pipeline: thresholding + connected-component segmentation, with a low-confidence heuristic for draft chromosome ordering. It does not perform validated chromosome identification or any clinical interpretation. A separate, in-development deep-learning track exists in this project's source but is not part of this demo — it is untrained.

## Data & privacy

No real patient or animal images are used by this Space. Please upload only de-identified or synthetic images — this Space is public and does not perform de-identification itself.

## Limitations

- The draft chromosome-numbering is a size-ordering heuristic, not a trained classifier — expect it to be wrong on real spreads.
- Segmentation degrades on touching/overlapping chromosomes and debris-heavy images.
- Not validated on any real dataset.

## Source & more information

- Full source and the in-progress deep-learning track: [github.com/Danngugi/Karyotype-ai-pipeline](https://github.com/Danngugi/Karyotype-ai-pipeline)
- Model card / architecture notes: [huggingface.co/ngugdan/DN-Cytogenetic-karyotyping](https://huggingface.co/ngugdan/DN-Cytogenetic-karyotyping)

## Maintainer

Dan Ngugi — Biomedical Scientist, Mombasa County Government; MSc Molecular Medicine, KEMRI Centre for Biotechnology Research and Development.
