Phase 14.10E.2A.2 recovery install

Original failure cause:
The isolated subprocess ran with the real Forest repository as cwd, causing Python to import the real ui package before the staged ui package.

Correction:
Both isolated tests were executed with the staged Forest root as cwd and PYTHONPATH.

Reasoning state/backend were not changed.
