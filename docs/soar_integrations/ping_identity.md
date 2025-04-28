# PingIdentity Integration

The Ping Identity integration for Chronicle SOAR allows interaction with the Ping Identity platform, enabling security teams to manage user identities and access as part of their incident response workflows.

## Overview

Ping Identity offers a comprehensive suite of Identity and Access Management (IAM) solutions, including Single Sign-On (SSO), Multi-Factor Authentication (MFA), directory services, and API security (often through products like PingFederate, PingOne, PingID, PingAccess).

This integration enables Chronicle SOAR to automate actions related to user accounts and sessions within the Ping Identity ecosystem, typically facilitating:

*   **User Account Management:** Disable user accounts, force password resets, or update user attributes.
*   **Session Management:** Terminate active user sessions.
*   **User/Group Information:** Retrieve details about users, group memberships, and potentially recent authentication activity.
*   **MFA Control:** Potentially trigger step-up authentication or manage MFA device status (depending on specific Ping product and API capabilities).

## Key Actions

Common actions available through a Ping Identity integration might include:

*   **Get User Details:** Retrieve information about a specific user account using their username or ID.
*   **Disable User:** Temporarily disable a user's account.
*   **Enable User:** Re-enable a previously disabled user account.
*   **Force Password Reset:** Require a user to reset their password upon their next login.
*   **Terminate User Sessions:** Invalidate all active login sessions for a user.
*   **Get Group Memberships:** List the groups a specific user belongs to.
*   **Add/Remove User from Group:** Modify a user's group memberships.
*   **Ping (Test Connectivity):** Verify the connection and authentication to the relevant Ping Identity API endpoint (e.g., PingOne API, PingFederate Admin API).

## Use Cases

*   **Compromised Account Response:** Automatically disable a user account and terminate their sessions in Ping Identity when a high-severity alert indicates account compromise.
*   **Privilege Escalation Containment:** Remove a user from sensitive groups in Ping Identity if suspicious activity is detected.
*   **Identity Verification:** Retrieve user details and group memberships from Ping Identity to enrich SOAR cases involving specific user accounts.
*   **Phishing Response:** Force a password reset for users who may have clicked on a phishing link and potentially compromised their credentials.

## Configuration

*(Details on configuring the integration, including obtaining API credentials/OAuth tokens from the relevant Ping Identity product (PingOne, PingFederate, etc.), specifying API endpoints, and configuring settings within the SOAR platform, should be added here.)*
