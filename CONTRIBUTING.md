# Contributing

1. Copy `TEMPLATE.md` to `techniques/T0XX-short-slug.md` using the next free id.
2. Fill in every section. Keep the **Minimal example inert**: static text only,
   reserved domains (`example.com` / `example.net`), no real hosts or
   credentials. If a technique can't be embedded safely (e.g. invisible
   characters), *describe* it instead.
3. Add a matching entry to `index.json`.
4. Validate:
   ```bash
   python3 scripts/validate.py
   ```
   CI runs the same check and will fail the PR if a section is missing or the
   index and files disagree.

## Scope

This is a *defensive* reference. Entries explain how an attack works so it can
be detected and prevented. Don't add working exploits, live payloads, or
anything whose main use is to cause harm.
