# this script parses a binding affinity index file and converts the binding values to nanomolar (nM) units.
import re
import csv

# function to convert binding values to nanomolar (nM) for consistency
def convert_to_nM(value, unit): 
    unit = unit.lower()
    factors = {'pm': 0.001, 'nm': 1, 'um': 1000, 'μm': 1000, 'mm': 1_000_000}
    return value * factors.get(unit, 1) 

# load the index file and parse the binding affinity data
# returns a list of tuples with the parsed data 
def load_index(index_path):
    data = []
    with open(index_path, 'r') as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split()
            pdb_id = parts[0]
            resolution = float(parts[1])
            year = int(parts[2])
            binding_info = parts[3]
            match = re.match(r"(Kd|Ki|IC50)=(\d*\.?\d+)([munp]?M)", binding_info, re.IGNORECASE)
            if match:
                binding_type = match.group(1)
                binding_val = float(match.group(2))
                unit = match.group(3)
                binding_val_nM = convert_to_nM(binding_val, unit)
            else:
                binding_type = binding_val = unit = binding_val_nM = None

            ligand_match = re.search(r'\(([^)]+)\)', line)
            ligand_name = ligand_match.group(1) if ligand_match else None

            data.append((pdb_id, resolution, year, binding_type, binding_val, unit, binding_val_nM, ligand_name))
    return data

# save the parsed data to a CSV file
def save_to_csv(data, csv_path):
    header = ['pdb_id', 'resolution', 'year', 'binding_type', 'binding_value', 'unit', 'binding_value_nM', 'ligand_name']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


# specifying the main function to run the script
# this will load the index file and save the parsed data to a CSV file
if __name__ == "__main__":
    index_file = "data/demo_v2021/index/INDEX_demo_PL_data.2021"
    csv_output = "data/demo_v2021/parsed_binding_data.csv"

    entries = load_index(index_file)
    save_to_csv(entries, csv_output)
    print(f"Saved {len(entries)} entries to {csv_output}")


