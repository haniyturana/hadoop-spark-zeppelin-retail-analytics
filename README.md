📦 Big Data Architecture and Retail Analytics Pipeline
This repository contains an end-to-end Big Data Engineering and Analytics pipeline designed to process, clean, and analyze large-scale e-commerce transactional datasets. The project orchestrates data preprocessing, interactive exploratory data analysis (EDA), and data profiling strategies within a distributed enterprise-grade big data ecosystem.

🏗️ Project Architecture & Tech Stack
The pipeline is strategically divided into independent environments to leverage individual frameworks for specialized workloads:

1. Pre-Ingestion Data Cleaning (Jupyter Notebook)
Executed schema validation and strict data scrubbing prior to cluster ingestion.

Handled structural string formatting, trailing whitespace removal, and noise filtration (e.g., standardizing headers and stripping damaged stock codes or warehouse test logs).

Formulated clean, intermediate data files saved in optimized Parquet columnar storage format.

2. Distributed File Storage & Cluster Management (Hadoop & Ambari)
Utilized Hadoop Distributed File System (HDFS) for distributed and fault-tolerant data storage.

Configured local storage boundaries and optimized multi-node operations using Apache Ambari for web-based cluster orchestration and health verification.

3. Interactive Analytical Engine (Apache Zeppelin & Spark SQL)
Registered PySpark DataFrames into native Spark SQL Temporary Virtual Views to execute high-performance analytical queries directly over HDFS.

Implemented nested Common Table Expressions (CTEs) and window ranking functions (ROW_NUMBER()) to profile global consumer demand patterns.

Performed deep-dive business intelligence validation, mapping market-specific structural segments such as high-volume retail (B2C) patterns in the United Kingdom versus high-yield wholesale bulk-purchasing behavior (B2B) in the Netherlands and Singapore.

🔬 Core Business Insights Discovered
Temporal Consumption Patterns: Retail activity exhibits a severe data skew toward daylight business hours, scaling up aggressively from 7:00 AM, peaking exactly between 12:00 PM and 1:00 PM, and showing minimal baseline retention on weekends.

Cross-Border Market Penetration: Novelty items and low-cost baking consumables function as primary drivers for international logistics. A prominent asset, 'PACK OF 72 RETROSPOT CAKE CASES', demonstrates absolute global versatility across fourteen distinct international markets.

B2B vs. B2C Purchasing Dynamics: Built data models proving extreme regional behavior differences. The United Kingdom represents a high-frequency, lower average order value (AOV) retail space, while the Netherlands and Singapore function as premium wholesale channels driving massive volumes per transaction.

🛠️ Prerequisites & Local Infrastructure Setup
To interact with the interactive scripts and review the analysis logs, ensure your host environment satisfies the following infrastructure constraints:

Hypervisor Engine: Oracle VM VirtualBox (configured with compatible booted Hadoop Cluster nodes).

Cluster Web Dashboard: Apache Ambari UI (accessible via http://127.0.0.1:1080/).

HDFS Storage Directory: Shared directory path configured at /onlineretail2/.

Execution Engine: Apache Spark Core running PySpark interpreter APIs.

Interactive Frontend UI: Apache Zeppelin Web UI (accessible via http://localhost:9995/).

📂 Repository Structure
Bash
├── cleancolumn_cleandescription.ipynb  # Pre-ingestion data cleansing notebook
├── onlineretail2_1.json                # Exported Apache Zeppelin analytical notebook
├── README.md                           # Documentation and infrastructure map
└── Apache_Zeppelin_EDA_Report.pdf      # Full analytical and architecture setup report

🚀 Step-by-Step Environment Execution Guide
Phase 1: Preprocessing & HDFS Ingestion

1. Execute the preprocessing pipeline inside cleancolumn_cleandescription.ipynb via Jupyter to clean and parse the source text patterns.
2. Launch the local Oracle VM VirtualBox environment and wait until the cluster nodes achieve a stable state.
3. Access the Apache Ambari UI, open the File View, and create a directory named /onlineretail2/.
4. Upload the parsed, clean Parquet data files straight into the created directory view.

Phase 2: Zeppelin Initialization & EDA
1. Open the Apache Zeppelin dashboard interface at port 9995.
2. Import or create a notebook session, ensuring the target interpreter properties are assigned to Spark execution paths.
3. Run the initial storage pointer configuration to map data files into memory buffers:
"df_zeppelin = spark.read.parquet("/onlineretail2/onlineretail_ii_v1.parquet")"
4. Register the structured schema into a Temporary Virtual View:
"df_zeppelin.createOrReplaceTempView("online_retail_final_metrics")"
5. Execute the integrated SQL cells to dynamically render the time-series charts, geographic analytics, and customer ranking visualizations.
