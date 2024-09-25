"""
Helpers Module for the Data Processing Application.

This module contains utility functions that are used across different modules
of the application. It includes functions for updating GUI elements, determining
periods based on dates, and other miscellaneous helpers.

Functions:
    update_report_textbox(textbox, message): Updates a Tkinter text box with a new message.
    determine_period(input_date): Determines the period identifier for a given date.
    clean_isin(isin): Cleans and standardizes ISIN codes.

Author: Ben Pfeffer
Date: 2024-09-23
"""

import pandas as pd
import tkinter as tk
from datetime import datetime, date

def update_report_textbox(textbox, message):
    """
    Updates a Tkinter text box with a new message.

    Args:
        textbox (tk.Text or ctk.CTkTextbox): The text box widget to update.
        message (str): The message to insert into the text box.
    """
    textbox.insert(tk.END, message)
    textbox.see(tk.END)  # Scroll to the end

def determine_period(input_date):
    """
    Determines the period identifier for a given date based on the Reference Period table.

    Args:
        input_date (datetime.date or datetime.datetime or str): The input date.

    Returns:
        str or None: The period identifier (e.g., 'P1', 'P2', etc.), or None if the date is invalid.
    """
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

    # Handle dates before the base date
    if input_date < base_date:
        return None

    # Calculate the year difference
    years_since_base = input_date.year - base_date.year

    # Determine the quarter based on the month
    if input_date.month <= 3:
        quarter = 4
        year = input_date.year - 1
    elif input_date.month <= 6:
        quarter = 1
        year = input_date.year
    elif input_date.month <= 9:
        quarter = 2
        year = input_date.year
    else:
        quarter = 3
        year = input_date.year

    # Calculate the period number
    period_number = (year - base_date.year) * 4 + quarter

    return f"P{period_number}"

# def determine_period(input_date):
#     """
#     Determines the period identifier for a given date.

#     The periods are defined based on specific date ranges, following a recurring
#     pattern every two years. The function calculates the period number based on
#     the input date.

#     Args:
#         input_date (datetime.date or datetime.datetime or str): The input date.

#     Returns:
#         str or None: The period identifier (e.g., 'P1', 'P2', etc.), or None if the date is invalid.
#     """
#     # Handle NaT values
#     if pd.isna(input_date):
#         return None

#     # Convert input_date to date object if it's a string
#     if isinstance(input_date, str):
#         try:
#             input_date = datetime.strptime(input_date, "%d/%m/%Y").date()
#         except ValueError:
#             return None  # Return None if the date string is invalid
#     elif isinstance(input_date, datetime):
#         input_date = input_date.date()
#     elif not isinstance(input_date, date):
#         return None  # Return None for any other unexpected type

#     # Define the base date (start of P1)
#     base_date = date(2020, 1, 1)

#     # Calculate the number of days since the base date
#     days_since_base = (input_date - base_date).days

#     # Handle dates before the base date
#     if days_since_base < 0:
#         return None  # or you could return a special period for pre-2020 dates

#     # Calculate the number of complete 2-year cycles
#     two_year_cycles = days_since_base // 730  # 730 days in 2 years (ignoring leap years for simplicity)

#     # Calculate the remaining days within the current 2-year cycle
#     days_in_cycle = days_since_base % 730

#     # Determine the period within the 2-year cycle
#     if days_in_cycle < 181:  # First 6 months (181 days)
#         period_in_cycle = 1
#     elif days_in_cycle < 273:  # Next 3 months (92 days)
#         period_in_cycle = 2
#     elif days_in_cycle < 365:  # Next 3 months (92 days)
#         period_in_cycle = 3
#     elif days_in_cycle < 456:  # Next 3 months (91 days)
#         period_in_cycle = 4
#     elif days_in_cycle < 547:  # Next 3 months (91 days)
#         period_in_cycle = 5
#     elif days_in_cycle < 638:  # Next 3 months (91 days)
#         period_in_cycle = 6
#     else:  # Last 3 months (92 days)
#         period_in_cycle = 7

#     # Calculate the final period number
#     period_number = two_year_cycles * 7 + period_in_cycle

#     return f"P{period_number}"

def clean_isin(isin):
    """
    Cleans and standardizes ISIN codes.

    Args:
        isin (str): The ISIN code to clean.

    Returns:
        str: The cleaned and standardized ISIN code.
    """
    return str(isin).strip().upper()
