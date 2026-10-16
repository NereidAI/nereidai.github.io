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
- Deployed automatically by GitHub Actions on push to `main`

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

## Editing

- Add or edit a page in **both** `docs/en/` and `docs/zh/`, and register it in the
  `nav` in `mkdocs.yml` (Chinese navigation labels are provided by the
  `nav_translations` block).
- Keep pages at the product / value / capability level. Do not copy implementation
  detail (internal services, ports, commands, migrations) from the product
  repositories — link to them instead with a `!!! info "Developer documentation"`
  (or `!!! info "开发者文档"`) pointer.
- New pages must build clean under `mkdocs build --strict`.

## Deployment

`.github/workflows/deploy.yml` builds the site and deploys it to GitHub Pages on
every push to `main` that touches `docs/**`, `mkdocs.yml`, or `requirements.txt`.
Enable **Settings → Pages → Source: GitHub Actions** in the repository once.

## License

Copyright (C) 2026 YIQISOFT — Apache License 2.0.
