# Update and Replace Commands

These commands are designed for Maple. They detect either repository location
used during the project.

## 1. Set repository paths

```bash
if [[ -d "$HOME/Projects/project-digital-cross" ]]; then
    export PDC_ROOT="$HOME/Projects/project-digital-cross"
elif [[ -d "$HOME/project-digital-cross" ]]; then
    export PDC_ROOT="$HOME/project-digital-cross"
else
    echo "Project Digital Cross repository not found."
    return 1 2>/dev/null || exit 1
fi

if [[ -d "$HOME/Projects/pdc-forest-language" ]]; then
    export FOREST_ROOT="$HOME/Projects/pdc-forest-language"
elif [[ -d "$HOME/pdc-forest-language" ]]; then
    export FOREST_ROOT="$HOME/pdc-forest-language"
else
    echo "Forest Language repository not found."
    return 1 2>/dev/null || exit 1
fi

export TEMPLATE_LIBRARY="$HOME/PDC-Template-Library-Draft11-Updated"

printf 'PDC_ROOT=%s\nFOREST_ROOT=%s\nTEMPLATE_LIBRARY=%s\n' \
    "$PDC_ROOT" "$FOREST_ROOT" "$TEMPLATE_LIBRARY"
```

## 2. Rename Forest Guide to Forest Compass

```bash
for repo in "$PDC_ROOT" "$FOREST_ROOT"; do
    old="$(find "$repo" -type f -name 'FOREST-GUIDE.md' -print -quit)"
    if [[ -n "$old" ]]; then
        new="${old%/*}/FOREST-COMPASS.md"
        if git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
            git -C "$repo" mv "${old#"$repo"/}" "${new#"$repo"/}"
        else
            mv "$old" "$new"
        fi
        printf 'Renamed: %s -> %s\n' "$old" "$new"
    fi
done
```

## 3. Locate the old monolithic pack

```bash
find "$PDC_ROOT" "$FOREST_ROOT" \
    -type f -name 'PDC_Template_Pack_Draft11.md' -print
```

After confirming the returned path, preserve it as Leaf Litter:

```bash
mkdir -p "$PDC_ROOT/leaf-litter/superseded/template-packs"

# Replace /FULL/PATH/FROM/FIND with the exact path printed above.
mv "/FULL/PATH/FROM/FIND/PDC_Template_Pack_Draft11.md" \
   "$PDC_ROOT/leaf-litter/superseded/template-packs/"
```

## 4. Review the new library before replacing anything

```bash
cd "$TEMPLATE_LIBRARY" || exit 1
less README.md
less CATALOG.md
```

Compare the template directories:

```bash
git diff --no-index -- \
    "$PDC_ROOT/templates" \
    "$TEMPLATE_LIBRARY/targets/project-digital-cross/templates" || true
```

Compare Forest language documents:

```bash
git diff --no-index -- \
    "$FOREST_ROOT" \
    "$TEMPLATE_LIBRARY/targets/pdc-forest-language" || true
```

## 5. Dry-run the update

```bash
cd "$TEMPLATE_LIBRARY" || exit 1
./scripts/APPLY-APPROVED-TEMPLATES.sh --dry-run
```

The dry run shows:

- files that would be backed up and replaced;
- new files that would be installed;
- stateful files that would be staged as `.draft11-candidate`.

## 6. Apply approved replacements

```bash
cd "$TEMPLATE_LIBRARY" || exit 1
./scripts/APPLY-APPROVED-TEMPLATES.sh --apply
```

## 7. Review staged stateful candidates

```bash
find "$PDC_ROOT" "$FOREST_ROOT" \
    -type f -name '*.draft11-candidate' -print | sort
```

Open each candidate beside its active file and merge deliberately.

Example:

```bash
diff -u \
    "$PDC_ROOT/trees/cherry/TREE.yaml" \
    "$PDC_ROOT/trees/cherry/TREE.yaml.draft11-candidate"
```

## 8. Verify and commit

```bash
git -C "$PDC_ROOT" status --short
git -C "$FOREST_ROOT" status --short
```

After review:

```bash
git -C "$PDC_ROOT" add .
git -C "$PDC_ROOT" commit -m "Update Draft 11 governed templates"

git -C "$FOREST_ROOT" add .
git -C "$FOREST_ROOT" commit -m "Update Draft 11 Forest language"
```
