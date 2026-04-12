from bytez import Bytez

key = "f8d2be0a0bbe23456c4928a3e8cffe3a"
sdk = Bytez(key)

model = sdk.model("openai/gpt-4.1")

results = model.run([
    {
        "role": "user",
        "content": "Hello"
    }
])

print({"error": results.error, "output": results.output})