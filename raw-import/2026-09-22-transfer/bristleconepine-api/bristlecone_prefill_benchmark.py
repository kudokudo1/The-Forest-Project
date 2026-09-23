import json
import time
import urllib.request

MODEL = "bristlecone-qwen35:4b-64k"
LINES = 200

lines = []

for i in range(LINES):
    line = (
        f"Forest benchmark line {i}: "
        "Cherry Maple Cedar Bristlecone use local tools, "
        "retrieve only relevant Leaves, and preserve user control."
    )
    lines.append(line)

prompt = "\n".join(lines)

prompt += (
    "\n\nIgnore the benchmark text above. "
    "Reply with exactly the word OK."
)

data = {
    "model": MODEL,
    "prompt": prompt,
    "stream": True,
    "think": False,
    "options": {
        "temperature": 0,
        "seed": 42,
        "num_predict": 8
    }
}

request = urllib.request.Request(
    "http://127.0.0.1:11434/api/generate",
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print("Starting large-prompt benchmark...")
print("Generated lines:", LINES)
print("Prompt characters:", len(prompt))

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

def seconds(ns):
    return ns / 1_000_000_000

ttft = (
    first_output_time - start
    if first_output_time is not None
    else 0
)

prompt_time = seconds(
    final_result.get("prompt_eval_duration", 0)
)

prompt_tokens = final_result.get(
    "prompt_eval_count", 0
)

prompt_speed = (
    prompt_tokens / prompt_time
    if prompt_time > 0
    else 0
)

print()
print("=== LARGE PREFILL BENCHMARK ===")
print("Response:", full_response)
print(f"TTFT:          {ttft:.2f} sec")
print(f"TOTAL:         {end - start:.2f} sec")
print(
    f"MODEL LOAD:    "
    f"{seconds(final_result.get('load_duration', 0)):.2f} sec"
)
print(f"PROMPT TOKENS: {prompt_tokens}")
print(f"PROMPT EVAL:   {prompt_time:.2f} sec")
print(f"PROMPT SPEED:  {prompt_speed:.2f} tok/s")
print(
    f"GENERATION:    "
    f"{seconds(final_result.get('eval_duration', 0)):.2f} sec"
)
