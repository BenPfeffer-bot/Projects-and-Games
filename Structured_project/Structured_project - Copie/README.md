# **Data Processing Application**

Welcome to the **Data Processing Application**! This application is designed to provide a user-friendly interface for processing ESMA_SI XML files, trade source data, and generating comprehensive reports. The application is built using Python and leverages a modular structure for maintainability and scalability.

---

## **Table of Contents**

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Launching the Application](#launching-the-application)
  - [Step-by-Step Guide](#step-by-step-guide)
- [GUI Overview](#gui-overview)
- [How It Works](#how-it-works)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## **Features**

- **XML to DataFrame Conversion**: Converts ESMA_SI XML files into a structured Pandas DataFrame for easy data manipulation.
- **Data Processing**: Processes trade source data with ESMA thresholds and performs calculations required for systematic internaliser review.
- **Report Generation**: Generates comprehensive reports summarizing the data processing results.
- **Modular Design**: Organized codebase with separate modules for GUI, data processing, utilities, and configuration.
- **User-Friendly Interface**: Intuitive GUI built with CustomTkinter, making it easy to navigate through different steps.
- **Threaded Operations**: Long-running tasks are executed in separate threads to keep the GUI responsive.

---

## **Prerequisites**

Before running the application, ensure you have the following installed:

- **Python 3.7 or higher**
- **pip** (Python package installer)

---

## **Installation**


1. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Main**

   Select the file *main.py* and press Play button on top right of the screen.
    
---

## **Project Structure**

```
data-processing-app/
├── main.py
├── gui/
│   ├── __init__.py
│   └── app.py
├── data_processing/
│   ├── __init__.py
│   ├── xml_processor.py
│   ├── data_processor.py
│   └── report_generator.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── requirements.txt
└── README.md
```

- **`main.py`**: Entry point of the application.
- **`gui/`**: Contains the GUI application code.
- **`data_processing/`**: Modules responsible for data processing and report generation.
- **`utils/`**: Utility functions used across the application.
- **`config/`**: Configuration settings and hard-coded data.
- **`requirements.txt`**: Lists all Python dependencies.

---

## **Usage**

### **Launching the Application**

To start the application, run:

```bash
python main.py
```

### **Step-by-Step Guide**

1. **Step 1: Convert XML to DataFrame**

   - **Select ESMA_SI XML Folder Path**: Click on the "Browse" button next to "ESMA_SI XML Folder Path" and navigate to the folder containing your XML files.
   - **Convert XML to DataFrame**: Click on the "Convert XML to DataFrame" button. The application will parse all XML files in the folder and convert them into a DataFrame.

2. **Step 2: Data Processing**

   - **Trade_Source Excel File Path**: Click on the "Browse" button and select your `Trade_Source.xlsx` file.
   - **Trade_Source_Scope Excel File Path**: Click on the "Browse" button and select your `Trade_Source_Scope.xlsx` file.
   - **ESMA_Threshold Excel File Path**: Click on the "Browse" button and select your `ESMA_Threshold.xlsx` file.
   - **Output Directory**: Click on the "Browse" button and choose the directory where you want the output files to be saved.
   - **Process Data**: Click on the "Process Data" button. The application will process the data and generate reports. Progress and messages will be displayed in the report text box.

3. **Download YTD Data**

   - After processing is complete, the "Download YTD Data" button will be enabled.
   - Click on it to save the Year-To-Date data as an Excel file to a location of your choice.

---

## **GUI Overview**

![GUI Overview](https://storage.googleapis.com/endurance-apps-liip/media/cache/credit-agricole-2021_no_filter_grid_fs/5c0532f82d40ce5721244112)


- **ESMA_SI XML Folder Path**: Input field to select the folder containing ESMA_SI XML files.
- **Convert XML to DataFrame**: Button to start the XML conversion process.
- **Trade_Source Excel File Path**: Input field to select the `Trade_Source.xlsx` file i.e. file received from BO.
- **Trade_Source_Scope Excel File Path**: Input field to select the `Trade_Source_Scope.xlsx` file same here.
- **ESMA_Threshold Excel File Path**: Input field to select the `ESMA_Threshold.xlsx` file.
- **Output Directory**: Input field to select the directory where output files will be saved.
- **Process Data**: Button to start data processing.
- **Report Text Box**: Displays progress messages and reports.
- **Download YTD Data**: Button to download the processed Year-To-Date data.

---

## **How It Works**

1. **XML Processing**

   - The application uses the `XMLProcessor` class to parse all XML files in the specified folder.
   - It extracts relevant data and compiles it into a Pandas DataFrame for further processing.

2. **Data Processing**

   - The `DataProcessor` class handles the core data processing logic.
   - It reads the trade source files and the ESMA threshold file.
   - Adds necessary columns and computes values required for the systematic internaliser review.

3. **Report Generation**

   - The `ReportGenerator` class saves the processed data to Excel files.
   - Generates a textual report summarizing the results, including statistics and key findings.

4. **Utilities and Helpers**

   - Utility functions in `utils/helpers.py` assist with common tasks like determining periods based on dates and updating GUI elements.

---

## **Logging**

- The application uses the `logging` module to log informational messages and errors.
- Logs are displayed in the report text box within the GUI for real-time feedback.
- Errors are also shown via message boxes to alert the user immediately.


---

## **Contact**

- **Author**: Ben Pfeffer

Feel free to reach out if you have any questions or need assistance with the application.

---

**Disclaimer**: This application is provided "as is" without warranty of any kind. Use it at your own risk.