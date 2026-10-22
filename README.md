# NereidAI — Official Website & Documentation

Source of the NereidAI official website and consolidated documentation, published
to GitHub Pages at <https://nereidai.github.io>.

The site is deliberately **upper-layer**: it describes *what* the platform and
its products are and *what you can do with them*. Deep, repository-specific
developer documentation is not duplicated here — each product links back to its
own repository under the [NereidAI organization](https://github.com/NereidAI).

## Stack

- [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [`mkdocs-static-i18n`](https://github.com/ultrabug/mkdocs-static-i18n) — bilingual,
  English (default, served at the site root) and Chinese (`/zh/`)
- [mike](https://github.com/jimporter/mike) + Material's version selector —
  frozen release snapshots under `/vX.Y.Z/`, rolling `dev` docs, header
  version switcher on every page
- Deployed automatically by GitHub Actions on push to `main` and on `v*` tags

## Layout

```text
docs/
  en/          English pages (default locale)
  zh/          Chinese pages
  assets/      logo, favicon, images (shared)
  theme/       custom.css
mkdocs.yml     site config: theme, plugins, nav, i18n
requirements.txt
```

Each locale mirrors the same tree:

```text
index.md
products/        suite overview + one page per product
solutions/       commercial industry solutions
architecture/    overview, topology, contracts
deployment/      air-gapped, kubernetes, edge-delivery
security/        overview, sso-oidc, rbac
development/     getting-started, contributing, conventions
community/       license, community-vs-enterprise, roadmap, support
```

## Local development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

mkdocs serve          # http://127.0.0.1:8000
mkdocs build --strict # CI uses the same strict build
```

`mkdocs serve` previews the working tree without a version label. To preview the
versioned site exactly as published (selector + all snapshots), publish locally
to a throwaway branch and serve it:

```bash
mike deploy dev                       # write working tree to local gh-pages
mike set-default latest               # optional, once a release exists
git worktree add site-preview gh-pages
cd site-preview && python -m http.server
```

## Editing

- Add or edit a page in **both** `docs/en/` and `docs/zh/`, and register it in the
  `nav` in `mkdocs.yml` (Chinese navigation labels are provided by the
  `nav_translations` block).
- Keep pages at the product / value / capability level. Do not copy implementation
  detail (internal services, ports, commands, migrations) from the product
  repositories — link to them instead with a `!!! info "Developer documentation"`
  (or `!!! info "开发者文档"`) pointer.
- New pages must build clean under `mkdocs build --strict`.

## Deployment & documentation versions

Documentation is versioned with [mike](https://github.com/jimporter/mike). All
snapshots are committed to the `gh-pages` branch by CI and uploaded together as
one GitHub Pages artifact — **Settings → Pages → Source: GitHub Actions** stays
unchanged.

| Event | Published URL | Meaning |
| --- | --- | --- |
| Push to `main` | `/dev/` | Rolling work-in-progress docs |
| Tag `vX.Y.Z` | `/vX.Y.Z/` (and `/latest/`) | Frozen release snapshot; `latest` moves to it |

The site root (`/`) redirects to `/latest/`. Every page shows a header version
switcher; pages that are not the latest release show an outdated-version banner.

**Cut a new release** (e.g. the first one):

```bash
git tag v0.0.1
git push origin v0.0.1
```

CI builds `/v0.0.1/`, moves the `latest` alias, and keeps every older snapshot
intact. The next release is `v0.0.2`, and so on. Never re-publish an existing
tag: published versions are meant to stay frozen. Management commands
(`mike list`, `mike retitle`, `mike delete`) run against the `gh-pages` branch;
see the [mike docs](https://github.com/jimporter/mike) for details.

## License

Copyright (C) 2026 YIQISOFT — Apache License 2.0.
