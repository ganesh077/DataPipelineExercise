# Real-Time Software Engineering Analytics

This project implements a data pipeline for capturing, processing, and visualizing service telemetry to monitor the health and performance of microservices.

## Background

The goal is to provide a platform engineering team with the tools to monitor microservice health, detect service degradation, slow response times, and increasing error rates. This is crucial for ensuring reliability in large-scale enterprise applications.

## Architecture

The data pipeline consists of the following layers:

1.  **Ingestion Layer:** Simulates streaming service logs and consumes them.
2.  **Transformation Layer:** Processes logs to flag slow responses, mark errors, and aggregate per-service metrics.
3.  **Storage Layer:** Stores the processed data in a columnar format (Parquet), partitioned by service and date.
4.  **Serving Layer:** Visualizes key metrics and creates alerts for SLO violations.

# Components

* **`generator.py`**: This Python script simulates streaming service telemetry logs in JSON format. It generates logs with fields like `id`, `service`, `timestamp`, `status_code`, `latency_ms`, and `error`. It uses the `confluent-kafka` library to produce these logs to a Kafka topic named `service-telemetry`.
* **`kafka.yaml`**: This Docker Compose file sets up a local Kafka environment using Bitnami's Zookeeper and Kafka images. It defines the necessary ports and configurations for Kafka to run.
* **`service_config.yaml`**: This YAML file configures service-specific parameters, including the owning team, latency thresholds, and error budgets (as a percentage). Examples are provided for `auth-service` and `payments-service`.
* **`dashboard.py`**: This Streamlit application provides a dashboard for visualizing key service metrics. It loads Parquet data, displays latency and error rate charts, and shows SLO violation metrics. It allows the user to select a service (`auth-service` or `payments-service`) from a sidebar dropdown.

## Data Transformation

The data transformation layer (which is part of the consumer logic, not a separate script in this example) performs the following:

* Flagging slow responses: Compares `latency_ms` against the `latency_threshold_ms` defined in `service_config.yaml`.
* Marking error logs: Checks if `status_code` is greater than or equal to 500.
* Aggregating metrics: Calculates average latency, error rate, and the 95th percentile latency per service.

## Storage

Processed data is stored in Parquet format, partitioned by `service` and `date`. This columnar format is efficient for analytical queries. The `dashboard.py` script assumes the data is stored in the `/data/parquet/` directory.

## Usage

1.  **Set up Kafka:** Use Docker Compose to start Kafka (`docker-compose -f kafka.yaml up -d`).
2.  **Generate Logs:** Run `generator.py` to start producing service telemetry logs.
3.  **Run the Dashboard:** Execute `dashboard.py` using Streamlit (`streamlit run dashboard.py`).
4.  **View Metrics:** Access the Streamlit dashboard in your browser to visualize service metrics and SLO violations.

## Stretch Goals (Not Implemented)

The exercise also suggests the following stretch goals:

* Create a status dashboard with green/yellow/red indicators.
* Add auto-scaling simulation.
* Integrate with orchestration tools like Airflow or Dagster.

## Interview Value

This project demonstrates practical skills in:

* Logging and monitoring
* Data pipeline development
* Observability and SRE concepts

It aligns with real-world systems used at high-scale companies.
