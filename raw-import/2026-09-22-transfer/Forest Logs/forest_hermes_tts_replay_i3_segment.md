# Project Forest — Hermes TTS, Replay, and i3 Hotkeys

## User

Now I want to add an optional txt to speech option to my Hermes, I want it to be a toggle so I can turn it on and go working on something else I have him speak or turn it off when working with him directly or he starts reading long lines of code. I don’t wanna hear. Is their a add on or app or something for that and how would affect my speeds 

## Assistant

Yes — and conveniently, **Hermes already added almost exactly what you described**.

Current Hermes has a built-in TTS/Voice system with these commands:

```text
/voice tts      # toggle spoken replies
/voice status   # check current state
/voice off      # completely silent
```

So you could be working somewhere else, turn `/voice tts` on, and Hermes will speak replies as they generate. When you're sitting at the terminal again, turn it off. Hermes streams speech sentence-by-sentence rather than waiting for the entire response. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode?utm_source=chatgpt.com))

### What I recommend for your setup

Because you're trying to keep Forest local and free, I'd use **Piper TTS** first.

Hermes now supports Piper natively. It is free, requires no API key, runs completely locally, works on CPU, and its voice models are only about **20–90 MB** depending on quality. Hermes can install it through its own tools menu. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts/?utm_source=chatgpt.com))

Start with:

```bash
hermes update --check
```

If Hermes says an update is available:

```bash
hermes update
```

The official updater backs up important Hermes state before updating. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/getting-started/updating?utm_source=chatgpt.com))

Then:

```bash
hermes tools
```

Look for:

**Voice & TTS → Piper**

Hermes can install `piper-tts` for you. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts/?utm_source=chatgpt.com))

Then launch Hermes:

```bash
hermes
```

and inside Hermes:

```text
/voice tts
```

That should give you the toggle behavior you want.

I'd also leave this setting:

```yaml
voice:
  auto_tts: false
```

That means Hermes **starts quiet** instead of suddenly talking every time you launch him. You deliberately turn speech on when you want it. Hermes exposes that setting in `~/.hermes/config.yaml`. ([github.com](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/voice-mode.md?utm_source=chatgpt.com))

### How much will it slow Hermes down?

Probably **very little in normal use**, with one important exception.

Hermes' TTS pipeline runs alongside generation: once it has enough of a sentence, it synthesizes and begins playing it while the LLM continues generating. So TTS does not normally mean:

```text
LLM finishes
↓
wait
↓
TTS starts
```

It's closer to:

```text
Hermes generates
████████████████████████

       Piper speaks
       ██████████████████
```

Hermes buffers complete sentences of at least about 20 characters and then sends them to TTS. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode?utm_source=chatgpt.com))

For **Piper**, the synthesis happens on your CPU. Therefore:

- If your LLM is primarily using a **GPU**, I expect little noticeable effect.
- If your LLM and Piper are both fighting heavily for the **CPU**, you may see some reduction in token-generation speed while Hermes is speaking.
- When TTS is off, Piper isn't continuously synthesizing, so there shouldn't be an ongoing inference penalty.
- The voice itself only adds a relatively small model to storage/RAM compared with an LLM. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts?utm_source=chatgpt.com))

There's also **KittenTTS**, which Hermes supports in very small local models—including a roughly 25 MB nano model—but I would test Piper first because it's specifically designed as a fast local CPU TTS engine. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts/?utm_source=chatgpt.com))

### Your code problem is the one thing I'd improve

Hermes already strips Markdown formatting, emoji, and internal `<think>` material before speaking. But the current documentation **doesn't say it automatically excludes code blocks**. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode?utm_source=chatgpt.com))

So something like:

```python
for item in giant_thing:
    ...
```

could still become an annoying robot recital.

For Forest, I'd eventually give Hermes/Maple a **Speech Filter**:

```text
Hermes response
       │
       ├──────────────► Terminal
       │                 full response
       │
       ▼
  Speech Filter
       │
       ├─ remove code blocks
       ├─ remove URLs
       ├─ remove huge tables
       ├─ shorten file paths
       └─ skip terminal output
       │
       ▼
     Piper
       │
       🔊
```

Then instead of reading 80 lines of Python, Hermes could say something like:

> “I've included the Python code on screen. The important change is that the function now checks the file before processing it.”

I actually think that should become a **Forest feature**, not just a Hermes modification. A Tree's **visual Fruit** and **spoken Fruit** don't necessarily need to be identical.

You could eventually have:

```text
Speech: OFF
Normal terminal work.

Speech: FULL
Speak essentially everything appropriate.

Speech: SMART
Speak explanations.
Skip code, logs, tables, URLs, and repetitive output.

Speech: BRIEF
Only speak important results, warnings, questions, and task completion.
```

**SMART** sounds like the mode you'd use most often.

For right now, I'd get **Piper + `/voice tts`** working first. After we confirm your audio is coming through properly, we can build the **don't-read-my-code filter** without changing Hermes' actual written responses.

## User

Can I be triggered mid prompt? After a prompt? Or way later, like could I scroll up click on a chat and have him read it out agin even though it is not the current message we are on

## Assistant

Yes, but there are **three slightly different cases**, and Hermes handles them differently right now.

While Hermes is **currently generating a reply**, TTS can speak it sentence-by-sentence as the text arrives. You can also interrupt the speech immediately by typing another message, using the voice key, or—when continuous voice mode is active—talking over it. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode?utm_source=chatgpt.com))

If Hermes has **already finished a reply**, you can ask something like **“Read the last response again.”** Hermes’ own voice-mode guide actually uses “Read the last error again” as an example workflow, so replaying/re-speaking recent conversational content through a new instruction is supported conceptually. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/guides/use-voice-mode-with-hermes?utm_source=chatgpt.com))

The part you’re specifically imagining—**scrolling way up, clicking an arbitrary old Hermes message, and pressing a speaker button**—does **not appear to be a documented built-in feature of the current Hermes CLI/TUI**. The documented controls are conversation-level `/voice` commands rather than per-message playback controls. ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode?utm_source=chatgpt.com))

And I think your version is better for Forest.

I’d want the future Bark/UI to let you do this:

```text
Old message
─────────────────────────────
Hermes:
Here is the explanation...

      🔊 Read     ⏸ Stop
      🔁 Restart  ⋯ More
─────────────────────────────
```

Then **Read** would send the already-existing text straight to TTS. It would **not ask the LLM to regenerate the response**, which means it should be much faster and use essentially no additional model inference.

We could take it further with selection:

```text
Highlight paragraph
        ↓
🔊 Read Selection
```

or:

```text
Right click message
├── Read whole message
├── Read from here
├── Read selected text
├── Read summary only
└── Skip code while reading
```

That last one would solve your earlier issue especially well.

There’s also a useful distinction I’d preserve for Forest:

**Live Speech** speaks new Fruit while it is being produced.

**Replay Speech** speaks existing Fruit from history.

Those should be independent. You could keep automatic TTS **off**, scroll back two hours later, tap a message, and have Maple/Hermes read just that message aloud.

And because the original response is already stored, **Replay Speech shouldn't need the main AI model at all**—only the TTS engine. That makes it ideal for mobile/Potted Forest use because it can be considerably lighter on power than asking the Tree to reason again.

## User

Could I bind these to i3 hotkeys 

## Assistant

Yes. **You can bind them to i3 hotkeys**, and with your Qubes setup I’d actually prefer doing it through Qubes rather than installing extra input-injection tools in dom0.

Hermes currently exposes voice controls as in-chat commands such as `/voice tts`, `/voice off`, and `/voice status`; it doesn’t document a separate shell-level TTS-toggle command. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A clean Forest-style setup would be:

```text
Super + Shift + V     Toggle Hermes TTS
Super + Shift + X     Speech OFF
Super + Shift + R     Read/replay selected text
Super + Shift + S     Stop current speech
```

For your setup, I’d run Hermes inside a named `tmux` session in the Cherry AI qube:

```bash
tmux new -s hermes
hermes
```

Then i3 in dom0 can send commands into that session with `qvm-run`. Qubes supports launching commands in another qube from dom0 this way. ([doc.qubes-os.org](https://doc.qubes-os.org/en/latest/user/troubleshooting/app-menu-shortcut-troubleshooting.html?utm_source=chatgpt.com))

For example, your i3 config could eventually contain something along these lines:

```text
# Hermes — toggle TTS
bindsym $mod+Shift+v exec --no-startup-id qvm-run Cherry-AI 'tmux send-keys -t hermes "/voice tts" Enter'

# Hermes — speech off
bindsym $mod+Shift+x exec --no-startup-id qvm-run Cherry-AI 'tmux send-keys -t hermes "/voice off" Enter'

# Hermes — voice status
bindsym $mod+Shift+i exec --no-startup-id qvm-run Cherry-AI 'tmux send-keys -t hermes "/voice status" Enter'
```

Replace `Cherry-AI` with the **exact qube name** you use for Hermes.

The advantage is that the shortcut can work while you're in another window:

```text
You working in Obsidian
        │
        │ Super+Shift+V
        ▼
       i3
        │
      dom0
        │
    qvm-run
        │
        ▼
    Cherry AI
        │
    tmux:hermes
        │
 /voice tts
        ▼
     🔊 Hermes
```

So you wouldn't have to click back into Hermes first.

### And replay can be even better

For **“read this old message”**, I wouldn't necessarily send it back through Hermes at all.

Eventually we can make:

1. Highlight any text.
2. Press something like **Super+Shift+R**.
3. i3 takes the selected text.
4. Sends it to the local TTS engine.
5. The voice reads it.

That means it could read **anything**, not only Hermes:

```text
Hermes response
Obsidian Leaf
web page text
terminal message
Markdown document
old Forest conversation
```

And because the LLM isn't being called, replay would be lightweight.

I'd also add **Super+Shift+S = shut up immediately**. 😆

That emergency stop key will probably become surprisingly useful once you accidentally trigger TTS on a wall of terminal output.

One thing I **wouldn't** do is install `xdotool` into dom0 solely for this. Since your environment is Qubes, keeping the actual speech tooling and Hermes control inside the appropriate qube maintains the cleaner isolation you're building around Forest. ([doc.qubes-os.org](https://doc.qubes-os.org/en/latest/user/troubleshooting/app-menu-shortcut-troubleshooting.html?utm_source=chatgpt.com))

When you're ready to implement it, we can do this in two stages: **first get Hermes TTS working normally**, then add the i3 bindings once we know the exact Cherry qube name and whether you're running Hermes directly, through Newelle, or in another wrapper.
