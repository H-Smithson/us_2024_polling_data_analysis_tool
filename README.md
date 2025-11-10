# US 2024 Polling Data Analysis Tool

**US 2024 Polling Data Analysis Tool** is a comprehensive data analysis project designed to explore, analyse, and visualise U.S. 2024 election polling data.  
It provides an intuitive, interactive Streamlit dashboard for exploring polling trends, pollster bias, methodology differences, and model-based predictions.  
This project combines **Python**, **data analytics**, **machine learning**, and **AI-assisted insights** to support evidence-based political trend analysis.

---

## Dataset Content
The dataset comes from [Kaggle – 2024 U.S. Election Generic Ballot Polling Data](https://www.kaggle.com/datasets/iamtanmayshukla/2024-u-s-election-generic-ballot-polling-data).  
It contains **608 records** of national-level generic ballot polls conducted between **November 2022 and August 2024**, featuring:
- Pollster names  
- Sample sizes  
- Start and end dates  
- Democratic (`dem`) and Republican (`rep`) support percentages  
- Methodology (phone, online, panel)  
- Pollster rating and numeric grade  

The dataset was cleaned, normalised, and saved as:
`data/clean/generic_ballot_polls_clean.csv`  
A model-ready version, `generic_ballot_polls_dashboard.csv`, was generated for dashboard use.

---

## How to Use This Project

### 🧱 Notebooks
Each notebook represents a key stage in the data analysis process:
| Notebook | Purpose |
|-----------|----------|
| **01_ETL_Pipeline.ipynb** | Loads, cleans, and prepares raw polling data. |
| **02_EDA.ipynb** | Performs exploratory data analysis and visualisation. |
| **03_Feature_Engineering_Modeling.ipynb** | Builds and evaluates machine learning models. |
| **04_Dashboard_Build.ipynb** | Prepares final dashboard dataset and writes Streamlit app. |

To run a notebook:
1. Open it in Jupyter Lab or VS Code.  
2. Run cells sequentially.  
3. Outputs (plots, cleaned CSVs, models) will be saved automatically to `/data/clean/` and `/models/`.

### 💻 Streamlit Dashboard
1. From your project root, install dependencies:
   ```bash
   pip install -r requirements.txt
2. Then, run 
   ```streamlit run dashboard/polling_data_dashboard.py

---

## Business Requirements
The project addresses these key business questions:
1. How do **party support levels** change over time?  
2. Which **pollsters** and **methodologies** show consistent bias?  
3. Does **sample size** affect the reported margin of support?  
4. Can we **predict the Democratic–Republican margin** using machine learning?  
5. How can polling data be visualised in an accessible, interactive dashboard?

---

## Hypothesis and how to validate?
| Hypothesis | Validation Method |
|-------------|------------------|
| 1. Democratic and Republican support move inversely over time. | Line plots and correlation matrix. |
| 2. Online polls show higher variance than phone polls. | Boxplots and standard deviation comparison by methodology. |
| 3. High-rated pollsters report results closer to the overall average. | Compare pollster bias (`margin_bias`) vs `numeric_grade`. |
| 4. Larger sample sizes produce less variability in results. | Scatter plots of `sample_size` vs `margin`. |
| 5. A Random Forest model can predict polling margins more accurately than Linear Regression. | Evaluate models using MSE, MAE, and R² metrics. |

---

## Project Plan
**Steps taken:**
1. **Data Collection & Cleaning (Notebook 01)**  
   - Loaded raw Kaggle dataset, cleaned missing values, standardised dates, normalised methodologies.
2. **Exploratory Data Analysis (Notebook 02)**  
   - Examined distributions, correlations, and trends across pollsters and methods.
3. **Feature Engineering & Modeling (Notebook 03)**  
   - Created new features (margin, rolling averages, encoding), trained Linear Regression and Random Forest models.
4. **Dashboard Development (Notebook 04)**  
   - Built Streamlit dashboard to visualise trends and predictions interactively.

**Data Management:**  
All raw and processed datasets are version-controlled under `/data/`. Missing values handled via imputation or removal; all features were stored in CSVs for reproducibility.

**Research Methodology:**  
An **observational, quantitative** approach using secondary polling data. AI assistance was incorporated for feature ideation and narrative generation.

---

## The rationale to map the business requirements to the Data Visualisations
| Business Requirement | Visualisation Type | Rationale |
|----------------------|--------------------|------------|
| 1. Track party support over time | Line chart with rolling average | Shows fluctuations and trends chronologically |
| 2. Compare distribution of support | Histogram with mean & std lines | Highlights central tendency and variance |
| 3. Pollster bias and count | Bar chart | Identifies polling consistency and lean direction |
| 4. Methodology bias | Grouped bar chart | Compares how methodology affects averages |
| 5. Relationship between sample size and margin | Scatter plot | Tests effect of sample size on margin variability |
| 6. Predictive trend visualisation | Line chart (Predicted vs Actual Margin) | Demonstrates model performance |

---

## Analysis techniques used
- **Descriptive Statistics:** Mean, median, standard deviation, correlation matrix.  
- **Inferential Analysis:** Margin bias across pollsters and methodologies.  
- **Predictive Modeling:** Linear Regression (baseline) and Random Forest (advanced).  
- **Feature Engineering:** Margin, rolling averages, one-hot encoding, scaling.  
- **AI Tools:** Used ChatGPT to suggest feature scaling, encoding, and storytelling summaries.

**Limitations & Alternatives:**  
- Dataset limited to national-level polls (no state data).  
- Future work could include time-series forecasting (ARIMA, Prophet).  
- Rolling averages help mitigate short-term variability.

---

## Ethical considerations
- Dataset is **public and anonymised** — no personal data collected.  
- Discussed **bias and fairness** in methodology comparisons.  
- Acknowledged limitations of predictive modeling in political forecasting.  
- Complies with **GDPR principles** — all data used responsibly and transparently.

---

## Dashboard Design
**Single-page Streamlit Dashboard:**  
Includes widgets for dynamic exploration:

| Element | Description |
|----------|-------------|
| **Date Range Selector** | Filters polls by time period |
| **Party Selection** | Choose which party series to plot |
| **Pollster Filter** | Multi-select for scatter and bias plots |
| **Methodology Filter** | Multi-select to compare online vs phone |
| **Histogram Toggle** | Show/hide mean & std annotations |
| **KPIs** | Total polls, average margin, predicted margin |
| **Plots** | Line charts, histograms, bar charts, scatter plots |

**Communication Design:**  
Visuals are colour-coded, labelled, and use tooltips for clarity.  
Complex data is simplified into accessible summaries and KPIs for non-technical users.

--- 

**Knowledge Gaps & Adaptation:**  
- Overcame initial issues with Streamlit layout using Plotly container width.  
- Learned model serialisation with `joblib` for integration into dashboard.  
- Incorporated AI feedback loops for optimisation and storytelling clarity.

---

## Development Roadmap
**Challenges & Strategies:**
- Cleaning inconsistent methodology strings → created `clean_methodology()` function.  
- Model overfitting → tuned Random Forest parameters and used rolling averages.  
- Dashboard alignment issues → used Plotly layout adjustments.

---

# Conclusions

- Polling trends remain relatively stable, with short-term fluctuations smoothed by rolling averages.

- Online and phone polls display measurable methodological bias.

- Larger sample sizes tend to reduce margin variability.

- The Random Forest model provides stronger predictive accuracy (lower MSE, higher R²) than Linear Regression.

- The interactive dashboard successfully communicates insights to both technical and non-technical audiences through intuitive visuals.

- AI assistance enhanced both feature engineering and storytelling, improving workflow efficiency and interpretability.

# Credits
# Content

- Dataset: Kaggle – 2024 U.S. Election Generic Ballot Polling Data

- Python & Streamlit documentation.

- Plotly and Scikit-learn official examples.
 
- AI suggestions (ChatGPT / Copilot) for feature engineering and narrative clarity.

- Learning materials provided by the code institute.

# Acknowledgements

Special thanks to the Code Institute, mentors, and AI tools that supported ideation, design thinking, and code optimisation throughout this project.
