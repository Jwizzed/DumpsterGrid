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
  testimonialName: string;
  testimonialRole: string;
  testimonialText: string;
  testimonialName2: string;
  testimonialRole2: string;
  testimonialText2: string;
  testimonialName3: string;
  testimonialRole3: string;
  testimonialText3: string;
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

  // Testimonial 1: Residential customer
  const testimonialNames1 = ['Mike R.', 'Jason T.', 'David L.', 'Chris M.', 'Brian K.'];
  const testimonialRoles1 = ['Homeowner', 'Property Owner', 'Resident', 'Home Renovator', 'DIY Homeowner'];
  const testimonialTexts1 = [
    `Fast delivery and fair pricing for my kitchen demo in ${city}. The driver placed it exactly where I needed on my driveway. Would absolutely use again.`,
    `Needed a 20-yard dumpster for a full garage cleanout in ${city}. Showed up next morning, picked up on time. No surprise fees. Exactly what was quoted.`,
    `Used them for a bathroom remodel in ${city}. The flat-rate pricing was transparent and the dumpster arrived within the delivery window. Very smooth process.`,
    `Rented a 30-yard for a major home renovation in ${city}. Competitive price, on-time delivery, and the pickup was scheduled exactly when I needed it.`
  ];

  // Testimonial 2: Contractor/Commercial
  const testimonialNames2 = ['Sarah M.', 'Jennifer P.', 'Amanda K.', 'Lisa D.', 'Karen W.'];
  const testimonialRoles2 = ['GC, Local Construction', 'Project Manager', 'Site Supervisor', 'Operations Manager', 'Renovation Contractor'];
  const testimonialTexts2 = [
    `We run multiple job sites across ${stateCode} and these guys consistently deliver the best rates in the ${city} area. Reliable partner for our crew.`,
    `Managing waste on a commercial tear-down in ${city} was seamless. They handled the permits guidance and had the 40-yard bin dropped same week.`,
    `Our construction company uses them for every project in the ${city} metro. Predictable flat rates make budgeting easy. No games with overage fees.`,
    `As a contractor working throughout ${stateFull}, their ${city} dispatch is always responsive. Good communication and fair pricing on every rental.`
  ];

  // Testimonial 3: Positive general
  const testimonialNames3 = ['Tom H.', 'Robert S.', 'James W.', 'Andrew F.', 'Daniel B.'];
  const testimonialRoles3 = [`${city} Resident`, 'Small Business Owner', 'Property Manager', 'Real Estate Investor', 'Landlord'];
  const testimonialTexts3 = [
    `Best dumpster rental experience I've had in ${city}. The online quote matched the final price exactly. Refreshingly honest service.`,
    `Compared 3 different haulers in ${city} and this was the most affordable by far. Clean dumpster, on-time drop, hassle-free pickup. 5 stars.`,
    `Managing a rental property cleanout in ${city}. They made it simple — booked online, dumpster arrived next day, picked up when I called. Perfect.`,
    `I've used local haulers in ${city} before but the pricing was always confusing. These flat rates are clear and the service was professional.`
  ];

  return {
    heroIntro: prng.pick(heroIntroOptions),
    pricingIntro: prng.pick(pricingIntroOptions),
    permitDetails: prng.pick(permitDetailsOptions),
    landfillDetails: prng.pick(landfillDetailsOptions),
    testimonialName: prng.pick(testimonialNames1),
    testimonialRole: prng.pick(testimonialRoles1),
    testimonialText: prng.pick(testimonialTexts1),
    testimonialName2: prng.pick(testimonialNames2),
    testimonialRole2: prng.pick(testimonialRoles2),
    testimonialText2: prng.pick(testimonialTexts2),
    testimonialName3: prng.pick(testimonialNames3),
    testimonialRole3: prng.pick(testimonialRoles3),
    testimonialText3: prng.pick(testimonialTexts3),
  };
}

export interface ActivityTickerItem {
  size: string;
  city: string;
  state: string;
  minutesAgo: number;
}

export function spinActivityTicker(slug: string, nearbyCity: string, stateCode: string): ActivityTickerItem[] {
  const seed = getSeed(slug + '-activity');
  const prng = createPRNG(seed);

  const sizes = ['10-Yard', '20-Yard', '30-Yard', '40-Yard'];
  const minutesOptions = [3, 7, 12, 18, 24, 31, 45];

  return [
    {
      size: prng.pick(sizes),
      city: nearbyCity,
      state: stateCode,
      minutesAgo: prng.pick(minutesOptions)
    },
    {
      size: prng.pick(sizes),
      city: nearbyCity,
      state: stateCode, 
      minutesAgo: prng.pick(minutesOptions)
    },
    {
      size: prng.pick(sizes),
      city: nearbyCity,
      state: stateCode,
      minutesAgo: prng.pick(minutesOptions)
    }
  ];
}
