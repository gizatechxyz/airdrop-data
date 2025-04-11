# Airdrop Data Processing

## Overview

This repository contains scripts to process and calculate token allocations for airdrop campaigns across multiple platforms. The script processes data from five different sources:

1. **ARMA Campaign** - Tier-based allocation system
2. **Layer3 Campaign** - Fixed allocation of 180 tokens per participant 
3. **Galxe Campaign** - Fixed allocation of 180 tokens per participant
4. **Megaphone Campaign** - Fixed allocation of 180 tokens per participant
5. **Community Campaign** - Fixed allocation of 385 tokens for specific participants
6. **Discord Role** - Added in the merging process

The purpose of this codebase is to transform raw participation data into fair token allocations using different distribution methodologies tailored to each campaign's objectives.

## Methodology

### ARMA Campaign
- Uses a tier-based allocation system
- Filters out entries with less than 60 points
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

### Layer3 Campaign
- Implements an equal distribution model
- All qualifying participants receive a fixed allocation of 180 tokens
- Focuses on rewarding participation itself rather than relative performance

### Galxe Campaign
- Equal distribution among qualifying participants
- Filters for participants with at least 160 points
- Each participant receives a fixed amount of 180 tokens
- Removes duplicates and standardizes data format

### Megaphone Campaign
- Equal distribution among qualifying participants (180 tokens each)
- Processes referral points by:
  1. Subtracting referral points from total points
  2. Capping referral points at 100
  3. Adding back the capped referral points to total points
- Filters for participants with more than 205 points

### Community Campaign
- Only considers participants from the Feedback sprint, not the oasis gathering
- Filters for participants who exist in the ARMA data
- Filters for participants with at least 100 points
- Allocates 385 tokens for participants with exactly 300 points

### Discord Role
- Added during the merge process
- Processed in merge_data.py and included in the final allocation

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

