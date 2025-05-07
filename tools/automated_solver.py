# Cool hacker-style banner
def print_banner():
    banner = r'''
                                                                              
  ███    ███ ██ ███    ██     ██████   █████  ████████ ██   ██               
  ████  ████ ██ ████   ██     ██   ██ ██   ██    ██    ██   ██               
  ██ ████ ██ ██ ██ ██  ██     ██████  ███████    ██    ███████               
  ██  ██  ██ ██ ██  ██ ██     ██      ██   ██    ██    ██   ██               
  ██      ██ ██ ██   ████     ██      ██   ██    ██    ██   ██               
                                                                              
  ███████  ██████  ██      ██    ██ ███████ ██████                           
  ██      ██    ██ ██      ██    ██ ██      ██   ██                          
  ███████ ██    ██ ██      ██    ██ █████   ██████                           
       ██ ██    ██ ██       ██  ██  ██      ██   ██                          
  ███████  ██████  ███████   ████   ███████ ██   ██        
'''
# A RichMix & Claude Vibe Code Collaboration to solve "Dynamic Paths" By Hack The Box

# ANSI color codes
    colors = [
        '\033[1;31m',  # Red
        '\033[1;32m',  # Green
        '\033[1;33m',  # Yellow
        '\033[1;34m',  # Blue
        '\033[1;35m',  # Magenta
        '\033[1;36m'   # Cyan
    ]
    
    reset = '\033[0m'
    color = random.choice(colors)
    
    print(f"{color}{banner}{reset}")
    print(f"{color}[*] Dynamic Programming CTF Solver - Minimum Path Sum Challenge{reset}")
    print(f"{color}[*] Target: 94.237.63.150:30878{reset}")
    print(f"{color}[*] Status: Initializing Attack Vector...{reset}")
    print(f"{color}{'=' * 80}{reset}")

#!/usr/bin/env python3
import socket
import sys
import re
import time

def parse_grid(rows, cols, grid_values):
    """Parse the flat list of values into a 2D grid."""
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(grid_values[i * cols + j])
        grid.append(row)
    return grid

def min_path_sum(grid, rows, cols):
    """
    Find the minimum path sum from top-left to bottom-right.
    Can only move right or down.
    """
    # Create a DP table to store the minimum path sum to each cell
    dp = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Initialize the starting point
    dp[0][0] = grid[0][0]
    
    # Fill the first row (can only come from the left)
    for j in range(1, cols):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    
    # Fill the first column (can only come from above)
    for i in range(1, rows):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    
    # Fill the rest of the dp table
    for i in range(1, rows):
        for j in range(1, cols):
            # For each cell, the minimum path is the minimum of coming from above or from the left
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    
    # Return the bottom-right value, which is our answer
    return dp[rows-1][cols-1]

def solve_test_case(rows, cols, grid_values):
    """Solve a test case."""
    grid = parse_grid(rows, cols, grid_values)
    return min_path_sum(grid, rows, cols)

def solve_with_netcat(host="[target_IP]", port=[port_number]):
    """Connect to the server and solve all test cases automatically."""
    try:
        # Create a socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        # Buffer to store received data
        buffer = ""
        
        # Process all 100 test cases
        for test_num in range(1, 101):
            # Wait for the test prompt
            waiting_for_test = True
            while waiting_for_test:
                # Receive data from socket
                data = sock.recv(4096).decode('utf-8')
                if not data:
                    print("Connection closed by server.")
                    return
                
                buffer += data
                print(data, end='')  # Show what we're receiving
                
                # Check if we've received a test prompt
                test_pattern = rf"Test {test_num}/100\s+(\d+)\s+(\d+)\s+([\d\s]+)\s*>"
                match = re.search(test_pattern, buffer)
                if match:
                    waiting_for_test = False
                    rows = int(match.group(1))
                    cols = int(match.group(2))
                    grid_str = match.group(3).strip()
                    grid_values = list(map(int, grid_str.split()))
                    
                    # Solve the test case
                    result = solve_test_case(rows, cols, grid_values)
                    print(f"\nTest {test_num} solution: {result}")
                    
                    # Send the answer
                    sock.sendall(f"{result}\n".encode('utf-8'))
                    
                    # Reset buffer after handling a test
                    buffer = ""
                    
                    # Short delay to avoid overwhelming the server
                    time.sleep(0.1)
        
        # After all tests, receive and print the final result
        final_data = sock.recv(4096).decode('utf-8')
        print(final_data)
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        sock.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Custom host and port
        host = sys.argv[1]
        port = int(sys.argv[2])
        solve_with_netcat(host, port)
    else:
        # Default host and port
        solve_with_netcat()
