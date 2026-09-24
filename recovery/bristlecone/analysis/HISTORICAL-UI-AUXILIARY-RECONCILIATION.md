# Bristlecone Pine — Historical UI and Auxiliary Runtime Reconciliation

Status: **RECONCILED AS HISTORICAL / NON-CANONICAL PRESENTATION SUPPORT**

## Historical UI

The surviving `ui/` tree is preserved under `recovery/bristlecone/historical/ui/` rather than promoted into the reconstructed production implementation.

That distinction is deliberate.

The UI source contains useful Forest architectural ideas:

- stable action identities separate WHAT a user requests from HOW a key/button invokes it;
- configurable in-window keybindings are separated from desktop-global shortcuts;
- presentation intent is platform-neutral;
- host adapters may satisfy or safely degrade presentation requests without changing Forest semantics;
- the reasoning menu delegates reasoning state/policy to the TaskSession reasoning-control backend rather than duplicating policy;
- the Qubes/i3/X11 host adapter owns host presentation behavior only.

However, the surviving current UI is tied to the historical Qubes/i3/GTK environment and is not required to establish the certified Bristlecone runtime boundary.

`ui/presentation.py` has an exact recovered Phase 14.10 recovery copy. The other current UI files are later surviving revisions without exact certified backup matches in the recovered inventory.

Therefore the full UI tree is preserved as historical implementation/reference material, not declared modern canonical Bark.

## Auxiliary runtime helpers

Two surviving late helper files are also preserved as historical auxiliary source:

- `runtime/helpers/hermes_profile_bridge.py`
- `runtime/tool_availability.py`

`hermes_profile_bridge.py` is a bounded Forest-to-Hermes helper allowing only the documented `default_model` and `api_key` operations, with Hermes-native code isolated behind the Hermes virtual environment.

`tool_availability.py` explicitly declares itself dormant by default while Hermes owns runtime tool availability. It describes a Forest-native replacement path for runtimes lacking equivalent availability caching.

Neither current helper has an exact certified backup match in the recovered inventory, and neither is needed to establish the L.10 certified core.

They are therefore retained as late architectural/support evidence rather than promoted as certified production dependencies.

## Historical runtime bootstrap

The recovery also preserves the surviving historical runtime bootstrap artifacts:

- Qwen 3.5 4B / 64k Ollama Modelfile
- Newelle local connection description
- Newelle profile instructions
- API architecture description

These document how historical Pine was connected to Hermes/Newelle. They do not define Pine's identity and do not constrain the modern Post-Apollo runtime choice.

## Modernization rule

Modern Bark/QML should preserve useful separation-of-concerns contracts from this historical UI, but should not mechanically port Qubes/i3/GTK host code into the new Sway/Wayland/Post-Apollo environment.