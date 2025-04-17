**Stock Market Pipeline
Overview**
The Stock Market Pipeline is an Apache Airflow-based data pipeline designed to fetch, process, and store stock market data for analysis. It retrieves stock prices from an API, processes the data using Apache Spark, stores it in MinIO (S3-compatible storage), and loads it into a PostgreSQL database. The project integrates Metabase for data visualization and includes a random number generator DAG for demonstration. Built with Astronomer CLI and Astro Runtime, it provides a robust environment for orchestrating data workflows.
Features:

**Acknowledgement:**
This project is based on Marc Lamberti’s Udemy course, “The Ultimate Hands-On Course to Master Apache Airflow” (https://www.udemy.com/course/the-ultimate-hands-on-course-to-master-apache-airflow/?couponCode=ST14MT150425G3).

**Data Ingestion**: Fetches stock market data from a configured API.
**Data Processing:** Processes stock data using Python and Apache Spark for formatting and transformation.
**Storage:** Stores raw and processed data in MinIO and PostgreSQL.
**Visualization:** Uses Metabase for querying and visualizing stock market data.
**Automation:** Schedules daily data updates via Airflow DAGs.
**Testing**: Includes unit tests for DAG integrity.


**Project Structure**
```
Stock-Market-Pipeline/
├── .astro/                        # Astronomer CLI configuration
│   ├── config.yaml
│   ├── dag_integrity_exceptions.txt
│   └── test_dag_integrity_default.py
├── .git/                          # Git repository files
├── dags/                          # Airflow DAGs
│   ├── stock_market.py            # Main stock market data pipeline DAG
│   ├── taskflow.py                # Example DAG for generating random numbers
│   └── __pycache__/               # Python compiled files
├── include/                       # Additional files and data
│   ├── data/                      # Storage for MinIO and Metabase
│   │   ├── metabase/              # Metabase data
│   │   └── minio/                 # MinIO storage
│   │       ├── .minio.sys/        # MinIO system files
│   │       └── stock-market/      # Stock market data (e.g., AAPL prices)
│   ├── helpers/                   # Utility scripts
│   │   └── minio.py               # MinIO interaction helper
│   └── stock_market/              # Stock market processing tasks
│       └── tasks.py               # Task definitions for stock processing
├── spark/                         # Spark configurations
│   ├── master/                    # Spark master setup
│   │   ├── Dockerfile
│   │   └── master.sh
│   ├── notebooks/                 # Spark notebooks
│   │   └── stock_transform/       # Stock transformation scripts
│   │       ├── Dockerfile
│   │       ├── requirements.txt
│   │       └── stock_transform.py
│   └── worker/                    # Spark worker setup
│       ├── Dockerfile
│       └── worker.sh
├── tests/                         # Test scripts
│   └── dags/
│       └── test_dag_example.py    # DAG unit tests
├── .dockerignore                  # Docker ignore rules
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
├── Dockerfile                     # Astro Runtime base image
├── airflow_settings.yaml          # Airflow connections and variables
├── docker-compose.override.yml     # Docker Compose overrides (MinIO, Spark, Metabase)
├── packages.txt                   # OS-level package dependencies (empty)
├── plugins/                       # Airflow plugins (empty)
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```
**Prerequisites**

Docker and Docker Compose: To run Airflow and additional services.

Astronomer CLI: For managing the Airflow project (astro command).

Python 3.8+: For local development or dependency installation.

Git: To clone or manage the repository.

Homebrew (macOS): Optional, for installing tools like tree.

**Installation**

Clone the Repository:
```git clone https://github.com/Aishwarya-1991/Stock-Market-Pipeline.git```
```cd Stock-Market-Pipeline```


**Install the Astronomer CLI:**
Follow the instructions at Astronomer CLI Documentation.
On macOS, you can use Homebrew:
```brew install astro```


**Install Dependencies:**
The requirements.txt specifies:
```minio==7.1.14```
```apache-airflow-providers-docker>=3.0.0,<4.0.0```

These are installed in the Astro Runtime environment when you start the project.
**Set Up Docker:**
Ensure Docker is running. The project uses Docker Compose to manage Airflow, MinIO, Spark, and Metabase.

**Usage**

Configure Airflow Connections: (I have completed it manually in Airflow UI)

Update airflow_settings.yaml with:

Stock API: Set stock_api connection (conn_type: http, conn_host, conn_extra with endpoint and headers).

MinIO: Set minio connection (conn_type: aws, conn_host: http://minio:9000, conn_login: minio, conn_password: minio123).

Postgres: Set postgres connection (conn_host: postgres, conn_port: 5432, conn_schema: public).

Example:
```
airflow:
  connections:
    - conn_id: stock_api
      conn_type: http
      conn_host: <api-host>
      conn_extra:
        endpoint: <api-endpoint>
        headers: { "Authorization": "Bearer <token>" }
    - conn_id: minio
      conn_type: aws
      conn_host: http://minio:9000
      conn_login: minio
      conn_password: minio123
    - conn_id: postgres
      conn_type: postgres
      conn_host: postgres
      conn_port: 5432
      conn_schema: public
```


**Start the Project:**
```astro dev start```

This launches Docker containers for:

Airflow (Webserver, Scheduler, Triggerer, Postgres)

MinIO (http://localhost:9000)

Spark (Master and Worker)

Metabase (http://localhost:3000)

Docker Proxy (for DockerOperator)


**Access Services:**

Airflow UI: http://localhost:8080 (login: admin/admin)
MinIO Console: http://localhost:9001 (login: minio/minio123)
Metabase: http://localhost:3000 (complete setup)
Spark Master UI: http://localhost:8082
Spark Worker UI: http://localhost:8081

**Run the DAGs:**

Enable and trigger stock_market and generate_random DAGs in the Airflow UI.
The stock_market DAG processes AAPL stock data and stores it in MinIO and Postgres.
The generate_random DAG generates a random number and checks if it’s odd or even.


**View Results:**

Stock data is stored in MinIO (s3://stock-market/AAPL/) and Postgres (stock_market table).
Use Metabase to visualize data from Postgres.



**DAGs**
1. stock_market

**Purpose:** Fetches and processes stock market data from an API

**Tasks:**
is_api_available: Checks API availability.
get_stock_prices: Fetches stock prices.
store_prices: Stores raw prices in MinIO.
format_prices: Processes data using Spark (via DockerOperator).
get_formatted_csv: Retrieves formatted CSV from MinIO.
load_to_dw: Loads data into Postgres.


The include/helpers/minio.py script facilitates MinIO interactions.
Dependencies
Python Packages (requirements.txt)

```minio==7.1.14
apache-airflow-providers-docker>=3.0.0,<4.0.0```

OS Packages (packages.txt)

Empty by default.

Testing

Location: tests/dags/test_dag_example.py

Purpose: Unit tests for DAG integrity.

**Run tests with:**
```astro dev pytest```



**Additional Services**

MinIO: S3-compatible storage.
Apache Spark: Data processing for format_prices.
Metabase: Data visualization.
Docker Proxy: Enables DockerOperator communication.



