---
title: Contributing
---

# Contributing

NereidAI is open source under the **Apache License 2.0**, developed across a set
of independent repositories under the
[NereidAI GitHub organization](https://github.com/NereidAI). This page describes
how to engage at a high level; the **authoritative detail lives in each
repository**.

!!! info "Developer documentation"
    Contribution rules, exact commands and review expectations are owned by each
    repository. Start from the [NereidAI organization](https://github.com/NereidAI)
    and read that repository's own contributing guide and operating rules first.

## Where to engage

Every product is its own repository with its own issue tracker. Use the product
repository that owns the area you are touching — a fix in the wrong repository is
not a license to fix it elsewhere.

| Repo (GitHub org) | Owns |
|---|---|
| `Sphere` | Portal, unified API gateway, cross-product event glue. |
| `Identity` | Suite SSO / identity federation. |
| `Link` | IoT pipeline: device access, rules, alerts, dashboards. |
| `Forge` | Model factory: datasets, training, export, registry. |
| `Horizon` | Edge distribution and rollout. |
| `Edge` | Southbound edge integration on field gateways. |
| `Fleet` | Robot fleet management. |
| `Mobile` | Mobile app and WeChat Mini Program. |

Discussion happens through GitHub issues and Discussions — that is the community
support channel. For enterprise questions, see
[Community & Support](../community/support.md).

## The contribution flow

1. **Pick the owning repository** and read its `README`, contributing guide and
   operating rules.
2. **Open or find an issue** describing the change before large work, so scope is
   agreed in the open.
3. **Branch, implement, and verify** in that repository using *its own*
   format / lint / type-check / test / build commands — never invent scripts a
   project does not have.
4. **Open a pull request** with a clear description; keep each change focused and
   reviewable.

!!! note "One change, one repository"
    Sibling repositories are treated as read-only from any single repository's
    work. A cross-repo fix is handed to the owning repository as a coordinated
    change, not applied sideways.

## Commit and authorship conventions

- **Conventional Commits.** Prefix messages with a type such as `feat:`,
  `fix:`, `chore:` or `docs:`.
- **DCO sign-off.** Every commit carries a `Signed-off-by` line; use
  `git commit -s`.

    ```bash
    git commit -s
    ```

- **One verified milestone per commit.** Stage only intended files, and commit a
  stage once it is verified rather than in one large batch.

## License header

Every hand-written source file (Go, Python, TS/TSX, SQL, authored YAML, proto,
shell) must start with the project header, in the comment syntax of the language:

```text
// Copyright (C) 2026 YIQISOFT
// SPDX-License-Identifier: Apache-2.0
```

!!! warning "Vendored code is different"
    Vendored / third-party subtrees follow **upstream** conventions — upstream
    license headers, formatting and workflow. Do not add or revert headers there.
    The header rule applies only to hand-written NereidAI code.

## Verify before you finish

Never finish on "edited successfully" — finish on "verified". Run the owning
repository's formatting, lint, type-check, tests and build, and fix every
failure. Note that front-end bundler builds do not type-check on their own, so
run the project's type checker separately. Clean up any test processes and
temporary files you created. The exact commands are listed in the repository.

## Versioning and contracts

- A repository-level `VERSION` file is the **release source of truth** and the
  source of derived image tags; do not change it without an explicit request.
- When a public API, request/response shape, WebSocket frame or wire contract
  changes, update the specification and the affected docs in the **same change**.

## Next steps

- [Getting Started](getting-started.md) — orient yourself in the suite.
- [Conventions](conventions.md) — the shared coding conventions.
- [Cross-Product Contracts](../architecture/contracts.md) — what the suite fixes.
