#!/bin/bash

# Validate input
if [ -z "$1" ]; then
    echo "Usage: $0 <time in seconds>"
    exit 1
fi

TIME=$1

#docker exec -it webtraffic sh -c "timeout $TIME python3 web_traffic.py" | while IFS= read -r line; do

# Containers and ports for web traffic
#CONTAINERS=("ueransim-ue-3")
CONTAINERS=("ueransim-ue-3" "ueransim-ue-4" "ueransim-ue-5")

# Start the web traffic server
echo "Starting web traffic server..."

adjusted_time=$((TIME + 3))

    for CONTAINER in "${CONTAINERS[@]}"; do
        echo "Sending traffic to $CONTAINER: $line"
        docker exec -it "$CONTAINER" bash -c "timeout $TIME python3  /scripts/web_traffic.py" # Replace with correct endpoint and port
    done

# Wait for all processes to complete
wait

echo "All web traffic processes finished."