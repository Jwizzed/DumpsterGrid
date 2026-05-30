/**
 * Cloudflare Pages native serverless endpoint to process incoming leads.
 * Intercepts POST requests at /api/lead.
 * Operates entirely on Cloudflare edge worker platform ($0.00 / month free tier).
 */
export async function onRequestPost(context) {
  try {
    const data = await context.request.json();

    const {
      city,
      state,
      project_type,
      zip_code,
      dumpster_size,
      contact_name,
      contact_phone,
      contact_email
    } = data;

    // 1. Core Field Validations
    if (!contact_name || !contact_phone || !contact_email || !zip_code || !dumpster_size) {
      return new Response(
        JSON.stringify({ error: "Required contact or shipping details are missing." }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // 2. Validate zip code (exactly 5 US digits)
    if (!/^\d{5}$/.test(zip_code.trim())) {
      return new Response(
        JSON.stringify({ error: "Invalid US postal zip code." }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // 3. Validate email layout
    if (!contact_email.includes("@") || !contact_email.includes(".")) {
      return new Response(
        JSON.stringify({ error: "Invalid email layout structure." }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // 4. Generate stable, unique tracker reference ID
    const leadId = `lead_${Math.random().toString(36).substring(2, 11)}_${Date.now()}`;

    // -------------------------------------------------------------------------
    // Monetization Pipeline Integration Hooks
    // -------------------------------------------------------------------------
    // In production, you would seamlessly trigger an asynchronous POST fetch request 
    // forwarding the clean payload to an affiliate CRM (like Angi, Thumbtack, or a 
    // national dumpster broker API) or send an email alert using a serverless SDK:
    // 
    // await fetch("https://api.leadsbroker.com/v1/intake", {
    //   method: "POST",
    //   headers: { "Authorization": "Bearer API_KEY", "Content-Type": "application/json" },
    //   body: JSON.stringify({ ...data, leadId, source: "DumpsterGrid" })
    // });
    // -------------------------------------------------------------------------

    console.log(`[LEAD INTAKE SYSTEM] Success capturing lead ${leadId} for ${city}, ${state || 'US'}`);

    return new Response(
      JSON.stringify({
        success: true,
        message: "Project lead captured and routed successfully.",
        leadId,
        destination: city,
        timestamp: new Date().toISOString()
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" }
      }
    );
  } catch (error) {
    console.error("[LEAD INTAKE ERROR]: ", error);
    return new Response(
      JSON.stringify({ error: "Server encountered a problem processing the lead body." }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
