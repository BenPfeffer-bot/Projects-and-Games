# Import necessary libraries
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import logging
from io import StringIO
import threading

from datetime import *


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------------------------
# Define the Main Application Class
# ---------------------------------------

class DataProcessingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.title("Data Processing Application")
        self.geometry("800x750")

        # Initialize variables to store file paths
        self.esma_si_xml_folder = tk.StringVar()
        self.trade_source_path = tk.StringVar()
        self.trade_source_scope_path = tk.StringVar()
        self.esma_threshold_path = tk.StringVar()
        self.output_directory = tk.StringVar()

        # Initialize variable to store processed ESMA_SI data
        self.esma_si_df = None

        # Store processed data for downloading
        self.processed_trade_source = None
        self.processed_trade_source_scope = None

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the inputs
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20)

        # Step 1: ESMA_SI XML Folder
        step1_label = ctk.CTkLabel(input_frame, text="Step 1: Convert XML to JSON")
        step1_label.grid(row=0, column=0, columnspan=3, pady=10)

        esma_si_label = ctk.CTkLabel(input_frame, text="ESMA_SI XML Folder Path:")
        esma_si_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        esma_si_entry = ctk.CTkEntry(input_frame, textvariable=self.esma_si_xml_folder, width=400)
        esma_si_entry.grid(row=1, column=1, padx=10, pady=5)
        esma_si_button = ctk.CTkButton(input_frame, text="Browse", command=self.browse_esma_si_xml_folder)
        esma_si_button.grid(row=1, column=2, padx=10, pady=5)

        convert_button = ctk.CTkButton(input_frame, text="Convert XML to JSON", command=self.convert_xml_to_json)
        convert_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Step 2: Data Processing
        step2_label = ctk.CTkLabel(input_frame, text="Step 2: Data Processing")
        step2_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Trade_Source File
        trade_source_label = ctk.CTkLabel(input_frame, text="Trade_Source Excel File Path:")
        trade_source_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        trade_source_entry = ctk.CTkEntry(input_frame, textvariable=self.trade_source_path, width=400)
        trade_source_entry.grid(row=4, column=1, padx=10, pady=5)
        trade_source_button = ctk.CTkButton(input_frame, text="Browse", command=self.browse_trade_source)
        trade_source_button.grid(row=4, column=2, padx=10, pady=5)

        # Trade_Source_Scope File
        trade_source_scope_label = ctk.CTkLabel(input_frame, text="Trade_Source_Scope Excel File Path:")
        trade_source_scope_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        trade_source_scope_entry = ctk.CTkEntry(input_frame, textvariable=self.trade_source_scope_path, width=400)
        trade_source_scope_entry.grid(row=5, column=1, padx=10, pady=5)
        trade_source_scope_button = ctk.CTkButton(input_frame, text="Browse", command=self.browse_trade_source_scope)
        trade_source_scope_button.grid(row=5, column=2, padx=10, pady=5)

        # ESMA_Threshold File
        esma_threshold_label = ctk.CTkLabel(input_frame, text="ESMA_Threshold Excel File Path:")
        esma_threshold_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        esma_threshold_entry = ctk.CTkEntry(input_frame, textvariable=self.esma_threshold_path, width=400)
        esma_threshold_entry.grid(row=6, column=1, padx=10, pady=5)
        esma_threshold_button = ctk.CTkButton(input_frame, text="Browse", command=self.browse_esma_threshold)
        esma_threshold_button.grid(row=6, column=2, padx=10, pady=5)

        # Output Directory
        output_dir_label = ctk.CTkLabel(input_frame, text="Output Directory:")
        output_dir_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        output_dir_entry = ctk.CTkEntry(input_frame, textvariable=self.output_directory, width=400)
        output_dir_entry.grid(row=7, column=1, padx=10, pady=5)
        output_dir_button = ctk.CTkButton(input_frame, text="Browse", command=self.browse_output_directory)
        output_dir_button.grid(row=7, column=2, padx=10, pady=5)

        # Process Button
        self.process_button = ctk.CTkButton(self, text="Process Data", command=self.process_data)
        self.process_button.pack(pady=20)
        # process_button = ctk.CTkButton(self, text="Process Data", command=self.process_data)
        # process_button.pack(pady=20)

        # Report Text Box
        self.report_text = ctk.CTkTextbox(self, width=760, height=200)
        self.report_text.pack(pady=10)

        # Download Button
        self.download_button = ctk.CTkButton(self, text="Download YTD Data", command=self.download_ytd_data)
        self.download_button.pack(pady=10)
        self.download_button.configure(state='disabled')  # Disable until data is processed

    # ---------------------------------------
    # Functions to Browse Files and Directories
    # ---------------------------------------

    def browse_esma_si_xml_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.esma_si_xml_folder.set(directory)

    def browse_trade_source(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            self.trade_source_path.set(filepath)

    def browse_trade_source_scope(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            self.trade_source_scope_path.set(filepath)

    def browse_esma_threshold(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            self.esma_threshold_path.set(filepath)

    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    # ---------------------------------------
    # Step 1: Convert XML Files to JSON and Create DataFrame
    # ---------------------------------------

    def convert_xml_to_json(self):
        folder_path = self.esma_si_xml_folder.get()

        if not folder_path:
            messagebox.showerror("Error", "Please provide the XML folder path.")
            return

        # Run in a separate thread to prevent GUI freezing
        threading.Thread(target=self.thread_convert_xml_to_json, args=(folder_path,)).start()

    def thread_convert_xml_to_json(self, folder_path):
        try:
            logging.info("Starting XML to JSON conversion.")
            self.update_report("Starting XML to JSON conversion.\n")
            # Convert XML files to JSON and create DataFrame
            self.esma_si_df = self.convert_esma_si_xml_folder_to_dataframe(folder_path)
            messagebox.showinfo("Success", "XML files converted to DataFrame successfully.")
            logging.info("XML files converted to DataFrame successfully.")
            self.update_report("XML files converted to DataFrame successfully.\n")

            # Optionally, you can save the combined data to a JSON or CSV file
            # For example, save to CSV
            output_dir = self.output_directory.get() or folder_path
            esma_si_output = os.path.join(output_dir, "esma_si_data.csv")
            self.esma_si_df.to_csv(esma_si_output, index=False)
            messagebox.showinfo("Success", f"ESMA_SI data saved to {esma_si_output}")
            logging.info(f"ESMA_SI data saved to {esma_si_output}.")
            self.update_report(f"ESMA_SI data saved to {esma_si_output}.\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during XML to JSON conversion:\n{str(e)}")
            logging.error(f"An error occurred during XML to JSON conversion: {e}")
            self.update_report(f"Error: {e}\n")

    # Function to Convert ESMA_SI XML Files in a Folder to DataFrame
    def convert_esma_si_xml_folder_to_dataframe(self, folder_path):
        all_data = []

        # List all XML files in the folder
        xml_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xml')]

        if not xml_files:
            raise FileNotFoundError("No XML files found in the selected folder.")

        for xml_file_path in xml_files:
            try:
                logging.info(f"Processing XML file: {xml_file_path}")
                # Parse the XML file
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Extract data from XML
                xml_data = self.extract_xml_data(root)

                # Extract the NonEqtyTrnsprncyData list
                try:
                    payload = xml_data.get('Pyld') or xml_data.get('payload')
                    document = payload.get('Document') or payload.get('document')
                    report_results = document.get('FinInstrmRptgNonEqtyTradgActvtyRslt') or document.get('finInstrmRptgNonEqtyTradgActvtyRslt')
                    non_equity_data_list = report_results.get('NonEqtyTrnsprncyData') or report_results.get('nonEqtyTrnsprncyData')
                except KeyError:
                    # Handle cases where the structure is different
                    continue

                # Prepare data for DataFrame
                for item in non_equity_data_list:
                    extracted_item = self.extract_item_data(item)
                    all_data.append(extracted_item)

            except FileNotFoundError as e:
                logging.error(f"The file {xml_file_path} does not exist.")
                raise FileNotFoundError(f"The file {xml_file_path} does not exist.")
            except ParseError as e:
                logging.error(f"Invalid XML format in {xml_file_path}. {e}")
                raise ParseError(f"Invalid XML format in {xml_file_path}. {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred during XML parsing of {xml_file_path}: {e}")
                raise Exception(f"An unexpected error occurred during XML parsing of {xml_file_path}: {e}")

        # Create DataFrame
        esma_si_df = pd.DataFrame(all_data)

        # Return the DataFrame
        return esma_si_df

    def extract_xml_data(self, root):
        """
        Recursively extract data from XML elements and return a nested dictionary.
        """
        data = {}
        for child in root:
            tag = child.tag.split('}')[-1]  # Remove namespace
            if len(child) == 0:
                data[tag] = child.text
            else:
                child_data = self.extract_xml_data(child)
                if tag in data:
                    if not isinstance(data[tag], list):
                        data[tag] = [data[tag]]
                    data[tag].append(child_data)
                else:
                    data[tag] = child_data
        return data

    def extract_item_data(self, item):
        """
        Extracts relevant data from a NonEqtyTrnsprncyData item.
        """
        extracted_item = {}

        # Extract ISIN
        id_info = item.get('Id', {})
        isin_info = id_info.get('ISINAndSubClss', {})
        extracted_item['ISIN'] = isin_info.get('ISIN', '')

        # Extract Calculation From Date and To Date
        rptg_prd = item.get('RptgPrd', {})
        frdt_todt = rptg_prd.get('FrDtToDt', {})
        extracted_item['Calculation From Date'] = frdt_todt.get('FrDt', '')
        extracted_item['Calculation To Date'] = frdt_todt.get('ToDt', '')

        # Extract Total number of transactions and Total turnover
        sttstcs = item.get('Sttstcs', {})
        extracted_item['Total number of transactions executed in the EU'] = int(sttstcs.get('TtlNbOfTxsExctd', 0))
        extracted_item['Total turnover executed in the EU'] = float(sttstcs.get('TtlVolOfTxsExctd', 0.0))

        return extracted_item

    # ---------------------------------------
    # Step 2: Function to Process Data
    # ---------------------------------------
    
    def validate_inputs(self):
        if not self.esma_si_xml_folder.get():
            messagebox.showerror("Error", "Please provide the ESMA_SI XML Folder Path.")
            return False
        if not self.trade_source_path.get():
            messagebox.showerror("Error", "Please provide the Trade_Source Excel File Path.")
            return False
        if not self.trade_source_scope_path.get():
            messagebox.showerror("Error", "Please provide the Trade_Source_Scope Excel File Path.")
            return False
        if not self.esma_threshold_path.get():
            messagebox.showerror("Error", "Please provide the ESMA_Threshold Excel File Path.")
            return False
        if not self.output_directory.get():
            messagebox.showerror("Error", "Please provide the Output Directory.")
            return False
        return True

    # Then in your process_data method:
    def process_data(self):
        if not self.validate_inputs():
            return
        # Clear the report text box
        self.report_text.delete("1.0", tk.END)

        # Get the file paths from the input fields
        trade_source_file = self.trade_source_path.get()
        trade_source_scope_file = self.trade_source_scope_path.get()
        esma_threshold_file = self.esma_threshold_path.get()
        output_dir = self.output_directory.get()

        # Validate file paths
        if not all([trade_source_file, trade_source_scope_file, esma_threshold_file, output_dir]):
            messagebox.showerror("Error", "Please provide all the required file paths and output directory.")
            return

        if self.esma_si_df is None or self.esma_si_df.empty:
            messagebox.showerror("Error", "Please complete Step 1: Convert XML to JSON before proceeding.")
            return

        # Disable the process button while processing
        self.process_button.configure(state='disabled')

        # Run in a separate thread to prevent GUI freezing
        threading.Thread(target=self.thread_process_data, args=(
            trade_source_file, trade_source_scope_file, esma_threshold_file, output_dir)).start()


    def thread_process_data(self, trade_source_file, trade_source_scope_file, esma_threshold_file, output_dir):
        try:
            logging.info("Starting data processing.")
            self.update_report("Starting data processing...\n")
            # Load ESMA_Threshold data
            esma_threshold = pd.read_excel(esma_threshold_file,header=4)
            logging.info("Loaded ESMA_Threshold data.")
            self.update_report("Loaded ESMA_Threshold data.\n")

            # Load Trade_Source and Trade_Source_Scope data
            trade_source = pd.read_excel(trade_source_file)
            trade_source_scope = pd.read_excel(trade_source_scope_file)
            logging.info("Loaded Trade_Source and Trade_Source_Scope data.")
            self.update_report("Loaded Trade_Source and Trade_Source_Scope data.\n")

            # Process the data
            report = self.run_data_processing(self.esma_si_df, esma_threshold, trade_source, trade_source_scope, output_dir)

            # Display the report
            self.update_report(report)

            # Enable the download button
            self.after(0, lambda: self.download_button.configure(state='normal'))

            messagebox.showinfo("Success", "Data processing completed successfully.")
            logging.info("Data processing completed successfully.")
        except Exception as e:
            error_message = f"An error occurred during data processing:\n{str(e)}"
            messagebox.showerror("Error", error_message)
            logging.error(error_message)
            self.update_report(f"Error: {e}\n")
        finally:
            # Always enable the process button after processing is done (success or failure)
            self.after(0, lambda: self.process_button.configure(state='normal'))


    # ---------------------------------------
    # Function to Run Data Processing Logic
    # ---------------------------------------

    def run_data_processing(self, esma_si, esma_threshold, trade_source, trade_source_scope, output_dir):
        # The data processing logic as per your requirements goes here

        # For brevity, I'll summarize the steps and include key parts

        # 1. Process Periods Data
        # No need to pre-calculate periods, as we're determining them dynamically now

        # 2. Add 'Period' Column to esma_si
        esma_si = self.add_period_to_esma_si(esma_si)

        # 3. Process Hard-Coded Data
        hard_coded_df = self.process_hard_coded_data()
        print("Columns in hard_coded_df:", hard_coded_df.columns.tolist())


        print("Columns in trade_source_scope before adding columns:", trade_source_scope.columns.tolist())
        

        # 4. Add Required Columns to Trade Data
        trade_source, trade_source_scope = self.add_columns_to_trade_data(trade_source, trade_source_scope, hard_coded_df)
        print("Columns in trade_source_scope:", trade_source_scope.columns.tolist())

        # 5. Add 'Period' Column to trade_source and trade_source_scope
        trade_source['Period'] = trade_source['M_TRN_DATE'].apply(self.determine_period)
        trade_source_scope['Period'] = trade_source_scope['M_TRN_DATE'].apply(self.determine_period)

        # Define all_periods
        all_periods = sorted(set(
            trade_source['Period'].dropna().unique().tolist() + 
            trade_source_scope['Period'].dropna().unique().tolist() + 
            esma_si['Period'].dropna().unique().tolist()
        ), key=lambda x: int(x[1:]))

        # Remove rows where 'Period' is None (dates not falling into any defined period)
        trade_source = trade_source.dropna(subset=['Period'])
        trade_source_scope = trade_source_scope.dropna(subset=['Period'])

        # 6. Perform F&S Review by ISIN
        result_df = self.perform_fs_review(trade_source, trade_source_scope, esma_si, all_periods)

        # Create F&S Review by Issuer
        issuer_review = self.create_fs_review_by_issuer(trade_source_scope, hard_coded_df)

        for period in all_periods:
            issuer_review = self.calculate_si_score(result_df, issuer_review, period)

        # 7. Save the Processed Data
        self.save_processed_data(trade_source, trade_source_scope, result_df, issuer_review, output_dir)

        # 8. Generate the Report
        report = self.generate_report(trade_source, trade_source_scope, result_df, issuer_review, output_dir, all_periods)

        return report

    # def process_periods_data(self):
    #     """
    #     Processes the periods data and returns a DataFrame with start and end dates.
    #     """
    #     # Define the assignment table as a DataFrame
    #     periods = pd.DataFrame({
    #         'Calculation From Date': ['01/01/2020', '01/04/2020', '01/07/2020', '01/10/2020', '01/01/2021',
    #                                   '01/04/2021', '01/07/2021', '01/10/2021', '01/01/2022', '01/04/2022',
    #                                   '01/07/2022', '01/01/2023', '01/03/2023', '01/10/2023', '01/01/2024', '01/03/2024'],
    #         'Calculation To Date': ['30/06/2020', '30/09/2020', '31/12/2020', '31/03/2021', '30/06/2021',
    #                                 '30/09/2021', '31/12/2021', '31/03/2022', '30/06/2022', '30/09/2022',
    #                                 '31/12/2022', '30/06/2023', '30/09/2023', '31/12/2023', '30/06/2024', '30/09/2024'],
    #         'Period': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16']
    #     })

    #     # Convert date strings to datetime objects
    #     def parse_date(date_str):
    #         if date_str == '-':
    #             return pd.NaT
    #         else:
    #             return pd.to_datetime(date_str, format='%d/%m/%Y', errors='coerce')

    #     periods['Start Date'] = periods['Calculation From Date'].apply(parse_date)
    #     periods['End Date'] = periods['Calculation To Date'].apply(parse_date)

    #     # Drop unnecessary columns
    #     periods_with_dates = periods[['Period', 'Start Date', 'End Date']].dropna(subset=['Start Date', 'End Date']).copy()

    #   return periods_with_dates

    def determine_period(self, input_date):
        # Handle NaT values
        if pd.isna(input_date):
            return None

        # Convert input_date to date object if it's a string
        if isinstance(input_date, str):
            try:
                input_date = datetime.strptime(input_date, "%d/%m/%Y").date()
            except ValueError:
                return None  # Return None if the date string is invalid
        elif isinstance(input_date, datetime):
            input_date = input_date.date()
        elif not isinstance(input_date, date):
            return None  # Return None for any other unexpected type
        
        # Define the base date (start of P1)
        base_date = date(2020, 1, 1)
        
        # Calculate the number of days since the base date
        days_since_base = (input_date - base_date).days
        
        # Handle dates before the base date
        if days_since_base < 0:
            return None  # or you could return a special period for pre-2020 dates
        
        # Calculate the number of complete 2-year cycles
        two_year_cycles = days_since_base // 730  # 730 days in 2 years (ignoring leap years for simplicity)
        
        # Calculate the remaining days within the current 2-year cycle
        days_in_cycle = days_since_base % 730
        
        # Determine the period within the 2-year cycle
        if days_in_cycle < 181:  # First 6 months (181 days)
            period_in_cycle = 1
        elif days_in_cycle < 273:  # Next 3 months (92 days)
            period_in_cycle = 2
        elif days_in_cycle < 365:  # Next 3 months (92 days)
            period_in_cycle = 3
        elif days_in_cycle < 456:  # Next 3 months (91 days)
            period_in_cycle = 4
        elif days_in_cycle < 547:  # Next 3 months (91 days)
            period_in_cycle = 5
        elif days_in_cycle < 638:  # Next 3 months (91 days)
            period_in_cycle = 6
        else:  # Last 3 months (92 days)
            period_in_cycle = 7
        
        # Calculate the final period number
        period_number = two_year_cycles * 7 + period_in_cycle
        
        return f"P{period_number}"



    def add_period_to_esma_si(self, esma_si):
        """
        Adds the 'Period' column to the esma_si DataFrame based on calculation dates.
        """
        esma_si['Calculation From Date'] = pd.to_datetime(esma_si['Calculation From Date'], errors='coerce')
        esma_si['Period'] = esma_si['Calculation From Date'].apply(self.determine_period)

        logging.info("Added 'Period' column to esma_si DataFrame.")
        self.update_report("Added 'Period' column to esma_si DataFrame.\n")

        return esma_si

    def process_hard_coded_data(self):
        """
        Processes the hard-coded data and returns a DataFrame.
        """
        # Hard-coded data as a string (update with your full data)
        hard_coded_data = """
IssuerCode_1,IssuerCode_2,MTS Market Maker (MM) exemption,AMF exemption
RAVIN,,No,Yes
RBBX,,Yes,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
EUROPFA,,No,Yes
BEILX,,No,Yes
MEUROSTA,,No,Yes
CEEBX,,No,Yes
FINLAN1,,Yes,No
TREPUB,CADES,Yes,No
RFABL,FMSMANA,Yes,No
,,No,No
,,No,No
,,No,No
IRELAND,,No,Yes
TRESORIT,,Yes,No
,,No,No
,,No,No
,,No,No
DUCHLUXZ,,No,No
,,No,No
DSTALHA,,No,Yes
,,No,No
,,No,No
PORTUGAL,,Yes,No
,,No,No
RSLOVAQ,,No,No
REPSLOV,,Yes,No
ESPAGNE,,Yes,No
KSWEDEN,,No,No
LABERLIN,,No,No
LDHESSE,,No,No
,,No,No
,,No,No
LANDBADE,,No,No
,,No,No
SCHLES,,No,No
,,No,No
LANDNWES,,No,No
,,No,No
,,No,No
,,No,No
BREMEN,,No,No
,,No,No
,,No,No
,,No,No
FLEMISC,,No,No
WALLONN,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
,,No,No
"""


        hard_coded_df = pd.read_csv(StringIO(hard_coded_data), sep=',', header=0)
        hard_coded_df.fillna('', inplace=True)

        # Ensure column names are correct
        hard_coded_df = hard_coded_df.rename(columns={
            'MTS Market Maker (MM) exemption': 'MTS MM Exempt',
            'AMF exemption': 'AMF exemption'
        })

        # Add 'SSR in Scope' column if it doesn't exist
        if 'SSR in Scope' not in hard_coded_df.columns:
            hard_coded_df['SSR in Scope'] = hard_coded_df['IssuerCode_1'].apply(lambda x: 'Yes' if x else 'No')

        logging.info("Processed hard-coded data.")
        self.update_report("Processed hard-coded data.\n")

        return hard_coded_df

    

    def add_columns_to_trade_data(self, trade_source, trade_source_scope, hard_coded_df):
        """
        Adds required columns to the trade data based on the hard-coded mappings.
        """
        # Create mappings
        mts_mm_exempt_mapping = {}
        amf_exempt_mapping = {}
        for idx, row in hard_coded_df.iterrows():
            issuer_codes = []
            if row['IssuerCode_1']:
                issuer_codes.append(row['IssuerCode_1'].strip().upper())
            if row['IssuerCode_2']:
                issuer_codes.append(row['IssuerCode_2'].strip().upper())
            for issuer_code in issuer_codes:
                mts_mm_exempt_mapping[issuer_code] = row['MTS MM Exempt']
                amf_exempt_mapping[issuer_code] = row['AMF exemption']

        # Remove Rows Where M_SPLIT_INI == 0
        trade_source = trade_source[trade_source['M_SPLIT_INI'] != 0]
        trade_source_scope = trade_source_scope[trade_source_scope['M_SPLIT_INI'] != 0]

        # Add Required Columns
        trade_source = self.add_required_columns(trade_source, mts_mm_exempt_mapping, amf_exempt_mapping)
        trade_source_scope = self.add_required_columns(trade_source_scope, mts_mm_exempt_mapping, amf_exempt_mapping)

        # Merge with hard-coded data
        trade_source_scope = trade_source_scope.merge(
        hard_coded_df[['IssuerCode_1', 'MTS MM Exempt', 'AMF exemption', 'SSR in Scope']],
        left_on='ISSUER',
        right_on='IssuerCode_1',
        how='left'
        )

        logging.info("Added required columns to trade data.")
        self.update_report("Added required columns to trade data.\n")

        return trade_source, trade_source_scope

    def add_required_columns(self, df, mts_mm_exempt_mapping, amf_exempt_mapping):
        """
        Adds required columns to the DataFrame based on mappings.
        """
        # Ensure we're working on a copy to prevent SettingWithCopyWarning
        df = df.copy()

        # Standardize 'ISSUER' column
        df['ISSUER'] = df['ISSUER'].astype(str).str.strip().str.upper()

        issuer_codes_set = set(mts_mm_exempt_mapping.keys()).union(set(amf_exempt_mapping.keys()))

        # Add 'SSR in Scope'
        df['SSR in Scope'] = df['ISSUER'].apply(
            lambda x: 'Yes' if x in issuer_codes_set else 'No'
        )

        # Add 'MTS MM Exempt' and 'AMF exemption'
        df['MTS MM Exempt'] = df['ISSUER'].apply(
            lambda x: mts_mm_exempt_mapping.get(x, 'No')
        )

        df['AMF exemption'] = df['ISSUER'].apply(
            lambda x: amf_exempt_mapping.get(x, 'No')
        )

        # Add 'SSR MM Review in scope'
        df['SSR MM Review in scope'] = df.apply(
            lambda row: 'Yes' if row['SSR in Scope'] == 'Yes' and row['MTS MM Exempt'] == 'No' else 'No',
            axis=1
        )

        # Add 'Auction order' column
        df['Auction order'] = df['COUNTERPART'].apply(
            lambda x: 'Order' if str(x) == '70627' else '-'
        )

        return df


    def add_control_columns(self, df):
        """
        Adds control columns for each period to the DataFrame.
        """
        # Ensure 'M_TRN_DATE' is in datetime format
        df['M_TRN_DATE'] = pd.to_datetime(df['M_TRN_DATE'], errors='coerce')

        # Get unique periods from the data
        unique_periods = df['M_TRN_DATE'].apply(lambda x: self.determine_period(x)).dropna().unique()

        # Add control columns
        for period in unique_periods:
            control_column = f'Period_{period}_Control'
            df[control_column] = df['M_TRN_DATE'].apply(
                lambda x: 'Yes' if self.determine_period(x) == period else 'No'
            )

        return df
    
    # @staticmethod
    # def clean_isin(isin):
    #     return str(isin).strip().upper()  

    def perform_fs_review(self, trade_source, trade_source_scope, esma_si, all_periods):
        """
        Performs the F&S review by ISIN and returns the result DataFrame.
        """
        try:
            # Ensure 'Period' column exists in trade_source
            trade_source['Period'] = trade_source['M_TRN_DATE'].apply(self.determine_period)

            # def clean_isin(isin):
            #     return str(isin).strip().upper()

            # # In the perform_fs_review function, before filtering trade_source:
            # trade_source['ISIN'] = trade_source['ISIN'].apply(clean_isin)
            # esma_si['ISIN'] = esma_si['ISIN'].apply(clean_isin)



            # Then proceed with filtering
            trade_source_filtered = trade_source[trade_source['SSR MM Review in scope'] == 'Yes']

            # Clean ISINs in trade_source filtered
            trade_source_filtered['ISIN'] = trade_source_filtered['ISIN'].astype(str).str.strip().str.upper()

            # Clean ISINs in esma_si
            esma_si['ISIN'] = esma_si['ISIN'].astype(str).str.strip().str.upper()

            # Group by 'ISIN' and 'Period' to count CA-CIB trades
            cacib_trades = trade_source_filtered.groupby(['ISIN', 'Period']).size().reset_index(name='CA-CIB nb of trades')

            # Check for duplicates
            duplicates = cacib_trades.duplicated(subset=['ISIN', 'Period'])
            if duplicates.any():
                logging.warning("Duplicates found in cacib_trades. Aggregating data.")
                self.update_report("Duplicates found in cacib_trades. Aggregating data.\n")

            # Create cacib_pivot
            cacib_pivot = cacib_trades.pivot_table(index='ISIN', columns='Period', values='CA-CIB nb of trades', aggfunc='sum', fill_value=0)
            cacib_pivot.columns = [f'{col} CA-CIB nb of trades' for col in cacib_pivot.columns]
            cacib_pivot.reset_index(inplace=True)

            # Process ESMA_SI data
            esma_si['Total number of transactions executed in the EU'] = pd.to_numeric(esma_si['Total number of transactions executed in the EU'], errors='coerce').fillna(0).astype(int)
            esma_trades = esma_si[['ISIN', 'Period', 'Total number of transactions executed in the EU']].copy()
            esma_trades.rename(columns={'Total number of transactions executed in the EU': 'ESMA nb of trades'}, inplace=True)
            esma_trades['2.50% x ESMA nb of trades'] = esma_trades['ESMA nb of trades'] * 0.025

            # Check for duplicates in esma_trades
            duplicates = esma_trades.duplicated(subset=['ISIN', 'Period'])
            if duplicates.any():
                logging.warning("Duplicates found in esma_trades. Aggregating data.")
                self.update_report("Duplicates found in esma_trades. Aggregating data.\n")

            # Pivot esma_trades using pivot_table
            esma_pivot = esma_trades.pivot_table(index='ISIN', columns='Period', values='2.50% x ESMA nb of trades', aggfunc='sum', fill_value=0)
            esma_pivot.columns = [f'{col} 2.50%xESMA nb of trades' for col in esma_pivot.columns]
            esma_pivot.reset_index(inplace=True)

            # Merge data
            isin_info = trade_source_filtered.groupby('ISIN').agg({
                'ISSUER': 'first',
                'ISSUER_FULLNAME': 'first'
            }).reset_index()

            result_df = isin_info.merge(cacib_pivot, on='ISIN', how='left').merge(esma_pivot, on='ISIN', how='left')
            result_df.fillna(0, inplace=True)

            # Get all unique periods processed
            all_periods = sorted(set(trade_source['Period'].dropna().unique()), key=lambda x: int(x[1:]))

            logging.info(f"Processed Periods: {', '.join(all_periods)}")
            self.update_report(f"Processed Periods: {', '.join(all_periods)}\n")

            # Add Auction columns
            for period in all_periods:
                result_df[f'{period} Auction'] = result_df['ISIN'].apply(
                    lambda isin: self.count_auctions(trade_source, isin, period)
                )

            # Add SI columns
            for period in all_periods:
                result_df[f'{period} SI'] = result_df.apply(
                    lambda row: self.calculate_si(row, period),
                    axis=1
                )

            # Build new column order
            columns_order = ['ISIN', 'ISSUER', 'ISSUER_FULLNAME']
            columns_order += [f'{period} CA-CIB nb of trades' for period in all_periods]
            columns_order += [f'{period} 2.50%xESMA nb of trades' for period in all_periods]
            columns_order += [f'{period} Auction' for period in all_periods]
            columns_order += [f'{period} SI' for period in all_periods]

            # Ensure all periods are included in the result DataFrame
            for period in all_periods:
                for col_prefix in ['CA-CIB nb of trades', '2.50%xESMA nb of trades', 'Auction', 'SI']:
                    col_name = f'{period} {col_prefix}'
                    if col_name not in result_df.columns:
                        result_df[col_name] = 0

            # Reorder the result DataFrame
            result_df = result_df.reindex(columns=columns_order, fill_value=0)

            logging.info("Performed F&S review by ISIN.")
            self.update_report("Performed F&S review by ISIN.\n")

            return result_df

        except KeyError as e:
            logging.error(f"KeyError in perform_fs_review: {e}")
            self.update_report(f"Error: Missing column - {e}\n")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in perform_fs_review: {e}")
            self.update_report(f"Unexpected error: {e}\n")
            raise


    # def get_period(self, date, periods_with_dates):
    #     """
    #     Maps a date to a period.
    #     """
    #     if pd.isna(date):
    #         return None
    #     for _, row in periods_with_dates.iterrows():
    #         start_date = row['Start Date']
    #         end_date = row['End Date']
    #         period = row['Period']
    #         if pd.isna(start_date) or pd.isna(end_date):
    #             continue
    #         if start_date <= date <= end_date:
    #             return period
    #     return None

    def count_auctions(self, trade_source, isin, period):
        """
        Counts the number of auctions for a given ISIN and period.
        """
        return ((trade_source['ISIN'] == isin) & 
                (trade_source['Auction order'] == 'Order') & 
                (trade_source['Period'] == period)).sum()

    def calculate_si_score(self, result_df, issuer_review, period):
        """
        Calculates the SI Score for a given period.
        """
        if f'{period} SI' not in result_df.columns:
            return issuer_review

        si_scores = result_df.groupby('ISSUER').apply(
            lambda x: (x[f'{period} SI'] == 1).sum() if 'SSR MM Review in scope' in x.columns and x['SSR MM Review in scope'].iloc[0] == 'Yes' else 0
        ).reset_index(name=f'{period} SI Score')
        
        return issuer_review.merge(si_scores, on='ISSUER', how='left')

    
    def create_fs_review_by_issuer(self, trade_source_scope, hard_coded_df):
        """
        Creates the F&S Review by Issuer DataFrame.
        """
        # Get unique issuers from trade_source_scope
        issuer_info = trade_source_scope[['ISSUER', 'ISSUER_FULLNAME']].drop_duplicates()

        # Print column names for debugging
        print("Columns in issuer_info:", issuer_info.columns.tolist())
        print("Columns in hard_coded_df:", hard_coded_df.columns.tolist())

        # Merge with hard-coded exemptions
        issuer_review = issuer_info.merge(hard_coded_df, left_on='ISSUER', right_on='IssuerCode_1', how='left')

        # Print column names after merge for debugging
        print("Columns in issuer_review after merge:", issuer_review.columns.tolist())

        # Fill NaN values
        issuer_review['MTS MM Exempt'] = issuer_review['MTS MM Exempt'].fillna('No')
        issuer_review['SSR MM Review in scope'] = issuer_review.apply(
            lambda row: 'Yes' if row['SSR in Scope'] == 'Yes' and row['MTS MM Exempt'] == 'No' else 'No',
            axis=1
        )


        # Select and rename columns
        issuer_review = issuer_review[['ISSUER', 'ISSUER_FULLNAME', 'SSR in Scope', 'MTS MM Exempt', 'SSR MM Review in scope', 'AMF exemption']]

        return issuer_review


    def calculate_si(self, row, period):
        """
        Calculates the SI value for a given row and period.
        """
        cacib_trades = row.get(f'{period} CA-CIB nb of trades', 0)
        esma_trades = row.get(f'{period} 2.50%xESMA nb of trades', 0)
        auctions = row.get(f'{period} Auction', 0)
        
        if (cacib_trades > 26 and 
            cacib_trades > esma_trades and 
            auctions == 0):
            return 1
        return 0



    def save_processed_data(self, trade_source, trade_source_scope, result_df, issuer_review, output_dir):
        """
        Saves the processed data to Excel files.
        """
        # Prepare output file paths
        trade_source_output = os.path.join(output_dir, "processed_trade_source.xlsx")
        trade_source_scope_output = os.path.join(output_dir, "processed_trade_source_scope.xlsx")
        f_s_review_output = os.path.join(output_dir, "F_S_review_by_ISIN.xlsx")
        # Save issuer_review to Excel
        issuer_review_output = os.path.join(output_dir, "F_S_review_by_Issuer.xlsx")
        issuer_review.to_excel(issuer_review_output, index=False)

        # Save DataFrames to Excel files
        trade_source.to_excel(trade_source_output, index=False)
        trade_source_scope.to_excel(trade_source_scope_output, index=False)
        result_df.to_excel(f_s_review_output, index=False)

        # Store the processed data for downloading
        self.processed_trade_source = trade_source
        self.processed_trade_source_scope = trade_source_scope

        logging.info("Saved processed data to Excel files.")
        self.update_report(f"Processed files saved in: {output_dir}\n")

    def generate_report(self, trade_source, trade_source_scope, result_df, issuer_review, output_dir, all_periods):
        """
        Generates a report summarizing the data processing results.
        """
        report = "Data processing completed successfully.\n"
        report += f"Processed Periods: {', '.join(all_periods)}\n"
        report += f"Number of records in trade_source: {len(trade_source)}\n"
        report += f"Number of records in trade_source_scope: {len(trade_source_scope)}\n"
        report += f"Number of ISINs in F&S review: {len(result_df)}\n"

        # Add more detailed statistics
        report += f"\nTrade Source Statistics:\n"
        report += f"SSR in Scope: {trade_source['SSR in Scope'].value_counts().to_dict()}\n"
        report += f"SSR MM Review in scope: {trade_source['SSR MM Review in scope'].value_counts().to_dict()}\n"
        report += "\nSystematic Internaliser Review Criteria:\n"
        report += ("Consistent with the calculation required for systematic internalisers, CACIB should review on a "
                "quarterly basis if it meets the following criteria:\n"
                "(i) OTC transactions are executed on average more than once a week; and\n"
                "(ii) on a frequency greater than 2.50% of the total number of transactions in the bond published "
                "by ESMA on their page 'Data for the systematic internaliser calculations' at the end of M+1 "
                "following each calendar quarter (i.e., 30/04, 31/07, 31/10, 31/01).\n"
                "=> When criteria is met for 1 ISIN, then exemption applies at the issuer level.\n")

        # Add information about exemptions
        report += "\nExemptions Summary:\n"
        report += f"Total Issuers: {len(issuer_review)}\n"
        report += f"Issuers with SSR In Scope: {issuer_review['SSR in Scope'].value_counts().get('Yes', 0)}\n"
        report += f"Issuers with MTS MM Exempt: {issuer_review['MTS MM Exempt'].value_counts().get('Yes', 0)}\n"
        report += f"Issuers with SSR MM Review in scope: {issuer_review['SSR MM Review in scope'].value_counts().get('Yes', 0)}\n"
        report += f"Issuers with AMF exemption: {issuer_review['AMF exemption'].value_counts().get('Yes', 0)}\n"
        report += f"\nF&S Review Summary:\n"

        for period in all_periods:
                cacib_trades_col = f'{period} CA-CIB nb of trades'
                esma_trades_col = f'{period} 2.50%xESMA nb of trades'
                si_score_col = f'{period} SI Score'
                if cacib_trades_col in result_df.columns:
                    total_cacib_trades = result_df[cacib_trades_col].sum()
                    report += f"Total CA-CIB trades in {period}: {total_cacib_trades}\n"
                else:
                    report += f"No CA-CIB trades data available for {period}\n"
                if esma_trades_col in result_df.columns:
                    total_esma_trades = result_df[esma_trades_col].sum()
                    report += f"Total 2.50% x ESMA nb of trades in {period}: {total_esma_trades}\n"
                else:
                    report += f"No ESMA trades data available for {period}\n"
                if si_score_col in issuer_review.columns:
                    total_si_score = issuer_review[si_score_col].sum()
                    report += f"Total SI Score for {period}: {total_si_score}\n"
                else:
                    report += f"No SI Score data available for {period}\n"



        # Add information about output files
        report += f"\nOutput Files:\n"
        report += f"Processed Trade Source: {os.path.join(output_dir, 'processed_trade_source.xlsx')}\n"
        report += f"Processed Trade Source Scope: {os.path.join(output_dir, 'processed_trade_source_scope.xlsx')}\n"
        report += f"F&S Review by ISIN: {os.path.join(output_dir, 'F_S_review_by_ISIN.xlsx')}\n"

        return report



    # ---------------------------------------
    # Function to Download YTD Data
    # ---------------------------------------

    def download_ytd_data(self):
        # Prompt the user to select a save location
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")])
        
        if not save_path:
            return  # User cancelled the file dialog

        try:
            # Create a Pandas Excel writer using XlsxWriter as the engine
            with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
                # Write Trade_Source data to a sheet
                if self.processed_trade_source is not None:
                    self.processed_trade_source.to_excel(writer, sheet_name='Trade_Source', index=False)
                
                # Write Trade_Source_Scope data to another sheet
                if self.processed_trade_source_scope is not None:
                    self.processed_trade_source_scope.to_excel(writer, sheet_name='Trade_Source_Scope', index=False)

            messagebox.showinfo("Success", f"YTD data has been saved to {save_path}")
            logging.info(f"YTD data saved to {save_path}")
            self.update_report(f"YTD data saved to {save_path}\n")

        except Exception as e:
            error_message = f"An error occurred while saving the YTD data:\n{str(e)}"
            messagebox.showerror("Error", error_message)
            logging.error(error_message)
            self.update_report(f"Error saving YTD data: {e}\n")


    # ---------------------------------------
    # Helper Function to Update Report Text Box
    # ---------------------------------------

    def update_report(self, message):
        """
        Updates the report text box with a new message.
        """
        self.report_text.insert(tk.END, message)
        self.report_text.see(tk.END)  # Scroll to the end

# ---------------------------------------
# Run the Application
# ---------------------------------------

if __name__ == "__main__":
    app = DataProcessingApp()
    app.mainloop()

