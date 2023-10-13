# **Installation**

### **Requirements**


*   Docker
*   Docker compose
*   'Rating Docker' project cloned to local machine


##### **1. Docker installation**

*   Docker installation on Linux : le lien
*   Docker installation on windows : le lien
*   Docker installation on Mac : le lien


##### **2. Docker Compose installation**

* Docker Compose installation on Linux : le lien
* Docker Compose installation on windows : le lien
* Docker Compose installation on Mac : le lien


##### **(Optional) PostgreSQL Client installation : pgadmin 4**

* You can download and install pgAdmin 4 by following the official instructions: https://www.pgadmin.org/download.

Choose the appropriate version for your operating system and follow the installation steps.

###### **3. Prometheus configuration**


**Disclaimer**: create a file /etc/promotheus/prometheus.yaml and copy the contents of the code below into this file.
 

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


postgresql_sd_configs:  # to read from postgres bind mount
  - host: /var/lib/postgresql/data

storage:
  tsdb:
	retention: 30d
```

### **Accessing Rating Docker**
Run the following command to start the containers defined in your Docker Compose configuration :
* sudo docker-compose up -d
##### **1. Accessing Prometheus Metric**
* ./prometheus_metric.py rating_rules.yaml
##### **2. Accessing Grafana Metric**
* ./grafana_metric.py rating_rules.yaml

##### **3. Accessing Rating_docker_api**
* python3 rating_docker_api.py
*  prometheus service : http://localhost:5000/prometheus
*  grafana service : http://localhost:5000/grafana



# **Uninstallation**
