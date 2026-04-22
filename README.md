# Behavioral Data Analysis

This repository contains a small portfolio project that demonstrates how to analyze behavioral data in Python.  The data used here are **simulated** to avoid sharing any sensitive or proprietary information.  The notebook walks through a typical workflow, from generating synthetic data to performing statistical tests.

## What this project does

The project shows how to:

* Generate a simple behavioral dataset for two experimental conditions (for example, a baseline and an adaptation condition) across multiple participants.
* Inspect and clean the data, including a basic quality check to identify participants who do not meet a minimum number of trials.
* Summarize the data at the participant level and visualize the distributions using bar plots with error bars.
* Perform a paired **t‑test** to compare conditions and a **repeated‑measures ANOVA** to assess within‑subject effects.

## How to run the analysis

1. **Clone the repository** and change into the project directory:

   ```bash
   git clone https://github.com/yourusername/behavioral-data-analysis.git
   cd behavioral-data-analysis
   ```

2. **Create and activate a virtual environment** (recommended but optional):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required Python packages** listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter Notebook** and open `analysis.ipynb`:

   ```bash
   jupyter notebook
   ```

   In your browser, navigate to `analysis.ipynb` to run or inspect the analysis.  Each code cell contains comments in English explaining the purpose of the step.

## Contents

| File | Description |
| --- | --- |
| `README.md` | This document, providing an overview of the project and instructions for running it. |
| `analysis.ipynb` | A Jupyter notebook demonstrating the generation and analysis of simulated behavioral data.  The notebook includes code cells with English variable names and explanatory comments. |
| `requirements.txt` | A list of Python packages required to run the notebook. |

Feel free to adapt this project for your own portfolio, adding more complex analyses or real data once you are comfortable with the workflow.
