# Overview

`rating-docker` is a Docker service that consume customizable **K**ey **P**erformance **I**ndicator as metrics. 

#### **Requirements**
This service is designed for docker environments, if you wish to test this service, you should have docker on your machine. 


Here is the list of prerequisites to be able to start `rating-docker`.


*   Docker  
*   Docker compose 
*   'Rating Docker' project cloned to local machine



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


##### **Node exporter configuration**

Use the node-exporter.yaml file if you want to add collectors not enabled by default in node-exporter.


exhaustive list of collectors : https://github.com/prometheus/node_exporter



```yaml
collectors:
  - collector name:
  
```


# **Accessing Rating Docker**


To start rating docker you need to start the docker-compose.yml file using this command : 

* **docker-compose up -d**

this command will start the following containers : 


* Prometheus
* Node exporter
* Grafana
* Timescaledb : is a PostgreSQL extension designed for improved handling of time-series data.


##### **1. Accessing Prometheus service**

This service exposes rating rules to prometheus, then saves the prometheus results in postgres.


* ./prometheus_metric.py /path/to/rating/rule(s)


##### **2. Accessing Grafana service**

This service uses grafana to display prometheus results stored in the postgres database.

* ./grafana_metric.py /path/to/rating/rule(s)


##### **3. Accessing rating results**


* ./raing_results_to_json.py metric_name


##### **(Deprecated) Accessing Rating_docker_api**
* python3 rating_docker_api.py
*  prometheus service : http://localhost:5000/prometheus
*  grafana service : http://localhost:5000/grafana



# **Uninstallation**
