#!/bin/bash

# Start required services
echo "Starting services using docker compose..."
docker compose up -d

# Function to check if services are healthy
wait_for_service() {
  local service=$1
  echo "Waiting for $service to be healthy..."
  
  # Wait for service to be created
  local container_id=""
  while [ -z "$container_id" ]; do
    container_id=$(docker compose ps -q $service)
    [ -z "$container_id" ] && sleep 1
  done

  # Now check health status
  until [ "$(docker inspect -f '{{.State.Health.Status}}' $container_id)" == "healthy" ]; do
    local status=$(docker inspect -f '{{.State.Health.Status}}' $container_id)
    if [ "$status" == "unhealthy" ]; then
      echo -e "\n$service is UNHEALTHY!"
      echo "Check logs with: docker compose logs $service"
      exit 1
    fi
    printf '.'
    sleep 2
  done
  echo -e "\n$service is healthy!"
}

# Wait for essential services
wait_for_service neo4j
wait_for_service redis
wait_for_service qdrant

# Run tests
echo "Running tests..."
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Run pytest
export PYTHONPATH=$PYTHONPATH:.
python3 -m pytest "$@"

# Shut down services after tests
echo "Shutting down services..."
docker compose down
