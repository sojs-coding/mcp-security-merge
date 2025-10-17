"""
API scope definitions and utilities for Falcon MCP Server

This module provides API scope definitions and related utilities for the Falcon MCP server.
"""

from typing import List, Optional

from .logging import get_logger

logger = get_logger(__name__)

# Map of API operations to required scopes
# This can be expanded as more modules and operations are added
API_SCOPE_REQUIREMENTS = {
    # Alerts operations (migrated from detections)
    "GetQueriesAlertsV2": ["Alerts:read"],
    "PostEntitiesAlertsV2": ["Alerts:read"],
    # Hosts operations
    "QueryDevicesByFilter": ["Hosts:read"],
    "PostDeviceDetailsV2": ["Hosts:read"],
    # Incidents operations
    "QueryIncidents": ["Incidents:read"],
    "GetIncidentDetails": ["Incidents:read"],
    "CrowdScore": ["Incidents:read"],
    "GetIncidents": ["Incidents:read"],
    "GetBehaviors": ["Incidents:read"],
    "QueryBehaviors": ["Incidents:read"],
    # Intel operations
    "QueryIntelActorEntities": ["Actors (Falcon Intelligence):read"],
    "QueryIntelIndicatorEntities": ["Indicators (Falcon Intelligence):read"],
    "QueryIntelReportEntities": ["Reports (Falcon Intelligence):read"],
    # Spotlight operations
    "combinedQueryVulnerabilities": ["Vulnerabilities:read"],
    # Discover operations
    "combined_applications": ["Assets:read"],
    "combined_hosts": ["Assets:read"],
    # Cloud operations
    "ReadContainerCombined": ["Falcon Container Image:read"],
    "ReadContainerCount": ["Falcon Container Image:read"],
    "ReadCombinedVulnerabilities": ["Falcon Container Image:read"],
    # Identity Protection operations
    "api_preempt_proxy_post_graphql": [
        "Identity Protection Entities:read",
        "Identity Protection Timeline:read",
        "Identity Protection Detections:read",
        "Identity Protection Assessment:read",
        "Identity Protection GraphQL:write",
    ],
    # Sensor Usage operations
    "GetSensorUsageWeekly": ["Sensor Usage:read"],
    # Serverless operations
    "GetCombinedVulnerabilitiesSARIF": ["Falcon Container Image:read"],
    # Add more mappings as needed
}


def get_required_scopes(operation: Optional[str]) -> List[str]:
    """Get the required API scopes for a specific operation.

    Args:
        operation: The API operation name

    Returns:
        List[str]: List of required API scopes
    """
    return API_SCOPE_REQUIREMENTS.get(operation, [])
