#!/usr/bin/env python3
import json
import subprocess
import sys
import time
import threading
import os

def test_mcp_server():
    """Test the MCP server using the built executable."""
    
    # Look for the built executable
    executable_paths = [
        "MCPServer/bin/Debug/net9.0/MCPServer.exe",
        "MCPServer/bin/Debug/net9.0/MCPServer",
        "MCPServer/bin/Release/net9.0/MCPServer.exe",
        "MCPServer/bin/Release/net9.0/MCPServer"
    ]
    
    executable = None
    for path in executable_paths:
        if os.path.exists(path):
            executable = path
            break
    
    if not executable:
        print("No built executable found. Let's build it first...")
        # Try to build the project
        try:
            build_result = subprocess.run(['dotnet', 'build', 'MCPServer'], 
                                        capture_output=True, text=True, timeout=30)
            if build_result.returncode == 0:
                print("Build successful!")
                # Look for executable again
                for path in executable_paths:
                    if os.path.exists(path):
                        executable = path
                        break
            else:
                print(f"Build failed: {build_result.stderr}")
                return
        except Exception as e:
            print(f"Could not build: {e}")
            return
    
    if not executable:
        print("Still no executable found after build")
        return
    
    print(f"Found executable: {executable}")
    print("Starting MCP server...")
    
    # Start the server
    server_process = subprocess.Popen(
        [f'./{executable}'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    def read_responses():
        """Read and print server responses"""
        while True:
            try:
                line = server_process.stdout.readline()
                if not line:
                    break
                if line.strip():
                    print(f"🔵 SERVER: {line.strip()}")
            except:
                break
    
    def read_errors():
        """Read and print server errors"""
        while True:
            try:
                line = server_process.stderr.readline()
                if not line:
                    break
                if line.strip():
                    print(f"🔴 ERROR: {line.strip()}")
            except:
                break
    
    # Start reader threads
    stdout_thread = threading.Thread(target=read_responses)
    stdout_thread.daemon = True
    stdout_thread.start()
    
    stderr_thread = threading.Thread(target=read_errors)
    stderr_thread.daemon = True
    stderr_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
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
            print(f"\n🟢 SENDING {i}: {json.dumps(message)}")
            server_process.stdin.write(json.dumps(message) + '\n')
            server_process.stdin.flush()
            time.sleep(3)  # Wait for response
            
        # Wait a bit more for final responses
        time.sleep(2)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\n🛑 Terminating server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except:
            server_process.kill()

if __name__ == "__main__":
    test_mcp_server()