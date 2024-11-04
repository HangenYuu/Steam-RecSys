# 1. SteamDB-RecSys
This is a personal project to demonstrate how data pipelines for offline ML training and serving in a recommendation system will look like. The project uses game review data scraped from Steam. The original data came from [Kaggle](https://www.kaggle.com/datasets/mohamedtarek01234/steam-games-reviews-and-rankings/data). I modified them and uploaded to [HuggingFace re-upload mirror](https://huggingface.co/datasets/HangenYuu/Steam_Games_Review).

The project started on 04/10/2024, by a undergraduate student who loves learning about data engineering, distributed system, and recommendation system.

Accompany this project is a series blog posts consolidating the knowledge I learnt from industry best practices, published in my blog at https://hung.bearblog.dev/. The particular posts are listed below.

- Part 1: Project Development - 
- Part 2: General Architecture - 
- Part 3: Scale Up Training & Serving: Offline - 
- Part 4: Scale Up Training & Serving: Online - (*In Progress*)

**Table of Contents**

- [1. SteamDB-RecSys](#1-steamdb-recsys)
- [2. Technologies](#2-technologies)
- [3. Running the Project](#3-running-the-project)
  - [3.1. Ingestion Pipeline](#31-ingestion-pipeline)
- [4. Business Requirements](#4-business-requirements)
  - [4.1. Overall Objective:](#41-overall-objective)
  - [4.2. Key Business Requirements:](#42-key-business-requirements)
    - [4.2.1. Personalized Recommendations:](#421-personalized-recommendations)
    - [4.2.2. Scalability:](#422-scalability)
    - [4.2.3. Real-time and Batch Processing:](#423-real-time-and-batch-processing)
    - [4.2.4. Robustness and Fault Tolerance:](#424-robustness-and-fault-tolerance)
    - [4.2.5. Usability:](#425-usability)
    - [4.2.6. Business Impact:](#426-business-impact)
- [5. Translated Technical Requirements](#5-translated-technical-requirements)
- [6. Schematic Designs](#6-schematic-designs)
  - [6.1. General Design](#61-general-design)
  - [6.2. Specific implementation](#62-specific-implementation)

# 2. Technologies
- Python 3.10.10.
- [GitHub Codespace](https://github.com/codespaces/) and [Lightning AI Studio](https://lightning.ai/studios) for development environments.
- [Polars](https://pola.rs/) and [Pandas](https://pandas.pydata.org/) for data processing.
- [Mage](https://www.mage.ai/) for data pipeline definition & orchestration.
- [PostgreSQL](https://www.postgresql.org/) for SQL database.
- [Docker](https://www.docker.com/) for containerization.
- [Google Cloud Storage](https://cloud.google.com/storage) to create data lake.

# 3. Running the Project

1. Go to the correct working directory and initialize the containers.
```bash
git clone https://github.com/HangenYuu/Steam-RecSys.git
cd data_pipeline
# Build and start the containers
docker compose up -d --build
```
2. Navigate to http://localhost:6789/ to view the Mage UI.
(Picture needed)
3. Edit the `io-config.yaml` file in the IDE or the file in Mage UI. We need to set the correct credentials for GCP, PostgreSQL, and MongoDB.
```yaml
# Google
GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/solid-acrobat-440004-g5-903ac2d18476.json"
GOOGLE_LOCATION: US # Optional
# MongoDB
# Specify the connection string or the (host, password, user, port) to connect to MongoDB.
MONGODB_CONNECTION_STRING: "mongodb+srv://{{ env_var('MONGODB_USER') }}:{{ env_var('MONGODB_PASSWORD') }}@{{ env_var('MONGODB_HOST') }}/"
MONGODB_DATABASE: sample_mflix
MONGODB_COLLECTION: rec_results
# PostgresSQL
POSTGRES_CONNECT_TIMEOUT: 10
POSTGRES_DBNAME: {{ env_var('POSTGRES_DBNAME') }}
POSTGRES_SCHEMA: {{ env_var('POSTGRES_SCHEMA') }}
POSTGRES_USER: {{ env_var('POSTGRES_USER') }}
POSTGRES_PASSWORD: {{ env_var('POSTGRES_PASSWORD') }}
POSTGRES_HOST: {{ env_var('POSTGRES_HOST') }}
POSTGRES_PORT: {{ env_var('POSTGRES_PORT') }}
```
4. Go to "Pipelines" in Mage UI, you should see 6 pipelines:
- 
1. Go to ... and run the 2 cells to check for PostgreSQL & GCS connections.
(Picture)
1. Go to ... and run the pipeline to ingest the data to the PostgreSQL database. **Note**: The PostgreSQL container has no volume so this should be run again if the containers are run again after `docker compose down`.

## 3.1. Ingestion Pipeline


# 4. Business Requirements
Here's a realistic business requirements possibly handed down by the business team. I included it as reference only.

<details>
  <summary>Read more</summary>

## 4.1. Overall Objective:
Design and implement a scalable recommendation system for Steam games that enhances user engagement by suggesting relevant games based on player preferences and interactions.
The system should **efficiently process large datasets** and **provide personalized game recommendations that can improve user satisfaction and increase game discoverability**.

## 4.2. Key Business Requirements:

### 4.2.1. Personalized Recommendations:

- The system must offer personalized game recommendations to users based on their interaction history, such as reviews and playtime, as well as game attributes like genres and system requirements.
- Recommendations should cater to both new and existing users, with minimal latency in generating suggestions.

### 4.2.2. Scalability:
- The system should be able to handle large datasets (millions of users, games, and reviews) while maintaining high performance.
- It must be capable of scaling horizontally to accommodate growing data volumes as the user base expands.

### 4.2.3. Real-time and Batch Processing:
- The primary focus is on offline recommendations, but the system should support periodic updates to reflect new game releases, reviews, and user interactions.
- Consideration will be given to integrating a near real-time recommendation feature for new user interactions.

### 4.2.4. Robustness and Fault Tolerance:
- The recommendation system must be reliable, with mechanisms for handling system failures, ensuring continuous operation without data loss or significant downtime.
- It should include monitoring and alerting to detect issues and ensure system stability.

### 4.2.5. Usability:
- The system should deliver recommendations in a user-friendly format, making it easy for users to explore suggested games.
- It must support multiple ranking options (e.g., relevance, sales, reviews) based on user preferences or behaviors.

### 4.2.6. Business Impact:
- The goal of the system is to improve user engagement and retention by suggesting games that align with user interests.
- It should drive increased game sales and discovery by highlighting top-ranked games or new releases within the user’s interest scope.

</details>

# 5. Translated Technical Requirements

- **Data source & format**: User reviews gathered in operational database e.g., MySQL or PostgreSQL. Since the data is used for ML training, they're better extracted out as flat files such as CSV or Parquet. Hence, I need to build an **ETL pipeline** to transfer the data from operational database to a storage server for my machine learning engineer (MLE) colleagues.
- **ML System Characteristics**: For offline system, the model will be trained and evaluated offline. Inference will be performed in batch offline at a cadence e.g., daily, then reverse ETL back to operational server to serve the results. Continual training with new data (new game released, new users, new reviews, etc.) will also be performed in batch at a longer cadence e.g., weekly, or when model performance dipped below a threshold.
- **Serving**: Inference results are produced in batch, offline. To serve the results, a **reverse ETL pipeline** is suitable for transferring inference results back to operational database.
In summary, the data engineer team will need to build 2[^1] data pipelines: one for operational data to training data, one for inference results to operational data.

# 6. Schematic Designs
## 6.1. General Design
![System 2](https://raw.githubusercontent.com/HangenYuu/blog-assets/refs/heads/main/System-2.excalidraw.png)

Components in the system:

1. A source database.
2. Pipelines for training and inference.
3. ETL pipeline for creating training data.
4. Reverse ETL pipeline for serving inference results.
5. Storage server for training data, training artifacts, and inference results.

## 6.2. Specific implementation

![System 4](https://github.com/HangenYuu/blog-assets/blob/main/System%204.excalidraw.png?raw=true)

- [Mage](https://www.mage.ai/) is used to implement the 2 data pipelines.
- [PostgreSQL](https://www.postgresql.org/) is used to emulate the source database server.
- [Google Cloud Storage](https://cloud.google.com/storage) is used as the storage server for all data.
