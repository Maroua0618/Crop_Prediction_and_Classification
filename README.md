# 🌾 AI-Driven Crop Prediction and Classification System

## Overview

This project implements a comprehensive AI-driven system for crop prediction and classification that goes beyond simple recommendations. The system analyzes soil conditions, environmental factors, and agricultural parameters to:

- **Predict optimal crops** for specific soil and environmental conditions
- **Recommend minimal-cost agricultural interventions** when soil conditions need improvement
- **Provide cost-benefit optimization** balancing improvement costs against expected yields

### Key Innovation

Unlike traditional crop recommendation systems that only provide predictions, our approach offers **prescriptive analytics** - when soil conditions aren't optimal for any crop, the system employs advanced search algorithms to recommend the least costly agricultural actions (fertilizers, irrigation, organic matter) to enhance soil properties for better crop matching.


## 🎯 Problem Statement

Modern agriculture faces several critical challenges:

- **Agronomic Variability**: Soil properties vary significantly across locations
- **Economic Stakes**: Wrong crop-soil pairings reduce yields and waste resources
- **Decision Complexity**: Farmers must balance multiple competing factors without data-driven support


## 🔬 Technical Approach

### AI Algorithms Implemented

The system employs four distinct AI approaches, each optimized for different scenarios:

| Algorithm | Best Use Case | Strengths | Performance |
|-----------|---------------|-----------|-------------|
| **Constraint Satisfaction Problem (CSP)** | Real-time applications | Fastest execution (0.12-0.71s) | ⭐⭐⭐⭐⭐ |
| **A* Search** | Balanced performance needs | Optimal pathfinding | ⭐⭐⭐⭐ |
| **Greedy Search** | Resource-constrained environments | Simple and fast | ⭐⭐⭐ |
| **Genetic Algorithm** | Complex intervention planning | Adaptive solutions for extreme conditions | ⭐⭐⭐⭐⭐ |

### Core Features

#### 🎯 **Dual-Mode Operation**
- Classification Mode
- Prediction Mode

#### 📊 **Data-Driven Approach**
- Built on [Smart Farming Data 2024 (SF24) – Kaggle](https://www.kaggle.com/datasets/datasetengineer/smart-farming-data-2024-sf24)
- 7 key environmental features selected using Random Forest Feature Importance
  
#### 💰 **Cost-Benefit Optimization**
- Economic modeling of agricultural interventions
- Resource efficiency prioritization
- Risk assessment and mitigation strategies


## 🏗️Technology Stack

**Backend:**
- **Flask**: Web framework for API endpoints and user management
- **SQLite**: Database for user data and prediction history
- **Pandas/NumPy**: Data manipulation and numerical computations

**Frontend:**
- **HTML5/CSS3**: Responsive web interface
- **JavaScript**: Interactive forms and visualizations

**AI/ML:**
- **Custom Algorithms**: CSP, A*, Greedy, Genetic Algorithm implementations
- **Optimization**: Cost-benefit analysis and resource allocation


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
