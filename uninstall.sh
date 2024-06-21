#!/bin/bash

# List of container names as specified in the docker-compose file
containers=("prometheus" "node-exporter" "grafana" "timescaledb")

# Stop and remove specified containers
for container in "${containers[@]}"; do
  if [ $(docker ps -a -q -f name="$container") ]; then
    echo "Stopping container: $container"
    docker stop $container
    echo "Removing container: $container"
    docker rm $container
  else
    echo "Container $container not found"
  fi
done

# List of images as specified in the docker-compose file
images=("quay.io/prometheus/prometheus:v2.33.1" "quay.io/prometheus/node-exporter:v1.3.1" "grafana/grafana" "timescale/timescaledb-ha:pg14-latest")

# Remove specified images
for image in "${images[@]}"; do
  if [ $(docker images -q "$image") ]; then
    echo "Removing image: $image"
    docker rmi $image
  else
    echo "Image $image not found"
  fi
done

# List of volumes as specified in the docker-compose file
volumes=("ratingdocker_grafana-data" "ratingdocker_timescaledb_data")

# Remove specified volumes
for volume in "${volumes[@]}"; do
  if [ $(docker volume ls -q -f name="$volume") ]; then
    echo "Removing volume: $volume"
    docker volume rm $volume
  else
    echo "Volume $volume not found"
  fi
done

# List of networks as specified in the docker-compose file
networks=("ratingdocker_monitoring_net")

# Remove specified networks
for network in "${networks[@]}"; do
  if [ $(docker network ls -q -f name="$network") ]; then
    echo "Removing network: $network"
    docker network rm $network
  else
    echo "Network $network not found"
  fi
done

echo "uninstallation completed"
