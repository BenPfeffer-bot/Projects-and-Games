"""
XML Processor Module for the Data Processing Application.

This module defines the `XMLProcessor` class, which is responsible for converting
ESMA_SI XML files into a Pandas DataFrame. It parses XML files in a given directory,
extracts relevant data, and compiles it into a structured DataFrame for further processing.

Classes:
    XMLProcessor: Handles the conversion of XML files to a DataFrame.

Author: Ben Pfeffer
Date: 2024-09-23
"""


import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import pandas as pd
import logging


class XMLProcessor:
    """
    A class to process ESMA_SI XML files and convert them into a Pandas DataFrame.

    Attributes:
        folder_path (str): The path to the folder containing XML files.
    """


def __init__(self, folder_path):
    """
    Initializes the XMLProcessor with the specified folder path.

    Args:
        folder_path (str): The path to the folder containing XML files.
    """
    self.folder_path = folder_path

    def convert_xml_to_dataframe(self):
        """
        Converts all XML files in the specified folder to a single Pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing data extracted from the XML files.

        Raises:
            FileNotFoundError: If no XML files are found in the specified folder.
            Exception: If an unexpected error occurs during XML parsing.
        """
        all_data = []

        # List all XML files in the folder
        xml_files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if f.endswith('.xml')]

        if not xml_files:
            raise FileNotFoundError("No XML files found in the selected folder.")

        for xml_file_path in xml_files:
            try:
                logging.info(f"Processing XML file: {xml_file_path}")
                # Parse the XML file
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Extract data from XML
                xml_data = self._extract_xml_data(root)

                # Extract the NonEqtyTrnsprncyData list
                non_equity_data_list = self._get_non_equity_data(xml_data)
                if not non_equity_data_list:
                    continue  # Skip if no data found

                # Prepare data for DataFrame
                for item in non_equity_data_list:
                    extracted_item = self._extract_item_data(item)
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


    def _extract_xml_data(self, root):
        """
        Recursively extracts data from XML elements and returns a nested dictionary.

        Args:
            root (xml.etree.ElementTree.Element): The root element of the XML tree.

        Returns:
            dict: A nested dictionary representing the XML structure.
        """
        data = {}
        for child in root:
            tag = child.tag.split('}')[-1]  # Remove namespace
            if len(child) == 0:
                data[tag] = child.text
            else:
                child_data = self._extract_xml_data(child)
                if tag in data:
                    if not isinstance(data[tag], list):
                        data[tag] = [data[tag]]
                    data[tag].append(child_data)
                else:
                    data[tag] = child_data
        return data

    def _get_non_equity_data(self, xml_data):
        """
        Extracts the NonEqtyTrnsprncyData list from the XML data dictionary.

        Args:
            xml_data (dict): The nested dictionary representing the XML data.

        Returns:
            list: A list of NonEqtyTrnsprncyData items, or None if not found.
        """
        try:
            payload = xml_data.get('Pyld') or xml_data.get('payload')
            document = payload.get('Document') or payload.get('document')
            report_results = document.get('FinInstrmRptgNonEqtyTradgActvtyRslt') or document.get('finInstrmRptgNonEqtyTradgActvtyRslt')
            non_equity_data_list = report_results.get('NonEqtyTrnsprncyData') or report_results.get('nonEqtyTrnsprncyData')
            return non_equity_data_list
        except AttributeError:
            logging.warning("NonEqtyTrnsprncyData not found in XML data.")
            return None


    def _extract_item_data(self, item):
        """
        Extracts relevant data from a NonEqtyTrnsprncyData item.

        Args:
            item (dict): A dictionary representing a NonEqtyTrnsprncyData item.

        Returns:
            dict: A dictionary containing extracted fields.
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

