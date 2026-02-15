"""Helper to hold the MCP instance and any related utilities."""

from mcp.server.fastmcp import FastMCP
from mcp.types import Icon, ToolAnnotations

from typing import Any, TypeVar, Callable

_CallableT = TypeVar("_CallableT", bound=Callable[..., Any])


class mcpWrapper(object):
    mcp: FastMCP | None = None
    funcs: list[dict[str, Any]] = []

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        for func in self.funcs:
            if not func["added"]:  # is added
                mcp.add_tool(func["fn"], **func["params"])
                func["added"] = True  # mark as added

    @staticmethod
    def tool(
        name: str | None = None,
        title: str | None = None,
        description: str | None = None,
        annotations: ToolAnnotations | None = None,
        icons: list[Icon] | None = None,
        meta: dict[str, Any] | None = None,
        structured_output: bool | None = None,
    ) -> Callable[[_CallableT], _CallableT]:

        # Check if user passed function directly instead of calling decorator
        if callable(name):
            raise TypeError(
                "The @tool decorator was used incorrectly. Did you forget to call it? Use @tool() instead of @tool"
            )

        def decorator(fn: _CallableT) -> _CallableT:
            mcpWrapper.funcs.append(
                {
                    "fn": fn,
                    "params": {
                        "name": name,
                        "title": title,
                        "description": description,
                        "annotations": annotations,
                        "icons": icons,
                        "meta": meta,
                        "structured_output": structured_output,
                    },
                    "added": False,
                }
            )
            return fn

        return decorator
