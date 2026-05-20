# Smart Grid Theft Detection & Accident Analytics

> Machine Learning, Geospatial Intelligence, NLP Pipelines, and Dashboard Engineering for Power Distribution Analytics

---

# Overview

This repository documents two data-driven projects developed during an internship focused on power distribution analytics and operational intelligence:

1. Electricity Theft Detection System  
2. Power Accident Cause Analysis & Dashboard

The work combines:
- Geospatial analytics
- Unsupervised learning
- Anomaly detection
- NLP classification pipelines
- Dashboard engineering

The objective was to automate the identification of suspicious electricity usage patterns and extract actionable insights from large-scale accident datasets.

---

# Project 1: Electricity Theft Detection

## Problem Statement

Electricity theft often occurs when:
- Commercial establishments are registered as domestic consumers
- Non-domestic establishments are registered as small industries to obtain tariff advantages

Traditional manual inspection is:
- Slow
- Expensive
- Difficult to scale

This project developed algorithmic approaches to automatically flag suspicious consumers using:
- Geospatial proximity analysis
- Consumption behavior analysis
- Address and ownership similarity matching

---

# System Architecture

```text
Google Maps API
        │
        ▼
Commercial Establishment Scraping
        │
        ▼
Consumer Meter Database
        │
        ├──────────────┐
        ▼              ▼
Geospatial        Consumption
Detection         Analytics
        │              │
        └──────┬───────┘
               ▼
        Risk Scoring Engine
               ▼
      High-Risk Theft Cases
```

---

# Approach 1: Non-Domestic Registered as Domestic

## Objective

Detect commercial establishments operating under domestic electricity connections.

---

## Algorithmic Workflow

### Step 1: Commercial Establishment Scraping

A Google Maps API based pipeline was built to scrape:
- Establishment names
- Coordinates
- Contact information
- Nearby businesses

Approximately **3500 commercial establishments** were collected within a **10 km radius** from Tonk city center.

---

## Suggested Figure

Add:
```text
images/google_maps_pipeline.png
```

Illustration idea:
```text
Google Maps API → Nearby Search → Commercial Database
```

---

## Step 2: Geospatial Nearest Neighbor Search

A brute-force distance comparison between all establishments and all meter locations was computationally expensive.

### Initial Complexity

```text
O(N × M)
```

Where:
- N = commercial establishments
- M = registered consumers

This took roughly:
- **20–25 minutes** per execution.

---

## Optimization Using BallTree

To accelerate nearest-neighbor search, the **BallTree algorithm** was implemented.

### Why BallTree?

BallTree partitions spatial points hierarchically using hyperspheres, enabling:
- Fast nearest-neighbor lookup
- Efficient geospatial queries
- Scalable radius searches

### Result

Execution time reduced from:

```text
20–25 minutes → 1–2 seconds
```

---

## Suggested Figure

Add:
```text
images/balltree_search.png
```

Illustration idea:
- Commercial point
- Nearest Domestic
- Nearest Non-Domestic
- Radius comparisons

---

## Theft Flagging Logic

A commercial establishment was flagged as suspicious when:

```python
distance_to_domestic < 5m
AND
distance_to_non_domestic > 5m
```

This indicates:
- The establishment physically exists
- Nearby registered meter is domestic
- No nearby legitimate commercial connection exists

---

## Result

After filtering:
- ~150 establishments
- Approximately 4% of the total dataset

were shortlisted as high-risk theft cases.

---

# Approach 2: Consumption-Based Detection

## Objective

Identify suspicious consumers using electricity usage behavior.

---

# Feature Engineering

A total of **19 engineered features** were extracted from historical meter consumption data.

## Features Used

### 1. Annual Consumption Features

Mean yearly consumption from:
- 2021
- 2022
- 2023
- 2024
- 2025

### 2. Monthly Consumption Trends

Average consumption for each calendar month.

### 3. Statistical Features

- Overall mean usage
- Standard deviation

---

# Principal Component Analysis (PCA)

## Why PCA?

The dataset had:
- Correlated temporal features
- High-dimensional consumption patterns

PCA was used to:
- Reduce dimensionality
- Identify latent behavioral trends
- Visualize category separation

---

## PCA Insights

### PC1 (~80% variance)

Represents:
- Overall consumption magnitude

All features showed strong positive loadings (~0.2).

---

### PC2 (~5% variance)

Strongly influenced by:
- 2024
- 2025 consumption averages

This captured recent behavioral changes.

---

## Total Variance Captured

```text
PC1 + PC2 ≈ 85%
```

---

# Behavioral Clustering

The PCA projection revealed two distinct behavioral patterns:

### Small Industries
- Linear cluster
- Negative slope trend

### Non-Domestic Consumers
- Positive slope cluster
- Increasing recent consumption trend

---

## Suggested Figure

Add:
```text
images/pca_plot.png
```

Caption:
> PCA distribution showing separation between Small Industries and Non-Domestic consumers.

---

# Anomaly Detection

A regression line was fitted over the Small Industry cluster.

Consumers significantly deviating from the expected distribution were flagged as anomalies.

### Logic

```text
Large deviation from SIP regression boundary
→ Potential misclassification
→ Possible electricity theft
```

---

# Approach 3: Address-Based Detection

## Objective

Cross-verify ownership and identity patterns between:
- Commercial establishments
- Registered meter records

---

# Pipeline

## Step 1: Fetch Establishment Details

Using:
- Google Maps API
- Google Places API

The pipeline extracted:
- Business names
- Phone numbers
- Address metadata

---

## Step 2: Nearby Small Industry Search

All nearby Small Industry connections within the search radius were identified.

---

## Step 3: Nearest Non-Domestic Matching

For every establishment:
- Closest Non-Domestic consumer was identified
- Registered details were extracted

---

## Step 4: Similarity Scoring

A similarity scoring system compared:
- Business names
- Phone numbers
- Ownership information

between:
- Google Maps data
- Registered meter database

---

# Example Output

The pipeline generated structured outputs containing:
- Establishment names
- Phone numbers
- Nearest meter records
- Similarity flags
- Distance metrics

---

# Future Improvements

Planned extensions include:

- Automated district-scale deployment
- Real-time monitoring dashboard
- Alternative ownership retrieval methods
- Continuous theft detection pipelines
- GitHub-based documentation and workflow automation

---

# Project 2: Accident Cause Analysis

## Objective

Analyze accident reports from the power distribution sector and automatically classify causes into structured categories.

---

# NLP Pipeline

## Step 1: Text Normalization

The raw reports contained:
- Krutidev encoded Hindi
- Devanagari script
- Mixed formatting

A custom conversion pipeline transformed:
- Krutidev → Unicode Hindi
- Hindi → English translation

This enabled downstream NLP processing.

---

# Supervised Classification

## Model Used

A prompt-engineering based classification pipeline was implemented using the DeepSeek API.

Features:
- Batch processing
- Automated categorization
- Scalable inference pipeline

---

# Accident Categories

The model classified incidents into six major groups:

- Accidental Contact
- Equipment Failure
- Unauthorized & Illegal Activity
- Unsafe Work Practices
- Weather & External Factors
- Unknown / Other

---

# Sub-Categorization

Each category was further divided into finer subclasses such as:

- Transformer Failure
- Wire Snap Fault
- Domestic Activity Contact
- Unsafe Equipment Handling
- Pole Collapse

---

# Dashboard Engineering

A Streamlit dashboard was developed for:
- Trend analysis
- Filtering
- Interactive visualization
- Circle-wise accident tracking



---

