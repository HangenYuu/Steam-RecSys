# 1. SteamDB-RecSys
This is a personal project to design, build, and deploy an offline recommendation system from scratch using game review data from Steam, hosted on [Kaggle](https://www.kaggle.com/datasets/mohamedtarek01234/steam-games-reviews-and-rankings/data) | [HuggingFace re-upload mirror](https://huggingface.co/datasets/HangenYuu/Steam_Games_Review).

The project was created on 04/10/2024, by a graduating undergraduate student looking to learn more about data engineering, distributed system, and recommendation system.

The details of building the project, as well as the knowledge learnt about industry best practices will be provided in my blog at https://hung.bearblog.dev/. The particular posts are listed below.

- Part 1: 
- Part 2:
- Part 3:

**Table of Contents**

- [1. SteamDB-RecSys](#1-steamdb-recsys)
- [2. Business Requirements](#2-business-requirements)
  - [2.1. Overall Objective:](#21-overall-objective)
  - [2.2. Key Business Requirements:](#22-key-business-requirements)
    - [2.2.1. Personalized Recommendations:](#221-personalized-recommendations)
    - [2.2.2. Scalability:](#222-scalability)
    - [2.2.3. Real-time and Batch Processing:](#223-real-time-and-batch-processing)
    - [2.2.4. Robustness and Fault Tolerance:](#224-robustness-and-fault-tolerance)
    - [2.2.5. Usability:](#225-usability)
    - [2.2.6. Business Impact:](#226-business-impact)
- [3. Translated Technical Requirements](#3-translated-technical-requirements)
- [4. Schematic Designs](#4-schematic-designs)
  - [4.1. General Design](#41-general-design)
  - [4.2. Specific implementation](#42-specific-implementation)
- [5. Implementations](#5-implementations)
  - [5.1. ETL Pipeline](#51-etl-pipeline)

# 2. Business Requirements
Here's a realistic business requirements possibly handed down by the business team.

<details>
  <summary>Read more</summary>

## 2.1. Overall Objective:
Design and implement a scalable recommendation system for Steam games that enhances user engagement by suggesting relevant games based on player preferences and interactions.
The system should **efficiently process large datasets** and **provide personalized game recommendations that can improve user satisfaction and increase game discoverability**.

## 2.2. Key Business Requirements:

### 2.2.1. Personalized Recommendations:

- The system must offer personalized game recommendations to users based on their interaction history, such as reviews and playtime, as well as game attributes like genres and system requirements.
- Recommendations should cater to both new and existing users, with minimal latency in generating suggestions.

### 2.2.2. Scalability:
- The system should be able to handle large datasets (millions of users, games, and reviews) while maintaining high performance.
- It must be capable of scaling horizontally to accommodate growing data volumes as the user base expands.

### 2.2.3. Real-time and Batch Processing:
- The primary focus is on offline recommendations, but the system should support periodic updates to reflect new game releases, reviews, and user interactions.
- Consideration will be given to integrating a near real-time recommendation feature for new user interactions.

### 2.2.4. Robustness and Fault Tolerance:
- The recommendation system must be reliable, with mechanisms for handling system failures, ensuring continuous operation without data loss or significant downtime.
- It should include monitoring and alerting to detect issues and ensure system stability.

### 2.2.5. Usability:
- The system should deliver recommendations in a user-friendly format, making it easy for users to explore suggested games.
- It must support multiple ranking options (e.g., relevance, sales, reviews) based on user preferences or behaviors.

### 2.2.6. Business Impact:
- The goal of the system is to improve user engagement and retention by suggesting games that align with user interests.
- It should drive increased game sales and discovery by highlighting top-ranked games or new releases within the user’s interest scope.

</details>

# 3. Translated Technical Requirements

- **Data source & format**: User reviews gathered in operational database e.g., MySQL or PostgreSQL. Since the data is used for ML training, they're better extracted out as flat files such as CSV or Parquet. Hence, I need to build an **ETL pipeline** to transfer the data from operational database to a storage server for my machine learning engineer (MLE) colleagues.
- **ML System Characteristics**: For offline system, the model will be trained and evaluated offline. Inference will be performed in batch offline at a cadence e.g., daily, then reverse ETL back to operational server to serve the results. Continual training with new data (new game released, new users, new reviews, etc.) will also be performed in batch at a longer cadence e.g., weekly, or when model performance dipped below a threshold.
- **Serving**: Inference results are produced in batch, offline. To serve the results, a **reverse ETL pipeline** is suitable for transferring inference results back to operational database.
In summary, the data engineer team will need to build 2[^1] data pipelines: one for operational data to training data, one for inference results to operational data.

# 4. Schematic Designs
## 4.1. General Design
![System 2](https://raw.githubusercontent.com/HangenYuu/blog-assets/refs/heads/main/System-2.excalidraw.png)

Components in the system:

1. A source database.
2. Pipelines for training and inference.
3. ETL pipeline for creating training data.
4. Reverse ETL pipeline for serving inference results.
5. Storage server for training data, training artifacts, and inference results.

## 4.2. Specific implementation

![System 4](https://github.com/HangenYuu/blog-assets/blob/main/System%204.excalidraw.png?raw=true)

- [Mage](https://www.mage.ai/) is used to implement the 2 data pipelines.
- [PostgreSQL](https://www.postgresql.org/) is used to emulate the source database server.
- [Google Cloud Storage](https://cloud.google.com/storage) is used as the storage server for all data.

# 5. Implementations
## 5.1. ETL Pipeline
Everything lives in the data_pipeline folder.
The PostgreSQL and Mage are containerized together with Docker Compose.

<details>
  <summary>Notes</summary>

Docker Compose also configures a common network for the two containers. In practice, when building the system for data processing, we need to configure the private network to extract the data with ODBC APIs (obviously, you cannot expose your database APIs publicly).

</details>

To run the applications:
1. Go to the correct working directory.
```bash
git clone https://github.com/HangenYuu/Steam-RecSys.git
cd data_pipeline
# Build the project
docker compose build
# Start the containers
docker compose up
```
2. Navigate to http://localhost:6789/ to view the Mage UI.
