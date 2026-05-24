# hadoop-spark-retail-analytics

This repository contains an end-to-end Big Data Engineering and Analytics pipeline for large-scale e-commerce transactional data. The project orchestrates data cleaning, interactive exploratory analysis, and advanced machine learning modeling using a distributed ecosystem.

---

## 🏗️ Project Architecture & Tech Stack

The pipeline is split into three main operational environments to leverage the strengths of different big data tools:

1. **Data Cleaning & Preprocessing (Jupyter Notebook - Pandas/PySpark)**
   * Handled raw parquet datasets.
   * Executed strict data scrubbing (removing warehouse logs, damaged flags, and system noise).
   * Performed "Strict Unified Description" mapping to resolve product description anomalies and typographical variations.

2. **Exploratory Data Analysis & Interactive BI (Apache Zeppelin - Spark SQL)**
   * Managed via **Apache Ambari** on a distributed Hadoop cluster.
   * Built interactive dashboard components tracking time-series trends (sales by month, peak order hours).
   * Analyzed geographic trends and market behavior profiles (e.g., Identifying United Kingdom as a high-volume B2C market vs. Netherlands as a high-value B2B/Wholesale market).

3. **Advanced Analytics & Machine Learning (Google Colab - Python/Scikit-Learn)**
   * Utilizes the pre-processed "perfect" dataset exported from the pipeline.
   * Focused on customer lifetime value metrics and behavioral segmentations.

---

## 🛠️ Prerequisites & Infrastructure

* **Cluster Management:** Apache Ambari
* **Storage Layer:** Hadoop Distributed File System (HDFS) / Parquet Columnar Storage
* **Execution Engines:** Apache Spark (PySpark) & Local Pandas
* **Notebooks:** Apache Zeppelin, Jupyter Notebook, Google Colab
