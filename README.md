Kearney-Theft-Detection: Anomaly Detection in Electric Meter Categorization
===========================================================================

This project aims to address the mis-categorization of electric meters for reduced tariff rates, focusing on the Tonk sub-division of Rajasthan.

> **Note on Tariff Rate Order:** The established tariff hierarchy is as follows:Non-Domestic > Industrial > Domestic > Agricultural

I. Identification of Non-Domestic Consumers Mis-categorized as Domestic
-----------------------------------------------------------------------

This phase focuses on identifying commercial entities that are incorrectly billed under a domestic tariff.

*   **Data Acquisition**: Commercial establishment data was systematically acquired using the Google Maps API to create a comprehensive list of known non-domestic entities within the Tonk sub-division.
    
*   **Geospatial Proximity Analysis**: A spatial analysis was conducted by comparing the geographic coordinates of the identified commercial establishments with the locations of domestic metered connections.
    
*   **Anomaly Flagging**: Connections where the Euclidean distance between a registered domestic meter and a known commercial establishment was below a predetermined threshold were flagged as potential cases of tariff mis-categorization.
    

II. Consumption-Based Modelling for Mis-categorization Detection
----------------------------------------------------------------

This section details the methodology for identifying Non-Domestic consumers erroneously categorized as Small Industrial, based on their electricity consumption patterns.

> **Data Note:** 30-40 months of consumption data was available for each connection, spanning the years 2021-2025. The dataset exhibited imbalances, with a higher incidence of null values in more recent years.

### APPROACH

#### 1\. Feature Engineering

The following features were engineered from the time-series consumption data for each connection:

*   **Monthly Average Consumption**: Mean consumption for each of the 12 calendar months (12 features).
    
*   **Annual Average Consumption**: Mean consumption for each year (2021, 2022, 2023, 2024, 2025).
    
*   **Overall Average Consumption**: The global mean consumption across the entire period for each connection.
    
*   **Consumption Volatility**: The standard deviation of monthly consumption.
    

#### 2\. Principal Component Analysis (PCA)

*   **Dimensionality Reduction & Results**:
    
    *   Component 1 explained ~80% of the variance.
        
    *   Component 2 explained ~5% of the variance.
        
*   **Component Interpretation**:
    
    *   **Component 1**: Exhibited nearly uniform positive loadings (~0.2) across all consumption features, representing the overall magnitude of electricity usage.
        
    *   **Component 2**: Showed heavier positive loadings on the '2024' and '2025' annual averages (~0.6), with near-zero loadings on other features.
        
*   **Cluster Analysis & Hypothesis**:
    
    *   When plotted with PC1 on the x-axis and PC2 on the y-axis:
        
        *   **Small Industries** formed a dense, linear cluster almost parallel to the y-axis.
            
        *   **Non-Domestic** connections formed a distinct, diverging cone along a trajectory with a slope of approximately 1.
            
    *   **Conjecture**: Connections classified as "Small Industrial" that deviate significantly from the primary industrial cluster are likely mis-categorized Non-Domestic consumers.
        
*   **Statistical Anomaly Detection**: Outliers were identified as data points located beyond 2.5 standard deviations from the centroid of the Small Industrial cluster. This method flagged ~10 anomalous connections.
    

#### 3\. Isolation Forest

*   **Unsupervised Anomaly Detection**: An Isolation Forest model was trained on the same set of consumption features to identify anomalies independently. While the internal workings are a black box, its results can be used for validation.
    
*   **Result Corroboration**: To strengthen the findings, the anomalies identified by the Isolation Forest were cross-referenced with those flagged by the PCA-based statistical method. A high degree of overlap provides a stronger basis for concluding that a connection is mis-categorized.
#### 4\. Phone Number Matching
