/*
 * Copyright (C) 2026 YIQISOFT
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scope the primary sidebar to a single product manual.
 *
 * /guides/ is a navigation landing page with no sidebar (handled by front
 * matter). On /guides/<product>/... pages we hide every other product entry
 * and the Overview entry, so the left navigation shows only that product's own
 * manual. Switching product goes through the top "Guides" tab -> landing page.
 *
 * A product entry is the <li> that is a direct child of the shared product
 * list <ul>. It is either a nested section (products with many pages) or a
 * single leaf (products with only a getting-started page), so we resolve it
 * structurally rather than by a class.
 */
(function () {
  'use strict';

  var PRODUCTS = [
    'sphere', 'identity', 'link', 'forge', 'horizon',
    'edge', 'fleet', 'mobile'
  ];

  function pathOf(href) {
    try {
      return new URL(href, window.location.href).pathname;
    } catch (e) {
      return '';
    }
  }

  function isProductLink(path, product) {
    var suffix = '/guides/' + product + '/getting-started/';
    return path.length >= suffix.length &&
      path.lastIndexOf(suffix) === path.length - suffix.length;
  }

  function scopeSidebar() {
    var match = window.location.pathname.match(/\/guides\/([a-z]+)\//);
    if (!match || PRODUCTS.indexOf(match[1]) === -1) {
      return;
    }

    var primary = document.querySelector(
      '.md-sidebar--primary nav.md-nav--primary'
    );
    if (!primary) {
      return;
    }

    var anchors = Array.prototype.slice.call(
      primary.querySelectorAll('a.md-nav__link')
    );

    // Resolve one anchor per product.
    var productAnchors = PRODUCTS.map(function (product) {
      for (var i = 0; i < anchors.length; i++) {
        if (isProductLink(pathOf(anchors[i].getAttribute('href')), product)) {
          return anchors[i];
        }
      }
      return null;
    }).filter(Boolean);

    if (productAnchors.length === 0) {
      return;
    }

    document.body.classList.add('nr-guide-scope');

    // The shared product list is the lowest <ul> that contains every product
    // link; each product entry is one of its direct <li> children.
    var productList = productAnchors[0].parentElement;
    while (productList && productList.tagName !== 'UL') {
      productList = productList.parentElement;
    }
    while (productList) {
      var containsAll = productAnchors.every(function (a) {
        return productList.contains(a);
      });
      if (containsAll) {
        break;
      }
      productList = productList.parentElement.closest('ul');
    }
    if (!productList) {
      return;
    }

    function entryOf(anchor) {
      var li = anchor.closest('li');
      while (li && li.parentElement !== productList) {
        li = li.parentElement.closest('li');
      }
      return li;
    }

    function isActive(li) {
      return li.classList.contains('md-nav__item--active') ||
        li.classList.contains('md-nav__item--current') ||
        !!li.querySelector('.md-nav__link--active, .md-nav__link--current');
    }

    // Keep only the active product entry; hide the rest.
    productAnchors.forEach(function (anchor) {
      var li = entryOf(anchor);
      if (li && !isActive(li)) {
        li.classList.add('nr-guide-hide');
      }
    });

    // Hide the Guides "Overview" landing entry while inside a product manual.
    anchors.forEach(function (a) {
      var p = pathOf(a.getAttribute('href'));
      if (p === '/guides/' || /\/guides\/$/.test(p)) {
        var li = entryOf(a);
        if (li) {
          li.classList.add('nr-guide-hide');
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scopeSidebar);
  } else {
    scopeSidebar();
  }
})();
