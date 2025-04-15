import pandas as pd
import numpy as np
import json

# Output files from processing scripts
TOTAL_ALLOCATIONS_FILE = "./processed/total_allocations.csv"
TOTAL_SUPPLY = 1_000_000_000

# Read the total allocations file
total_allocations = pd.read_csv(TOTAL_ALLOCATIONS_FILE)

# Print summary of the data
print(f"Total unique addresses: {len(total_allocations)}")

# Calculate and display the sum of allocations for each campaign
campaign_sums = {
    "ARMA": total_allocations["ARMA"].sum(),
    "Layer3": total_allocations["Layer3"].sum(),
    "Galxe": total_allocations["Galxe"].sum(),
    "Community": total_allocations["Community"].sum(),
    "Discord": total_allocations["Discord"].sum(),
    "Megaphone": total_allocations["Megaphone"].sum(),
    "Total": total_allocations["Total"].sum(),
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
