

# Stock Market Pipeline

## Overview

The Stock Market Pipeline is an Apache Airflow-based data pipeline designed to fetch, process, and store stock market data for analysis. It retrieves stock prices from an API, processes the data using Apache Spark, stores it in MinIO (S3-compatible storage), and loads it into a PostgreSQL database. The pipeline integrates Metabase for data visualization. Built with Astronomer CLI and Astro Runtime, it provides a robust environment for orchestrating data workflows.

### Features
- **Data Ingestion**: Fetches stock market data from a configured API.
- **Data Processing**: Processes stock data using Python and Apache Spark for formatting and transformation.
- **Storage**: Stores raw and processed data in MinIO and PostgreSQL.
- **Visualization**: Uses Metabase for querying and visualizing stock market data.
- **Automation**: Schedules daily data updates via Airflow DAGs.
- **Testing**: Includes unit tests for DAG integrity.

### Acknowledgement
This project was developed based on Marc Lamberti’s Udemy course, “The Ultimate Hands-On Course to Master Apache Airflow,” available at: [https://www.udemy.com/course/the-ultimate-hands-on-course-to-master-apache-airflow/?couponCode=ST14MT150425G3](https://www.udemy.com/course/the-ultimate-hands-on-course-to-master-apache-airflow/?couponCode=ST14MT150425G3).

## Project Structure

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
├── docker-compose.override.yml    # Docker Compose overrides (MinIO, Spark, Metabase)
├── packages.txt                   # OS-level package dependencies
├── plugins/                       # Airflow plugins (empty)
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```

## Prerequisites

- **Docker and Docker Compose**: To run Airflow and additional services.
- **Astronomer CLI**: For managing the Airflow project (`astro` command).
- **Python 3.8+**: For local development or dependency installation.
- **Git**: To clone or manage the repository.
- **Homebrew (macOS)**: Optional, for installing tools like `tree`.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aishwarya-1991/Stock-Market-Pipeline.git
   cd Stock-Market-Pipeline
   ```

2. **Install Astronomer CLI**:
   - Follow the [Astronomer CLI Documentation](https://docs.astronomer.io/astro/cli/install-cli).
   - On macOS, use Homebrew:
     ```bash
     brew install astro
     ```

3. **Install Dependencies**:
   - The `requirements.txt` includes:
     ```
     minio==7.1.14
     apache-airflow-providers-docker>=3.0.0,<4.0.0
     ```
   - These are automatically installed in the Astro Runtime environment when you start the project.

4. **Set Up Docker**:
   - Ensure Docker Desktop is running. The project uses Docker Compose to manage Airflow, MinIO, Spark, and Metabase.

## Usage

1. **Configure Airflow Connections**:
   - Update `airflow_settings.yaml` with the following connections (or configure manually in Airflow UI):
     ```yaml
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
   - Replace `<api-host>`, `<api-endpoint>`, and `<token>` with your stock API credentials.

2. **Start the Project**:
   ```bash
   astro dev start
   ```
   This launches Docker containers for:
   - Airflow (Webserver, Scheduler, Triggerer, Postgres)
   - MinIO (http://localhost:9000)
   - Spark (Master and Worker)
   - Metabase (http://localhost:3000)
   - Docker Proxy (for DockerOperator)

3. **Access Services**:
   - **Airflow UI**: [http://localhost:8080](http://localhost:8080) (login: `admin`/`admin`)
   - **MinIO Console**: [http://localhost:9001](http://localhost:9001) (login: `minio`/`minio123`)
   - **Metabase**: [http://localhost:3000](http://localhost:3000) (complete setup)
   - **Spark Master UI**: [http://localhost:8082](http://localhost:8082)
   - **Spark Worker UI**: [http://localhost:8081](http://localhost:8081)

4. **Run the DAGs**:
   - In the Airflow UI, enable and trigger the `stock_market` and `generate_random` DAGs.
   - The `stock_market` DAG processes AAPL stock data and stores it in MinIO and Postgres.
   - The `generate_random` DAG generates a random number and checks if it’s odd or even.

5. **View Results**:
   - Stock data is stored in MinIO (`s3://stock-market/AAPL/`) and Postgres (`stock_market` table).
   - Use Metabase to query and visualize data from Postgres.

## DAGs

### 1. `stock_market`
- **Purpose**: Fetches and processes stock market data from an API.
- **Tasks**:
  - `is_api_available`: Checks API availability.
  - `get_stock_prices`: Fetches stock prices.
  - `store_prices`: Stores raw prices in MinIO.
  - `format_prices`: Processes data using Spark (via DockerOperator).
  - `get_formatted_csv`: Retrieves formatted CSV from MinIO.
  - `load_to_dw`: Loads data into Postgres.
- **Helper Script**: `include/helpers/minio.py` facilitates MinIO interactions.

## Dependencies

### Python Packages (`requirements.txt`)
```
minio==7.1.14
apache-airflow-providers-docker>=3.0.0,<4.0.0
```

### OS Packages (`packages.txt`)
- Empty by default.

## Testing

- **Location**: `tests/dags/test_dag_example.py`
- **Purpose**: Unit tests for DAG integrity.
- **Run Tests**:
  ```bash
  astro dev pytest
  ```

## Additional Services

- **MinIO**: S3-compatible storage for raw and processed data.
- **Apache Spark**: Processes stock data in the `format_prices` task.
- **Metabase**: Visualizes data stored in Postgres.
- **Docker Proxy**: Enables DockerOperator communication for Spark tasks.



---

### Changes Made
- **Formatting**:
  - Used consistent Markdown headings (`#`, `##`, `###`) for hierarchy.
  - Formatted code blocks with triple backticks (```) and specified languages (e.g., `bash`, `yaml`).
  - Organized lists with dashes (`-`) for clarity.
  - Enclosed file paths and commands in backticks for inline code.
  - Used bold (`**`) for emphasis on key terms (e.g., **Purpose**, **Tasks**).
- **Grammar and Clarity**:
  - Refined the acknowledgment based on your grammar check (April 16, 2025, 12:14), using “was developed based on” and proper article usage.
  - Clarified ambiguous phrases (e.g., “processes AAPL stock data” instead of generic “stock data” where specific).
  - Standardized terminology (e.g., “Astronomer CLI” instead of “Astronomer CLI” or “astro command”).
- **Structure**:
  - Moved **Acknowledgement** under **Overview** as a subsection, following your prior project structure (April 16, 2025, 11:07).
  - Grouped **DAGs**, **Dependencies**, **Testing**, and **Additional Services** as separate sections for clarity.
  - Ensured **Project Structure** uses a code block for the directory tree, improving readability.
- **Consistency**:
  - Aligned with your prior request for a copy-pasteable README (April 16, 2025, 12:14).
  - Maintained all details from your input, including specific ports (e.g., `http://localhost:8080`) and file paths (e.g., `include/helpers/minio.py`).
  - Included the exact `requirements.txt` and `airflow_settings.yaml` examples as provided.

### Notes
- **Context Integration**: The README complements your Stock Market Pipeline project, which uses Astro CLI for Airflow, unlike the dbt/Snowflake pipeline (April 16, 2025, 11:07). It excludes dbt components as they weren’t mentioned here but can be added if needed.
- **Repository**: Assumes `Aishwarya-1991/Stock-Market-Pipeline` is the correct repository. If it’s different, update the `git clone` URL.
- **Airflow Connections**: The `airflow_settings.yaml` example requires API credentials (`<api-host>`, `<token>`). Replace placeholders with your stock API details (e.g., Alpha Vantage, Yahoo Finance).
- **Metabase Setup**: The README notes that Metabase requires manual setup at `http://localhost:3000`, as per your input.

You can copy the content within the `<xaiArtifact>` tags directly into your `README.md` file. If you need further refinements (e.g., adding setup steps, integrating dbt, or adjusting for a specific stock API), let me know!
