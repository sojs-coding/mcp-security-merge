# PhishTank Integration

The PhishTank integration for Chronicle SOAR allows querying the PhishTank database, a collaborative clearinghouse for data and information about phishing on the internet. This enables checking the reputation of URLs identified during security investigations.

## Overview

PhishTank is a free community site where anyone can submit, verify, track, and share phishing data. It provides a database of known phishing URLs, verified by the community.

This integration typically allows Chronicle SOAR to:

*   **Check URL Reputation:** Query PhishTank to determine if a specific URL is listed in their database of verified phishing sites.

*Note: While PhishTank allows users to submit suspected phishing URLs through their website, API-based submission might require specific registration or have limitations. The primary use case for SOAR integration is typically checking existing URLs.*

## Key Actions

The main action expected from this integration is:

*   **Check URL:** Submit a URL to PhishTank to check if it's known to be malicious (verified phishing). The response usually indicates if the URL is known/verified, unknown, or potentially invalid.
*   **Ping (Test Connectivity):** Verify the connection to the PhishTank API endpoint and check API key validity if required.

## Use Cases

*   **Phishing Email Triage:** Automatically check URLs from suspected phishing emails against PhishTank during initial analysis within a SOAR playbook.
*   **URL Enrichment:** Add PhishTank reputation data (known phish/unknown) to URL entities within SOAR cases.
*   **Indicator Validation:** Use PhishTank as one source among others to assess the maliciousness of a URL found in logs or alerts.

## Configuration

*(Details on configuring the integration, including obtaining a PhishTank API key (if required/available for the specific API usage), specifying the PhishTank API URL, potential rate limits, and SOAR platform settings, should be added here.)*
