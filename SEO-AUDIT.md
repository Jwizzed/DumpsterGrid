# SEO audit and remediation plan — 2026-09-05

**Verdict: the build is competent, the data is fabricated. Data is the SEO problem.**

Google Search Console, window ending 2026-08-26: **0 clicks, 1 indexed page, 3 not indexed**,
against **10,060 URLs in a valid live sitemap**. That gap is the whole finding.

---

## What is NOT broken

Deploy serves 200s. `sitemap-index.xml` is valid and lists 10,060 URLs. Canonicals are correct and
absolute. Titles and meta descriptions render per page. `robots.txt` allows all and declares the
sitemap. Astro SSG + Cloudflare Pages is a sound stack for this.

**Do not spend effort here.** Nothing in the technical layer explains 1 indexed page.

## What IS broken

| # | Finding | Evidence |
|---|---|---|
| 1 | **Every local fact is fabricated** | `0` of 10,000 rows carry a real landfill name — all are `"<City> County Resource Recovery"`. The ~150 real names in `scripts/seed_db.py` `CITIES_DATA` were never written to the DB |
| 2 | **5,000 invented phone numbers, published as business contact data** | `scripts/seed_db.py:260` → `f"800-508-{4000 + idx}"`, rendered inside `LocalBusiness` schema and `tel:` links. Parts of the 800-508 range are assigned to real businesses |
| 3 | **Prices are 10 combinations wearing 10,000 hats** | `select count(distinct avg_low_10yd\|\|'-'\|\|avg_high_40yd)` → `10`. Shipped as *"Rent a roll-off dumpster in Chicago, IL starting at $480"* |
| 4 | **Copy spinning** | `src/lib/spin.ts` — deterministic PRNG text spinning across 10,000 pages. Named explicitly in Google's scaled-content-abuse policy |
| 5 | **Intent stated in the source** | `scripts/seed_db.py:281` — *"slight random perturbation ... to look authentic"* |

**Why only 1 page indexed:** a brand-new domain with zero backlinks gets a near-zero crawl budget.
Google sampled the site, found templated pages with no corroborating external signal, and stopped.
Submitting the sitemap harder does not buy crawl budget. **Fixing crawl before fixing data only
reaches the penalty faster.**

---

## The plan — three file-exclusive lanes, then build and push

### Lane A — data layer *(owns `scripts/seed_db.py`, `dumpsters.db`)*
1. Rewrite the seeder so the ~150 curated cities keep their **real** landfill names and populations.
2. Add `data_quality TEXT` — `verified` for the curated set, `estimated` for the rest.
3. Add `price_basis TEXT` — every price is a **national estimate**, never a local quote. Say so in data.
4. **Delete the phone column's fabricated values.** One sitewide contact, or none.
5. Never generate a facility name. `landfill_name` is `NULL` when unknown; the template must handle NULL.

### Lane B — city template *(owns `src/pages/locations/[slug].astro`, `src/lib/spin.ts`, `src/layouts/Layout.astro`)*
1. **Delete `spin.ts`** and every call to it. Differentiation comes from real fields or not at all.
2. `<meta name="robots" content="noindex, follow">` on every `data_quality='estimated'` page,
   behind a single exported constant so it flips back in one line.
3. Replace `LocalBusiness` schema — the site is not a local business in 10,000 cities. Use
   `Service` + `BreadcrumbList` + `FAQPage`.
4. Drop `AggregateOffer` price claims, or scope them to a labelled national estimate range.
5. Remove every `tel:` link and phone render. The lead form is the conversion path.

### Lane C — hubs, crawl architecture, config *(owns `src/pages/locations/index.astro`, `src/pages/locations/[state]/index.astro`, `src/pages/dumpster-sizes/[size].astro`, `astro.config.mjs`, `public/robots.txt`)*
1. **Sitemap carries indexable URLs only** — filter `estimated` pages out via the sitemap integration.
   10,060 → ~200. This is the actual indexing fix.
2. State hubs link to their verified cities directly; no city page deeper than 2 clicks from root.
3. Size pages get real, non-spun content and link into the verified city set.

### Finish — build, verify, push
`npm run build`, confirm sitemap URL count dropped, confirm `noindex` present on an estimated page
and absent on a verified one, confirm zero `800-508-` strings in `dist/`.

---

## Two judgment calls made without asking, both one-line reversible

- **Phone removed sitewide**, lead form only. Restoring needs one real number JJ controls.
- **Estimated cities set to `noindex`**, cutting the indexable set from 10,060 to ~200. Flip the
  constant in `[slug].astro` to revert. This is what makes indexing possible at all: 200 crawlable
  pages on a new domain is a budget Google will spend; 10,060 is not.
