import json
import time
import urllib.request

MODEL = "bristlecone-qwen35:4b-64k"

data = {
    "model": MODEL,
    "prompt": "Reply with exactly the word OK.",
    "stream": True,
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

print("Starting TTFT benchmark...")

start = time.perf_counter()
first_output_time = None
full_response = ""
final_result = {}

with urllib.request.urlopen(request) as response:
    for line in response:
        chunk = json.loads(line)

        text = chunk.get("response", "")

        if text and first_output_time is None:
            first_output_time = time.perf_counter()

        full_response += text

        if chunk.get("done"):
            final_result = chunk

end = time.perf_counter()

if first_output_time is not None:
    ttft = first_output_time - start
else:
    ttft = 0

def seconds(ns):
    return ns / 1_000_000_000

print()
print("=== TTFT BENCHMARK ===")
print("Response:", full_response)
print(f"TTFT:        {ttft:.2f} sec")
print(f"TOTAL:       {end - start:.2f} sec")
print(
    f"MODEL LOAD:  "
    f"{seconds(final_result.get('load_duration', 0)):.2f} sec"
)
print(
    f"PROMPT EVAL: "
    f"{seconds(final_result.get('prompt_eval_duration', 0)):.2f} sec"
)
print(
    f"GENERATION:  "
    f"{seconds(final_result.get('eval_duration', 0)):.2f} sec"
)
