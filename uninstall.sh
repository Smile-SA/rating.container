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

echo "uninstallation completed"
