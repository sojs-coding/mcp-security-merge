"""
Intel module for Falcon MCP Server

This module provides tools for accessing and analyzing CrowdStrike Falcon intelligence data.
"""

from typing import Any, Dict, List

from mcp.server import FastMCP
from mcp.server.fastmcp.resources import TextResource
from pydantic import AnyUrl, Field

from falcon_mcp.common.errors import handle_api_response
from falcon_mcp.common.logging import get_logger
from falcon_mcp.common.utils import prepare_api_parameters
from falcon_mcp.modules.base import BaseModule
from falcon_mcp.resources.intel import (
    QUERY_ACTOR_ENTITIES_FQL_DOCUMENTATION,
    QUERY_INDICATOR_ENTITIES_FQL_DOCUMENTATION,
    QUERY_REPORT_ENTITIES_FQL_DOCUMENTATION,
)

logger = get_logger(__name__)


class IntelModule(BaseModule):
    """Module for accessing and analyzing CrowdStrike Falcon intelligence data."""

    def register_tools(self, server: FastMCP) -> None:
        """Register tools with the MCP server.

        Args:
            server: MCP server instance
        """
        # Register tools
        self._add_tool(
            server=server,
            method=self.query_actor_entities,
            name="search_actors",
        )

        self._add_tool(
            server=server,
            method=self.query_indicator_entities,
            name="search_indicators",
        )

        self._add_tool(
            server=server,
            method=self.query_report_entities,
            name="search_reports",
        )

    def register_resources(self, server: FastMCP) -> None:
        """Register resources with the MCP server.

        Args:
            server: MCP server instance
        """
        search_actors_fql_resource = TextResource(
            uri=AnyUrl("falcon://intel/actors/fql-guide"),
            name="falcon_search_actors_fql_guide",
            description="Contains the guide for the `filter` param of the `falcon_search_actors` tool.",
            text=QUERY_ACTOR_ENTITIES_FQL_DOCUMENTATION,
        )

        search_indicators_fql_resource = TextResource(
            uri=AnyUrl("falcon://intel/indicators/fql-guide"),
            name="falcon_search_indicators_fql_guide",
            description="Contains the guide for the `filter` param of the `falcon_search_indicators` tool.",
            text=QUERY_INDICATOR_ENTITIES_FQL_DOCUMENTATION,
        )

        search_reports_fql_resource = TextResource(
            uri=AnyUrl("falcon://intel/reports/fql-guide"),
            name="falcon_search_reports_fql_guide",
            description="Contains the guide for the `filter` param of the `falcon_search_reports` tool.",
            text=QUERY_REPORT_ENTITIES_FQL_DOCUMENTATION,
        )

        self._add_resource(
            server,
            search_actors_fql_resource,
        )
        self._add_resource(
            server,
            search_indicators_fql_resource,
        )
        self._add_resource(
            server,
            search_reports_fql_resource,
        )

    def query_actor_entities(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL query expression that should be used to limit the results. IMPORTANT: use the `falcon://intel/actors/fql-guide` resource when building this filter parameter.",
        ),
        limit: int = Field(
            default=10,
            ge=1,
            le=5000,
            description="Maximum number of records to return. Max 5000",
            examples={10, 20, 100},
        ),
        offset: int | None = Field(
            default=None,
            description="Starting index of overall result set from which to return ids.",
            examples=[0, 10],
        ),
        sort: str | None = Field(
            default=None,
            description="The field and direction to sort results on. The format is {field}|{asc/desc}. Valid values include: name, target_countries, target_industries, type, created_date, last_activity_date and last_modified_date. Ex: created_date|desc",
            examples={"created_date|desc"},
        ),
        q: str | None = Field(
            default=None,
            description="Free text search across all indexed fields.",
            examples={"BEAR"},
        ),
    ) -> List[Dict[str, Any]]:
        """Research threat actors and adversary groups tracked by CrowdStrike intelligence.

        IMPORTANT: You must use the `falcon://intel/actors/fql-guide` resource when you need to use the `filter` parameter.
        This resource contains the guide on how to build the FQL `filter` parameter for the `falcon_search_actors` tool.
        """
        # Prepare parameters
        params = prepare_api_parameters(
            {
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
                "q": q,
            }
        )

        # Define the operation name
        operation = "QueryIntelActorEntities"

        logger.debug("Searching actors with params: %s", params)

        # Make the API request
        command_response = self.client.command(operation, parameters=params)

        # Handle the response
        api_response = handle_api_response(
            command_response,
            operation=operation,
            error_message="Failed to search actors",
            default_result=[],
        )

        if self._is_error(api_response):
            return [api_response]

        return api_response

    def query_indicator_entities(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL query expression that should be used to limit the results. IMPORTANT: use the `falcon://intel/indicators/fql-guide` resource when building this filter parameter.",
        ),
        limit: int = Field(
            default=10,
            ge=1,
            le=5000,
            description="Maximum number of records to return. (Max: 5000)",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting index of overall result set from which to return ids.",
        ),
        sort: str | None = Field(
            default=None,
            description="The field and direction to sort results on. The format is {field}|{asc/desc}. Valid values are: id, indicator, type, published_date, last_updated, and _marker. Ex: published_date|desc",
            examples={"published_date|desc"},
        ),
        q: str | None = Field(
            default=None,
            description="Free text search across all indexed fields.",
        ),
        include_deleted: bool = Field(
            default=False,
            description="Flag indicating if both published and deleted indicators should be returned.",
        ),
        include_relations: bool = Field(
            default=False,
            description="Flag indicating if related indicators should be returned.",
        ),
    ) -> List[Dict[str, Any]]:
        """Search for threat indicators and indicators of compromise (IOCs) from CrowdStrike intelligence.

        IMPORTANT: You must use the `falcon://intel/indicators/fql-guide` resource when you need to use the `filter` parameter.
        This resource contains the guide on how to build the FQL `filter` parameter for the `falcon_search_indicators` tool.
        """
        # Prepare parameters
        params = prepare_api_parameters(
            {
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
                "q": q,
                "include_deleted": include_deleted,
                "include_relations": include_relations,
            }
        )

        # Define the operation name
        operation = "QueryIntelIndicatorEntities"

        logger.debug("Searching indicators with params: %s", params)

        # Make the API request
        command_response = self.client.command(operation, parameters=params)

        # Handle the response
        api_response = handle_api_response(
            command_response,
            operation=operation,
            error_message="Failed to search indicators",
            default_result=[],
        )

        if self._is_error(api_response):
            return [api_response]

        return api_response

    def query_report_entities(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL query expression that should be used to limit the results. IMPORTANT: use the `falcon://intel/reports/fql-guide` resource when building this filter parameter.",
        ),
        limit: int = Field(
            default=10,
            ge=1,
            le=5000,
            description="Maximum number of records to return. (Max: 5000)",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting index of overall result set from which to return ids.",
        ),
        sort: str | None = Field(
            default=None,
            description="The field and direction to sort results on in the format of: {field}.{asc}or {field}.{desc}. Valid values include: name, target_countries, target_industries, type, created_date, last_modified_date. Ex: created_date|desc",
            examples={"created_date|desc"},
        ),
        q: str | None = Field(
            default=None,
            description="Free text search across all indexed fields.",
        ),
    ) -> List[Dict[str, Any]]:
        """Access CrowdStrike intelligence publications and threat reports.

        This tool returns comprehensive intelligence report details based on your search criteria.
        Use this when you need to find CrowdStrike intelligence publications matching specific conditions.
        For guidance on building FQL filters, use the `falcon://intel/reports/fql-guide` resource.

        IMPORTANT: You must use the `falcon://intel/reports/fql-guide` resource when you need to use the `filter` parameter.
        This resource contains the guide on how to build the FQL `filter` parameter for the `falcon_search_reports` tool.
        """
        # Prepare parameters
        params = prepare_api_parameters(
            {
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
                "q": q,
            }
        )

        # Define the operation name
        operation = "QueryIntelReportEntities"

        logger.debug("Searching reports with params: %s", params)

        # Make the API request
        command_response = self.client.command(operation, parameters=params)

        # Handle the response
        api_response = handle_api_response(
            command_response,
            operation=operation,
            error_message="Failed to search reports",
            default_result=[],
        )

        # If handle_api_response returns an error dict instead of a list,
        # it means there was an error, so we return it wrapped in a list
        if self._is_error(api_response):
            return [api_response]

        return api_response
