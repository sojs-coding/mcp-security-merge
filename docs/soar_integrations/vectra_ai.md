# Vectra SOAR Integration

## Overview

This document outlines the tools available for the Vectra integration within the SOAR platform. These tools allow interaction with the Vectra API for managing endpoints, detections, tags, notes, and triage rules.

## Tools

### `vectra_enrich_endpoint`

Fetch endpoint's system information by its hostname or IP address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `vectra_update_note`

Update note for the endpoint or detection.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `item_type` (List[Any], required): Select on which item type you want to update a note.
*   `item_id` (str, required): Specify ID of the detection/endpoint.
*   `note` (str, required): Specify what note you want to have on the detection/endpoint.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `vectra_ping`

Test connectivity to Vectra with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `vectra_remove_tags`

Remove tags from the endpoint or detection in Vectra.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `item_type` (List[Any], required): Select from which item type you want to remove tags.
*   `item_id` (str, required): Specify ID of the detection/endpoint.
*   `tags` (str, required): Specify what tags you want to remove from detection/endpoint. Tags should be separated by comma, e.g tag1, tag2.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `vectra_get_triage_rule_details`

Get detailed information about triage rules.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `triage_rule_i_ds` (str, required): Specify a comma-separated list of triage rule IDs. Example: 28,29.
*   `create_insights` (bool, optional, default=None): If enabled, action will create a separate insight for every processed triage rule.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `vectra_update_detection_status`

Update status of the detection.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detection_id` (str, required): Specify the detection ID on which you want to update the status.
*   `status` (List[Any], required): Specify what status to set on the detection.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `vectra_add_tags`

Add tags to the endpoint or detection in Vectra.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `item_type` (List[Any], required): Select to which item type you want to add tags.
*   `item_id` (str, required): Specify ID of the detection/endpoint.
*   `tags` (str, required): Specify what tags you want to add to detection/endpoint. Tags should be separated by comma, e.g tag1, tag2.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
