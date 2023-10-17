# Overview

`rating-docker` is a Docker service that consume customizable **K**ey **P**erformance **I**ndicator as metrics and provide interfaces to exploit them. 


## **Installation**

This service is designed for docker environments, if you wish to test this service, you should have docker on your machine. 

You will find below the links to the official documentation in order to install docker on your machine.


Here is the list of prerequisites to be able to start `rating-docker`.
### **Requirements**


*   Docker
*   Docker compose
*   'Rating Docker' project cloned to local machine


##### **1. Docker installation**

*   Docker installation on Linux : https://docs.docker.com/desktop/install/linux-install/
*   Docker installation on Windows : https://docs.docker.com/desktop/install/windows-install/
*   Docker installation on Mac : https://docs.docker.com/desktop/install/mac-install/


##### **2. Docker Compose installation**

* Official documentation for Docker Compose installation : https://docs.docker.com/compose/install/


##### **(Optional) PostgreSQL Client installation : pgadmin 4**

* You can download and install pgAdmin 4 by following the official instructions: https://www.pgadmin.org/download.

Choose the appropriate version for your operating system and follow the installation steps.

##### **Prometheus configuration**

**Important**: create a file prometheus.yaml on /etc/promotheus and copy the contents of the code below into this file. 

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node-exporter'
	static_configs:
  	- targets: ['node-exporter:9100']  # Use the service name defined in your docker-compose.yml

  - job_name: 'prometheus'
	static_configs:
  	- targets: ['localhost:9090']

storage:
  tsdb:
	retention: 30d
```


### **Accessing Rating Docker**


Rating Docker is a docker compose service, to start rating docker you need to start the docker-compose.yml file using this command : 

docker-compose up -d

this command will start the following containers : 


* Prometheus
* Node exporter
* Grafana
* Postgres 


##### **1. Accessing Prometheus service**

This service exposes rating rules to prometheus, then saves the prometheus results in postgres.


* ./prometheus_metric.py /path/to/rating/rule(s)


##### **2. Accessing Grafana service**

This service uses grafana to display prometheus results stored in the postgres database.

* ./grafana_metric.py /path/to/rating/rule(s)

##### **(Deprecated) Accessing Rating_docker_api**
* python3 rating_docker_api.py
*  prometheus service : http://localhost:5000/prometheus
*  grafana service : http://localhost:5000/grafana



# **Uninstallation**
