---
project: The Forest
status: active
created: 2026-08-08
updated: 2026-08-08
tags:
  - the-forest
---
# Project Forest — Early Seed Training / Leaf Foliage Prompt Collection

## Original Prompts

### Prompt 1

MB

Cancel this a new part of the forest project

This next phase will be part of the preparation and implementation of our early seed training. 

I am currently working on getting Obsidian set up so I can better train the current set of AI to help me develop future seeds and the rest of project forest. I currently have the app already downloaded, but I don’t know how to use it much. I want to start transmitting some of the markdown files. We’ve been making into Obsidian so that they’re even easier for me to transfer between cubes and multiple models to train off of.

### Prompt 2

My current plan is to use Obsidian as a temporary, if not somewhat long-term substitute and model for what will eventually become my own user storage system aka leaf foliage 

I also want to do the same for other Obsidian supporting apps and programs and implement them into the forest as well along with many Hermes and other ai agent features this would make the forest a fully compatible one time download all in one AI system that can be easily added to nearly any device, this would also make it a lot more user-friendly and avoid new users from having to learn how to stack programs or learn what programs are compatible or most optimal to be used together

### Prompt 3

One problem is, I don’t know how Obsidian currently link or stores user data to connect to other plug-ins or services. I’ve seen people create “ second brain” using Obsidian and a few other plug-ins where connected ideas would be visually represented on the user screen but many of them use a service like Google Drive I was thinking that the fourth could be completely local and have online connectivity be 100% optional like if I use one to connect a forest to a garden they could easily create potted versions of most of their plants and copy them onto their mobile device, but if they want to, they can connect the two via sync, which will get a fourth equivalent later

### Prompt 4

And I don’t know if this is a thing yet or why it isn’t if there’s a good reason, please tell me, but I was also thinking the garden or potted plants can have similar if not the same functionality as most AI agents like Hermes, where they can interact with the users device or that be through prompt or automated. Most phones can already detect when the user is sleeping or it has been at rest for for long period of time. I could imagine it would be possible to allow potted plants to temporarily run in the background and perform task like set reminders, organize files, etc., or even detect when the user is sleeping or the phone is not in use and perform automated task that the user has already permitted or queued like making a purchase, emailing a coworker, sending out math, social media post, organizing their calendar or anything else that would take more resources or the user screen. We can even implement a special garden on a potted plant or Settings that allows the user or trees to automatically detect the battery percentage and charger connectivity, and know if they should pause functions to reserve battery life I’m thinking maybe maple will be the best fit for this if we made it a tree’s responsibility because of his role and data management and the fact that he will probably be the main tree performing a lot of these task so having him the only tree running will keep the power usage low

---

## Suggestions

The following are suggestions only and are not edits to the original prompts.

1. **Define a native Forest data format / Leaf manifest.**
   Decide what information travels with a Leaf or Potted Plant beyond Markdown: IDs, relationships, provenance, permissions, lifecycle state, attachments, and AI visibility.

2. **Separate portable knowledge from rebuildable indexes.**
   Keep the user’s actual Leaves and metadata portable, while treating embeddings, graph caches, thumbnails, and search indexes as disposable data that Forest can rebuild locally.

3. **Create a capability and permission manifest for Trees and Potted Plants.**
   A Potted Plant could declare which files, sensors, accounts, network functions, or device actions it may access. Trunk would enforce those permissions.

4. **Define an offline-first synchronization protocol early.**
   Even before native Garden Sync exists, document how conflicts, versions, deletions, device identities, and reconnects should eventually work.

5. **Distinguish copying from syncing.**
   A copied Pot should be able to become independent, while a synced Pot retains a relationship with its source Plant.

6. **Add a Forest task queue.**
   Tasks could include conditions such as charging state, battery threshold, idle state, network availability, device temperature, and task priority.

7. **Separate the lightweight scheduler from the AI model.**
   A small Forest daemon could wait for operating-system events and wake Maple or another Tree only when actual reasoning is needed.

8. **Define action-risk levels.**
   Local organization and indexing can be highly automated, while communications, account changes, purchases, destructive actions, and other consequential operations should have stronger approval requirements.

9. **Allow Garden workload handoff.**
   When optional Garden connectivity exists, a low-power device could delegate approved heavy work to another trusted Forest device and receive the result later.

10. **Track provenance for Seed Training.**
    Each training Leaf should retain where it came from, who approved it, when it changed, whether it is trusted, and which Seeds/Trees are allowed to learn from it.

11. **Create a compatibility layer rather than hard dependencies.**
    During development, Obsidian, Hermes, Ollama, and other tools can act as prototypes or replaceable backends. Forest-facing interfaces should remain stable so components can later be replaced by native equivalents.

12. **Document a minimum viable local Forest.**
    Define the smallest set of components needed for a completely offline Forest to function. Everything involving Garden, remote models, cloud services, or external accounts should be additive rather than required.
