import pandas as pd
import numpy as np

# Output files from processing scripts
ARMA_OUTPUT_FILE = "./processed/arma_allocations.csv"
LAYER3_OUTPUT_FILE = "./processed/layer3_allocations.csv"
GALXE_OUTPUT_FILE = "./processed/galxe_allocations.csv"
MARKETING_OUTPUT_FILE = "./processed/marketing_allocations.csv"
DISCORD_OUTPUT_FILE = "./processed/discord_role.csv"  # Note: Using discord_role.csv instead of discord_allocations.csv
MEGAPHONE_OUTPUT_FILE = "./processed/megaphone_allocations.csv"

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
    df_marketing = pd.read_csv(MARKETING_OUTPUT_FILE)
    df_discord = pd.read_csv(DISCORD_OUTPUT_FILE)
    df_megaphone = pd.read_csv(MEGAPHONE_OUTPUT_FILE)

    # Standardize column names (Galxe file has lowercase 'token')
    if "token" in df_galxe.columns:
        df_galxe = df_galxe.rename(columns={"token": "Token"})

    # Ensure all dataframes have only Address and Token columns
    df_arma = df_arma[["Address", "Token"]]
    df_layer3 = df_layer3[["Address", "Token"]]
    df_galxe = df_galxe[["Address", "Token"]]
    df_marketing = df_marketing[["Address", "Token"]]
    df_discord = df_discord[["Address", "Token"]]
    df_megaphone = df_megaphone[["Address", "Token"]]

    # Merge dataframes on Address
    # First, merge ARMA with Layer3 using outer join to include all addresses from both
    merged_df = pd.merge(
        df_arma, df_layer3, on="Address", how="outer", suffixes=("_arma", "_layer3")
    )

    # Then merge with Galxe, again using outer join to include all addresses
    merged_df = pd.merge(
        merged_df, df_galxe, on="Address", how="outer", suffixes=("", "_galxe")
    )

    # Merge with Marketing
    merged_df = pd.merge(
        merged_df, df_marketing, on="Address", how="outer", suffixes=("", "_marketing")
    )

    # Merge with Discord
    merged_df = pd.merge(
        merged_df, df_discord, on="Address", how="outer", suffixes=("", "_discord")
    )

    # Merge with Megaphone
    merged_df = pd.merge(
        merged_df, df_megaphone, on="Address", how="outer", suffixes=("", "_megaphone")
    )

    # Replace NaN values with 0 (addresses that didn't participate in a particular campaign)
    merged_df = merged_df.fillna(0)

    # Add a Total column that sums the tokens from all sources
    merged_df["Total"] = (
        merged_df["Token_arma"]
        + merged_df["Token_layer3"]
        + merged_df["Token"]
        + merged_df["Token_marketing"]
        + merged_df["Token_discord"]
        + merged_df["Token_megaphone"]
    )

    # Rename columns for clarity
    merged_df = merged_df.rename(
        columns={
            "Token_arma": "ARMA",
            "Token_layer3": "Layer3",
            "Token": "Galxe",
            "Token_marketing": "Marketing",
            "Token_discord": "Discord",
            "Token_megaphone": "Megaphone",
        }
    )

    # Rearrange columns for better readability
    merged_df = merged_df[
        [
            "Address",
            "ARMA",
            "Layer3",
            "Galxe",
            "Marketing",
            "Discord",
            "Megaphone",
            "Total",
        ]
    ]

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(TOTAL_OUTPUT_FILE, index=False)

    # Print confirmation and summary information
    print(f"Merged data saved to {TOTAL_OUTPUT_FILE}")
    print(f"Total rows in merged data: {len(merged_df)}")

    # Calculate and display the sum of allocations for each campaign
    campaign_sums = {
        "ARMA": merged_df["ARMA"].sum(),
        "Layer3": merged_df["Layer3"].sum(),
        "Galxe": merged_df["Galxe"].sum(),
        "Marketing": merged_df["Marketing"].sum(),
        "Discord": merged_df["Discord"].sum(),
        "Megaphone": merged_df["Megaphone"].sum(),
        "Total": merged_df["Total"].sum(),
    }

    print("\nAllocation Summary:")
    print("-" * 50)
    for campaign, total in campaign_sums.items():
        print(f"{campaign}: {total:,.0f} tokens")
    print("-" * 50)
    print(f"Total Allocation: {campaign_sums['Total']:,.0f} tokens")


if __name__ == "__main__":
    main()
