Define the Tree's job
What it owns.
What it should never do.
Whether it is user-facing, background, or both.
What other Trees it collaborates with.
Define its intelligence requirements
General reasoning
Coding
Agent/tool use
Planning
Long-context ability
Retrieval
Memory behavior
Multimodal capability
Security reasoning
Personality/conversation quality
Autonomy level
Define its operational constraints
Small / Big model role
RAM/VRAM target
CPU/GPU expectations
Desired latency
Context-window requirements
Concurrent use with other Trees
Local-only vs optional remote models
Quantization tolerance
Define Forest-specific requirements
Workshop/tool compatibility
deterministic routing compatibility
Leaf Foliage integration
long-term learning
multi-agent communication
structured output reliability
ability to operate under very small capability sets
portability away from a specific runtime such as Ollama/Hermes
Define model-origin/licensing requirements
Open weights vs closed
commercial-use rights
fine-tuning rights
redistribution
your preference for non-Chinese models where practical
whether we're willing to accept an exception if a model is uniquely strong
Only then research candidates.
Shortlist maybe 3–5, rather than throwing 20 models at the Tree.
Design a Tree-specific benchmark instead of relying entirely on generic benchmarks.
Select Small / Big / specialist models, because a Tree doesn't necessarily need to equal one LLM.

That last part is important. We might ultimately get architectures such as:

Cherry
→ Small conversational/agent model
→ Big reasoning model
→ optional specialist

while:

Cedar
→ Small security monitor
→ Big security-reasoning model
→ deterministic security tools

and:

Maple
→ potentially a very different model family optimized for organization, files, retrieval, and procedural work.

So Cherry, Maple, Cedar, McIntosh, etc. don't even need the same model-selection philosophy.

I also think we should keep a running candidate board while we do this:

Tree → Role → Must-haves → Nice-to-haves → Disqualifiers → Candidate models → Tests → Decision

But I won't start filling any of that in until you choose which Tree we define first.