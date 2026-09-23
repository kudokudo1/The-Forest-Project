import json
import time
import urllib.request

MODEL = "bristlecone-qwen35:4b-64k"

data = {
    "model": MODEL,
    "prompt": "Reply with exactly the word OK.",
    "stream": False,
    "think": False,
    "options": {
        "temperature": 0,
        "seed": 42,
        "num_predict": 16
    }
}

request = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print("Starting benchmark...")
start = time.perf_counter()

with urllib.request.urlopen(request) as response:
    result = json.load(response)

end = time.perf_counter()

def seconds(ns):
    return ns / 1_000_000_000

load = seconds(result.get("load_duration", 0))
prompt = seconds(result.get("prompt_eval_duration", 0))
generation = seconds(result.get("eval_duration", 0))

eval_count = result.get("eval_count", 0)

if generation > 0:
    speed = eval_count / generation
else:
    speed = 0

print()
print("=== BRISTLECONE BENCHMARK ===")
print("Response:", result.get("response"))
print(f"TOTAL:       {end - start:.2f} sec")
print(f"MODEL LOAD:  {load:.2f} sec")
print(f"PROMPT EVAL: {prompt:.2f} sec")
print(f"GENERATION:  {generation:.2f} sec")
print(f"TOKENS:      {eval_count}")
print(f"SPEED:       {speed:.2f} tok/s")
