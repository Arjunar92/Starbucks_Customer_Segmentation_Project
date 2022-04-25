# Udacity Data Science NCapstone Project

## Customer Segmentation Starbucks


## Introduction:

This Project is the final project for the completion of the Udacity Data Science Nanodegree Program in collaboration with Starbucks. This data set contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. This data set contains three files. 


## Project Goal:

The major focus of the project will be to analyze the offer performance across demographic groups and customer segments. Through this project we will be achieving the following:

* Analyze offer performance per demographic group. 
* Analyze offer performance per customer segment. 
* Explore different segmentation techniques and suggest the best suited for the business.
* Implement project using CRISP-DM methodology. 

## CRISP-DM methodology

CRISP-DM stands for Cross-Industry Process for Data Mining. The CRISP-DM methodology provides a structured approach to planning a data mining project.
The CRISP-DM process model has six major phases:

* Business Understanding
* Data Understanding
* Data Preparation/Data Engineering
* Modeling
* Model Validation
* Visualization & Analysis

## I. Business Understanding:

Starbucks is among the largest coffee company based in Seattle, Washington with many coffee house chains globally. Like many other major food and beverage chains, they too have a dedicated mobile app where customers can purchase items, and avail rewards and offers from Starbucks. The data provided for this project is simulated data that mimics customer behavior on the Starbucks rewards mobile app. The objective of this project is to analyze the experimental data and develop insights and recommendations for Starbucks regarding their Offer performance.


## II. Data Understanding:

The first file describes offer characteristics including its duration and difficulty. The second file contains customer demographic data of each customer and when they created an account on the Starbucks rewards mobile application. The third file describes customer purchases and when they received, viewed, and completed an offer.

**portfolio.js
* id (string) - offer id
* offer_type (string) - type of offer ie BOGO, discount, informational
* difficulty (int) - minimum required spend to complete an offer
* reward (int) - reward given for completing an offer
* duration (int) - time for offer to be open, in days
* channels (list of strings)

**profile.json**
* age (int) - age of the customer 
* became_member_on (int) - date when customer created an app account
* gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
* id (str) - customer id
* income (float) - customer's income

**transcript.json**
* event (str) - record description (ie transaction, offer received, offer viewed, etc.)
* person (str) - customer id
* time (int) - time in hours since start of test. The data begins at time t=0
* value - (dict of strings) - either an offer id or transaction amount depending on the record

## III. Data Preparation/Data Engineering
Perform data structuring by converting the data types into an appropriate format that's will be useful for analysis.
(a). Data Cleaing
(b). Feature Engineering
(c). Data Publishing

## Part 1: Analyze Overall Offer Performance

### I. Modeling
### II. Model Evaluation
### III. Visualizatoon and Analysis


## Part 2: Customer Segmentation:

### (A). Customer Segementation using RFM Analysis: 

### I. Modeling
* Method1: RFM Using K-Means
* Method 2: RFM Using ranking

### II. Model Evaluation
* Method 1 VS Method 2
 
### III. Visualizatoon and Analysis
* Visualize Segment wise offer performance and provide insights. 

### (B). Customer Segmentation: Cluster Analysis: 

### I. Modeling
* K-means clustering 
* Hierarchical clustering

### II. Model Evaluation
*  K-means clustering VS Hierarchical clustering

### III. Visualizatoon and Analysis
* Visualize Segment wise offer performance and provide insights. 

## Final Conclusion
