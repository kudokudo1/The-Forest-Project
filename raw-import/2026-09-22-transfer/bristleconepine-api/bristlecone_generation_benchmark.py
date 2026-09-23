import json
import time
import urllib.request

MODEL = "bristlecone-qwen35:4b-64k"

data = {
    "model": MODEL,
    "prompt": (
        "Write a concise explanation of why testing software "
        "before deployment is important. Use plain paragraphs."
    ),
    "stream": False,
    "think": False,
    "options": {
        "temperature": 0,
        "seed": 42,
        "num_predict": 128
    }
}

request = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print("Starting generation benchmark...")
start = time.perf_counter()

with urllib.request.urlopen(request) as response:
    result = json.load(response)

end = time.perf_counter()

def seconds(ns):
    return ns / 1_000_000_000

load = seconds(result.get("load_duration", 0))
prompt = seconds(result.get("prompt_eval_duration", 0))
generation = seconds(result.get("eval_duration", 0))

prompt_tokens = result.get("prompt_eval_count", 0)
generated_tokens = result.get("eval_count", 0)

prompt_speed = prompt_tokens / prompt if prompt > 0 else 0
generation_speed = generated_tokens / generation if generation > 0 else 0

print()
print("=== GENERATION BENCHMARK ===")
print(f"TOTAL:              {end - start:.2f} sec")
print(f"MODEL LOAD:         {load:.2f} sec")
print(f"PROMPT EVAL:        {prompt:.2f} sec")
print(f"PROMPT TOKENS:      {prompt_tokens}")
print(f"PROMPT SPEED:       {prompt_speed:.2f} tok/s")
print(f"GENERATION:         {generation:.2f} sec")
print(f"GENERATED TOKENS:   {generated_tokens}")
print(f"GENERATION SPEED:   {generation_speed:.2f} tok/s")
