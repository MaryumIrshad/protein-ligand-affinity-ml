# this script combines ligand fingerprints with binding affinity data
# to create a dataset suitable for machine learning tasks.
import csv

# loads the binding affinity data from a CSV file
# The CSV file is expected to have columns 'pdb_id' and 'binding_value_nM'.
def load_binding_data(binding_csv):
    data = {}
    with open(binding_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdb_id = row['pdb_id']
            binding_nM = row['binding_value_nM']
            if binding_nM: # Ensure binding value is not empty
                data[pdb_id] = float(binding_nM)
    return data

# combines the ligand fingerprints with binding affinity data
def combine_fingerprints_with_binding(fp_csv, binding_dict, output_csv):
    with open(fp_csv, 'r') as f_in, open(output_csv, 'w', newline='') as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        header = next(reader)
        writer.writerow(header + ['binding_nM'])

        for row in reader:
            pdb_id = row[0]
            if pdb_id in binding_dict:
                writer.writerow(row + [binding_dict[pdb_id]])

if __name__ == "__main__":
    binding_csv = "data/demo_v2021/parsed_binding_data.csv"
    fp_csv = "data/demo_v2021/ligand_fingerprints.csv"
    output_csv = "data/demo_v2021/ml_dataset.csv"

    binding_dict = load_binding_data(binding_csv)
    combine_fingerprints_with_binding(fp_csv, binding_dict, output_csv)

    print(f"Combined dataset saved to {output_csv}")
