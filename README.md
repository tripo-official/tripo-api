# Tripo API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/tripo3d/tripo?utm_source=github&utm_medium=ugc&utm_campaign=tripo-official&utm_content=readme-badge&utm_term=tier-c)

Tripo is an AI 3D generation platform from VAST that turns a single image or a text prompt into a textured 3D mesh in seconds. This repository is a small Python client for the Tripo API as hosted on Synexa, so you can convert product photos, concept art or sprites into GLB models from a script with one `pip install` and an API token, without running a 3D generation model yourself.

You get a blocking `run()` that uploads an image and returns the mesh URL, a non-blocking create-and-poll path for batch conversion, and webhook delivery for pipelines that would rather be called back. The client has a single runtime dependency and no model weights. It is aimed at developers building game asset pipelines, e-commerce 3D viewers, AR product previews or procedural content tools who want Tripo-class image-to-3D as an HTTP call.

> **Try it now:** [https://synexa.ai/explore/tripo3d/tripo](https://synexa.ai/explore/tripo3d/tripo?utm_source=github&utm_medium=ugc&utm_campaign=tripo-official&utm_content=readme-top&utm_term=tier-c) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Tripo](#about-tripo)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **No GPU to provision.** Image-to-3D models that produce textured meshes need a datacenter GPU with tens of gigabytes of VRAM for the shape and texture stages together. The hosted endpoint runs on Synexa's fleet and you pay per model.
- **No mesh toolchain to build.** A self-hosted pipeline chains shape generation, texture baking, mesh cleanup and GLB export, each with its own dependencies. The endpoint returns a finished GLB with PBR textures.
- **No cold start.** The model is resident on the endpoint; a single conversion and a thousand-item catalogue run see the same per-item latency, with nothing to load before the first request.
- **Predictable cost.** `tripo3d/tripo` is billed at $0.16 per run, and the alternative `tencent/hunyuan3d-3.1` at the same $0.16, so converting a catalogue of 500 products costs $80 either way.

## Installation

```bash
pip install git+https://github.com/tripo-official/tripo-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=tripo-official&utm_content=readme-apikey&utm_term=tier-c)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import tripo_api

output = tripo_api.run({
    "image": "https://example.com/input.png"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from tripo_api import Client

client = Client(api_key="sk-...")
output = client.run({"image": "https://example.com/input.png"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`tripo3d/tripo`](https://synexa.ai/explore/tripo3d/tripo?utm_source=github&utm_medium=ugc&utm_campaign=tripo-official&utm_content=readme-models&utm_term=tier-c) | image-to-3d | State-of-the-art single-image to 3D object generation. Produces production-ready GLB meshes with PBR textures in under a second. | $0.16 |
| [`tencent/hunyuan3d-3.1`](https://synexa.ai/explore/tencent/hunyuan3d-3.1?utm_source=github&utm_medium=ugc&utm_campaign=tripo-official&utm_content=readme-models&utm_term=tier-c) | image-to-3d | Generate high-quality 3D models with accurate geometry and realistic textures from input images. | $0.16 |

The default model is **`tripo3d/tripo`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `tripo3d/tripo`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `image` | file | yes | `https://files.synexa.ai/models/hyper3d-c…` | — | Input image to convert to 3D model |

### `tencent/hunyuan3d-3.1`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `image` | file | yes | `https://files.synexa.ai/models/hyper3d-c…` | — | Input image to convert to 3D model |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from tripo_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Tripo

Tripo ([tripo3d.ai](https://www.tripo3d.ai)) is a 3D generation platform developed by VAST, a Beijing-based 3D AI research company. The platform produces 3D models from a single image or a text prompt, and adds downstream tools such as retexturing, rigging and animation, stylisation and export to common engine formats. VAST also released TripoSR, an open-weights fast image-to-3D reconstruction model developed together with Stability AI, and later open-sourced further models under the Tripo name, so the platform is known both for its hosted service and for its research releases.

The hosted Tripo model this client wraps performs single-image to 3D object generation. Given one image, it infers the full geometry including unseen sides, generates a clean mesh and bakes physically based rendering textures, then exports a GLB. Generation takes on the order of a second on the endpoint. The only required input is `image`; the output is a GLB file that loads directly in three.js, Babylon.js, Unity, Unreal, Blender and most AR viewers. Results are best when the subject is a single object on a plain background, photographed or drawn from a three-quarter view with the whole object visible; cluttered scenes, heavy occlusion and thin structures such as wires reduce quality.

Typical outputs are game props and characters at a fidelity suitable for prototyping and, after cleanup, for production; product models for web and AR viewers generated from catalogue photos; and quick 3D blockouts from concept sketches. Limits to plan for: one image produces one object, texture fidelity on the unseen side is inferred rather than observed, and topology is generated rather than artist-authored, so retopology may be needed for rigged characters.

The hosted endpoint used by this client is `tripo3d/tripo` on Synexa, which is Tripo's own image-to-3D model served through Synexa's API. The client also exposes `tencent/hunyuan3d-3.1`, Tencent's Hunyuan3D image-to-3D model at the same price; it is a different model, included so you can compare outputs on the same input. Tripo's full platform, including text-to-3D, rigging, retexturing and its own API, is at [tripo3d.ai](https://www.tripo3d.ai).

**Official project:** https://www.tripo3d.ai

## Use cases

- **Game prop generation** — pass a concept sketch or reference photo as `image` and drop the returned GLB into Unity or Unreal for blockout and prototyping.
- **E-commerce 3D viewers** — batch-convert catalogue photos through the poll path and serve the GLBs in a three.js or model-viewer component.
- **AR product previews** — generate a mesh from a product shot and convert the GLB to USDZ for iOS Quick Look.
- **Concept-to-blockout** — turn 2D character or vehicle art into a rough 3D base that an artist refines rather than starting from a cube.
- **Model comparison** — run the same image against `tripo3d/tripo` and `tencent/hunyuan3d-3.1` and keep whichever mesh has cleaner topology for your use.
- **Procedural content tools** — wire the webhook path into a content pipeline that generates, validates and imports meshes without a human in the loop.

## FAQ

**Is there a Tripo API?**

Yes. Tripo offers a developer API on its own platform, and its image-to-3D model is also hosted on Synexa as `tripo3d/tripo`. This client talks to the Synexa endpoint, which takes one image and returns a textured GLB mesh.

**How much does the Tripo API cost through this client?**

The hosted `tripo3d/tripo` endpoint is billed at $0.16 per run, where one run converts one image into one model. The alternative `tencent/hunyuan3d-3.1` is also $0.16 per run. There is no subscription; you pay per completed generation.

**Can I run Tripo without a GPU?**

With this client, yes. Generation happens on Synexa's GPUs; your machine only needs Python and network access. VAST's open-weights releases such as TripoSR can be run locally, but they require a CUDA GPU and are not what this endpoint serves.

**Does this client work with TripoSR or Blender?**

It does not load TripoSR weights or drive Blender. It calls the hosted endpoint and returns a GLB, which you can then import into Blender or any engine that reads glTF.

**What input formats does it accept?**

The only required field is `image`, a single picture of the object to convert. A single object on a plain background, seen from a three-quarter angle with nothing cropped, gives the best result. The output is a GLB file with PBR textures.

**Is this the official Tripo SDK?**

No. This is an independent client that wraps the Synexa-hosted endpoint. Tripo's official platform, API and SDKs are at https://www.tripo3d.ai.

## Related

- [Tripo](https://www.tripo3d.ai) — official platform and developer API
- [Tripo guide](https://tripoai.online) — walkthroughs and examples for Tripo image-to-3D
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose SDK this client builds on
- [tripo3d/tripo on Synexa](https://synexa.ai/explore/tripo3d/tripo) — the hosted Tripo image-to-3D endpoint
- [tencent/hunyuan3d-3.1 on Synexa](https://synexa.ai/explore/tencent/hunyuan3d-3.1) — Tencent's image-to-3D model at the same price

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Tripo. Model weights and trademarks belong to their respective owners.



_Last reviewed: 2026-09-22_
