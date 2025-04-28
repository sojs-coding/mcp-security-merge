# Whois RDP Integration

The Whois RDP integration for Chronicle SOAR likely utilizes the Registration Data Access Protocol (RDAP) to query registration data for Internet resources like domain names, IP addresses, and Autonomous System Numbers (ASNs). RDAP is the successor to the traditional Whois protocol, designed to provide more structured, secure, and standardized access to this information, typically via RESTful web services returning JSON responses.

## Overview

RDAP provides a standardized way to query registration data maintained by Domain Name Registries and Regional Internet Registries (RIRs). Compared to the text-based Whois protocol, RDAP offers advantages like structured JSON responses, support for internationalization, and more secure access mechanisms.

This integration typically enables Chronicle SOAR to:

*   **Query Domain Information:** Retrieve structured registration details for a domain name (registrar, dates, contacts, nameservers, status).
*   **Query IP/ASN Information:** Retrieve structured allocation/assignment details for IP addresses or ASNs (owning organization, network range, contacts).
*   **Parse Structured Data:** Leverage the JSON format of RDAP responses for easier parsing and use within SOAR playbooks compared to parsing plain text Whois.

## Key Actions

*(Since the specific Python file is unavailable, the exact actions and parameters cannot be listed. Common actions would likely mirror Whois but use RDAP:*
*   *`Lookup Domain (RDAP)`*
*   *`Lookup IP Address (RDAP)`*
*   *`Lookup ASN (RDAP)`*
*   *`Ping (Test Connectivity - may verify RDAP endpoint access or library availability)`)*

## Use Cases

Similar to the traditional Whois integration, but potentially offering more reliable data extraction due to the structured format:

*   **Domain/IP Enrichment:** Enrich entities with structured registration data from RDAP lookups.
*   **Phishing/Infrastructure Investigation:** Analyze registration details (dates, contacts, nameservers) obtained via RDAP for suspicious patterns.
*   **Automated Lookups:** Integrate RDAP queries into playbooks for automated enrichment of domains and IPs found in alerts.

## Configuration

*(Details on configuring the integration, such as specifying RDAP bootstrap servers or preferred endpoints, handling potential authentication requirements (though basic RDAP is often public), rate limiting considerations, and any specific SOAR platform settings, should be added here.)*
