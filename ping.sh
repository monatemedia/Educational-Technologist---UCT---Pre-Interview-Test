#!/bin/bash

# Script to ping servers from a list file and log unresponsive ones

SERVER_LIST="servers.txt"
ERROR_LOG="error.log"

# Check if the server list file exists
if [ ! -f "$SERVER_LIST" ]; then
    echo "Error: Server list file '$SERVER_LIST' not found."
    exit 1
fi

# Clear existing error log
> "$ERROR_LOG"

# Count total servers for statistics
TOTAL_SERVERS=$(grep -v "^$" "$SERVER_LIST" | wc -l)
UNREACHABLE=0

echo "Checking connectivity for $TOTAL_SERVERS servers..."

# Read each server from the list and ping it
while read -r server || [ -n "$server" ]; do
    # Skip empty lines
    if [ -z "$server" ]; then
        continue
    fi
    
    echo -n "Pinging $server... "
    
    # Try to ping the server once with a 2-second timeout
    if ping -c 1 -W 2 "$server" > /dev/null 2>&1; then
        echo "OK"
    else
        echo "FAILED"
        # Log the unresponsive server to the error log
        echo "$server" >> "$ERROR_LOG"
        ((UNREACHABLE++))
    fi
done < "$SERVER_LIST"

# Print summary
echo ""
echo "Summary: $UNREACHABLE of $TOTAL_SERVERS servers unreachable."
echo "Unreachable servers have been logged to $ERROR_LOG"

exit 0