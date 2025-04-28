# Proofpoint PS Integration

The Proofpoint Protection Server (PPS) integration for Chronicle SOAR allows interaction with the Proofpoint email security gateway. This enables security teams to manage email threats, investigate messages, and update policies directly from the SOAR platform.

## Overview

Proofpoint Protection Server is a core component of Proofpoint's email security suite, providing protection against malware, phishing, spam, and other email-borne threats. It inspects incoming and outgoing emails, enforces policies, and often includes features like quarantine management and URL defense.

This integration typically allows Chronicle SOAR to:

*   **Manage Quarantined Messages:** Search for, release, or delete messages held in the Proofpoint quarantine.
*   **Manage Sender/Recipient Lists:** Add or remove senders/recipients from blocklists (blocked senders) or safelists (allowed senders).
*   **Retrieve Message Details:** Get information about specific emails processed by Proofpoint, such as delivery status, headers, and threat classification.
*   **Manage Users/Policies:** Potentially manage user accounts or specific policy settings within Proofpoint (depending on API capabilities).

## Key Actions

Common actions available through a Proofpoint PS integration might include:

*   **Find Quarantined Messages:** Search the quarantine based on sender, recipient, subject, or message ID.
*   **Release Quarantined Message:** Release a specific message from quarantine to the intended recipient.
*   **Delete Quarantined Message:** Permanently delete a message from quarantine.
*   **Add Sender to Blocklist:** Block future emails from a specific sender address or domain.
*   **Remove Sender from Blocklist:** Unblock a previously blocked sender.
*   **Add Sender to Safelist:** Ensure emails from a specific sender are allowed.
*   **Remove Sender from Safelist:** Remove a sender from the allowed list.
*   **Get Message Trace/Logs:** Retrieve tracking information or logs for specific emails.
*   **Ping (Test Connectivity):** Verify the connection and authentication to the Proofpoint Protection Server API.

## Use Cases

*   **Phishing Response:** When a user reports a phishing email (potentially via another integration like PhishRod or a direct submission), use the Proofpoint PS integration to search for and delete similar messages from quarantine or user inboxes (if supported). Block the sender.
*   **False Positive Management:** If an analyst determines a quarantined email is legitimate, release it from quarantine using the SOAR interface and potentially add the sender to a safelist.
*   **Threat Hunting:** Query Proofpoint message logs for emails matching specific indicators (e.g., sender IP, subject line keywords) identified during an investigation.
*   **Automated Blocking:** Automatically add malicious senders identified through threat intelligence feeds or other alerts to the Proofpoint blocklist.

## Configuration

*(Details on configuring the integration, including the Proofpoint Protection Server hostname/IP address, API credentials (often requiring specific user roles/permissions within Proofpoint), port numbers, and SOAR platform settings, should be added here.)*
