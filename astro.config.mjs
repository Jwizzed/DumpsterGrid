// @ts-check
import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';

import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// ---------------------------------------------------------------------------
// Sitemap must carry indexable URLs only.
//
// GSC (window ending 2026-08-26): 0 clicks, 1 indexed page, against 10,060
// URLs in the live sitemap. A brand-new domain with zero backlinks gets a
// near-zero crawl budget; listing 10,060 thin/duplicate city pages spends
// that budget on pages Google will never keep. The fix is not a bigger
// crawl budget — it's a sitemap that only asks for what's actually worth
// indexing.
//
// "estimated" city pages (9,834 of them) carry no verified local fact
// (landfill name, permit cost) and are marked
// <meta name="robots" content="noindex, follow"> in [slug].astro. They stay
// OUT of the sitemap, but they are NOT blocked in robots.txt and are still
// linked from the state hubs, so they keep passing crawl equity — see the
// comment in public/robots.txt for why that distinction matters.
//
// "verified" city pages (166 of them) carry a real landfill name sourced by
// Lane A and are the only per-city pages worth asking Google to index.
// ---------------------------------------------------------------------------

const __dirname = dirname(fileURLToPath(import.meta.url));
const dbPath = join(__dirname, 'dumpsters.db');

const db = new DatabaseSync(dbPath);
const verifiedSlugs = /** @type {Array<{ slug: string }>} */ (
  db.prepare(`SELECT slug FROM locations WHERE data_quality = 'verified'`).all()
).map((row) => `/locations/${row.slug}`);
db.close();

const verifiedSlugSet = new Set(verifiedSlugs);

/** @param {string} pathname */
function normalize(pathname) {
  return pathname.length > 1 ? pathname.replace(/\/$/, '') : pathname;
}

/** @param {string} pathname */
function isIndexable(pathname) {
  const path = normalize(pathname);

  // Home, the locations hub, and each of the 4 size pages.
  if (path === '/' || path === '/locations') return true;
  if (/^\/dumpster-sizes\/\d{2}-yard$/.test(path)) return true;

  // The 50-state (+ DC, PR) hubs, e.g. /locations/ny.
  if (/^\/locations\/[a-z]{2}$/.test(path)) return true;

  // Only the ~166 verified city pages. Estimated city pages are
  // intentionally excluded — see the header comment above.
  return verifiedSlugSet.has(path);
}

// https://astro.build/config
export default defineConfig({
  site: 'https://dumpstergrid.com',
  integrations: [
    sitemap({
      // Single build-time date applied to every entry — not a per-page
      // fabricated "last updated" claim, just when this sitemap was cut.
      lastmod: new Date(),
      filter: (page) => isIndexable(new URL(page).pathname)
    })
  ],
  vite: {
    plugins: [tailwindcss()]
  }
});
