/**
 * Zero-dependency copy spinning engine for pSEO.
 * Uses a deterministic Seeded PRNG based on the city's slug.
 * This guarantees stable text across builds (SSG) while maintaining 
 * high uniqueness across 10,000+ localized pages.
 */

// Simple DJB2 string hashing function to generate a stable seed from slug
function getSeed(str: string): number {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = (hash * 33) ^ str.charCodeAt(i);
  }
  return Math.abs(hash);
}

// Linear Congruential Generator (PRNG) for stable, seeded random selection
function createPRNG(seed: number) {
  let current = seed;
  return {
    next: () => {
      current = (current * 1664525 + 1013904223) % 4294967296;
      return current / 4294967296;
    },
    pick: <T>(arr: T[]): T => {
      const rand = (current * 1664525 + 1013904223) % 4294967296;
      current = rand;
      const index = Math.floor((rand / 4294967296) * arr.length);
      return arr[index];
    }
  };
}

export interface SpinInput {
  city: string;
  stateCode: string;
  stateFull: string;
  slug: string;
  landfillName: string;
  permitCost: number;
  permitRequired: number;
}

export interface SpunCopy {
  heroIntro: string;
  pricingIntro: string;
  permitDetails: string;
  landfillDetails: string;
}

export function spinLocationCopy(input: SpinInput): SpunCopy {
  const seed = getSeed(input.slug);
  const prng = createPRNG(seed);

  const { city, stateCode, stateFull, landfillName, permitCost, permitRequired } = input;

  // ----------------------------------------------------
  // Paragraph 1: Hero Intro Choices (Overview / Purpose)
  // ----------------------------------------------------
  const heroIntroOptions = [
    `Planning a residential cleanout, commercial remodel, or construction project in ${city}? We coordinate directly with local waste dispatch teams to deliver robust roll-off dumpsters right to your driveway or job site.`,
    `Tackling a major renovation or cleanout in the ${city} area? We pool local hauler networks together to secure next-day dumpster drops, keeping your waste disposal simple and incredibly affordable.`,
    `Need a reliable dumpster for a residential purge or commercial construction site in ${city}? Our dynamic local aggregation maps out the lowest-priced waste haulers near you for immediate drops.`,
    `From home cleanups to heavy-duty building demolition projects in ${city}, getting rid of solid waste shouldn't be stressful. We connect you with verified local haulers for seamless next-day drops.`
  ];

  // ----------------------------------------------------
  // Paragraph 2: Pricing Intro Choices
  // ----------------------------------------------------
  const pricingIntroOptions = [
    `Waste removal pricing shouldn't be a guessing game. In ${city}, our flat-rate bundles include delivery, local landfill tipping allowances, and scheduled pickups, with zero hidden environmental surcharges.`,
    `We believe in absolute transparency. Our localized ${city} pricing plans bundle delivery, pickup, rental days, and landfill weight fees into a single upfront rate, protecting you from surprise bills.`,
    `Forget the complicated billing systems of legacy haulers. Our rates in the ${city} metro area are fully bundled, covering drop-offs, pickups, and waste limits so you can budget with total confidence.`,
    `Streamlined debris management is key to keeping your project on track. We offer straightforward flat rates in ${city} that cover everything from transport to standard weight allocations.`
  ];

  // ----------------------------------------------------
  // Paragraph 3: Permit Details Choices
  // ----------------------------------------------------
  const permitDetailsOptions = permitRequired === 1
    ? [
        `Because public right-of-way placements require compliance, ${city} mandates a **Right-of-Way (ROW) Permit** if your bin must sit on public streets or sidewalks. The typical application fee is estimated at **$${permitCost.toFixed(2)}**. Our dispatch team can assist you with municipal paperwork.`,
        `If your dumpster needs to be positioned on a public street, sidewalk, or alley in ${city}, you will need to secure a **street placement permit** for approximately **$${permitCost.toFixed(2)}**. Bins placed entirely on your private driveway require no permits.`,
        `Local city codes in ${city} require a **municipal street permit** (averaging **$${permitCost.toFixed(2)}**) if you place the container on public property. If you have space on a private driveway or yard, you can bypass this fee entirely.`
      ]
    : [
        `Good news for local residents: ${city} has highly relaxed public placement rules. Bins sitting on standard residential streets usually do not require complex ROW permits, provided they don't block fire hydrants or traffic.`,
        `Street placement rules in ${city} are remarkably straightforward. Typically, no right-of-way permit is required for residential drop-offs, making it simple to place a bin curbside if driveway space is limited.`,
        `Placement rules are highly relaxed across ${city}. You generally won't face municipal permit fees for placing a bin on public residential streets, though keeping it on a private driveway is always the safest option.`
      ];

  // ----------------------------------------------------
  // Paragraph 4: Landfill Details Choices
  // ----------------------------------------------------
  const landfillDetailsOptions = [
    `To support environmental compliance, all sorted recycling materials and general solid waste collected in ${city} is hauled directly to the eco-certified ${landfillName} processing center.`,
    `Ecological responsibility is a core focus. All residential cleanout junk and construction debris gathered in the ${city} area is taken directly to ${landfillName} for proper sorting and disposal.`,
    `We route all dumpsters straight to local waste facilities, ensuring that debris from your ${city} project is processed responsibly at the highly compliant ${landfillName}.`,
    `Waste is transported directly to ${landfillName}, where recyclables are separated from landfill-bound debris to maintain eco-compliance in the greater ${city} area.`
  ];

  return {
    heroIntro: prng.pick(heroIntroOptions),
    pricingIntro: prng.pick(pricingIntroOptions),
    permitDetails: prng.pick(permitDetailsOptions),
    landfillDetails: prng.pick(landfillDetailsOptions)
  };
}
