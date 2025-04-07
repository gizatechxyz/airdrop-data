import pandas as pd
import numpy as np
from web3 import Web3

# Input data files
ARMA_FILE = "./data/arma_leaderboard.csv"
MARKETING_FILE = "./data/marketing_campaign.csv"
LAYER3_FILE = "./data/layer3_campaign.csv"
GALXE_FILE = "./data/galxe_campaign.csv"
MEGAPHONE_CAMPAIGN_FILE = "./data/megaphone_campaign.csv"

# Output allocation files
ARMA_OUTPUT_FILE = "./processed/arma_allocations.csv"
LAYER3_OUTPUT_FILE = "./processed/layer3_allocations.csv"
GALXE_OUTPUT_FILE = "./processed/galxe_allocations.csv"
MEGAPHONE_OUTPUT_FILE = "./processed/megaphone_allocations.csv"
MARKETING_OUTPUT_FILE = "./processed/marketing_allocations.csv"

# Token allocation constants
ARMA_ALLOCATION = 15_000_000  # 1.5% of total supply
LAYER3_ALLOCATION = 2_500_000  # 0.25% of total supply
GALXE_ALLOCATION = 2_500_000  # 0.25% of total supply
MEGAPHONE_ALLOCATION = 2_500_000  # 0.25% of total supply


def calculate_arma_allocations():
    """
    Calculates token allocations for the ARMA campaign.

    Methodology:
    1. Merge entries from main ARMA file and extra file, adding points for matching EOAs
    2. Apply square root transformation to raw points to reduce the gap between top and bottom participants
    3. Calculate each participant's proportion of the total transformed points
    4. Distribute the ARMA_ALLOCATION proportionally based on the transformed points

    This square root transformation ensures a more equitable distribution by reducing the impact of
    extremely high scores while still rewarding higher participation.
    """
    # Read and clean data
    df = pd.read_csv(ARMA_FILE)

    # Convert addresses to checksum format
    df["eoa"] = df["eoa"].apply(lambda x: Web3.to_checksum_address(x))

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["eoa"], keep=False)]
    if not duplicates.empty:
        print("\nDuplicate addresses found in ARMA campaign:")
        print(duplicates[["eoa", "points"]].sort_values("eoa"))

    # Remove duplicates keeping the first occurrence
    df = df.drop_duplicates(subset=["eoa"], keep="first")

    # Calculate square root of points
    df["sqrt_points"] = np.sqrt(df["points"])

    # Calculate total transformed points
    total_sqrt_points = df["sqrt_points"].sum()

    # Calculate token allocation for each user based on their proportion of transformed points
    df["Token"] = (df["sqrt_points"] / total_sqrt_points) * ARMA_ALLOCATION

    # Assert results are correct
    assert round(df["Token"].sum()) == ARMA_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"eoa": "Address"}, inplace=True)
    df.drop("points", axis=1, inplace=True)
    df.drop("sqrt_points", axis=1, inplace=True)

    # Display total tokens
    print(f"\nARMA Campaign Total Tokens: {df['Token'].sum():,.2f}")

    # Save the processed allocation data
    df.to_csv(ARMA_OUTPUT_FILE, index=False)


def calculate_marketing_allocations():
    """
    Calculates token allocations for the marketing campaign.
    From the Feedback sprint and the oasis gathering
    - 1200 tokens for 100+ points
    - 2400 tokens for 300+ points
    People had to be in the ARMA data to get the tokens

    Methodology:
    - Filter addresses that exist in ARMA data
    - Allocate tokens based on points thresholds:
        * 1200 tokens for participants with 100+ points
        * 2400 tokens for participants with 300+ points
    - Save results to MARKETING_OUTPUT_FILE
    """
    # Read input data
    df = pd.read_csv(MARKETING_FILE)
    df_arma = pd.read_csv(ARMA_FILE)

    # Convert addresses to checksum format
    df["eoa"] = df["eoa"].apply(lambda x: Web3.to_checksum_address(x))
    df_arma["eoa"] = df_arma["eoa"].apply(lambda x: Web3.to_checksum_address(x))

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["eoa"], keep=False)]
    if not duplicates.empty:
        print("\nDuplicate addresses found in Marketing campaign:")
        print(duplicates[["eoa", "points"]].sort_values("eoa"))

    # Remove duplicates keeping the first occurrence
    df = df.drop_duplicates(subset=["eoa"], keep="first")

    # Filter marketing addresses that exist in ARMA data and create a copy
    filtered_df = df[df["eoa"].isin(df_arma["eoa"])].copy()

    # Initialize Token column and allocate based on points thresholds
    filtered_df["Token"] = 0
    filtered_df.loc[filtered_df["points"] >= 100, "Token"] = 1200
    filtered_df.loc[filtered_df["points"] >= 300, "Token"] = 2400

    # Clean up and standardize column names
    filtered_df = filtered_df[["eoa", "Token"]]
    filtered_df.rename(columns={"eoa": "Address"}, inplace=True)

    # Display total tokens
    print(f"\nMarketing Campaign Total Tokens: {filtered_df['Token'].sum():,.2f}")

    # Save the processed allocation data
    filtered_df.to_csv(MARKETING_OUTPUT_FILE, index=False)

    return filtered_df


def calculate_layer3_allocations():
    """
    Calculates token allocations for the Layer3 campaign.

    Methodology:
    - Equal distribution model where all qualifying participants receive the same allocation
    - The total LAYER3_ALLOCATION is divided equally among all participants

    This is a simple, fair approach when participation itself is the primary metric
    and we want to encourage broad community engagement.
    """
    # Read and clean data
    df = pd.read_csv(LAYER3_FILE)

    # Convert addresses to checksum format
    df["UserAddress"] = df["UserAddress"].apply(lambda x: Web3.to_checksum_address(x))

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["UserAddress"], keep=False)]
    if not duplicates.empty:
        print("\nDuplicate addresses found in Layer3 campaign:")
        print(duplicates[["UserAddress", "Quest"]].sort_values("UserAddress"))

    # Remove duplicates keeping the first occurrence
    df = df.drop_duplicates(subset=["UserAddress"], keep="first")

    # Remove unnecessary columns and standardize column names
    df.drop("Quest", axis=1, inplace=True)
    df.rename(columns={"UserAddress": "Address"}, inplace=True)

    # Calculate per-address allocation
    allocation = LAYER3_ALLOCATION / len(df)
    df["Token"] = allocation

    # Verify the total allocation
    assert df["Token"].sum() == LAYER3_ALLOCATION

    # Display total tokens
    print(f"\nLayer3 Campaign Total Tokens: {df['Token'].sum():,.2f}")

    # Save the processed allocation data
    df.to_csv(LAYER3_OUTPUT_FILE, index=False)


def calculate_galxe_allocations():
    """
    Calculates token allocations for the Galxe campaign.

    Methodology:
    1. Apply square root transformation to points to create a more equitable distribution
    2. Calculate each participant's proportion of the total transformed points
    3. Distribute the GALXE_ALLOCATION proportionally based on the transformed points

    Similar to the ARMA allocation strategy, this transformation reduces the impact of
    extremely high scores while still rewarding higher participation.
    """
    # Read and clean data
    df = pd.read_csv(GALXE_FILE)

    # Convert addresses to checksum format
    df["Wallet_20_Address"] = df["Wallet_20_Address"].apply(
        lambda x: Web3.to_checksum_address(x)
    )

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["Wallet_20_Address"], keep=False)]
    if not duplicates.empty:
        print("\nDuplicate addresses found in Galxe campaign:")
        print(
            duplicates[["Wallet_20_Address", "Point"]].sort_values("Wallet_20_Address")
        )

    # Remove duplicates keeping the first occurrence
    df = df.drop_duplicates(subset=["Wallet_20_Address"], keep="first")

    # Filter for participants with at least 150 points
    df = df[df["Point"] >= 150]

    # Apply square root transformation to points
    df["sqrt_points"] = np.sqrt(df["Point"])

    # Calculate total transformed points
    total_sqrt_points = df["sqrt_points"].sum()

    # Calculate proportional token allocation
    df["Token"] = (df["sqrt_points"] / total_sqrt_points) * GALXE_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"Wallet_20_Address": "Address"}, inplace=True)
    df.drop(
        ["Address_20_Type", "Point", "Ranking", "sqrt_points"], axis=1, inplace=True
    )

    # Display total tokens
    print(f"\nGalxe Campaign Total Tokens: {df['Token'].sum():,.2f}")

    # Save the processed allocation data
    df.to_csv(GALXE_OUTPUT_FILE, index=False)


def calculate_megaphone_allocations():
    # Read and clean data
    df = pd.read_csv(MEGAPHONE_CAMPAIGN_FILE)

    # Remove rows with NaN wallet addresses
    df = df.dropna(subset=["walletAddress"])

    # Convert wallet addresses to string and remove any whitespace
    df["walletAddress"] = df["walletAddress"].astype(str).str.strip()

    # Convert addresses to checksum format
    df["walletAddress"] = df["walletAddress"].apply(
        lambda x: Web3.to_checksum_address(x)
    )

    # Check for duplicates
    duplicates = df[df.duplicated(subset=["walletAddress"], keep=False)]
    if not duplicates.empty:
        print("\nDuplicate addresses found in Megaphone campaign:")
        print(duplicates[["walletAddress", "totalPoints"]].sort_values("walletAddress"))

    # Remove duplicates keeping the first occurrence
    df = df.drop_duplicates(subset=["walletAddress"], keep="first")

    # Filter for participants with at least 200 points
    df = df[df["totalPoints"] >= 200]

    # Apply square root transformation to points
    df["sqrt_points"] = np.sqrt(df["totalPoints"])

    # Calculate total transformed points
    total_sqrt_points = df["sqrt_points"].sum()

    # Calculate proportional token allocation
    df["token"] = (df["sqrt_points"] / total_sqrt_points) * MEGAPHONE_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"walletAddress": "Address", "token": "Token"}, inplace=True)
    df = df[["Address", "Token"]]

    # Display total tokens
    print(f"\nMegaphone Campaign Total Tokens: {df['Token'].sum():,.2f}")

    # Save the processed allocation data
    df.to_csv(MEGAPHONE_OUTPUT_FILE, index=False)


def main():
    """
    Main execution function that processes all three campaign allocations.
    """
    calculate_layer3_allocations()
    calculate_arma_allocations()
    calculate_galxe_allocations()
    calculate_marketing_allocations()
    calculate_megaphone_allocations()


if __name__ == "__main__":
    main()
