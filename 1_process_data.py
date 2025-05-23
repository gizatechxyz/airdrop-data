import pandas as pd
import numpy as np
from web3 import Web3

# Input data files
ARMA_FILE = "./data/arma_leaderboard.csv"
COMMUNITY_FILE = "./data/community_campaign.csv"
LAYER3_FILE = "./data/layer3_campaign.csv"
GALXE_FILE = "./data/galxe_campaign.csv"
MEGAPHONE_CAMPAIGN_FILE = "./data/megaphone_campaign.csv"
DISCORD_FILE = "./processed/discord_role.csv"

# Output allocation files
ARMA_OUTPUT_FILE = "./processed/arma_allocations.csv"
LAYER3_OUTPUT_FILE = "./processed/layer3_allocations.csv"
GALXE_OUTPUT_FILE = "./processed/galxe_allocations.csv"
MEGAPHONE_OUTPUT_FILE = "./processed/megaphone_allocations.csv"
COMMUNITY_OUTPUT_FILE = "./processed/community_allocations.csv"
DISCORD_OUTPUT_FILE = "./processed/discord_role.csv"

TOTAL_SUPPLY = 1_000_000_000
SOCIALS_ALLOCATION = 180  # Fixed allocation for social campaigns


def calculate_arma_allocations():
    """
    Calculates token allocations for the ARMA campaign using a tier-based approach.

    Methodology:
    1. Filter out entries with less than 60 points
    2. Allocate tokens based on points tiers:
        - 60-100 points: 180 tokens
        - 100-250 points: 385 tokens
        - 250-500 points: 1150 tokens
        - 500-1000 points: 1715 tokens
        - 1000-2000 points: 2850 tokens
        - 2000-5000 points: 5700 tokens
        - 5000-10000 points: 11430 tokens
        - 10000-25000 points: 17000 tokens
        - 25000-50000 points: 25000 tokens
        - 50000-100000 points: 52500 tokens
        - 100000+ points: 85000 tokens
    """
    print("--- Processing ARMA Campaign ---")
    # Read and clean data
    df = pd.read_csv(ARMA_FILE)
    initial_count = len(df)
    print(f"Initial addresses: {initial_count}")

    # Convert addresses to checksum format
    df["eoa"] = df["eoa"].apply(lambda x: Web3.to_checksum_address(x))

    # Filter out entries with less than 60 points
    count_before_points_filter = len(df)
    df = df[df["points"] >= 60]
    count_after_points_filter = len(df)
    print(
        f"Addresses after filtering points < 60: {count_after_points_filter} (dropped {count_before_points_filter - count_after_points_filter})"
    )

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["eoa"], keep=False)]
    if not duplicates.empty:
        print(f"Duplicate addresses found in ARMA campaign: {len(duplicates)}")
        # print(duplicates[["eoa", "points"]].sort_values("eoa")) # Optional: uncomment to see duplicates

    # Remove duplicates keeping the first occurrence
    count_before_duplicates = len(df)
    df = df.drop_duplicates(subset=["eoa"], keep="first")
    count_after_duplicates = len(df)
    print(
        f"Addresses after removing duplicates: {count_after_duplicates} (dropped {count_before_duplicates - count_after_duplicates})"
    )

    # Initialize Token column
    df["Token"] = 0

    # Apply tier-based token allocation
    df.loc[(df["points"] > 60) & (df["points"] <= 100), "Token"] = 180
    df.loc[(df["points"] > 100) & (df["points"] <= 250), "Token"] = 385
    df.loc[(df["points"] > 250) & (df["points"] <= 500), "Token"] = 1150
    df.loc[(df["points"] > 500) & (df["points"] <= 1000), "Token"] = 1715
    df.loc[(df["points"] > 1000) & (df["points"] <= 2000), "Token"] = 2850
    df.loc[(df["points"] > 2000) & (df["points"] <= 5000), "Token"] = 5700
    df.loc[(df["points"] > 5000) & (df["points"] <= 10000), "Token"] = 11430
    df.loc[(df["points"] > 10000) & (df["points"] <= 25000), "Token"] = 17000
    df.loc[(df["points"] > 25000) & (df["points"] <= 50000), "Token"] = 25000
    df.loc[(df["points"] > 50000) & (df["points"] <= 100000), "Token"] = 52500
    df.loc[df["points"] > 100000, "Token"] = 85000

    # Clean up and standardize column names
    df.rename(columns={"eoa": "Address"}, inplace=True)
    df = df[["Address", "Token"]]

    # Display total tokens
    print(f"ARMA Campaign Final Count: {len(df)}")
    print(f"ARMA Campaign Total Tokens: {df['Token'].sum():,.2f}")
    print(f"ARMA Campaign Total Tokens: {df['Token'].sum() / TOTAL_SUPPLY:.2%}")
    # Save the processed allocation data
    df.to_csv(ARMA_OUTPUT_FILE, index=False)


def calculate_community_allocations():
    """
    Calculates token allocations for the community campaign.
    Only considers participants from the Feedback sprint, not the oasis gathering.

    Methodology:
    - Filter addresses that exist in ARMA data
    - Filter for participants with at least 100 points
    - Allocate 385 tokens for participants with exactly 300 points
    - Save results to COMMUNITY_OUTPUT_FILE
    """
    print("--- Processing Community Campaign ---")
    # Read input data
    df = pd.read_csv(COMMUNITY_FILE)
    df_arma = pd.read_csv(ARMA_FILE)
    initial_count = len(df)
    print(f"Initial addresses: {initial_count}")

    # Convert addresses to checksum format
    df["eoa"] = df["eoa"].apply(lambda x: Web3.to_checksum_address(x))
    df_arma["eoa"] = df_arma["eoa"].apply(lambda x: Web3.to_checksum_address(x))

    # Filter marketing addresses that exist in ARMA data
    count_before_arma_filter = len(df)
    filtered_df = df[df["eoa"].isin(df_arma["eoa"])].copy()
    count_after_arma_filter = len(filtered_df)
    print(
        f"Addresses after filtering for existence in ARMA: {count_after_arma_filter} (dropped {count_before_arma_filter - count_after_arma_filter})"
    )

    # Filter for participants with at least 100 points
    count_before_points_filter = len(filtered_df)
    filtered_df = filtered_df[filtered_df["points"] >= 100]
    count_after_points_filter = len(filtered_df)
    print(
        f"Addresses after filtering points <= 100: {count_after_points_filter} (dropped {count_before_points_filter - count_after_points_filter})"
    )

    # Initialize Token column to 0 for all remaining participants
    filtered_df["Token"] = 0

    # Set token allocation for 300 points participants
    filtered_df.loc[filtered_df["points"] == 300, "Token"] = 385
    # Optional: Add a check for NaNs if needed
    # nan_token_count = filtered_df['Token'].isna().sum()
    # if nan_token_count > 0:
    #     print(f"Warning: {nan_token_count} addresses have NaN token values after allocation.")

    # Clean up and standardize column names
    filtered_df.rename(columns={"eoa": "Address"}, inplace=True)
    filtered_df = filtered_df[["Address", "Token"]]

    # Display total tokens
    print(f"Community Campaign Final Count: {len(filtered_df)}")
    print(f"Community Campaign Total Tokens: {filtered_df['Token'].sum():,.2f}")
    print(
        f"Community Campaign Total Tokens: {filtered_df['Token'].sum() / TOTAL_SUPPLY:.3%}"
    )
    # Save the processed allocation data
    filtered_df.to_csv(COMMUNITY_OUTPUT_FILE, index=False)

    return filtered_df


def calculate_layer3_allocations():
    """
    Calculates token allocations for the Layer3 campaign.

    Methodology:
    - Equal distribution model where all qualifying participants receive the same allocation
    - Each participant receives a fixed amount of 180 tokens
    - Filter addresses to only include those present in the ARMA leaderboard
    """
    print("--- Processing Layer3 Campaign ---")
    # Read and clean data
    df = pd.read_csv(LAYER3_FILE)
    df_arma = pd.read_csv(ARMA_FILE)
    initial_count = len(df)
    print(f"Initial addresses: {initial_count}")

    # Convert addresses to checksum format
    df["UserAddress"] = df["UserAddress"].apply(lambda x: Web3.to_checksum_address(x))
    df_arma["eoa"] = df_arma["eoa"].apply(lambda x: Web3.to_checksum_address(x))

    # Filter Layer3 addresses that exist in ARMA data
    count_before_arma_filter = len(df)
    df = df[df["UserAddress"].isin(df_arma["eoa"])].copy()
    count_after_arma_filter = len(df)
    print(
        f"Addresses after filtering for existence in ARMA: {count_after_arma_filter} (dropped {count_before_arma_filter - count_after_arma_filter})"
    )

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["UserAddress"], keep=False)]
    if not duplicates.empty:
        print(f"Duplicate addresses found in Layer3 campaign: {len(duplicates)}")
        # print(duplicates[["UserAddress", "Quest"]].sort_values("UserAddress")) # Optional: uncomment to see duplicates

    # Remove duplicates keeping the first occurrence
    count_before_duplicates = len(df)
    df = df.drop_duplicates(subset=["UserAddress"], keep="first")
    count_after_duplicates = len(df)
    print(
        f"Addresses after removing duplicates: {count_after_duplicates} (dropped {count_before_duplicates - count_after_duplicates})"
    )

    # Remove unnecessary columns and standardize column names
    df.drop("Quest", axis=1, inplace=True)
    df.rename(columns={"UserAddress": "Address"}, inplace=True)

    # Fixed allocation of 180 tokens per participant
    df["Token"] = SOCIALS_ALLOCATION

    # Display total tokens
    print(f"Layer3 Campaign Final Count: {len(df)}")
    print(f"Layer3 Campaign Total Tokens: {df['Token'].sum():,.2f}")
    print(f"Layer3 Campaign Total Tokens: {df['Token'].sum() / TOTAL_SUPPLY:.2%}")

    # Save the processed allocation data
    df.to_csv(LAYER3_OUTPUT_FILE, index=False)


def calculate_galxe_allocations():
    """
    Calculates token allocations for the Galxe campaign.

    Methodology:
    - Equal distribution model where all qualifying participants receive the same allocation
    - Filters for participants with at least 160 points
    - Each participant receives a fixed amount of 180 tokens
    """
    print("--- Processing Galxe Campaign ---")
    # Read and clean data
    df = pd.read_csv(GALXE_FILE)
    initial_count = len(df)
    print(f"Initial addresses: {initial_count}")

    # Convert addresses to checksum format
    df["Wallet_20_Address"] = df["Wallet_20_Address"].apply(
        lambda x: Web3.to_checksum_address(x)
    )

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["Wallet_20_Address"], keep=False)]
    if not duplicates.empty:
        print(f"Duplicate addresses found in Galxe campaign: {len(duplicates)}")
        # print(duplicates[["Wallet_20_Address", "Point"]].sort_values("Wallet_20_Address")) # Optional

    # Remove duplicates keeping the first occurrence
    count_before_duplicates = len(df)
    df = df.drop_duplicates(subset=["Wallet_20_Address"], keep="first")
    count_after_duplicates = len(df)
    print(
        f"Addresses after removing duplicates: {count_after_duplicates} (dropped {count_before_duplicates - count_after_duplicates})"
    )

    # Filter for participants with at least 160 points
    count_before_points_filter = len(df)
    df = df[df["Point"] >= 160]
    count_after_points_filter = len(df)
    print(
        f"Addresses after filtering points < 160: {count_after_points_filter} (dropped {count_before_points_filter - count_after_points_filter})"
    )

    # Fixed allocation of 180 tokens per participant
    df["Token"] = SOCIALS_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"Wallet_20_Address": "Address"}, inplace=True)
    df.drop(["Address_20_Type", "Point", "Ranking"], axis=1, inplace=True)

    # Display total tokens
    print(f"Galxe Campaign Final Count: {len(df)}")
    print(f"Galxe Campaign Total Tokens: {df['Token'].sum():,.2f}")
    print(f"Galxe Campaign Total Tokens: {df['Token'].sum() / TOTAL_SUPPLY:.2%}")

    # Save the processed allocation data
    df.to_csv(GALXE_OUTPUT_FILE, index=False)


def calculate_megaphone_allocations():
    """
    Calculates token allocations for the Megaphone campaign.

    Methodology:
    - Process referral points by:
      1. Subtracting referral points from total points
      2. Capping referral points at 100
      3. Adding back the capped referral points to total points
    - Filter participants with more than 205 points
    - Each participant receives a fixed amount of 180 tokens
    """
    print("--- Processing Megaphone Campaign ---")
    # Read and clean data
    df = pd.read_csv(MEGAPHONE_CAMPAIGN_FILE)
    initial_count = len(df)
    print(f"Initial addresses: {initial_count}")

    # Remove rows with NaN wallet addresses
    count_before_nan_drop = len(df)
    df = df.dropna(subset=["walletAddress"])
    count_after_nan_drop = len(df)
    print(
        f"Addresses after dropping NaN walletAddress: {count_after_nan_drop} (dropped {count_before_nan_drop - count_after_nan_drop})"
    )

    # Convert wallet addresses to string and remove any whitespace
    df["walletAddress"] = df["walletAddress"].astype(str).str.strip()

    # Convert addresses to checksum format
    df["walletAddress"] = df["walletAddress"].apply(
        lambda x: Web3.to_checksum_address(x)
    )

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["walletAddress"], keep=False)]
    if not duplicates.empty:
        print(f"Duplicate addresses found in Megaphone campaign: {len(duplicates)}")
        # print(duplicates[["walletAddress", "totalPoints"]].sort_values("walletAddress")) # Optional

    # Remove duplicates keeping the first occurrence
    count_before_duplicates = len(df)
    df = df.drop_duplicates(subset=["walletAddress"], keep="first")
    count_after_duplicates = len(df)
    print(
        f"Addresses after removing duplicates: {count_after_duplicates} (dropped {count_before_duplicates - count_after_duplicates})"
    )

    # Subtract referralPoints from totalPoints
    df["totalPoints"] = df["totalPoints"] - df["referralPoints"]

    # Cap referralPoints to 100
    df["referralPoints"] = df["referralPoints"].clip(upper=100)

    # Add back capped referralPoints to totalPoints
    df["totalPoints"] = df["totalPoints"] + df["referralPoints"]

    # Filter for participants with more than 205 points
    count_before_points_filter = len(df)
    df = df[df["totalPoints"] > 205]
    count_after_points_filter = len(df)
    print(
        f"Addresses after filtering points <= 205: {count_after_points_filter} (dropped {count_before_points_filter - count_after_points_filter})"
    )

    # Fixed allocation of 180 tokens per participant
    df["token"] = SOCIALS_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"walletAddress": "Address", "token": "Token"}, inplace=True)
    df = df[["Address", "Token"]]

    # Display total tokens
    print(f"Megaphone Campaign Final Count: {len(df)}")
    print(f"Megaphone Campaign Total Tokens: {df['Token'].sum():,.2f}")
    print(f"Megaphone Campaign Total Tokens: {df['Token'].sum() / TOTAL_SUPPLY:.2%}")
    # Save the processed allocation data
    df.to_csv(MEGAPHONE_OUTPUT_FILE, index=False)


def checksum_discord_roles():
    """
    Checksum addresses in the Discord role CSV file.
    """
    print("--- Checksuming Discord Roles ---")
    df = pd.read_csv(DISCORD_FILE)
    df["Address"] = df["Address"].apply(lambda x: Web3.to_checksum_address(x))
    df.to_csv(DISCORD_OUTPUT_FILE, index=False)


def main():
    """
    Main execution function that processes all five campaign allocations.
    """
    calculate_arma_allocations()
    calculate_layer3_allocations()
    calculate_galxe_allocations()
    calculate_megaphone_allocations()
    calculate_community_allocations()
    checksum_discord_roles()


if __name__ == "__main__":
    main()
