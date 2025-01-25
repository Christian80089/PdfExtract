
# Project Name: Data Processing and Dashboard

## Overview
This project is designed for processing various data types (such as bank transactions, salary records, light bills, and others) and visualizing them in an interactive dashboard using Streamlit. The backend processes the data, transforms it, and stores it in CSV files. The frontend, built with Streamlit, provides a user interface to visualize and analyze the processed data.

## Backend Overview
The backend consists of the following tasks:
- Processing data from multiple sources: bank transactions, light bills, salary records, etc.
- Transforming the raw data into structured formats using custom functions and transformations.
- Storing the transformed data in CSV files.
- Handling the interactions with external services like Copilot for extracting data from PDF files.

### Key Backend Components:
- **Data Transformers**: Each data type has a corresponding transformer that processes raw data files into clean, structured data (e.g., `IngTransform` for bank transactions, `BerebelTransform` for Berebel records, etc.).
- **Copilot Integration**: Uses Copilot to extract relevant information from unstructured PDF files.
- **Checkpoints**: Tracks which files have already been processed to avoid reprocessing.

## Frontend Overview
The frontend provides an interactive dashboard using **Streamlit** to visualize the processed salary data. The dashboard includes:
- **Salary Dashboard**: Visualizes key metrics like total gross salary, deductions, net salary, and other statistics.
- **Other Charts**: Provides additional charts such as the breakdown of earnings and deductions.

### Key Frontend Features:
- **Date Range Filtering**: Allows users to filter salary data by date range.
- **Company Filtering**: Users can filter data by company.
- **Net Salary Trend**: Displays a bar chart showing the net salary trend over time.
- **Earnings/Deductions Breakdown**: A pie chart showing the distribution of earnings and deductions.

## Requirements

### Backend
- Python 3.7+
- pandas
- plotly
- streamlit
- openai (for Copilot interaction)
- other custom libraries as defined in the project

### Frontend
- Streamlit for the interactive dashboard
- plotly for interactive visualizations

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the required data files in the `resources/input_data` directory for the backend to process.

## Usage

### Backend
To run the backend script for data processing:
```bash
python backend/main.py
```

This will process the CSV and PDF files found in the `resources/input_data` folder, transform the data, and save the results to `resources/output_data`.

### Frontend (Streamlit Dashboard)
To run the frontend and view the interactive dashboard:
```bash
streamlit run frontend/app.py
```

This will start a local Streamlit server where you can explore the salary data using the interactive dashboard.

## Folder Structure

```
├── backend
  ├── external_system
    ├── Airtable.py
    ├── AivenPostgreSqlDb.py
    ├── Copilot.py
    ├── external_resources
      ├── aiven
      ├── google
    ├── Google.py
  ├── main.py
  ├── project_structure_main.py
  ├── resources
    ├── checkpoints
    ├── constants
      ├── bank_transactions
        ├── BankConstants.py
      ├── berebel
        ├── BerebelConstants.py
      ├── common
        ├── Constants.py
      ├── light_bills
        ├── LightBillsConstants.py
      ├── salary
        ├── RelatechConstants.py
    ├── functions
      ├── AirtableFunctions.py
      ├── AivenFunctions.py
      ├── CopilotFunctions.py
      ├── DataFrameFunctions.py
      ├── Functions.py
      ├── GoogleFunctions.py
      ├── PdfFunctions.py
    ├── input_data
      ├── bank_transactions
        ├── deutsche
        ├── ing
      ├── berebel
      ├── light_bills
        ├── enel
        ├── eni
      ├── salary
        └── relatech
    ├── output_data
      ├── bank_transactions
        ├── deutsche
        ├── ing
      ├── berebel
      ├── light_bills
      └── salary
  ├── transformations
    ├── bank_transactions
      ├── DeutscheTransform.py
      ├── IngTransform.py
    ├── berebel
      ├── BerebelTransform.py
    ├── light_bills
      ├── EnelTransform.py
    └── salary
      ├── RelatechTransform.py
├── frontend
  ├── app.py
```

## File Formats

- **CSV Files**: The backend processes CSV files containing various data types like bank transactions, salary records, etc.
- **PDF Files**: The backend can also process PDF files containing unstructured data, extracting relevant information using Copilot.

## Error Handling

The backend includes error handling for cases such as:
- Missing files
- Incorrect data formats
- Unhandled directories or file types

If a file fails to be processed, an error message will be logged, and the file will be skipped.

## Contributing
Feel free to open issues or submit pull requests if you want to contribute. Please ensure that you test any changes before submitting.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
