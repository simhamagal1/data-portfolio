# Flight Delays Analysis (US Flights 2015)

This project analyzes large-scale operational flight data to understand delay patterns and evaluate the feasibility of modeling flight delays using data-driven approaches.

## Project Overview
The analysis is based on a comprehensive dataset of US domestic flights from 2015, containing approximately 5.8 million records and 31 features.  
The project combines exploratory data analysis with unsupervised and supervised learning, under real-world constraints such as scale, sparsity, and feature complexity.

## Data Preparation & Exploration
- Data cleaning and removal of redundant or non-informative features
- Handling missing values and scale limitations
- Feature engineering, including construction of a total delay variable
- One-Hot Encoding of categorical variables (expanding to ~1,300 features)
- Exploratory analysis using descriptive statistics and visualizations

Key observations included strong relationships between departure and arrival delays, as well as structural patterns related to distance, timing, and flight volume.

## Unsupervised Learning
- K-Means clustering with Elbow and Silhouette analysis
- Dimensionality reduction and visualization using PCA, t-SNE, MDS, and Isomap
- Clusters reflected operational characteristics (e.g., distance and air time) rather than delay magnitude

## Supervised Learning
- Regression-based modeling of total delay duration
- Evaluation of linear models and neural networks
- Early identification and prevention of data leakage
- Performance analysis under different regularization and validation setups

## Tech Stack
Python, Pandas, NumPy, scikit-learn, TensorFlow, Jupyter Notebook
