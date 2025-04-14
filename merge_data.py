import pandas as pd
import numpy as np
import json

# Output files from processing scripts
ARMA_OUTPUT_FILE = "./processed/arma_allocations.csv"
LAYER3_OUTPUT_FILE = "./processed/layer3_allocations.csv"
GALXE_OUTPUT_FILE = "./processed/galxe_allocations.csv"
COMMUNITY_OUTPUT_FILE = "./processed/community_allocations.csv"
DISCORD_OUTPUT_FILE = "./processed/discord_role.csv"  # Note: Using discord_role.csv instead of discord_allocations.csv
MEGAPHONE_OUTPUT_FILE = "./processed/megaphone_allocations.csv"

# Merged output file
TOTAL_OUTPUT_FILE = "./processed/total_allocations.csv"
ELIGIBILITY_OUTPUT_FILE = "./processed/eligibility.json"

TOTAL_SUPPLY = 1_000_000_000


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
    df_community = pd.read_csv(COMMUNITY_OUTPUT_FILE)
    df_discord = pd.read_csv(DISCORD_OUTPUT_FILE)
    df_megaphone = pd.read_csv(MEGAPHONE_OUTPUT_FILE)

    # Ensure all dataframes have only Address and Token columns
    df_arma = df_arma[["Address", "Token"]]
    df_layer3 = df_layer3[["Address", "Token"]]
    df_galxe = df_galxe[["Address", "Token"]]
    df_community = df_community[["Address", "Token"]]
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
        merged_df, df_community, on="Address", how="outer", suffixes=("", "_community")
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
        + merged_df["Token_community"]
        + merged_df["Token_discord"]
        + merged_df["Token_megaphone"]
    )

    # Rename columns for clarity
    merged_df = merged_df.rename(
        columns={
            "Token_arma": "ARMA",
            "Token_layer3": "Layer3",
            "Token": "Galxe",
            "Token_community": "Community",
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
            "Community",
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
        "Community": merged_df["Community"].sum(),
        "Discord": merged_df["Discord"].sum(),
        "Megaphone": merged_df["Megaphone"].sum(),
        "Total": merged_df["Total"].sum(),
    }

    # Calculate category totals
    socials_total = (
        campaign_sums["Layer3"] + campaign_sums["Galxe"] + campaign_sums["Megaphone"]
    )
    community_total = campaign_sums["Community"] + campaign_sums["Discord"]

    print("\nAllocation Summary:")
    print("-" * 50)
    for campaign, total in campaign_sums.items():
        print(f"{campaign}: {total:,.0f} tokens ({total / TOTAL_SUPPLY:.3%})")
    print("-" * 50)
    print(
        f"Socials (Layer3 + Galxe + Megaphone): {socials_total:,.0f} tokens ({socials_total / TOTAL_SUPPLY:.3%})"
    )
    print(
        f"Community (Community + Discord): {community_total:,.0f} tokens ({community_total / TOTAL_SUPPLY:.3%})"
    )
    print("-" * 50)
    print(
        f"Total Allocation: {campaign_sums['Total']:,.0f} tokens ({campaign_sums['Total'] / TOTAL_SUPPLY:.3%})"
    )

    # Create eligibility mapping
    create_eligibility_mapping(merged_df)


def create_eligibility_mapping(merged_df):
    """
    Creates a JSON file that maps each address to their eligibility status across three categories:
    - ARMA: True if the address received tokens from ARMA campaign
    - Socials: True if the address received tokens from Layer3, Galxe, or Megaphone
    - Community: True if the address received tokens from Marketing or Discord

    Args:
        merged_df: DataFrame containing all addresses and their allocations from different campaigns
    """
    eligibility_mapping = {}

    for _, row in merged_df.iterrows():
        address = row["Address"]

        # Determine eligibility for each category
        arma_eligible = row["ARMA"] > 0
        socials_eligible = row["Layer3"] > 0 or row["Galxe"] > 0 or row["Megaphone"] > 0
        community_eligible = row["Community"] > 0 or row["Discord"] > 0

        # Create the mapping for this address
        eligibility_mapping[address] = {
            "ARMA": arma_eligible,
            "Socials": socials_eligible,
            "Community": community_eligible,
        }

    # Write the mapping to a JSON file
    with open(ELIGIBILITY_OUTPUT_FILE, "w") as f:
        json.dump(eligibility_mapping, f, indent=2)

    print(f"Eligibility mapping saved to {ELIGIBILITY_OUTPUT_FILE}")
    print(f"Total addresses in eligibility mapping: {len(eligibility_mapping)}")


if __name__ == "__main__":
    main()
