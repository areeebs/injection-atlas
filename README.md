# injection-atlas

A documented, reproducible catalog of **prompt-injection and skill/MCP
poisoning techniques** — what each one is, a minimal inert example, why it
works, how to detect it, and how to mitigate it.

Scanners publish rule counts; defenders need to understand the *techniques*
themselves. injection-atlas is a reference you can read, cite, and build tests
from. The machine-readable [`index.json`](index.json) lets other projects pull
the catalog in — for example to generate benchmark samples for
[`skill-sec-bench`](https://github.com/areeebs/skill-sec-bench).

## Techniques

| id   | technique                               | category            | severity |
|------|-----------------------------------------|---------------------|----------|
| T001 | Hidden HTML-comment directive           | prompt-injection    | high     |
| T002 | Tool-description poisoning              | tool-poisoning      | high     |
| T003 | Credential exfiltration via diagnostics | data-exfiltration   | critical |
| T004 | Permission overreach                    | permission-mismatch | high     |
| T005 | Invisible Unicode tag smuggling         | prompt-injection    | high     |

Each entry lives in [`techniques/`](techniques/) and follows a fixed structure:
Summary, How it works, Minimal example, Why it works, Detection, Mitigation,
References.

## Safety

Every example is **inert**: static text, reserved example domains
(`example.com` / `example.net`), and nothing runnable. Anything that can't be
made safely inert (such as invisible characters) is *described* rather than
embedded. This is a defensive reference.

## Validate

```bash
python3 scripts/validate.py
```

Checks that every technique file has the required front matter and sections, and
that `index.json` matches the files on disk. CI runs this on every push and PR.

## Contributing

New techniques welcome — copy [`TEMPLATE.md`](TEMPLATE.md), fill it in, add an
`index.json` entry, and run the validator. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE).
