"""
Data Processor Module for the Data Processing Application.

This module defines the `DataProcessor` class, which encapsulates the core data
processing logic of the application. It processes the ESMA_SI DataFrame along with
Trade_Source, Trade_Source_Scope, and ESMA_Threshold Excel files to perform
calculations, add necessary columns, and prepare data for report generation.

Classes:
    DataProcessor: Handles data validation, processing, and computations.

Author: Ben Pfeffer
Date: 2024-09-23
"""


import pandas as pd
import pandas as pd
import logging
import os
from datetime import datetime, date
from config.settings import HARD_CODED_DATA
from utils.helpers import determine_period, update_report_textbox

class DataProcessor:
    """
    A class to process data for the Data Processing Application.

    Attributes:
        esma_si_df (pd.DataFrame): DataFrame containing ESMA_SI data.
        trade_source_file (str): Path to the Trade_Source Excel file.
        trade_source_scope_file (str): Path to the Trade_Source_Scope Excel file.
        esma_threshold_file (str): Path to the ESMA_Threshold Excel file.
        output_dir (str): Directory where output files will be saved.
        trade_source (pd.DataFrame): Processed Trade_Source DataFrame.
        trade_source_scope (pd.DataFrame): Processed Trade_Source_Scope DataFrame.
        result_df (pd.DataFrame): DataFrame resulting from F&S review by ISIN.
        issuer_review (pd.DataFrame): DataFrame resulting from F&S review by Issuer.
        all_periods (list): List of all periods processed.
    """

    def __init__(self, esma_si_df, trade_source_file, trade_source_scope_file, esma_threshold_file):
        """
        Initializes the DataProcessor with the necessary data files.

        Args:
            esma_si_df (pd.DataFrame): DataFrame containing ESMA_SI data.
            trade_source_file (str): Path to the Trade_Source Excel file.
            trade_source_scope_file (str): Path to the Trade_Source_Scope Excel file.
            esma_threshold_file (str): Path to the ESMA_Threshold Excel file.
        """
        self.esma_si_df = esma_si_df
        self.trade_source_file = trade_source_file
        self.trade_source_scope_file = trade_source_scope_file
        self.esma_threshold_file = esma_threshold_file

        self.trade_source = None
        self.trade_source_scope = None
        self.result_df = None
        self.issuer_review = None
        self.all_periods = None

    def process_data(self):
        """
        Processes the data by performing validation, loading data, and running computations.

        Raises:
            Exception: If any error occurs during data processing.
        """
        try:
            # Validate inputs
            self._validate_inputs()

            # Load data
            self._load_data()

            # Add 'Period' column to esma_si_df
            self._add_period_to_esma_si()

            # Process hard-coded data
            hard_coded_df = self._process_hard_coded_data()

            # Add required columns to trade data
            self._add_columns_to_trade_data()

            # Perform F&S review by ISIN
            self._perform_fs_review()

            # Create F&S review by Issuer
            self._create_fs_review_by_issuer()

            logging.info("Data processing completed successfully.")

        except Exception as e:
            logging.error(f"An error occurred during data processing: {e}")
            raise

    def _validate_inputs(self):
        """
        Validates that all necessary files are provided and exist.

        Raises:
            FileNotFoundError: If any of the required files are not found.
        """
        files_to_check = [
            self.trade_source_file,
            self.trade_source_scope_file,
            self.esma_threshold_file
        ]

        for file_path in files_to_check:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Required file not found: {file_path}")

        logging.info("All input files are validated and exist.")

    def _load_data(self):
        """
        Loads Trade_Source, Trade_Source_Scope, and ESMA_Threshold data into DataFrames.
        """
        # Load ESMA_Threshold data
        self.esma_threshold = pd.read_excel(self.esma_threshold_file, header=4)
        logging.info("Loaded ESMA_Threshold data.")

        # Load Trade_Source and Trade_Source_Scope data
        self.trade_source = pd.read_excel(self.trade_source_file)
        self.trade_source_scope = pd.read_excel(self.trade_source_scope_file)
        logging.info("Loaded Trade_Source and Trade_Source_Scope data.")

    def _add_period_to_esma_si(self):
        """
        Adds the 'Period' column to the esma_si_df DataFrame based on calculation dates.
        """
        if 'Calculation From Date' not in self.esma_si_df.columns:
            raise KeyError("'Calculation From Date' column not found in esma_si_df.")
        
        self.esma_si_df['Calculation From Date'] = pd.to_datetime(
            self.esma_si_df['Calculation From Date'], errors='coerce')
        self.esma_si_df['Period'] = self.esma_si_df['Calculation From Date'].apply(determine_period)
        logging.info("Added 'Period' column to esma_si_df DataFrame.")

    def _process_hard_coded_data(self):
        """
        Processes the hard-coded data and returns a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the processed hard-coded data.
        """
        from io import StringIO

        hard_coded_df = pd.read_csv(StringIO(HARD_CODED_DATA), sep=',', header=0)
        hard_coded_df.fillna('', inplace=True)

        # Rename columns for consistency
        hard_coded_df.rename(columns={
            'MTS Market Maker (MM) exemption': 'MTS MM Exempt',
            'AMF exemption': 'AMF exemption'
        }, inplace=True)

        # Add 'SSR in Scope' column
        if 'SSR in Scope' not in hard_coded_df.columns:
            hard_coded_df['SSR in Scope'] = hard_coded_df['IssuerCode_1'].apply(
                lambda x: 'Yes' if x else 'No')

        logging.info("Processed hard-coded data.")
        return hard_coded_df


    def _add_columns_to_trade_data(self, hard_coded_df):
        """
        Adds required columns to the trade data based on the hard-coded mappings.

        Args:
            hard_coded_df (pd.DataFrame): DataFrame containing hard-coded mappings.
        """
        # Create mappings from hard-coded data
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

        # Remove rows where 'M_SPLIT_INI' == 0
        self.trade_source = self.trade_source[self.trade_source['M_SPLIT_INI'] != 0]
        self.trade_source_scope = self.trade_source_scope[self.trade_source_scope['M_SPLIT_INI'] != 0]

        # Add required columns
        self.trade_source = self._add_required_columns(
            self.trade_source, mts_mm_exempt_mapping, amf_exempt_mapping)
        self.trade_source_scope = self._add_required_columns(
            self.trade_source_scope, mts_mm_exempt_mapping, amf_exempt_mapping)

        logging.info("Added required columns to trade data.")


    def _add_required_columns(self, df, mts_mm_exempt_mapping, amf_exempt_mapping):
        """
        Adds required columns to the DataFrame based on mappings.

        Args:
            df (pd.DataFrame): DataFrame to which columns will be added.
            mts_mm_exempt_mapping (dict): Mapping for 'MTS MM Exempt'.
            amf_exempt_mapping (dict): Mapping for 'AMF exemption'.

        Returns:
            pd.DataFrame: DataFrame with the new columns added.
        """
        required_columns = ['ISSUER', 'COUNTERPART']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Required column '{col}' not found in DataFrame.")

        df = df.copy()
#        df['ISSUER'] = df['ISSUER'].astype(str).str.strip().str.upper()
        df['ISSUER'] = df['ISSUER'].fillna('').astype(str).str.strip().str.upper()

        issuer_codes_set = set(mts_mm_exempt_mapping.keys()).union(set(amf_exempt_mapping.keys()))

        # Add 'SSR in Scope'
        df['SSR in Scope'] = df['ISSUER'].apply(
            lambda x: 'Yes' if x in issuer_codes_set else 'No')

        # Add 'MTS MM Exempt' and 'AMF exemption'
        df['MTS MM Exempt'] = df['ISSUER'].apply(
            lambda x: mts_mm_exempt_mapping.get(x, 'No'))

        df['AMF exemption'] = df['ISSUER'].apply(
            lambda x: amf_exempt_mapping.get(x, 'No'))

        # Add 'SSR MM Review in scope'
        df['SSR MM Review in scope'] = df.apply(
            lambda row: 'Yes' if row['SSR in Scope'] == 'Yes' and row['MTS MM Exempt'] == 'No' else 'No',
            axis=1)

        # Add 'Auction order' column
        df['Auction order'] = df['COUNTERPART'].apply(
            lambda x: 'Order' if str(x) == '70627' else '-')

        return df


    def _perform_fs_review(self):
        """
        Performs the F&S review by ISIN and updates the result DataFrame.
        """
        # Ensure 'Period' column exists in trade_source
        self.trade_source['Period'] = self.trade_source['M_TRN_DATE'].apply(determine_period)
        self.trade_source_scope['Period'] = self.trade_source_scope['M_TRN_DATE'].apply(determine_period)

        # Remove rows with no 'Period' (dates not in any defined period)
        self.trade_source.dropna(subset=['Period'], inplace=True)
        self.trade_source_scope.dropna(subset=['Period'], inplace=True)

        # Get all unique periods
        self.all_periods = sorted(set(
            self.trade_source['Period'].dropna().unique().tolist() +
            self.trade_source_scope['Period'].dropna().unique().tolist() +
            self.esma_si_df['Period'].dropna().unique().tolist()
        ), key=lambda x: int(x[1:]))

        # Filter trade_source for 'SSR MM Review in scope' == 'Yes'
        trade_source_filtered = self.trade_source[self.trade_source['SSR MM Review in scope'] == 'Yes']

        # Clean ISINs
        trade_source_filtered['ISIN'] = trade_source_filtered['ISIN'].astype(str).str.strip().str.upper()
        self.esma_si_df['ISIN'] = self.esma_si_df['ISIN'].astype(str).str.strip().str.upper()

        # Group by 'ISIN' and 'Period' to count CA-CIB trades
        cacib_trades = trade_source_filtered.groupby(['ISIN', 'Period']).size().reset_index(name='CA-CIB nb of trades')

        # Pivot CA-CIB trades
        cacib_pivot = cacib_trades.pivot_table(
            index='ISIN', columns='Period', values='CA-CIB nb of trades', aggfunc='sum', fill_value=0)
        cacib_pivot.columns = [f'{col} CA-CIB nb of trades' for col in cacib_pivot.columns]
        cacib_pivot.reset_index(inplace=True)

        # Process ESMA_SI data
        self.esma_si_df['Total number of transactions executed in the EU'] = pd.to_numeric(
            self.esma_si_df['Total number of transactions executed in the EU'], errors='coerce').fillna(0).astype(int)
        esma_trades = self.esma_si_df[['ISIN', 'Period', 'Total number of transactions executed in the EU']].copy()
        esma_trades.rename(columns={'Total number of transactions executed in the EU': 'ESMA nb of trades'}, inplace=True)
        esma_trades['2.50% x ESMA nb of trades'] = esma_trades['ESMA nb of trades'] * 0.025

        # Pivot ESMA trades
        esma_pivot = esma_trades.pivot_table(
            index='ISIN', columns='Period', values='2.50% x ESMA nb of trades', aggfunc='sum', fill_value=0)
        esma_pivot.columns = [f'{col} 2.50%xESMA nb of trades' for col in esma_pivot.columns]
        esma_pivot.reset_index(inplace=True)

        # Merge data
        isin_info = trade_source_filtered.groupby('ISIN').agg({
            'ISSUER': 'first',
            'ISSUER_FULLNAME': 'first'
        }).reset_index()

        self.result_df = isin_info.merge(cacib_pivot, on='ISIN', how='left').merge(esma_pivot, on='ISIN', how='left')
        self.result_df.fillna(0, inplace=True)

        # Add Auction columns and SI calculations
        for period in self.all_periods:
            self.result_df[f'{period} Auction'] = self.result_df['ISIN'].apply(
                lambda isin: self._count_auctions(isin, period))
            self.result_df[f'{period} SI'] = self.result_df.apply(
                lambda row: self._calculate_si(row, period), axis=1)

        # Reorder columns
        self._reorder_result_columns()

        logging.info("Performed F&S review by ISIN.")

    def _count_auctions(self, isin, period):
        """
        Counts the number of auctions for a given ISIN and period.

        Args:
            isin (str): The ISIN code.
            period (str): The period identifier.

        Returns:
            int: The count of auctions.
        """
        return ((self.trade_source['ISIN'] == isin) &
                (self.trade_source['Auction order'] == 'Order') &
                (self.trade_source['Period'] == period)).sum()

    def _calculate_si(self, row, period):
        """
        Calculates the SI value for a given row and period.

        Args:
            row (pd.Series): A row from the result DataFrame.
            period (str): The period identifier.

        Returns:
            int: 1 if SI criteria are met, 0 otherwise.
        """
        cacib_trades = row.get(f'{period} CA-CIB nb of trades', 0)
        esma_trades = row.get(f'{period} 2.50%xESMA nb of trades', 0)
        auctions = row.get(f'{period} Auction', 0)

        if (cacib_trades > 26 and cacib_trades > esma_trades and auctions == 0):
            return 1
        return 0


    def _reorder_result_columns(self):
        """
        Reorders the columns in the result DataFrame for better readability.
        """
        columns_order = ['ISIN', 'ISSUER', 'ISSUER_FULLNAME']
        for period in self.all_periods:
            columns_order += [
                f'{period} CA-CIB nb of trades',
                f'{period} 2.50%xESMA nb of trades',
                f'{period} Auction',
                f'{period} SI'
            ]

        # Ensure all columns are present
        for col in columns_order:
            if col not in self.result_df.columns:
                self.result_df[col] = 0

        self.result_df = self.result_df[columns_order]


    def _create_fs_review_by_issuer(self):
        """
        Creates the F&S Review by Issuer DataFrame following the specified steps.
        """

        # Step 1: Copy Trade_source_scope columns
        self.issuer_review = self.trade_source_scope[
            ['ISSUER', 'ISSUER_FULLNAME', 'SSR in Scope', 'MTS MM Exempt', 'SSR MM Review in scope', 'AMF exemption']
        ].drop_duplicates()

        # Step 2: Drop duplicates (already done with drop_duplicates())

        # Step 3: Fill NaN values in specified columns with 'No'
        columns_to_fill = ['SSR in Scope', 'MTS MM Exempt', 'SSR MM Review in scope', 'AMF exemption']
        self.issuer_review[columns_to_fill] = self.issuer_review[columns_to_fill].fillna('No')

        # Step 4: Sum all the SI values for each 'ISSUER' and fill NaN with 0
        # For each period, calculate the SI Score and merge into issuer_review
        si_score_columns = []
        for period in self.all_periods:
            si_col = f'{period} SI'
            si_score_col = f'{period} SI Score'
            si_score_columns.append(si_score_col)

            if si_col in self.result_df.columns:
                # Group result_df by 'ISSUER' and sum SI values for this period
                si_scores = self.result_df.groupby('ISSUER')[si_col].sum().reset_index(name=si_score_col)
                # Merge SI scores into issuer_review
                self.issuer_review = self.issuer_review.merge(si_scores, on='ISSUER', how='left')
            else:
                # If SI column is not in result_df, fill with zeros
                self.issuer_review[si_score_col] = 0

        # Fill NaN SI Scores with 0
        self.issuer_review[si_score_columns] = self.issuer_review[si_score_columns].fillna(0)

        # Remove periods where all SI Score columns are zero
        cols_to_drop = [col for col in si_score_columns if self.issuer_review[col].sum() == 0]
        self.issuer_review.drop(columns=cols_to_drop, inplace=True)

        self.issuer_review['Total SI Score'] = self.issuer_review[[col for col in self.issuer_review.columns if 'SI Score' in col]].sum(axis=1)

        logging.info("Created F&S review by Issuer with adjusted logic.")
