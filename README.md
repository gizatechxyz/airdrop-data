# Airdrop Data Processing

## Overview

This repository contains scripts to process and calculate token allocations for airdrop campaigns across multiple platforms. The script processes data from five different sources:

1. **ARMA Campaign** - Tier-based allocation system based on points reflecting on-chain activity.
2. **Layer3 Campaign** - Fixed allocation for completing specific quests.
3. **Galxe Campaign** - Fixed allocation for achieving a minimum point threshold.
4. **Megaphone Campaign** - Fixed allocation for social engagement, with referral point capping.
5. **Community Campaign** - Specific allocation for community feedback participants also active on-chain.
6. **Discord Role** - Added in the merging process (source data required separately).

The primary goal of this codebase is to transform raw participation data into fair token allocations, applying various filters and methodologies tailored to each campaign's objectives. A key focus is on **Sybil resistance** – ensuring that allocations primarily reward genuine, active participants rather than potentially automated or low-effort accounts.

## Token Allocation Framework

The total supply for this token distribution is **1,000,000,000** tokens.
The allocation is structured to reward different types of engagement and contribution within the ecosystem:

*   **On-chain Activity (ARMA Campaign):** A significant portion is allocated based on demonstrable on-chain activity and interaction, measured via the ARMA point system. This rewards users actively using the platform.
*   **Social Engagement Campaigns (Layer3, Galxe, Megaphone):** A fixed amount (180 tokens per participant per campaign, subject to specific campaign filters) is dedicated to rewarding participation in social and quest-based campaigns across various platforms. This encourages broader community growth and awareness.
*   **Community Contributions (Community Campaign, Discord Roles):** Specific allocations are reserved for rewarding direct community involvement, such as providing feedback (Community Campaign) or holding designated roles (Discord). This values qualitative contributions and sustained community presence.

The precise token amounts distributed via each campaign are determined by the filtering logic and participation numbers detailed in the Methodology section below. The `merge_data.py` script provides a final summary of the tokens distributed across these categories relative to the total supply.

## Methodology

The following sections detail the specific processing steps and filtering logic applied to each campaign's raw data within `process_data.py`. These steps are designed to clean the data, identify eligible participants based on defined criteria, and mitigate the impact of potential Sybil behavior.

### ARMA Campaign (`calculate_arma_allocations`)
- Uses a tier-based allocation system
- Filters out entries with less than 60 points
- Allocates tokens based on points tiers reflecting on-chain activity levels.
- **Filtering:**
  - **Points Threshold:** Entries with less than 60 points are removed. This establishes a minimum baseline of on-chain activity required for eligibility.
  - **Duplicate Removal:** Duplicate wallet addresses are removed, keeping only the first occurrence. This prevents single entities from receiving multiple allocations from this campaign via the same address.
- Allocates tokens based on points tiers:
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

### Layer3 Campaign (`calculate_layer3_allocations`)
- Rewards completion of specific quests with a fixed allocation.
- **Filtering:**
  - **Cross-Campaign Check (ARMA):** Only participants whose addresses are *also* present in the ARMA leaderboard data are considered eligible. This acts as a Sybil filter, requiring participants to have demonstrated some level of on-chain activity in addition to completing Layer3 quests.
  - **Duplicate Removal:** Duplicate wallet addresses are removed, keeping the first occurrence.
- **Allocation:** Qualifying participants receive a fixed amount of 180 tokens.

### Galxe Campaign (`calculate_galxe_allocations`)
- Rewards participation based on achieving a points threshold.
- **Filtering:**
  - **Duplicate Removal:** Duplicate wallet addresses are removed, keeping the first occurrence.
  - **Points Threshold:** Participants must have accumulated at least 160 points in the Galxe campaign. This sets a minimum engagement level.
- **Allocation:** Qualifying participants receive a fixed amount of 180 tokens.

### Megaphone Campaign (`calculate_megaphone_allocations`)
- Rewards social engagement with adjustments for referral activity.
- **Filtering & Point Adjustment:**
  - **NaN Address Removal:** Entries without a valid wallet address are dropped.
  - **Duplicate Removal:** Duplicate wallet addresses are removed, keeping the first occurrence.
  - **Referral Point Capping:** To prevent excessive rewards solely from referrals (a potential Sybil vector), referral points are capped at 100 before being added back to the participant's base points.
    1. `totalPoints` = `totalPoints` - `referralPoints`
    2. `referralPoints` = min(`referralPoints`, 100)
    3. `totalPoints` = `totalPoints` + `referralPoints` (capped)
  - **Points Threshold:** Participants must have a final `totalPoints` (after referral capping) greater than 205 to qualify.
- **Allocation:** Qualifying participants receive a fixed amount of 180 tokens.

### Community Campaign (`calculate_community_allocations`)
- Rewards specific community contributions (Feedback sprint) from participants also active on-chain.
- **Filtering:**
  - **Cross-Campaign Check (ARMA):** Only participants whose addresses are *also* present in the ARMA leaderboard data are considered eligible. This links community contribution to on-chain activity.
  - **Points Threshold:** Participants must have accumulated at least 100 points in the community campaign.
- **Allocation:** Only participants meeting the above criteria *and* having exactly 300 points receive a fixed allocation of 385 tokens. Others meeting the filter criteria receive 0 from this specific campaign.

### Discord Role
- Data for Discord role holders (address and allocation amount, typically fixed) needs to be provided separately in `./processed/discord_role.csv` before running the merge script.
- This data is directly incorporated during the merge step.

### Data Merging and Finalization (`merge_data.py`)
After processing individual campaigns, `merge_data.py` consolidates all allocations:
- **Aggregation:** It reads the individual `_allocations.csv` files (and `discord_role.csv`) from the `processed/` directory.
- **Outer Join:** Performs an outer merge on the wallet addresses. This ensures that *all* unique addresses across *all* campaigns are included in the final `total_allocations.csv` file.
- **Handling Non-Participation:** Uses `fillna(0)` to replace any `NaN` values that result from the outer join. This means if an address participated in Campaign A but not Campaign B, it will have its allocation from Campaign A and 0 for Campaign B in the final table.
- **Total Calculation:** Sums the allocations from all campaigns for each address into a `Total` column.
- **Output Files:**
  - `total_allocations.csv`: The main output file showing the breakdown per campaign and the total allocation for every unique participating address.
  - `eligibility.json`: A helper file mapping each address to boolean flags indicating whether they qualified for allocations under the broad categories of ARMA, Socials (Layer3, Galxe, Megaphone), and Community (Community campaign, Discord).

## Data Processing Features

- **Checksum Address Handling**: All Ethereum addresses are converted to checksum format for consistency and validation
- **Duplicate Detection**: Identifies and handles duplicate addresses in each campaign
- **Data Validation**: Ensures data integrity through various checks and transformations
- **Transparent Reporting**: Displays token totals and duplicate addresses for verification
- **Eligibility Mapping**: Creates a JSON mapping of addresses to their eligibility status across categories

## Directory Structure

```
.
├── data/                  # Input data files
│   ├── arma_leaderboard.csv
│   ├── layer3_campaign.csv
│   ├── galxe_campaign.csv
│   ├── megaphone_campaign.csv
│   └── community_campaign.csv
├── processed/             # Output allocation files
│   ├── arma_allocations.csv
│   ├── layer3_allocations.csv
│   ├── galxe_allocations.csv
│   ├── megaphone_allocations.csv
│   ├── community_allocations.csv
│   ├── discord_role.csv
│   ├── total_allocations.csv
│   └── eligibility.json
├── process_data.py        # Main processing script
├── merge_data.py          # Script to combine all allocations
├── pyproject.toml         # Python project dependencies
├── uv.lock                # Lock file for uv package manager
└── README.md              # This documentation
```

## Requirements

- Python 3.13 or higher (as specified in pyproject.toml)
- pandas 2.2.3 or higher
- numpy (used in the scripts)
- web3 (for Ethereum address handling)
- eth-utils (for Ethereum address handling)
- matplotlib (for potential visualization)
- uv (Python package manager)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/airdrop-data.git
   cd airdrop-data
   ```

2. This project uses `uv` for dependency management. If you don't have `uv` installed, you can install it following the instructions at [uv.io](https://github.com/astral-sh/uv).

3. Set up the environment and install dependencies using `uv`:
   ```bash
   # Create and activate a virtual environment
   uv venv

   # Install dependencies from pyproject.toml
   uv pip sync
   ```

## Usage

### Processing Individual Campaign Data

1. Ensure your data files are placed in the `data/` directory with the correct filenames:
   - `arma_leaderboard.csv`
   - `layer3_campaign.csv`
   - `galxe_campaign.csv`
   - `megaphone_campaign.csv`
   - `community_campaign.csv`

2. Run the processing script using `uv`:
   ```bash
   uv run process_data.py
   ```

3. The processed allocation files will be generated in the `processed/` directory:
   - `arma_allocations.csv`
   - `layer3_allocations.csv`
   - `galxe_allocations.csv`
   - `megaphone_allocations.csv`
   - `community_allocations.csv`

4. The script will display:
   - Total tokens allocated for each campaign
   - Any duplicate addresses found (if any)
   - Processing status and completion

### Merging Allocations

After processing the individual campaign data, you can merge the allocations into a single comprehensive file:

1. Ensure you have the `discord_role.csv` file in the `processed/` directory.

2. Run the merge script using `uv`:
   ```bash
   uv run merge_data.py
   ```

3. This will create consolidated files in the `processed/` directory:
   - `total_allocations.csv` - Combined allocations from all campaigns
   - `eligibility.json` - Mapping of addresses to their eligibility status

