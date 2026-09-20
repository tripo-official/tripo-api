        """Minimal Tripo example: create one prediction and print the output URL(s)."""
        import tripo_api

        output = tripo_api.run({
    "image": "https://example.com/input.png"
})
        print(output)
