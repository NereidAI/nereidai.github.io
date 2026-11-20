# Copyright (C) 2026 YIQISOFT
# SPDX-License-Identifier: Apache-2.0

"""Run Material's blog plugin correctly with mkdocs-static-i18n.

The blog plugin normally runs before i18n. i18n then replaces the blog's File
objects and removes its generated archive/category views, which leaves posts
rendered as ordinary pages. This hook keeps the standard Material blog setup
and only adapts the event order and localized output metadata:

* blog's files/navigation events run after i18n;
* generated non-default-language pages retain their language URL prefix;
* generated views receive the same canonical and alternate links as posts.

See https://squidfunk.github.io/mkdocs-material/plugins/blog/ for blog usage.
"""

import copy
import os
from pathlib import PurePath

from material.plugins.blog.plugin import BlogPlugin
from mkdocs.plugins import event_priority

_BLOG_PRIORITY = -150
_HOOK_PRIORITY = -200


def _is_blog_url(url, language, default_language):
    """Return whether a final or unlocalized URL belongs to the blog."""
    if language != default_language and url.startswith(f"{language}/"):
        url = url[len(language) + 1 :]
    return url == "blog/" or url.startswith("blog/")


@event_priority(_HOOK_PRIORITY)
def on_config(config):
    """Reorder only Material blog events, leaving all other plugins intact."""
    if not config.plugins.get("i18n"):
        return

    for event_name in ("files", "nav"):
        methods = config.plugins.events[event_name]
        for method in methods:
            if isinstance(getattr(method, "__self__", None), BlogPlugin):
                method.__func__.mkdocs_priority = _BLOG_PRIORITY
        methods.sort(key=lambda method: -getattr(method, "mkdocs_priority", 0))


@event_priority(_HOOK_PRIORITY)
def on_files(files, config):
    """Restore i18n metadata and language prefixes after blog URL generation."""
    i18n = config.plugins.get("i18n")
    if not i18n:
        return

    language = i18n.current_language
    default_language = i18n.default_language
    for file in files:
        if not _is_blog_url(file.url, language, default_language):
            continue

        # Generated archive/category files do not pass through i18n themselves.
        if not hasattr(file, "locale"):
            file.locale = default_language
            file.localization = None
            file.norm_src_uri = file.src_uri
        file.locale_alternate_of = language

        if (
            language == default_language
            or file.dest_uri.startswith(f"{language}/")
        ):
            continue
        file.dest_path = (PurePath(language) / file.dest_path).as_posix()
        file.abs_dest_path = os.path.join(config.site_dir, file.dest_path)
        file.url = file._get_url(config.use_directory_urls)


@event_priority(_HOOK_PRIORITY)
def on_nav(nav, config, files):
    """Finalize blog alternates after posts and generated views have URLs."""
    i18n = config.plugins.get("i18n")
    if not i18n:
        return

    language = i18n.current_language
    default_language = i18n.default_language
    for file in files.documentation_pages():
        if not _is_blog_url(file.url, language, default_language):
            continue

        base_dest_uri = file.dest_uri
        if (
            language != default_language
            and base_dest_uri.startswith(f"{language}/")
        ):
            base_dest_uri = base_dest_uri[len(language) + 1 :]

        alternates = {}
        for alternate_language in i18n.build_languages:
            if alternate_language == language:
                alternate = file
            else:
                alternate = copy.copy(file)
                alternate.dest_uri = (
                    base_dest_uri
                    if alternate_language == default_language
                    else f"{alternate_language}/{base_dest_uri}"
                )
                alternate.abs_dest_path = os.path.join(
                    config.site_dir, alternate.dest_uri
                )
                alternate.url = alternate._get_url(config.use_directory_urls)
                alternate.locale_alternate_of = alternate_language
                alternate.page = None
            alternates[alternate_language] = alternate

        file.alternates = alternates
        if file.page:
            file.page._set_canonical_url(config.site_url)

    # Include generated views in i18n's sitemap/language-switcher file store.
    i18n.i18n_files_per_language[language] = files.documentation_pages()
