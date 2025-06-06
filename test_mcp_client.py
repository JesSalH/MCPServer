#!/usr/bin/env python3
import json
import subprocess
import sys
import threading
import time

def send_message(process, message):
    """Send a JSON-RPC message to the MCP server."""
    json_message = json.dumps(message) + '\n'
    print(f"Sending: {json_message.strip()}")
    process.stdin.write(json_message.encode())
    process.stdin.flush()

def read_messages(process):
    """Read messages from the MCP server."""
    while True:
        try:
            line = process.stdout.readline()
            if not line:
                break
            if line.strip():
                print(f"Received: {line.decode().strip()}")
        except Exception as e:
            print(f"Error reading: {e}")
            break

def test_mcp_server():
    """Test the MCP server by calling a weather tool."""
    print("Please start your MCP server manually in another terminal with:")
    print("cd /mnt/d/DEV/projects/agents/anthropic/MCPServer/MCPServer && dotnet run")
    print("Then press Enter here to continue...")
    input()
    
    # Connect to stdin/stdout of current process for testing
    # This is a simplified version - in reality, you'd connect to the running server
    print("Simulating MCP client communication...")
    
    # For demonstration, let's show what messages would be sent
    init_message = {
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
    }
    
    print("Would send initialize message:")
    print(json.dumps(init_message, indent=2))
    
    list_tools_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    print("\nWould send list tools message:")
    print(json.dumps(list_tools_message, indent=2))
    
    call_tool_message = {
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
    
    print("\nWould send call tool message:")
    print(json.dumps(call_tool_message, indent=2))
    
    return
    
    # Start a thread to read server responses
    reader_thread = threading.Thread(target=read_messages, args=(server_process,))
    reader_thread.daemon = True
    reader_thread.start()
    
    try:
        time.sleep(2)  # Give server time to start
        
        # 1. Initialize the MCP connection
        init_message = {
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
        }
        send_message(server_process, init_message)
        time.sleep(1)
        
        # 2. Send initialized notification
        initialized_message = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        send_message(server_process, initialized_message)
        time.sleep(1)
        
        # 3. List available tools
        list_tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        send_message(server_process, list_tools_message)
        time.sleep(2)
        
        # 4. Call the GetAlerts weather tool
        call_tool_message = {
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
        send_message(server_process, call_tool_message)
        time.sleep(3)
        
        print("Test completed. Check the output above for responses.")
        
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_mcp_server()