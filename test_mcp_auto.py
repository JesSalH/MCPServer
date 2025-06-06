#!/usr/bin/env python3
import json
import subprocess
import sys
import time
import threading

def test_mcp_server():
    """Automatically test the MCP server by sending JSON-RPC messages."""
    
    # Find dotnet executable
    try:
        dotnet_result = subprocess.run(['which', 'dotnet'], capture_output=True, text=True)
        if dotnet_result.returncode != 0:
            # Try common paths
            dotnet_paths = ['/usr/bin/dotnet', '/usr/local/bin/dotnet', '/opt/dotnet/dotnet']
            dotnet_cmd = None
            for path in dotnet_paths:
                try:
                    subprocess.run([path, '--version'], capture_output=True, check=True)
                    dotnet_cmd = path
                    break
                except:
                    continue
            if not dotnet_cmd:
                print("Error: dotnet not found. Please install .NET SDK")
                return
        else:
            dotnet_cmd = 'dotnet'
    except:
        print("Error: dotnet not found. Please install .NET SDK")
        return

    print("Starting MCP server...")
    
    # Start the server
    server_process = subprocess.Popen(
        [dotnet_cmd, 'run'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='MCPServer',
        text=True,
        bufsize=0
    )
    
    def read_responses():
        """Read and print server responses"""
        while True:
            try:
                line = server_process.stdout.readline()
                if not line:
                    break
                if line.strip():
                    print(f"SERVER RESPONSE: {line.strip()}")
            except:
                break
    
    # Start response reader thread
    reader_thread = threading.Thread(target=read_responses)
    reader_thread.daemon = True
    reader_thread.start()
    
    # Wait a moment for server to start
    time.sleep(3)
    
    # Test messages
    messages = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        },
        {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        },
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        },
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "GetAlerts",
                "arguments": {"state": "CA"}
            }
        }
    ]
    
    try:
        for i, message in enumerate(messages, 1):
            print(f"\nSending message {i}: {json.dumps(message)}")
            server_process.stdin.write(json.dumps(message) + '\n')
            server_process.stdin.flush()
            time.sleep(2)  # Wait for response
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nTerminating server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_mcp_server()