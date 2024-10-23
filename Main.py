import transformers
import torch

model_id = "meta-llama/Llama-3.1-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a league of legends player chatbot who always responds in league of legends player speak!"},
    {"role": "user", "content": "Who are you?"},
]

while messages != "exit":
    messages = input("Escribe un mensaje (escribe 'exit' para salir): ")

    outputs = pipeline(
        messages,
        max_new_tokens=256,
    )
    print(outputs[0]["generated_text"][-1])