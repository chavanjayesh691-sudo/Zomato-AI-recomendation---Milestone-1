# Project Context: AI-Powered Restaurant Recommendation System

> Source: [Docs/Problemstatement.txt](Docs/Problemstatement.txt)

## Overview

Build an AI-powered restaurant recommendation service inspired by Zomato. The system intelligently suggests restaurants based on user preferences by combining structured data with a Large Language Model (LLM).

## Objective

Design and implement an application that:

- Takes user preferences (such as location, budget, cuisine, and ratings)
- Uses a real-world dataset of restaurants
- Leverages an LLM to generate personalized, human-like recommendations
- Displays clear and useful results to the user

## System Workflow

### 1. Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:  
  https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
- Extract relevant fields such as restaurant name, location, cuisine, cost, rating, etc.

### 2. User Input

Collect user preferences:

| Preference | Examples |
|---|---|
| Location | indiranagar, bellandur, btm, hsr, whitefield |
| Budget | low, medium, high |
| Cuisine | Italian, Chinese |
| Minimum rating | numeric threshold |
| Additional preferences | family-friendly, quick service |

### 3. Integration Layer

- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason and rank options

### 4. Recommendation Engine

Use the LLM to:

- Rank restaurants
- Provide explanations (why each recommendation fits)
- Optionally summarize choices

### 5. Output Display

Present top recommendations in a user-friendly format:

- Restaurant Name
- Cuisine
- Rating
- Estimated Cost
- AI-generated explanation

## Key Requirements Summary

1. **Data source**: Zomato restaurant dataset on Hugging Face (`ManikaSaini/zomato-restaurant-recommendation`)
2. **User-facing inputs**: location, budget tier, cuisine, minimum rating, optional free-text preferences
3. **Core pipeline**: filter dataset → build LLM prompt → rank and explain → display results
4. **Output fields**: name, cuisine, rating, cost, AI explanation

## External Resources

- **Dataset**: https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
