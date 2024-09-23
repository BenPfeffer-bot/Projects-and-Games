import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s:%(message)s")

def load_processed_data(output_dir):
    """
    Load the processed data from the output directory.
    """
    try:
        trade_source = pd.read_excel(os.path.join(output_dir, "processed_trade_source.xlsx"))
        trade_source_scope = pd.read_excel(os.path.join(output_dir, "processed_trade_source_scope.xlsx"))

        result_df = pd.read_excel(os.path.join(output_dir, "F_S_review_by_ISIN.xlsx"))
        issuer_review = pd.read_excel(os.path.join(output_dir, "F_S_review_by_issuer.xlsx"))
        logging.info("Successfully loaded processed data.")

    except Exception as e:
        logging.error(f"Error loading processed data: {e}")
        raise

def combine_data_for_visualization(trade_source, trade_source_scope, result_df, issuer_review):
    """
    Combines issuer review and result data to create a comprehensive DataFrame for visualization.
    """
    # Ensure ISSUER columns are of string type
    trade_source_scope['ISSUER'] = trade_source_scope['ISSUER'].astype(str)
    issuer_review['ISSUER'] = issuer_review['ISSUER'].astype(str)
    result_df['ISSUER'] = result_df['ISSUER'].astype(str)

    # Melt result_df to long format for SI results
    si_columns = [col for col in result_df.columns if col.endswith('SI')]
    melted_si_df = result_df.melt(id_vars=['ISIN','ISSUER','ISSUER_FULLNAME'], value_vars=si_columns, var_name='Period',value_name='SI_Result')
    melted_si_df['Period'] = melted_si_df['Period'].str.replace('SI','')

    #Melt trade columns to long format
    trade_metrics = ["CA-CIB nb of trades","2.5%xESMA nb of trades","Auction"]
    melted_trade_df = pd.DataFrame()
    for metric in trade_metrics:
        metric_columns = [col for col in result_df.columns if col.endswith(metric)]
        temp_df =result_df.melt(id_vars=['ISIN','ISSUER','ISSUER_FULLNAME'], value_vars=metric_columns, var_name='Period',value_name=metric)
        temp_df['Period']= temp_df['Period'].str.replace(f'{metric}','')

        if melted_trade_df.empty:
            melted_trade_df = temp_df
        else:
            melted_trade_df = melted_trade_df.merge(
                temp_df,
                on=['ISIN','ISSUER','ISSUER_FULLNAME','Period'],
                how='outer'
            )

    #Merge SI results with trade metrics
    combined_isin_df = melted_si_df.merge(melted_trade_df,
                                          on=['ISIN','ISSUER','ISSUER_FULLNAME','Period'],
                                          how='left')
    
    #Merge with issuer_review
    combined_df = combined_isin_df.merge(
        issuer_review,
        on=['ISSUER','ISSUER_FULLNAME'],
        how='left'
    )

    #Add SI obligation flag
    combined_df['SI_Obligation'] = combined_df['SI_Result'].apply(lambda x:'Yes' if x == 1 else 'No')
    logging.info("Sucessfully combined data for visualization.")
    return combined_df

def save_combined_data(combined_df, output_dir):
    """Saves the combined DataFrame to an Excel file for visualization."""
    visualization_output = os.path.join(output_dir,'combined_data_for_visualization.xlsx')
    try:
        combined_df.to_excel(visualization_output, index=False)
        logging.info(f"Combined data saved to {visualization_output}")
    except Exception as e:
        logging.error(f"Error saving combined data: {e}")
        raise

def main():
    # Specify the ouput directory where the processed data is stored
    output_dir = input("Enter the path to the directory:  ").strip()
    if not os.path.isdir(output_dir):
        print("Invalid directory. Please check the path and try again.")
        return

    try:
        #Load processed data
        trade_source, trade_source_scope, result_df, issuer_review = load_processed_data(output_dir)

        #Combine data for vizua
        combined_df = combine_data_for_visualization(trade_source_scope, result_df, issuer_review)

        #Save the combined data
        save_combined_data(combined_df, output_dir)

        print(f"Report generation completed successfully.")
        print(f"Combined data visualization saved in {os.path.join(output_dir, 'combined_data_for_visualization.xlsx')}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()