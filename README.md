# 1. SteamDB-RecSys This project aims to be an educational project to build
This is a personal project to design, build, and deploy an offline recommendation system from scratch using game review data from Steam, hosted on [Kaggle](https://www.kaggle.com/datasets/mohamedtarek01234/steam-games-reviews-and-rankings/data) | HuggingFace  mirror.

The project was created on 04/10/2024, by a graduating undergraduate student looking to learn more about data engineering, distributed system, and recommendation system.

The details of building the system, as well as the knowledge learnt about industry best practices will be provided in my blog at https://hung.bearblog.dev/. The particular posts are listed below.

- [1. SteamDB-RecSys This project aims to be an educational project to build](#1-steamdb-recsys-this-project-aims-to-be-an-educational-project-to-build)
- [2. Business Requirements](#2-business-requirements)
  - [2.1. Overall Objective:](#21-overall-objective)
  - [2.2. Key Business Requirements:](#22-key-business-requirements)
    - [2.2.1. Personalized Recommendations:](#221-personalized-recommendations)
    - [2.2.2. Scalability:](#222-scalability)
    - [2.2.3. Real-time and Batch Processing:](#223-real-time-and-batch-processing)
    - [2.2.4. Robustness and Fault Tolerance:](#224-robustness-and-fault-tolerance)
    - [2.2.5. Usability:](#225-usability)
    - [2.2.6. Business Impact:](#226-business-impact)
- [3. Technical Designs](#3-technical-designs)
  - [3.1. MB case](#31-mb-case)
- [4. Technical Stack](#4-technical-stack)
- [5. Implementations](#5-implementations)

# 2. Business Requirements
Here's a realistic business requirements possibly handed down by the business team...
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

# 3. Technical Designs
For technical designs, I will do 2 rounds: for the actual dataset at hand (477MB), and for an imaginary dataset 10,000 times bigger (4.77TB). While the 10,000? It's because I want to learn realistically, and TB worth of reviews is more realistic for a large game/music/video distribution or e-commerce platform, like Steam in this case (or Spotify, YouTube, TikTok, Amazon, etc.). Of course, system changes with data and speed requirements, the design I create for the MB case using a single VM is not applicable for the TB case, which is almost surely a distributed system.
## 3.1. MB case


# 4. Technical Stack

# 5. Implementations