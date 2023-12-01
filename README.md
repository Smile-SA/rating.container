# Overview

`rating-docker` is a Docker service that consume customizable **K**ey **P**erformance **I**ndicator as metrics.

This project provides a Dockerized environment for a rating system that utilizes Prometheus, Grafana, Node Exporter, and TimescaleDB. The rating rules are managed using a Python script. 


This service is designed for docker environments, if you wish to test this service, you should have docker on your machine. 

## **Installation**

Follow these steps to get the project up and running:

Here is the list of prerequisites to be able to start `rating-docker`.


- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)


### Clone the Repository

```bash
git clone https://git.rnd.smile.fr/overboard/5gbiller/rating.docker.git

cd rating.docker
```
## Start Rating Docker 


```bash
./start-rating-docker.sh
```

This script launches the necessary services defined in the `docker-compose.yml` file, including Prometheus, Grafana, Node Exporter, and TimescaleDB. And exposes rating rules defined in the configuration file to prometheus.

- Prometheus is accessible at [http://localhost:9090](http://localhost:9090).
- Grafana is accessible at [http://localhost:3000](http://localhost:3000). Login with the provided credentials (admin/admin) and configure Prometheus as a data source.


### **Rating rules management**

Exposes rating rules to prometheus, then saves the results in postgres.

#### **Rating rules runtime options**


The **rating_rules_manager.py** script is designed to manage Prometheus metric rating rules specified in YAML files. It provides functionalities to add, remove, and update rating rules.

- **Add a Rule:**
Add a new rating rule 

  ```bash
  ./rating_rules_manager.py --add /path/to/your/rule.yaml
  ```

- **Remove a Rule:** Remove an existing rating rule 

  ```bash
  ./rating_rules_manager.py --rm /path/to/rule 
  ```

- **Update a Rule:**  Update an existing rating rule 

  ```bash
  ./rating_rules_manager.py --update /path/to/rule 
  ```

- **Create Rating Rule Instance:** Create an instance from template and value.

  ```bash
  ./rating_rules_manager --templates /path/to/template --values /path/to/value --instance /path/to/instance
  ```

* ./rating_rules_manager.py /path/to/rating/rule(s) : Expose rating rules to Prometheus, then saves the Prometheus results in Postgres.



## Notes

- The `config.env` file contains the path to the folder containing your rating rules YAML files. Adjust this file if your rules are stored in a different location.

- Ensure proper permissions for the script files (`start-rating-docker.sh` and `rating_rules_manager.py`) to execute.


##### **Config file**

Use config.env to define the path to the rating rules.



```env
# .env file

RULES_FOLDER=./rating-rules  
```

## Configuration details
##### **Node exporter configuration**

Use the node-exporter.yaml file if you want to add collectors not enabled by default in node-exporter.


exhaustive list of collectors : https://github.com/prometheus/node_exporter



```yaml
collectors:
  - collector name:
  
```
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






## Cleanup

To stop and remove the Docker containers, use:

```bash
docker-compose down
```












