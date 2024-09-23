"""
Main entry point for the Data Processing Application.

This script initializes and runs the main GUI application, which provides
an interface for users to convert XML files to JSON, process data, and
generate reports based on ESMA_SI and trade source data.

Author: Ben Pfeffer
Date: 2024-09-23
"""

from gui.app import DataProcessingApp

if __name__ == "__main__":
    app = DataProcessingApp()
    app.mainloop()
