# Python-Reporting-API-Program
Python Program with several API's for updating Google Sheets Reports

This used to be a program that i have created for the company that i have worked with so the reports are automated, hence some file and variable names are related to that.

The program runs from the main.py and opens a GUI with buttons for operations to choose from.

# 📊 Automated API-to-Google Sheets Reporting Pipeline

An automated data integration and reporting pipeline built with Python. This desktop application extracts data from business intelligence and mobile tracking tools via APIs, processes the data, and dynamically updates Google Sheets dashboards. 

It eliminates manual reporting workloads by connecting **Metabase**, **Adjust**, and **Google Sheets** through a user-friendly Tkinter GUI.

## 🚀 Key Features

* **Multi-API Integration:** Extracts real-time business and marketing metrics from [Metabase](https://www.metabase.com/) and [Adjust](https://www.adjust.com/) APIs.
* **Automated Dashboard Updates:** Uses the **Google Sheets API v4** to dynamically locate cells and batch-update weekly and daily reporting spreadsheets.
* **Data Processing:** Utilizes `pandas` and `numpy` for data cleaning, aggregation, and transformation before pushing to spreadsheets.
* **Desktop GUI:** Features a lightweight GUI built with `Tkinter` to trigger different reporting scripts (e.g., Weekly Reports, Active Buyer Reports) with a single click.
* **Secure API Handling:** Manages temporary public link generation and deletion for Metabase to securely extract CSV data.

## 📁 Project Structure

* **`main.py`**: The entry point of the application. Initializes the Tkinter GUI and routes button clicks to the respective reporting modules.
* **`main_weekly.py` & `active_buyer.py`**: Core automation scripts. They manage the logic of fetching data from APIs and mapping them to the correct Google Sheets cells.
* **`metabase_api_weekly.py`**: Handles Metabase authentication, session management, and CSV data extraction.
* **`Adjust_api_weekly.py`**: Connects to the Adjust API to fetch mobile app KPIs (impressions, clicks, installs) across iOS and Android.
* **`config.py` & `config_weekly.py`**: Configuration files storing specific Google Sheets IDs and target ranges.
