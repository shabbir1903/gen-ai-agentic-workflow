from mcp_sdk import MCPServer # Simulation of standard protocol [cite: 169]

# MCP standardizes tool schemas so the LLM understands them natively [cite: 177, 194]
mcp_tools = [
    {
        "name": "fetch_user_orders",
        "description": "Retrieve order history from SQL Server",
        "input_schema": {
            "type": "object",
            "properties": {"user_id": {"type": "string"}},
            "required": ["user_id"]
        }
    }
]

# Security Guardrail: Human-in-the-loop for sensitive data [cite: 164, 195]
def authorized_mcp_call(tool_name, params):
    if tool_name == "delete_record":
        confirm = human_approval_service(tool_name) # Human-in-the-loop [cite: 164]
        if not confirm: return "Unauthorized"
    return execute_tool(tool_name, params)