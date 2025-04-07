# Airdrop Data Processing

## Overview

This repository contains scripts to process and calculate token allocations for airdrop campaigns across multiple platforms. The script processes data from five different sources:

1. **ARMA Campaign** - 15,000,000 tokens (1.5% of total supply)
2. **Layer3 Campaign** - 2,500,000 tokens (0.25% of total supply)
3. **Galxe Campaign** - 2,500,000 tokens (0.25% of total supply)
4. **Megaphone Campaign** - 2,500,000 tokens (0.25% of total supply)
5. **Marketing Campaign** - Variable allocation based on participation tiers

The purpose of this codebase is to transform raw participation data into fair token allocations using different distribution methodologies tailored to each campaign's objectives.

## Methodology

### ARMA Campaign
- Uses a square root transformation on points to reduce the gap between high and low performers
- Allocates tokens proportionally based on transformed points
- This approach rewards higher participation while preventing excessive concentration

### Layer3 Campaign
- Implements an equal distribution model
- All qualifying participants receive the same allocation
- Focuses on rewarding participation itself rather than relative performance

### Galxe Campaign
- Similar to ARMA, uses a square root transformation on points
- Filters for participants with at least 150 points
- Proportionally distributes tokens based on transformed points
- Balances reward for participation while reducing extreme concentration

### Megaphone Campaign
- Uses a square root transformation on points
- Filters for participants with at least 200 points
- Proportionally distributes tokens based on transformed points

### Marketing Campaign
- Two-tier allocation system:
  - 1,200 tokens for participants with 100+ points
  - 2,400 tokens for participants with 300+ points
- Only participants who exist in the ARMA data are eligible

## Data Processing Features

- **Checksum Address Handling**: All Ethereum addresses are converted to checksum format for consistency and validation
- **Duplicate Detection**: Identifies and handles duplicate addresses in each campaign
- **Data Validation**: Ensures data integrity through various checks and transformations
- **Transparent Reporting**: Displays token totals and duplicate addresses for verification

## Directory Structure

```
.
├── data/                  # Input data files
│   ├── arma_leaderboard.csv
│   ├── layer3_campaign.csv
│   ├── galxe_campaign.csv
│   ├── megaphone_campaign.csv
│   └── marketing_campaign.csv
├── processed/             # Output allocation files
│   ├── arma_allocations.csv
│   ├── layer3_allocations.csv
│   ├── galxe_allocations.csv
│   ├── megaphone_allocations.csv
│   ├── marketing_allocations.csv
│   └── total_allocations.csv
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
   - `marketing_campaign.csv`

2. Run the processing script using `uv`:
   ```bash
   uv run process_data.py
   ```

3. The processed allocation files will be generated in the `processed/` directory:
   - `arma_allocations.csv`
   - `layer3_allocations.csv`
   - `galxe_allocations.csv`
   - `megaphone_allocations.csv`
   - `marketing_allocations.csv`

4. The script will display:
   - Total tokens allocated for each campaign
   - Any duplicate addresses found (if any)
   - Processing status and completion

### Merging Allocations

After processing the individual campaign data, you can merge the allocations into a single comprehensive file:

1. Run the merge script using `uv`:
   ```bash
   uv run merge_data.py
   ```

2. This will create a consolidated file in the `processed/` directory:
   - `total_allocations.csv`

