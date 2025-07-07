# this script extracts ligand fingerprints from SDF files and saves them to a CSV file.
# It uses RDKit to generate Morgan fingerprints for each ligand.
import os
import csv
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator


# Load a ligand molecule from an SDF file
def load_ligand_mol(sdf_path):
    suppl = Chem.SDMolSupplier(sdf_path)
    mol = next(iter(suppl), None)
    return mol

# Generate a Morgan fingerprint for the molecule
# `radius` is the radius of the fingerprint, and `nBits` is the size of the fingerprint.
# # Default values are set to 2 and 2048, respectively.
def get_fingerprint(mol, radius=2, nBits=2048):
    if mol is None:
        return None
    fpgen = GetMorganGenerator(radius=2, fpSize=2048)
    fp = fpgen.GetFingerprint(mol)
    return fp

# Convert the fingerprint to a list of bits (0s and 1s)
def fingerprint_to_list(fp):
    if fp is None:
        return []
    return list(map(int, fp.ToBitString()))

# Get PDB IDs from ligand SDF files in the specified folder
# The function assumes that the SDF files are named in the format "pdb_id_l
def get_pdb_ids_from_ligand_files(ligand_folder):
    pdb_ids = []
    for filename in os.listdir(ligand_folder):
        if filename.endswith('_ligand.sdf'):
            pdb_id = filename.split('_ligand.sdf')[0]
            pdb_ids.append(pdb_id)
    return pdb_ids

# Extract features from ligand SDF files and save them to a CSV file
# The CSV file will contain the PDB ID and the corresponding fingerprint bits.
def extract_features(ligand_folder, pdb_ids, output_csv):
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['pdb_id'] + [f'fp_{i}' for i in range(2048)])

        for pdb_id in pdb_ids:
            sdf_file = os.path.join(ligand_folder, f"{pdb_id}_ligand.sdf")
            mol = load_ligand_mol(sdf_file)
            fp = get_fingerprint(mol)
            fp_bits = fingerprint_to_list(fp)

            if fp_bits:
                writer.writerow([pdb_id] + fp_bits)
            else:
                print(f"Warning: Could not process {pdb_id}")

# Main function to run the feature extraction
if __name__ == "__main__":
    ligand_dir = "data/demo_v2021/ligands"
    pdb_ids = get_pdb_ids_from_ligand_files(ligand_dir)
    print(f"Found {len(pdb_ids)} ligand files")

    output_file = "data/demo_v2021/ligand_fingerprints.csv"
    extract_features(ligand_dir, pdb_ids, output_file)
    print(f"Ligand fingerprints saved to: {output_file}")
