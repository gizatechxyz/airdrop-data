from dataclasses import dataclass
from pathlib import Path
import csv
from typing import List, Tuple
import json
from multiproof import StandardMerkleTree
from eth_utils import is_checksum_address, to_checksum_address


@dataclass
class AirdropConfig:
    input_file: Path
    output_file: Path
    proof_file: Path


class AirdropMerkleGenerator:
    def __init__(self, config: AirdropConfig):
        self.config = config
        self.tree = None

    def read_airdrop_data(self) -> List[Tuple[str, int]]:
        """Read and parse the airdrop CSV file."""
        if not self.config.input_file.exists():
            raise FileNotFoundError(f"Airdrop file not found: {self.config.input_file}")

        values: List[Tuple[str, int]] = []
        seen_addresses = set()
        with open(self.config.input_file, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    address = row[0]
                    # Validate and convert to checksum address
                    if not is_checksum_address(address):
                        try:
                            address = to_checksum_address(address)
                        except ValueError as e:
                            raise ValueError(
                                f"Invalid Ethereum address format: {address}"
                            ) from e

                    # Check for duplicate addresses
                    if address in seen_addresses:
                        raise ValueError(f"Duplicate address found in CSV: {address}")
                    seen_addresses.add(address)

                    # Validate amount
                    try:
                        amount = int(row[1])
                        if amount < 0:
                            raise ValueError(
                                f"Amount must be non-negative, got: {amount}"
                            )
                        if not str(amount).isdigit():
                            raise ValueError(
                                f"Amount must be a whole number, got: {row[1]}"
                            )
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid amount format in row {row}: {str(e)}"
                        ) from e

                    values.append((address, amount))
                except (IndexError, ValueError) as e:
                    raise ValueError(f"Invalid row format in CSV: {row}") from e
        return values

    def generate_tree(self, values: List[Tuple[str, int]]) -> StandardMerkleTree:
        """Generate the Merkle tree from the provided values."""
        return StandardMerkleTree.of(values, ["address", "uint256"])

    def save_tree(self, tree: StandardMerkleTree) -> None:
        """Save the Merkle tree to a JSON file."""
        with open(self.config.output_file, "w") as file:
            json.dump(tree.to_json(), file, indent=2)

    def generate_proof(self, tree: StandardMerkleTree) -> None:
        """Generate the Merkle proof for each value in the tree."""
        output = []
        for i, leaf in enumerate(tree.values):
            proof = tree.get_proof(i)
            output.append(
                {"address": leaf.value[0], "amount": leaf.value[1], "proof": proof}
            )
        with open(self.config.proof_file, "w") as file:
            json.dump(output, file, indent=2)

    def process(self) -> str:
        """Process the airdrop data and return the Merkle root."""
        values = self.read_airdrop_data()
        tree = self.generate_tree(values)
        self.save_tree(tree)
        self.generate_proof(tree)
        return tree.root


def main() -> None:
    config = AirdropConfig(
        input_file=Path("./processed/total_allocations_for_merkle.csv"),
        output_file=Path("./airdrop_proof/tree.json"),
        proof_file=Path("./airdrop_proof/proof.json"),
    )

    generator = AirdropMerkleGenerator(config)
    try:
        root = generator.process()
        print(f"Merkle root: {root}")
    except Exception as e:
        print(f"Error processing airdrop: {e}")
        raise


if __name__ == "__main__":
    main()
