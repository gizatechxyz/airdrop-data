import pandas as pd
import numpy as np
import json

# Output files from processing scripts
TOTAL_ALLOCATIONS_FILE = "./processed/total_allocations.csv"
FINAL_PROOF = "./airdrop_proof/proof.json"
TOTAL_SUPPLY = 1_000_000_000

# Read the total allocations file
total_allocations = pd.read_csv(TOTAL_ALLOCATIONS_FILE)


def print_summary():
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


def verify_proof():
    """
    Verify the proof of the merkle tree.
    """
    print("--- Verifying Proof ---")

    # Get total from allocations file
    allocations_data = pd.read_csv(TOTAL_ALLOCATIONS_FILE)
    allocations_total = allocations_data["Total"].sum()

    # Get total from proof file
    try:
        with open(FINAL_PROOF, "r") as f:
            proof_data = json.load(f)

        # The proof is an array of objects with address and amount
        proof_total_wei = sum(int(entry["amount"]) for entry in proof_data)

        # Convert from wei (10^18) to tokens
        proof_total = proof_total_wei / 10**18

    except Exception as e:
        print(f"Error reading proof file: {e}")
        proof_total = 0

    # Print comparison
    print(f"Total in allocations file: {allocations_total:,.0f}")
    print(f"Total in proof file: {proof_total:,.0f}")

    # Check if they match
    if abs(allocations_total - proof_total) < 1:  # Allow for small rounding errors
        print("✅ Totals match!")
    else:
        print(
            f"❌ Totals do not match! Difference: {abs(allocations_total - proof_total):,.0f}"
        )

    # Verify individual address allocations
    print("\n--- Verifying Individual Address Allocations ---")

    # Create dictionaries for both datasets
    allocations_dict = dict(zip(allocations_data["Address"], allocations_data["Total"]))
    proof_dict = {
        entry["address"]: int(entry["amount"]) / 10**18 for entry in proof_data
    }

    # Compare number of addresses
    allocations_count = len(allocations_dict)
    proof_count = len(proof_dict)

    print(f"Number of addresses in allocations file: {allocations_count}")
    print(f"Number of addresses in proof file: {proof_count}")

    if allocations_count == proof_count:
        print("✅ Number of addresses match!")
    else:
        print(
            f"❌ Number of addresses do not match! Difference: {abs(allocations_count - proof_count)}"
        )

    # Find addresses that are in allocations but not in proof
    allocations_only = set(allocations_dict.keys()) - set(proof_dict.keys())
    if allocations_only:
        print(
            f"\n❌ Found {len(allocations_only)} addresses in allocations but not in proof."
        )
        if len(allocations_only) <= 5:
            for addr in allocations_only:
                print(f"  {addr}: {allocations_dict[addr]}")
        else:
            print(f"  First 5: {list(allocations_only)[:5]}")
    else:
        print("\n✅ All addresses in allocations are also in proof!")

    # Find addresses that are in proof but not in allocations
    proof_only = set(proof_dict.keys()) - set(allocations_dict.keys())
    if proof_only:
        print(
            f"\n❌ Found {len(proof_only)} addresses in proof but not in allocations."
        )
        if len(proof_only) <= 5:
            for addr in proof_only:
                print(f"  {addr}: {proof_dict[addr]}")
        else:
            print(f"  First 5: {list(proof_only)[:5]}")
    else:
        print("\n✅ All addresses in proof are also in allocations!")

    # Verify individual amounts
    print("\n--- Verifying Individual Amounts ---")
    mismatches = []
    for address, alloc_amount in allocations_dict.items():
        if address in proof_dict:
            proof_amount = proof_dict[address]
            if (
                abs(alloc_amount - proof_amount) > 0.001
            ):  # Small tolerance for floating point errors
                mismatches.append((address, alloc_amount, proof_amount))

    if mismatches:
        print(f"❌ Found {len(mismatches)} addresses with mismatched amounts!")
        print("\nFirst 5 mismatches:")
        for address, alloc_amount, proof_amount in mismatches[:5]:
            print(
                f"  {address}: Allocations={alloc_amount}, Proof={proof_amount}, Diff={alloc_amount-proof_amount}"
            )
    else:
        print("✅ All individual address amounts match between files!")


def main():
    print_summary()
    verify_proof()


if __name__ == "__main__":
    main()
