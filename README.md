# Protein-ligand Binding Affinity Prediction

This min-project aims to predict protein-ligand binding affinity using machine learning models trained on molecular fingerprints derived from ligand structures. The goal is to showcase practical ML skills applied to cheminformatics and regression tasks.
 

## Project Structure 
- `data/`: raw and processed datasets  
- `src/`: Python scripts for data processing and modeling 
- `results/`: plots and model output scores

---

## Step-by-step Workflow

1. **Data Download & Parsing**  
   - Dowloaded demo sample of ligand-protein binding data from PDBbind+ (https://www.pdbbind-plus.org.cn/download).
   - This data package includes 285 protein-ligand complexes: protein and pocket `.pdb` files, and ligands `.sdf` and `.mol2` files.
   - Parsed the Index files (INDEX_demo_PL_data.2021) to extract:
   ```
   pdb_id,resolution,year,binding_type,binding_value,unit,binding_value_nM,ligand_name
   ```
   - While parsing the data, all binding affinity values were converted to **nM** for consistency. 

2. **Feature Extraction: Morgan Fingerprints**  
   - Computed **Morgan fingerprints** using RDKit from ligand `.sdf` files.  
   - Morgan fingerprints encode molecular substructures into fixed-length binary vectors that are ML-friendly.

3. **Dataset Preparation**  
   - Final dataset includes:
     - PDB IDs  
     - 2048-bit Morgan fingerprint vectors  
     - Binding affinity values in nM  
   - Dataset split into training and testing sets.

4. **Model Training and Evaluation**  
   - Trained regression models:
     - Random Forest  
     - Ridge Regression  
     - Lasso Regression  
     - Support Vector Regression (SVR)  
     - XGBoost  
     - LightGBM  
   - Evaluated using: **MSE**, **RMSE**, **MAE**, and **R²**


---

## What Are Morgan Fingerprints and Why Use Them?

Morgan fingerprints are circular fingerprints that represent chemical environments around each atom. They encode the molecular structure into a binary vector, making them suitable for machine learning.

They are widely used in drug discovery for:
- Virtual screening  
- Molecular similarity comparison  
- QSAR modeling

---

## Machine Learning Models Summary

- **Random Forest:** Ensemble of decision trees reducing overfitting and capturing nonlinearities.  
- **Ridge Regression:** Linear regression with L2 regularization to prevent overfitting.  
- **Lasso Regression:** Linear regression with L1 regularization performing feature selection.  
- **Support Vector Regression (SVR):** Uses support vectors with a margin to model nonlinear relationships.  
- **XGBoost:** Gradient boosting framework building trees sequentially to minimize errors.  
- **LightGBM:** Optimized gradient boosting method designed for speed and efficiency.

---

## Results and Observations

| Model         | MSE    | RMSE   | MAE    | R²     |
|---------------|--------|--------|--------|--------|
| Random Forest | 3.3494 | 1.8301 | 1.5120 | 0.2412 |
| Ridge         | 2.9292 | 1.7115 | 1.4877 | 0.3364 |
| Lasso         | 4.0191 | 2.0048 | 1.6370 | 0.0895 |
| SVR           | 3.0648 | 1.7507 | 1.4822 | 0.3057 |
| XGBoost       | 4.1986 | 2.0490 | 1.7467 | 0.0488 |
| LightGBM      | 3.3796 | 1.8384 | 1.4909 | 0.2343 |

- **Best performance:** Ridge Regression showed the best R² (0.3364) and lowest RMSE (1.7115), indicating a good balance of bias and variance for this dataset.  
- **Nonlinear models:** Random Forest and SVR performed well, showing nonlinear relationships exist.  
- **Boosting models:** XGBoost and LightGBM underperformed, possibly due to dataset size or default hyperparameters.  
- **Lasso:** may have over-penalization leading to loss of important features.


## How to Run

1. Clone the repository:
   
   git clone https://github.com/yourusername/protein-ligand-ml.git
   cd protein-ligand-ml

2. Create and activate a virtual environment:
   
   conda create -n molbindenv python=3.9
   conda activate molbindenv

3. Install dependencies

   pip install -r requirements.txt

4. Run the pipline
   python src/parse_index.py
   python feature_extraction.py
   python src/final_dataset.py
   python src/ml_model.py

5. View Results
   - output scores for all the models will be saved in `results/` folder
   - scattering plots for each model will be saved there too

---

## 📌 Note

This project is intended for educational and portfolio purposes.  
Contributions and suggestions are welcome!