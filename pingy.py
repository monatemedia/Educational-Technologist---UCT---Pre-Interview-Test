import subprocess
import platform
import sys
import socket
import time
import ssl
import http.client
from urllib.parse import urlparse
import datetime
import os

def ping_server(hostname):
    """
    Ping a server to check if it's responding via ICMP.
    Returns True if server responds, False otherwise.
    
    Adapts the ping command based on operating system.
    """
    # Determine ping parameters based on the OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    timeout_value = '2000' if platform.system().lower() == 'windows' else '2'
    
    # Construct the ping command
    command = ['ping', param, '1', timeout_param, timeout_value, hostname]
    
    try:
        # Run the ping command and check the result
        result = subprocess.run(command, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True,
                               check=False)  # Don't raise exception on non-zero return
        
        # Return True if the server responded (exit code 0)
        return result.returncode == 0
    except Exception as e:
        # Print error if ping fails and return False
        print(f"Error pinging {hostname}: {e}")
        return False

def http_check(url):
    """
    Check if a website is responding via HTTP/HTTPS using standard library.
    Returns True if website responds with 200-399 status code, False otherwise.
    """
    # Parse the URL to extract hostname and path
    parsed_url = urlparse(url)
    
    # If no scheme (http or https) is provided, default to https
    if not parsed_url.scheme:
        url = 'https://' + url
        parsed_url = urlparse(url)
    
    hostname = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"
    
    # Try HTTPS first
    if parsed_url.scheme == '' or parsed_url.scheme == 'https':
        try:
            # Create an unverified SSL context for secure connections
            context = ssl._create_unverified_context()
            # Establish an HTTPS connection and make a HEAD request
            conn = http.client.HTTPSConnection(hostname, timeout=5, context=context)
            conn.request("HEAD", path, headers={"User-Agent": "Mozilla/5.0"})
            response = conn.getresponse()
            
            # Handle redirects (300-399 status codes)
            if 300 <= response.status < 400:
                location = response.getheader('Location')
                if location:
                    print(f"\n  Following redirect to {location}...", end=" ", flush=True)
                    return http_check(location)
            
            # Return True if the status code indicates success (200-399)
            return 200 <= response.status < 400
        except Exception as e:
            pass  # If HTTPS fails, try HTTP
    
    # Try HTTP if HTTPS failed
    if parsed_url.scheme == '' or parsed_url.scheme == 'http' or parsed_url.scheme == 'https':
        try:
            # Establish an HTTP connection and make a HEAD request
            conn = http.client.HTTPConnection(hostname, timeout=5)
            conn.request("HEAD", path, headers={"User-Agent": "Mozilla/5.0"})
            response = conn.getresponse()
            
            # Handle redirects (300-399 status codes)
            if 300 <= response.status < 400:
                location = response.getheader('Location')
                if location:
                    print(f"\n  Following redirect to {location}...", end=" ", flush=True)
                    return http_check(location)
            
            # Return True if the status code indicates success (200-399)
            return 200 <= response.status < 400
        except Exception as e:
            # Return False if HTTP connection fails
            return False
    
    return False # If neither HTTP nor HTTPS worked, return False

def dns_check(hostname):
    """
    Check if a hostname can be resolved through DNS.
    Returns True if hostname can be resolved, False otherwise.
    """
    try:
        # Try to resolve the hostname to an IP address
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False # Return False if DNS resolution fails
    except Exception as e:
        # Print error if DNS resolution fails
        print(f"  DNS error: {e}")
        return False

def check_connectivity(server):
    """
    Comprehensive connectivity check using multiple methods.
    Returns a dictionary with results for DNS, HTTP, and Ping checks.
    """
    results = {}
    
    # Parse the URL to extract the hostname
    original_input = server
    url_parsed = urlparse(server)
    
    hostname = url_parsed.netloc
    
    # If no hostname is found, attempt to extract it from the URL
    if not hostname:
        if "://" in server:
            parts = server.split("://", 1)
            hostname = parts[1].split("/", 1)[0]
        else:
            hostname = server
    
    # If no scheme (http/https) is found, default to HTTPS
    if url_parsed.scheme:
        url_for_check = server
    else:
        url_for_check = f"https://{server}"
    
    # Perform DNS lookup
    print(f"DNS lookup for {hostname}... ", end='', flush=True)
    dns_result = dns_check(hostname)
    print("OK" if dns_result else "FAILED")
    results['dns'] = dns_result
    
    time.sleep(0.2) # Short delay before the next check
    
    # Perform HTTP check
    print(f"HTTP check for {url_for_check}... ", end='', flush=True)
    http_result = http_check(url_for_check)
    print("OK" if http_result else "FAILED")
    results['http'] = http_result
    
    time.sleep(0.2) # Short delay before the next check
    
    # Perform Ping check
    print(f"Ping check for {hostname}... ", end='', flush=True)
    ping_result = ping_server(hostname)
    print("OK" if ping_result else "FAILED")
    results['ping'] = ping_result
    
    
    # Overall result is True if both DNS and HTTP are successful
    overall = results['dns'] and results['http']
    
    return {
        'server': original_input,
        'hostname': hostname,
        'results': results,
        'overall': overall
    }

def read_server_list(file_path):
    """
    Read server list from file, ignoring blank lines and comments.
    Comments are lines that start with #.
    """
    servers = []
    
    try:
        # Open the file and read each line
        with open(file_path, 'r') as f:
            for line in f:
                clean_line = line.strip() # Remove leading/trailing whitespace
                # Ignore blank lines and comments
                if clean_line and not clean_line.startswith('#'):
                    servers.append(clean_line)
                    
        return servers
    except FileNotFoundError:
        # Print error if file not found and exit
        print(f"Error: Could not find server list file '{file_path}'")
        sys.exit(1)

def main():
    """
    Main function to execute the script.
    """
    server_list_file = "servers.txt" # Default server list file
    error_log_file = "error.log" # Default error log file
    
    # Check if any command line arguments were passed
    if len(sys.argv) > 1:
        # If first argument is a file path, read from that file
        if sys.argv[1].endswith('.txt'):
            server_list_file = sys.argv[1]
            servers = read_server_list(server_list_file)
        else:
            # Otherwise, treat them as server addresses
            servers = sys.argv[1:]
    else:
        # Default to reading from "servers.txt" if no arguments are passed
        servers = read_server_list(server_list_file)
        
        
        # Exit if no servers were found
        if not servers:
            print(f"No valid servers found in {server_list_file}.")
            print("Please add server addresses to the file or provide them as command-line arguments.")
            sys.exit(1)
    
    try:
        # List to store servers that couldn't be reached
        error_results = []
        
        # Print initial information
        print(f"Checking connectivity for {len(servers)} servers...")
        print(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        servers_checked = 0 # Counter for checked servers
        servers_unreachable = 0 # Counter for unreachable servers
        
        # Check each server's connectivity
        for server in servers:
            servers_checked += 1
            print(f"\nChecking {server}:")
            
            result = check_connectivity(server)
            
            # If the server is unreachable, log it
            if not result['results']['http']:
                servers_unreachable += 1
                error_results.append(f"{server}")
            
            # Print status of the server (reachable or unreachable)
            print(f"  Status: {'Reachable' if result['overall'] else 'Unreachable'}")
        
        # Print summary of results
        print(f"\nChecked {servers_checked} servers, {servers_unreachable} unreachable.")
        
        # Write the error results to the log file
        with open(error_log_file, 'w') as f:
            if error_results:
                for error in error_results:
                    f.write(f"{error}\n")
            else:
                print(F"All servers responded successfully.\n")
                print(F"Nothing was written to the `error.log` file.\n")
    
    except Exception as e:
        # Handle any exceptions that occur during execution
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
