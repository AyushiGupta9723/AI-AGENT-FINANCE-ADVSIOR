from mcp.client import Client
from langchain_core.tools import Tool

class MCPToolAdapter:
    def __init__(self, server_url: str):
        self.client = Client(server_url)

    def get_langchain_tools(self):
        tools = []
        for tool in self.client.list_tools():
            tools.append(
                Tool(
                    name=tool.name,
                    description=tool.description,
                    func=self._make_tool_fn(tool.name),
                )
            )
        return tools

    def _make_tool_fn(self, tool_name: str):
        def _fn(**kwargs):
            return self.client.call_tool(tool_name, kwargs)
        return _fn
