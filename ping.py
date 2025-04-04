#!/usr/bin/env python3
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
    # Determine the correct ping command parameters based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    
    # For Windows, -w uses milliseconds, for Unix/Linux -W uses seconds
    timeout_value = '2000' if platform.system().lower() == 'windows' else '2'
    
    # Build the command
    command = ['ping', param, '1', timeout_param, timeout_value, hostname]
    
    try:
        # Execute the ping command and capture output
        result = subprocess.run(command, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True,
                               check=False)  # Don't raise exception on non-zero return
        
        # Check if the ping was successful (return code 0)
        return result.returncode == 0
    except Exception as e:
        print(f"Error pinging {hostname}: {e}")
        return False

def http_check(url):
    """
    Check if a website is responding via HTTP/HTTPS using standard library.
    Returns True if website responds with 200-399 status code, False otherwise.
    """
    # Parse URL
    parsed_url = urlparse(url)
    
    # Add https:// prefix if not present
    if not parsed_url.scheme:
        url = 'https://' + url
        parsed_url = urlparse(url)
    
    hostname = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"
    
    # Try HTTPS first if no scheme is specified or if https:// is specified
    if parsed_url.scheme == '' or parsed_url.scheme == 'https':
        try:
            # Create an SSL context that ignores certificate validation
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(hostname, timeout=5, context=context)
            conn.request("HEAD", path, headers={"User-Agent": "Mozilla/5.0"})
            response = conn.getresponse()
            
            # Check for redirect
            if 300 <= response.status < 400:
                location = response.getheader('Location')
                if location:
                    print(f"\n  Following redirect to {location}...", end=" ", flush=True)
                    return http_check(location)
            
            # Success if 2xx or 3xx status
            return 200 <= response.status < 400
        except Exception as e:
            # If HTTPS fails, try HTTP
            pass
    
    # Try HTTP if HTTPS failed or if http:// was specified
    if parsed_url.scheme == '' or parsed_url.scheme == 'http' or parsed_url.scheme == 'https':
        try:
            conn = http.client.HTTPConnection(hostname, timeout=5)
            conn.request("HEAD", path, headers={"User-Agent": "Mozilla/5.0"})
            response = conn.getresponse()
            
            # Check for redirect
            if 300 <= response.status < 400:
                location = response.getheader('Location')
                if location:
                    print(f"\n  Following redirect to {location}...", end=" ", flush=True)
                    return http_check(location)
            
            # Success if 2xx or 3xx status
            return 200 <= response.status < 400
        except Exception as e:
            return False
    
    return False

def dns_check(hostname):
    """
    Check if a hostname can be resolved through DNS.
    Returns True if hostname can be resolved, False otherwise.
    """
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False
    except Exception as e:
        print(f"  DNS error: {e}")
        return False

def check_connectivity(server):
    """
    Comprehensive connectivity check using multiple methods.
    """
    results = {}
    
    # Parse URL if needed
    original_input = server
    url_parsed = urlparse(server)
    
    # Extract hostname
    hostname = url_parsed.netloc
    
    # If no netloc, the input might be just a hostname or the parser didn't recognize the scheme
    if not hostname:
        if "://" in server:
            # URL with scheme but not parsed correctly
            parts = server.split("://", 1)
            hostname = parts[1].split("/", 1)[0]
        else:
            # Just a hostname
            hostname = server
    
    # Form a proper URL for HTTP checks
    if url_parsed.scheme:
        url_for_check = server
    else:
        url_for_check = f"https://{server}"
    
    # Check DNS resolution
    print(f"DNS lookup for {hostname}... ", end='', flush=True)
    dns_result = dns_check(hostname)
    print("OK" if dns_result else "FAILED")
    results['dns'] = dns_result
    
    # Small delay for readability
    time.sleep(0.2)
    
    # Check HTTP/HTTPS
    print(f"HTTP check for {url_for_check}... ", end='', flush=True)
    http_result = http_check(url_for_check)
    print("OK" if http_result else "FAILED")
    results['http'] = http_result
    
    # Small delay for readability
    time.sleep(0.2)
    
    # Check ping (often blocked by firewalls)
    print(f"Ping check for {hostname}... ", end='', flush=True)
    ping_result = ping_server(hostname)
    print("OK" if ping_result else "FAILED")
    results['ping'] = ping_result
    
    # Overall status
    overall = results['dns'] and results['http']  # Consider ping optional
    
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
        with open(file_path, 'r') as f:
            for line in f:
                # Remove leading/trailing whitespace
                clean_line = line.strip()
                
                # Skip empty lines and comment lines (starting with #)
                if clean_line and not clean_line.startswith('#'):
                    servers.append(clean_line)
                    
        return servers
    except FileNotFoundError:
        print(f"Error: Could not find server list file '{file_path}'")
        sys.exit(1)

def main():
    # Define file paths
    server_list_file = "servers.txt"
    error_log_file = "error.log"
    
    # Check if servers were provided as command-line arguments
    if len(sys.argv) > 1:
        servers = sys.argv[1:]
    else:
        # Read servers from file, ignoring blank lines and comments
        servers = read_server_list(server_list_file)
        
        if not servers:
            print(f"No valid servers found in {server_list_file}.")
            print("Please add server addresses to the file or provide them as command-line arguments.")
            sys.exit(1)
    
    try:
        # Collect results for error log table
        error_results = []
        
        # Print header information
        print(f"Checking connectivity for {len(servers)} servers...")
        print(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Track statistics
        servers_checked = 0
        servers_unreachable = 0
        
        # Check each server
        for server in servers:
            servers_checked += 1
            print(f"\nChecking {server}:")
            
            result = check_connectivity(server)
            
            if not result['overall']:
                servers_unreachable += 1
                error_results.append({
                    'server': server,
                    'dns': result['results']['dns'],
                    'http': result['results']['http'],
                    'ping': result['results']['ping']
                })
            
            print(f"Overall status: {'ONLINE' if result['overall'] else 'OFFLINE'}")
            print("-" * 60)
        
        # Write error log in a nice table format
        with open(error_log_file, 'w') as error_log:
            # Write table header
            error_log.write("# Server Connectivity Check - Error Report\n")
            error_log.write(f"# Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Table headers
            error_log.write("| Server | DNS | HTTP | Ping |\n")
            error_log.write("|" + "-" * 50 + "|" + "-" * 10 + "|" + "-" * 10 + "|" + "-" * 10 + "|\n")
            
            # Table rows
            for result in error_results:
                dns_status = "OK" if result['dns'] else "**FAIL**"
                http_status = "OK" if result['http'] else "**FAIL**"
                ping_status = "OK" if result['ping'] else "**FAIL**"
                
                error_log.write(f"| {result['server']} | {dns_status} | {http_status} | {ping_status} |\n")
        
        # Print summary
        print(f"\nSummary: {servers_unreachable} of {servers_checked} servers unreachable.")
        print(f"Detailed report written to {error_log_file}")
        
        # If on Windows, open the error log with the default viewer
        if platform.system().lower() == 'windows' and error_results:
            try:
                os.startfile(error_log_file)
            except:
                pass
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()