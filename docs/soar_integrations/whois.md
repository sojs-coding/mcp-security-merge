# Whois Integration

The Whois integration for Chronicle SOAR allows querying public Whois databases to retrieve registration information for domain names and potentially IP addresses.

## Overview

Whois is a query and response protocol widely used for querying databases that store the registered users or assignees of an Internet resource, such as a domain name, an IP address block, or an autonomous system number. This integration provides a way to access this public information directly within SOAR workflows.

This integration typically enables Chronicle SOAR to:

*   **Query Domain Information:** Retrieve registration details for a domain name, including registrar, registrant contact information (often redacted for privacy), registration/expiration dates, and name servers.
*   **Query IP Information:** Retrieve allocation details for an IP address, including the owning organization (RIR/ISP), network range, and potentially abuse contact information.

## Key Actions

*(Since the specific Python file is unavailable, the exact actions and parameters cannot be listed. Common actions would include:*
*   *`Lookup Domain`*
*   *`Lookup IP Address`*
*   *`Ping (Test Connectivity - may just verify the underlying library/tool is available)`)*

## Use Cases

*   **Domain Enrichment:** Enrich domain name entities within SOAR cases with registration details to understand ownership, age, and registrar information.
*   **Phishing Investigation:** Check the Whois record of a suspicious domain to identify recently registered domains or unusual registrant information.
*   **IP Address Context:** Look up the owner of an IP address involved in an incident to identify the ISP or hosting provider.
*   **Infrastructure Mapping:** Gather information about related domains or infrastructure based on registrant details (though privacy redaction often limits this).

## Configuration

*(Details on configuring the integration, such as specifying preferred Whois servers, handling rate limits, or any specific SOAR platform settings, should be added here. Basic Whois lookups often don't require API keys but might rely on system tools or specific Python libraries.)*
