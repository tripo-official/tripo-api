"""The same client drives every hosted model listed in tripo_api.MODELS."""
from tripo_api import Client, MODELS

client = Client()
for slug, info in MODELS.items():
    print(slug, "->", info["category"], "required:", info["required"])
# pick one explicitly
output = client.run({"image": "https://example.com/input.png"}, model="tencent/hunyuan3d-3.1")
print(output)
