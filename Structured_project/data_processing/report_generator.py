"""
Report Generator Module for the Data Processing Application.

This module defines the `ReportGenerator` class, which is responsible for saving
processed data to Excel files and generating a textual report summarizing the
results of the data processing. The report includes statistics and key information
that can be used for further analysis or auditing.

Classes:
    ReportGenerator: Handles saving data and generating reports.

Author: Ben Pfeffer
Date: 2024-09-23
"""


import os
import pandas as pd
import logging


class ReportGenerator:
    """
    A class to generate reports and save processed data for the Data Processing Application.

    Attributes:
        output_dir (str): Directory where output files will be saved.
    """


    def __init__(self, output_dir):
        """
        Initializes the ReportGenerator with the specified output directory.

        Args:
            output_dir (str): The path to the directory where output files will be saved.
        """
        self.output_dir = output_dir


    def save_processed_data(self, trade_source, trade_source_scope, result_df, issuer_review):
        """
        Saves the processed data to Excel files in the output directory.

        Args:
            trade_source (pd.DataFrame): Processed Trade_Source DataFrame.
            trade_source_scope (pd.DataFrame): Processed Trade_Source_Scope DataFrame.
            result_df (pd.DataFrame): DataFrame resulting from F&S review by ISIN.
            issuer_review (pd.DataFrame): DataFrame resulting from F&S review by Issuer.
        """
        # Prepare output file paths
        trade_source_output = os.path.join(self.output_dir, "processed_trade_source.xlsx")
        trade_source_scope_output = os.path.join(self.output_dir, "processed_trade_source_scope.xlsx")
        f_s_review_output = os.path.join(self.output_dir, "F_S_review_by_ISIN.xlsx")
        issuer_review_output = os.path.join(self.output_dir, "F_S_review_by_Issuer.xlsx")

        # Save DataFrames to Excel files
        trade_source.to_excel(trade_source_output, index=False)
        trade_source_scope.to_excel(trade_source_scope_output, index=False)
        result_df.to_excel(f_s_review_output, index=False)
        issuer_review.to_excel(issuer_review_output, index=False)

        os.makedirs(self.output_dir, exist_ok=True)


        logging.info("Saved processed data to Excel files.")


    def generate_report(self, esma_si_df, trade_source, trade_source_scope, result_df, issuer_review, all_periods):
        """
        Generates a textual report summarizing the data processing results, including data analysis.

        Args:
            esma_si_df (pd.DataFrame): ESMA_SI DataFrame.
            trade_source (pd.DataFrame): Processed Trade_Source DataFrame.
            trade_source_scope (pd.DataFrame): Processed Trade_Source_Scope DataFrame.
            result_df (pd.DataFrame): DataFrame resulting from F&S review by ISIN.
            issuer_review (pd.DataFrame): DataFrame resulting from F&S review by Issuer.
            all_periods (list): List of all periods processed.

        Returns:
            str: The generated report as a string.
        """
        report = "Data processing completed successfully.\n"
        report += f"Processed Periods: {', '.join(all_periods)}\n\n"

        # -----------------------------
        # Data Analysis Section
        # -----------------------------
        report += "=== Data Analysis ===\n\n"

        # ESMA_SI Data Analysis
        report += "ESMA_SI Data Analysis:\n"
        report += f"Total records in ESMA_SI data: {len(esma_si_df)}\n"

        # Get date range in ESMA_SI data
        esma_dates = esma_si_df['Calculation From Date'].dropna()
        if not esma_dates.empty:
            min_date = esma_dates.min().strftime('%Y-%m-%d')
            max_date = esma_dates.max().strftime('%Y-%m-%d')
            report += f"Date range in ESMA_SI data: {min_date} to {max_date}\n"

            # Determine periods corresponding to the date range
            periods = esma_si_df['Period'].dropna().unique().tolist()
            periods.sort(key=lambda x: int(x[1:]))
            report += f"Periods in ESMA_SI data: {', '.join(periods)}\n"
        else:
            report += "No valid dates found in ESMA_SI data.\n"

        report += "\n"

        # Trade_Source Data Analysis
        report += "Trade_Source Data Analysis:\n"
        report += f"Total records in Trade_Source data: {len(trade_source)}\n"

        # Get date range in Trade_Source data
        trade_source_dates = trade_source['M_TRN_DATE'].dropna()
        if not trade_source_dates.empty:
            min_date = trade_source_dates.min().strftime('%Y-%m-%d')
            max_date = trade_source_dates.max().strftime('%Y-%m-%d')
            report += f"Date range in Trade_Source data: {min_date} to {max_date}\n"

            # Determine periods corresponding to the date range
            periods = trade_source['Period'].dropna().unique().tolist()
            periods.sort(key=lambda x: int(x[1:]))
            report += f"Periods in Trade_Source data: {', '.join(periods)}\n"
        else:
            report += "No valid dates found in Trade_Source data.\n"

        report += "\n"

        # Trade_Source_Scope Data Analysis
        report += "Trade_Source_Scope Data Analysis:\n"
        report += f"Total records in Trade_Source_Scope data: {len(trade_source_scope)}\n"

        # Get date range in Trade_Source_Scope data
        trade_source_scope_dates = trade_source_scope['M_TRN_DATE'].dropna()
        if not trade_source_scope_dates.empty:
            min_date = trade_source_scope_dates.min().strftime('%Y-%m-%d')
            max_date = trade_source_scope_dates.max().strftime('%Y-%m-%d')
            report += f"Date range in Trade_Source_Scope data: {min_date} to {max_date}\n"

            # Determine periods corresponding to the date range
            periods = trade_source_scope['Period'].dropna().unique().tolist()
            periods.sort(key=lambda x: int(x[1:]))
            report += f"Periods in Trade_Source_Scope data: {', '.join(periods)}\n"
        else:
            report += "No valid dates found in Trade_Source_Scope data.\n"

        report += "\n"

        # -----------------------------
        # Original Report Content
        # -----------------------------

        report += "Trade Source Statistics:\n"
        report += f"SSR in Scope: {trade_source['SSR in Scope'].value_counts().to_dict()}\n"
        report += f"SSR MM Review in scope: {trade_source['SSR MM Review in scope'].value_counts().to_dict()}\n"

        report += "\nSystematic Internaliser Review Criteria:\n"
        report += (
            "Consistent with the calculation required for systematic internalisers, CACIB should review on a "
            "quarterly basis if it meets the following criteria:\n"
            "(i) OTC transactions are executed on average more than once a week; and\n"
            "(ii) on a frequency greater than 2.50% of the total number of transactions in the bond published "
            "by ESMA on their page 'Data for the systematic internaliser calculations' at the end of M+1 "
            "following each calendar quarter (i.e., 30/04, 31/07, 31/10, 31/01).\n"
            "=> When criteria is met for 1 ISIN, then exemption applies at the issuer level.\n"
        )

        # Add information about exemptions
        report += "\nExemptions Summary:\n"
        report += f"Total Issuers: {len(issuer_review)}\n"
        report += f"Issuers with SSR in Scope: {issuer_review['SSR in Scope'].value_counts().get('Yes', 0)}\n"
        report += f"Issuers with MTS MM Exempt: {issuer_review['MTS MM Exempt'].value_counts().get('Yes', 0)}\n"
        report += f"Issuers with SSR MM Review in scope: {issuer_review['SSR MM Review in scope'].value_counts().get('Yes', 0)}\n"
        report += f"Issuers with AMF exemption: {issuer_review['AMF exemption'].value_counts().get('Yes', 0)}\n"

        # New section: List of Issuers Eligible for Exemptions
        report += "\nIssuers Eligible for Exemptions:\n"

        # Issuers with MTS MM Exempt == 'Yes'
        mts_mm_exempt_issuers = issuer_review[issuer_review['MTS MM Exempt'] == 'Yes']['ISSUER'].unique()
        report += "Issuers with MTS MM Exempt:\n"
        report += ', '.join(mts_mm_exempt_issuers) + '\n\n'

        # Issuers with AMF exemption == 'Yes'
        amf_exempt_issuers = issuer_review[issuer_review['AMF exemption'] == 'Yes']['ISSUER'].unique()
        report += "Issuers with AMF Exemption:\n"
        report += ', '.join(amf_exempt_issuers) + '\n'

        report += "\nF&S Review Summary:\n"

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
        report += "\nOutput Files:\n"
        report += f"Processed Trade Source: {os.path.join(self.output_dir, 'processed_trade_source.xlsx')}\n"
        report += f"Processed Trade Source Scope: {os.path.join(self.output_dir, 'processed_trade_source_scope.xlsx')}\n"
        report += f"F&S Review by ISIN: {os.path.join(self.output_dir, 'F_S_review_by_ISIN.xlsx')}\n"
        report += f"F&S Review by Issuer: {os.path.join(self.output_dir, 'F_S_review_by_Issuer.xlsx')}\n"

        logging.info("Generated report with data analysis and corresponding periods.")
        return report

