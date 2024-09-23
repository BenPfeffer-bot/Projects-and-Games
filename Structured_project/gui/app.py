"""
GUI Application Module for the Data Processing Application.

This module defines the `DataProcessingApp` class, which is a custom Tkinter
application using the CustomTkinter library. The application provides a graphical
user interface for users to select files, convert XML to DataFrame, process data,
and generate reports.

Classes:
    DataProcessingApp(ctk.CTk): The main GUI application class.

Author: Ben Pfeffer
Date: 2024-09-23
"""


import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import logging
import os
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_processing.xml_processor import XMLProcessor
from data_processing.data_processor import DataProcessor
from data_processing.report_generator import ReportGenerator
from utils.helpers import update_report_textbox


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class DataProcessingApp(ctk.CTk):
    """
    The main GUI application class for the Data Processing Application.

    This class inherits from `customtkinter.CTk` and sets up the GUI components,
    event handlers, and integrates with data processing modules.

    Attributes:
        esma_si_xml_folder (tk.StringVar): Variable to store ESMA_SI XML folder path.
        trade_source_path (tk.StringVar): Variable to store Trade_Source Excel file path.
        trade_source_scope_path (tk.StringVar): Variable to store Trade_Source_Scope Excel file path.
        esma_threshold_path (tk.StringVar): Variable to store ESMA_Threshold Excel file path.
        output_directory (tk.StringVar): Variable to store output directory path.
        esma_si_df (pd.DataFrame): DataFrame to store processed ESMA_SI data.
        processed_trade_source (pd.DataFrame): DataFrame to store processed Trade_Source data.
        processed_trade_source_scope (pd.DataFrame): DataFrame to store processed Trade_Source_Scope data.
    """


    def __init__(self):
        """
        Initializes the DataProcessingApp GUI application.
        """
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
        """
        Creates and places all GUI widgets in the application window.
        """
        # Create a frame for the inputs
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20)

        # Step 1: ESMA_SI XML Folder
        step1_label = ctk.CTkLabel(input_frame, text="Step 1: Convert XML to DataFrame")
        step1_label.grid(row=0, column=0, columnspan=3, pady=10)

        esma_si_label = ctk.CTkLabel(input_frame, text="ESMA_SI XML Folder Path:")
        esma_si_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        esma_si_entry = ctk.CTkEntry(input_frame, textvariable=self.esma_si_xml_folder, width=400)
        esma_si_entry.grid(row=1, column=1, padx=10, pady=5)
        esma_si_button = ctk.CTkButton(input_frame, text="Browse", command=self.browse_esma_si_xml_folder)
        esma_si_button.grid(row=1, column=2, padx=10, pady=5)

        convert_button = ctk.CTkButton(input_frame, text="Convert XML to DataFrame", command=self.convert_xml_to_json)
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

        # Dashboard Button
        self.dashboard_button = ctk.CTkButton(self, text="Show Dashboard", command=self.show_dashboard)
        self.dashboard_button.pack(pady=10)
        self.dashboard_button.configure(state='disabled')  # Disable until data is processed

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
        """
        Opens a dialog to select the ESMA_SI XML folder and updates the variable.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.esma_si_xml_folder.set(directory)

    def browse_trade_source(self):
        """
        Opens a dialog to select the Trade_Source Excel file and updates the variable.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            self.trade_source_path.set(filepath)

    def browse_trade_source_scope(self):
        """
        Opens a dialog to select the Trade_Source_Scope Excel file and updates the variable.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            self.trade_source_scope_path.set(filepath)

    def browse_esma_threshold(self):
        """
        Opens a dialog to select the ESMA_Threshold Excel file and updates the variable.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            self.esma_threshold_path.set(filepath)

    def browse_output_directory(self):
        """
        Opens a dialog to select the output directory and updates the variable.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    # ---------------------------------------
    # Step 1: Convert XML Files to DataFrame
    # ---------------------------------------

    def convert_xml_to_json(self):
        """
        Initiates the XML to DataFrame conversion process in a separate thread.
        """
        folder_path = self.esma_si_xml_folder.get()

        if not folder_path:
            messagebox.showerror("Error", "Please provide the XML folder path.")
            return

        # Run in a separate thread to prevent GUI freezing
        threading.Thread(target=self.thread_convert_xml_to_dataframe, args=(folder_path,)).start()

    def thread_convert_xml_to_dataframe(self, folder_path):
        """
        Threaded function to convert XML files to a DataFrame.

        Args:
            folder_path (str): Path to the folder containing XML files.
        """
        try:
            logging.info("Starting XML to DataFrame conversion.")
            update_report_textbox(self.report_text, "Starting XML to DataFrame conversion...\n")

            # Create an instance of XMLProcessor
            xml_processor = XMLProcessor(folder_path)
            self.esma_si_df = xml_processor.convert_xml_to_dataframe()

            messagebox.showinfo("Success", "XML files converted to DataFrame successfully.")
            logging.info("XML files converted to DataFrame successfully.")
            update_report_textbox(self.report_text, "XML files converted to DataFrame successfully.\n")

            # Optionally, save the DataFrame to CSV
            output_dir = self.output_directory.get() or folder_path
            esma_si_output = os.path.join(output_dir, "esma_si_data.csv")
            self.esma_si_df.to_csv(esma_si_output, index=False)
            messagebox.showinfo("Success", f"ESMA_SI data saved to {esma_si_output}")
            logging.info(f"ESMA_SI data saved to {esma_si_output}.")
            update_report_textbox(self.report_text, f"ESMA_SI data saved to {esma_si_output}.\n")
            

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during XML to DataFrame conversion:\n{str(e)}")
            logging.error(f"An error occurred during XML to DataFrame conversion: {e}")
            update_report_textbox(self.report_text, f"Error: {e}\n")

    # ---------------------------------------
    # Step 2: Data Processing Functions
    # ---------------------------------------

    def process_data(self):
        """
        Validates inputs and initiates the data processing in a separate thread.
        """
        if not self.validate_inputs():
            return

        # Clear the report text box
        self.report_text.delete("1.0", tk.END)

        # Get the file paths from the input fields
        trade_source_file = self.trade_source_path.get()
        trade_source_scope_file = self.trade_source_scope_path.get()
        esma_threshold_file = self.esma_threshold_path.get()
        output_dir = self.output_directory.get()

        if self.esma_si_df is None or self.esma_si_df.empty:
            messagebox.showerror("Error", "Please complete Step 1: Convert XML to DataFrame before proceeding.")
            return False


        # Disable the process button while processing
        self.process_button.configure(state='disabled')

        # Run in a separate thread to prevent GUI freezing
        threading.Thread(target=self.thread_process_data, args=(
            trade_source_file, trade_source_scope_file, esma_threshold_file, output_dir)).start()

    def thread_process_data(self, trade_source_file, trade_source_scope_file, esma_threshold_file, output_dir):
        """
        Threaded function to process data.

        Args:
            trade_source_file (str): Path to Trade_Source Excel file.
            trade_source_scope_file (str): Path to Trade_Source_Scope Excel file.
            esma_threshold_file (str): Path to ESMA_Threshold Excel file.
            output_dir (str): Path to output directory.
        """
        try:
            logging.info("Starting data processing.")
            update_report_textbox(self.report_text, "Starting data processing...\n")

            # Create an instance of DataProcessor
            data_processor = DataProcessor(
                self.esma_si_df,
                trade_source_file,
                trade_source_scope_file,
                esma_threshold_file
            )

            # Process the data
            data_processor.process_data()

            # Retrieve processed data
            self.processed_trade_source = data_processor.trade_source
            self.processed_trade_source_scope = data_processor.trade_source_scope

            # Generate the report
            report_generator = ReportGenerator(output_dir)
            report_generator.save_processed_data(
                self.processed_trade_source,
                self.processed_trade_source_scope,
                data_processor.result_df,
                data_processor.issuer_review
            )

            report = report_generator.generate_report(
                esma_si_df=self.esma_si_df,
                trade_source=self.processed_trade_source,
                trade_source_scope=self.processed_trade_source_scope,
                result_df=data_processor.result_df,
                issuer_review=data_processor.issuer_review,
                all_periods=data_processor.all_periods
            )


            # Display the report
            update_report_textbox(self.report_text, report)

            # Enable the download button
            self.after(0, lambda: self.download_button.configure(state='normal'))

            # Enable the dashboard button
            self.after(0, lambda: self.dashboard_button.configure(state='normal'))

            messagebox.showinfo("Success", "Data processing completed successfully.")
            logging.info("Data processing completed successfully.")

        except Exception as e:
            error_message = f"An error occurred during data processing:\n{str(e)}"
            messagebox.showerror("Error", error_message)
            logging.error(error_message)
            update_report_textbox(self.report_text, f"Error: {e}\n")

        finally:
            # Always enable the process button after processing is done
            self.after(0, lambda: self.process_button.configure(state='normal'))

    def validate_inputs(self):
        """
        Validates that all required input fields are provided.

        Returns:
            bool: True if all inputs are valid, False otherwise.
        """
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


    # ---------------------------------------
    # Function for DASHBOARD
    # ---------------------------------------

    def show_dashboard(self):
        """
        Opens a new window to display the dashboard with key metrics.
        """
        if self.processed_trade_source is None or self.processed_trade_source_scope is None:
            messagebox.showerror("Error", "Please process the data before viewing the dashboard.")
            return

        # Create a new window for the dashboard
        dashboard_window = tk.Toplevel(self)
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("900x700")

        # Create a notebook to hold multiple tabs (if desired)
        notebook = ttk.Notebook(dashboard_window)
        notebook.pack(expand=1, fill='both')

        # Example: Total Trades per Period
        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text='Total Trades per Period')

        fig1 = plt.Figure(figsize=(8, 6))
        ax1 = fig1.add_subplot(111)

        periods = self.processed_trade_source['Period'].unique()
        trade_counts = self.processed_trade_source['Period'].value_counts().reindex(periods)

        ax1.bar(periods, trade_counts)
        ax1.set_title('Total Trades per Period')
        ax1.set_xlabel('Period')
        ax1.set_ylabel('Number of Trades')

        canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        # Example: SI Scores per Issuer
        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text='SI Scores per Issuer')

        fig2 = plt.Figure(figsize=(8, 6))
        ax2 = fig2.add_subplot(111)

        # Assuming issuer_review DataFrame has a 'Total SI Score' column
        issuer_si_scores = self.issuer_review[['ISSUER', 'Total SI Score']]
        issuer_si_scores = issuer_si_scores.sort_values('Total SI Score', ascending=False).head(10)

        ax2.barh(issuer_si_scores['ISSUER'], issuer_si_scores['Total SI Score'])
        ax2.set_title('Top 10 Issuers by SI Score')
        ax2.set_xlabel('SI Score')
        ax2.set_ylabel('Issuer')

        canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

        # Add more frames and plots as needed

    # ---------------------------------------
    # Function to Download YTD Data
    # ---------------------------------------

    def download_ytd_data(self):
        """
        Allows the user to download the Year-To-Date data as an Excel file.
        """
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
            update_report_textbox(self.report_text, f"YTD data saved to {save_path}\n")

        except Exception as e:
            error_message = f"An error occurred while saving the YTD data:\n{str(e)}"
            messagebox.showerror("Error", error_message)
            logging.error(error_message)
            update_report_textbox(self.report_text, f"Error saving YTD data: {e}\n")

