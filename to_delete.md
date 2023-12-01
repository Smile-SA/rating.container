
* ./rating_rules_manager --templates /path/to/template --values /path/to/value --instance /path/to/instance : Create an instance from template and value.
# **Uninstallation**



# Rating Docker Project

This project provides a Dockerized environment for a rating system that utilizes Prometheus, Grafana, Node Exporter, and TimescaleDB. The rating rules are managed using a Python script.

## Getting Started

Follow these steps to get the project up and running:

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Docker Compose Setup

1. Adjust the configuration files in the `config` directory according to your preferences.

2. Start the Docker containers:

```bash
./start-rating-docker.sh
```

This script launches the necessary services defined in the `docker-compose.yml` file, including Prometheus, Grafana, Node Exporter, and TimescaleDB.

3. Configure Prometheus and Grafana:

   - Prometheus is accessible at [http://localhost:9090](http://localhost:9090).
   - Grafana is accessible at [http://localhost:3000](http://localhost:3000). Login with the provided credentials (admin/admin) and configure Prometheus as a data source.

### Rating Rules Management

The `rating_rules_manager.py` script in the `utils` directory allows you to manage rating rules. Here are some examples:

- **Add a Rule:**

  ```bash
  ./rating_rules_manager.py --add /path/to/your/rule.yaml
  ```

- **Remove a Rule:**

  ```bash
  ./rating_rules_manager.py --rm your_rule.yaml
  ```

- **Update a Rule:**

  ```bash
  ./rating_rules_manager.py --update your_rule.yaml
  ```

- **Create Rating Rule Instance:**

  ```bash
  ./rating_rules_manager.py --instance /path/to/templates --t /path/to/templates --v /path/to/values
  ```

### Cleanup

To stop and remove the Docker containers, use:

```bash
docker-compose down
```

## Notes

- The `config.env` file contains the path to the folder containing your rating rules YAML files. Adjust this file if your rules are stored in a different location.

- Ensure proper permissions for the script files (`start-rating-docker.sh` and `rating_rules_manager.py`) to execute.

Feel free to explore and customize the project based on your requirements!