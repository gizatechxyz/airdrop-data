import pandas as pd
import numpy as np

# Input data files
ARMA_FILE = "./data/arma_leaderboard.csv"
LAYER3_FILE = "./data/layer3_campaign.csv"
GALXE_FILE = "./data/galxe_campaign.csv"

# Output allocation files
ARMA_OUTPUT_FILE = "./processed/arma_allocations.csv"
LAYER3_OUTPUT_FILE = "./processed/layer3_allocations.csv"
GALXE_OUTPUT_FILE = "./processed/galxe_allocations.csv"

# Token allocation constants
ARMA_ALLOCATION = 15_000_000  # 1.5% of total supply
LAYER3_ALLOCATION = 2_500_000  # 0.25% of total supply
GALXE_ALLOCATION = 5_000_000  # 0.5% of total supply


def calculate_arma_allocations():
    """
    Calculates token allocations for the ARMA campaign.

    Methodology:
    1. Apply square root transformation to raw points to reduce the gap between top and bottom participants
    2. Calculate each participant's proportion of the total transformed points
    3. Distribute the ARMA_ALLOCATION proportionally based on the transformed points

    This square root transformation ensures a more equitable distribution by reducing the impact of
    extremely high scores while still rewarding higher participation.
    """
    df = pd.read_csv(ARMA_FILE)

    # Calculate square root of points - this transformation reduces the disparity between high and low scores
    df["sqrt_points"] = np.sqrt(df["points"])

    # Calculate total transformed points
    total_sqrt_points = df["sqrt_points"].sum()

    # Calculate token allocation for each user based on their proportion of transformed points
    df["Token"] = (df["sqrt_points"] / total_sqrt_points) * ARMA_ALLOCATION

    # Assert results are correct - total allocation should match the predefined amount
    assert df["Token"].sum() == ARMA_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"eoa": "Address"}, inplace=True)
    df.drop("points", axis=1, inplace=True)
    df.drop("rank", axis=1, inplace=True)
    df.drop("sqrt_points", axis=1, inplace=True)

    # Save the processed allocation data
    df.to_csv(ARMA_OUTPUT_FILE, index=False)


def calculate_layer3_allocations():
    """
    Calculates token allocations for the Layer3 campaign.

    Methodology:
    - Equal distribution model where all qualifying participants receive the same allocation
    - The total LAYER3_ALLOCATION is divided equally among all participants

    This is a simple, fair approach when participation itself is the primary metric
    and we want to encourage broad community engagement.
    """
    df = pd.read_csv(LAYER3_FILE)

    # Remove unnecessary columns and standardize column names
    df.drop("Quest", axis=1, inplace=True)
    df.rename(columns={"UserAddress": "Address"}, inplace=True)

    # Calculate per-address allocation by dividing total allocation by number of participants
    allocation = LAYER3_ALLOCATION / len(df)
    df["Token"] = allocation

    # Verify the total allocation matches the predefined amount
    assert df["Token"].sum() == LAYER3_ALLOCATION

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
    df = pd.read_csv(GALXE_FILE)

    # Apply square root transformation to points
    df["sqrt_points"] = np.sqrt(df["Point"])

    # Calculate total transformed points
    total_sqrt_points = df["sqrt_points"].sum()

    # Calculate proportional token allocation based on transformed points
    df["token"] = (df["sqrt_points"] / total_sqrt_points) * GALXE_ALLOCATION

    # Clean up and standardize column names
    df.rename(columns={"Wallet_20_Address": "Address"}, inplace=True)
    df.drop("Address_20_Type", axis=1, inplace=True)
    df.drop("Point", axis=1, inplace=True)
    df.drop("Ranking", axis=1, inplace=True)
    df.drop("sqrt_points", axis=1, inplace=True)

    # Save the processed allocation data
    df.to_csv(GALXE_OUTPUT_FILE, index=False)


def main():
    """
    Main execution function that processes all three campaign allocations.
    """
    calculate_layer3_allocations()
    calculate_arma_allocations()
    calculate_galxe_allocations()


if __name__ == "__main__":
    main()
