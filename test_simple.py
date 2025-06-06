#!/usr/bin/env python3
import json

# MCP messages to test the server
messages = [
    # 1. Initialize
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    },
    
    # 2. Initialized notification
    {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    },
    
    # 3. List tools
    {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    },
    
    # 4. Call GetAlerts tool
    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "GetAlerts",
            "arguments": {
                "state": "CA"
            }
        }
    }
]

print("Copy and paste these JSON messages one by one into your running MCP server:")
print("=" * 70)

for i, message in enumerate(messages, 1):
    print(f"\nMessage {i}:")
    print(json.dumps(message))
    print("-" * 50)

print("\nTo test manually:")
print("1. Start your server: cd MCPServer && dotnet run")
print("2. Copy each JSON message above")
print("3. Paste it into the server terminal and press Enter")
print("4. Observe the server's JSON response")