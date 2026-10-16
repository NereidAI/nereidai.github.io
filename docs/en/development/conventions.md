---
title: Conventions
---

# Conventions

The suite shares a small set of conventions that hold across every product
repository. This page is a concise, upper-layer summary — the **authoritative
detail lives in the repositories**, in each product's operating rules and its
own contributor documentation.

!!! info "Developer documentation"
    Treat this as orientation, not as the rulebook. The binding version of every
    convention below is defined in the repository. Start from the
    [NereidAI organization](https://github.com/NereidAI).

## Language and comments

- **Comments are English only.** Chinese comments in source are not allowed.
- **Every file has a module/package-level comment** describing what it does, its
  architectural role, and important invariants.
- **Doc comments start with the identifier name.** Every exported function,
  method, type, interface and constant carries a doc comment beginning with the
  identifier it documents; non-trivial unexported code is commented too.
- **Comments explain *why*** — intent, invariants, ordering, workarounds — not
  a restatement of the code.

## License header

Every hand-written source file (Go, Python, TS/TSX, SQL, authored YAML, proto,
shell) begins with the project header, using the language's comment syntax:

```text
// Copyright (C) 2026 YIQISOFT
// SPDX-License-Identifier: Apache-2.0
```

Generated files are exempt only where the generator controls the header;
vendored / third-party subtrees keep their upstream headers and follow upstream
conventions.

## Change discipline

The simplest complete solution wins, and the order of preference for every
change is **Delete > Replace > Add**:

- Solve problems at the owner of the behaviour rather than guarding a symptom.
- Search the repository before adding anything; reuse or extend what exists.
- Keep scope minimal — no speculative flags, shims or unrelated cleanup.
- Keep one authoritative definition per fact (defaults, labels, image tags) and
  align every copy in the same change.

## API and data conventions

| Convention | Rule |
|---|---|
| **API specification** | Public APIs are described with **OpenAPI 3.1**; the spec moves in the same change as the code, and must parse. |
| **Empty arrays** | Arrays are emitted as `[]`, never `null`. Clients may rely on the shape. |
| **No invented semantics** | The platform never guesses meaning — e.g. units come only from user-defined descriptors. |
| **Neutral contracts** | Wire contracts and platform APIs stay protocol-, stack-, and vendor-agnostic. |
| **Migrations** | Schema changes ship as explicit, numbered, reversible (paired up/down) migrations — never auto-mutated at startup. |

## Internationalization

- **No hardcoded user-facing strings.** Every label and message goes through the
  project's translation mechanism (`t(...)`).
- **Both locales move together.** New keys land in the English and Chinese
  locales in the same change, and the project's i18n check runs as part of it.
- Operator-visible behaviour is documented in both languages' help docs in the
  same change.

## Language and stack (confirmed)

Where a convention is language-specific, it follows the product's own stack:

- **Go services** use the standard library `net/http` (Sphere) and `pgx`
  for PostgreSQL access (Link).
- **Python services** use FastAPI (Forge, and Fleet's planned
  platform API).

> These are orientation notes only; each repository documents the exact
> libraries, versions and tooling it uses.

## Next steps

- [Getting Started](getting-started.md) — orient yourself in the suite.
- [Contributing](contributing.md) — how to engage with the repositories.
- [Cross-Product Contracts](../architecture/contracts.md) — the contract rules.
