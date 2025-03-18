import pandas as pd
import numpy as np

# Output files from processing scripts
ARMA_OUTPUT_FILE = "./processed/arma_allocations.csv"
LAYER3_OUTPUT_FILE = "./processed/layer3_allocations.csv"
GALXE_OUTPUT_FILE = "./processed/galxe_allocations.csv"

# Merged output file
TOTAL_OUTPUT_FILE = "./processed/total_allocations.csv"


def main():
    """
    Merges the processed allocation files from different campaigns into a single comprehensive file.

    This function:
    1. Reads the individual allocation files for each campaign
    2. Standardizes column names
    3. Merges all allocations based on wallet addresses
    4. Calculates total token allocation for each address
    5. Saves the merged data to a new CSV file

    The resulting file contains all unique addresses from all campaigns,
    with zero values for campaigns where an address didn't participate.
    """
    # Read the individual allocation CSV files
    df_arma = pd.read_csv(ARMA_OUTPUT_FILE)
    df_layer3 = pd.read_csv(LAYER3_OUTPUT_FILE)
    df_galxe = pd.read_csv(GALXE_OUTPUT_FILE)

    # Standardize column names (Galxe file has lowercase 'token')
    if "token" in df_galxe.columns:
        df_galxe = df_galxe.rename(columns={"token": "Token"})

    # Merge dataframes on Address
    # First, merge ARMA with Layer3 using outer join to include all addresses from both
    merged_df = pd.merge(
        df_arma, df_layer3, on="Address", how="outer", suffixes=("_arma", "_layer3")
    )

    # Then merge with Galxe, again using outer join to include all addresses
    final_df = pd.merge(merged_df, df_galxe, on="Address", how="outer")

    # Replace NaN values with 0 (addresses that didn't participate in a particular campaign)
    final_df = final_df.fillna(0)

    # Add a Total column that sums the tokens from all three sources
    final_df["Total"] = (
        final_df["Token_arma"] + final_df["Token_layer3"] + final_df["Token"]
    )

    # Rename columns for clarity
    final_df = final_df.rename(
        columns={"Token_arma": "ARMA", "Token_layer3": "Layer3", "Token": "Galxe"}
    )

    # Rearrange columns for better readability
    final_df = final_df[["Address", "ARMA", "Layer3", "Galxe", "Total"]]

    # Save the merged dataframe to a new CSV file
    final_df.to_csv(TOTAL_OUTPUT_FILE, index=False)

    # Print confirmation and summary information
    print(f"Merged data saved to {TOTAL_OUTPUT_FILE}")
    print(f"Total rows in merged data: {len(final_df)}")


if __name__ == "__main__":
    main()
