"""
Lark FastMCP Server

A Model Context Protocol (MCP) server for Lark API v3 integration.
Provides tools to fetch messages, documents, and tasks from Lark.

Installation:
    pip install fastmcp httpx pydantic python-dotenv

Usage:
    python3 lark-mcp-server.py

Credential priority (highest → lowest):
    1. System environment variables  ← recommended
    2. .env file in vault root       ← local fallback
    3. LARK_API_TOKEN direct override ← advanced

Environment Variables:
    LARK_APP_ID:     Lark App ID (required)
    LARK_APP_SECRET: Lark App Secret (required)
    LARK_API_BASE:   Lark API base URL (default: https://open.larksuite.com)
    LARK_API_TOKEN:  (optional) direct tenant access token — skips App ID/Secret auth

MCP Tools:
    - lark.fetch_messages:  Fetch messages from a channel
    - lark.fetch_documents: Fetch documents from a team/space
    - lark.fetch_tasks:     Fetch tasks by status
    - lark.get_user_info:   Get user info by ID
    - lark.search_messages: Search messages by keyword

Security note:
    NEVER hardcode credentials. Use system env vars or a gitignored .env file.
    See docs/lark-setup-guide.md for instructions.
"""

import os
import logging
from typing import Optional, Any
from datetime import datetime
import time
import httpx
from pydantic import BaseModel, Field

# ── Credential loading: system env vars take priority; .env is the fallback ──
try:
    from dotenv import load_dotenv
    load_dotenv()  # no-op if .env doesn't exist; system env vars are never overwritten
except ImportError:
    pass  # python-dotenv not installed — system env vars only (that's fine)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = FastMCP("lark-mcp")


class LarkConfig(BaseModel):
    """Configuration for Lark API client."""
    app_id: str = Field(default="", description="Lark App ID")
    app_secret: str = Field(default="", description="Lark App Secret")
    api_token: str = Field(default="", description="Direct tenant token (optional; auto-fetched if empty)")
    api_base: str = Field(default="https://open.larksuite.com", description="Lark API base URL")
    timeout: int = Field(default=30, description="Request timeout in seconds")


class LarkClient:
    """Lark API v3 client with automatic token refresh."""

    def __init__(self, config: LarkConfig):
        self.app_id = config.app_id
        self.app_secret = config.app_secret
        self.api_base = config.api_base
        self.timeout = config.timeout
        self._token = config.api_token
        self._token_expires_at = 0
        self.client = httpx.Client(timeout=self.timeout, http2=True)
        if not self._token:
            self._refresh_token()

    def _refresh_token(self):
        """Fetch a new tenant access token using App ID + App Secret."""
        if not self.app_id or not self.app_secret:
            raise ValueError(
                "LARK_APP_ID and LARK_APP_SECRET must be set "
                "(or provide LARK_API_TOKEN directly). "
                "See docs/lark-setup-guide.md."
            )
        url = f"{self.api_base}/open-apis/auth/v3/tenant_access_token/internal"
        resp = httpx.post(
            url,
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=self.timeout
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise ValueError(f"Lark auth error: {data.get('msg')} (code={data.get('code')})")
        self._token = data["tenant_access_token"]
        self._token_expires_at = time.time() + data.get("expire", 7200) - 60
        logger.info("Lark token refreshed, expires in ~%.0f min" % ((self._token_expires_at - time.time()) / 60))

    def _get_token(self) -> str:
        if time.time() >= self._token_expires_at:
            self._refresh_token()
        return self._token

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._get_token()}", "Content-Type": "application/json"}

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.api_base}{endpoint}"
        kwargs.setdefault("headers", self._headers())
        try:
            response = self.client.request(method, url, **kwargs)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def fetch_messages(self, container_id: str, limit: int = 20, sort_by: str = "create_time", order: str = "desc") -> dict:
        """Fetch messages from a channel/group."""
        limit = min(max(1, limit), 50)
        return self._request("GET", "/open-apis/im/v1/messages", params={
            "container_id": container_id, "page_size": limit, "sort_by": sort_by, "order": order
        })

    def fetch_documents(self, parent_token: str, limit: int = 20, types: Optional[str] = None) -> dict:
        """Fetch documents from a team/space."""
        limit = min(max(1, limit), 50)
        params = {"parent_token": parent_token, "page_size": limit, "order_by": "modified_time", "direction": "desc"}
        if types:
            params["type"] = types
        return self._request("GET", "/open-apis/drive/v1/files", params=params)

    def fetch_tasks(self, status: str = "open", limit: int = 20, assignee_id: Optional[str] = None) -> dict:
        """Fetch tasks by status and optional assignee."""
        limit = min(max(1, limit), 50)
        params = {"status": status, "page_size": limit, "order_by": "updated_at", "direction": "desc"}
        if assignee_id:
            params["assignee"] = assignee_id
        return self._request("GET", "/open-apis/task/v2/tasks", params=params)

    def get_user_info(self, user_id: str) -> dict:
        """Get user information by ID."""
        return self._request("GET", f"/open-apis/contact/v3/users/{user_id}")

    def search_messages(self, query: str, container_id: Optional[str] = None, limit: int = 20) -> dict:
        """Search messages by keyword."""
        limit = min(max(1, limit), 50)
        params = {"query": query, "page_size": limit}
        if container_id:
            params["container_id"] = container_id
        return self._request("GET", "/open-apis/im/v1/messages/search", params=params)

    def close(self):
        self.client.close()


_lark_client: Optional[LarkClient] = None


def get_lark_client() -> LarkClient:
    """Lazy-initialize the Lark client (reads env at first use)."""
    global _lark_client
    if _lark_client is None:
        config = LarkConfig(
            app_id=os.getenv("LARK_APP_ID", ""),
            app_secret=os.getenv("LARK_APP_SECRET", ""),
            api_token=os.getenv("LARK_API_TOKEN", ""),
            api_base=os.getenv("LARK_API_BASE", "https://open.larksuite.com"),
        )
        if not config.app_id and not config.api_token:
            raise ValueError(
                "Lark credentials not found.\n"
                "Option A (recommended): set LARK_APP_ID and LARK_APP_SECRET as system env vars.\n"
                "Option B: create a .env file in your vault root — see docs/lark-setup-guide.md."
            )
        _lark_client = LarkClient(config)
    return _lark_client


@server.list_tools()
async def list_tools():
    return [
        {
            "name": "lark.fetch_messages",
            "description": "Fetch recent messages from a Lark channel or conversation",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "container_id": {"type": "string", "description": "Lark channel/conversation ID (e.g. 'oc_xxxxx')"},
                    "limit": {"type": "integer", "description": "Number of messages to fetch (1-50)", "default": 20},
                    "sort_by": {"type": "string", "enum": ["create_time", "update_time"], "default": "create_time"},
                    "order": {"type": "string", "enum": ["asc", "desc"], "default": "desc"}
                },
                "required": ["container_id"]
            }
        },
        {
            "name": "lark.fetch_documents",
            "description": "Fetch documents from a Lark team or space folder",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "parent_token": {"type": "string", "description": "Parent folder/space token (e.g. 'fldxxxxxx')"},
                    "limit": {"type": "integer", "description": "Number of documents to fetch (1-50)", "default": 20},
                    "types": {"type": "string", "enum": ["doc", "sheet", "bitable", "docx", "mindnote", "file"]}
                },
                "required": ["parent_token"]
            }
        },
        {
            "name": "lark.fetch_tasks",
            "description": "Fetch tasks by status and optional assignee",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["open", "completed", "closed", "all"], "default": "open"},
                    "limit": {"type": "integer", "description": "Number of tasks to fetch (1-50)", "default": 20},
                    "assignee_id": {"type": "string", "description": "Optional Lark user ID to filter by assignee"}
                }
            }
        },
        {
            "name": "lark.get_user_info",
            "description": "Get user information by Lark user ID",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "Lark user ID (e.g. 'ou_xxxxx')"}
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "lark.search_messages",
            "description": "Search messages by keyword across Lark",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or phrase"},
                    "container_id": {"type": "string", "description": "Optional channel ID to limit scope"},
                    "limit": {"type": "integer", "description": "Number of results (1-50)", "default": 20}
                },
                "required": ["query"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Any:
    client = get_lark_client()
    try:
        if name == "lark.fetch_messages":
            result = client.fetch_messages(
                container_id=arguments["container_id"],
                limit=arguments.get("limit", 20),
                sort_by=arguments.get("sort_by", "create_time"),
                order=arguments.get("order", "desc")
            )
        elif name == "lark.fetch_documents":
            result = client.fetch_documents(
                parent_token=arguments["parent_token"],
                limit=arguments.get("limit", 20),
                types=arguments.get("types")
            )
        elif name == "lark.fetch_tasks":
            result = client.fetch_tasks(
                status=arguments.get("status", "open"),
                limit=arguments.get("limit", 20),
                assignee_id=arguments.get("assignee_id")
            )
        elif name == "lark.get_user_info":
            result = client.get_user_info(user_id=arguments["user_id"])
        elif name == "lark.search_messages":
            result = client.search_messages(
                query=arguments["query"],
                container_id=arguments.get("container_id"),
                limit=arguments.get("limit", 20)
            )
        else:
            return {"success": False, "error": f"Unknown tool: {name}"}

        return {"success": True, "data": result, "timestamp": datetime.now().isoformat()}

    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", 8000))
    host = os.getenv("MCP_HOST", "127.0.0.1")
    logger.info(f"Starting Lark MCP server on {host}:{port}")
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        if _lark_client:
            _lark_client.close()
