# this script trains various machine learning models on a dataset of protein-ligand binding affinities.
# It evaluates the models using metrics like MSE, RMSE, MAE, and R2 score.
# It also generates scatter plots of true vs predicted binding affinities for each model.   
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import learning_curve

# data loading and preprocessing
data = pd.read_csv("data/demo_v2021/ml_dataset.csv")
data = data[data['binding_nM'] > 0]
data['log_binding'] = -np.log10(data['binding_nM'])

# Drop unnecessary columns and prepare features and target variable
X = data.drop(columns=['pdb_id', 'binding_nM', 'log_binding'])
y = data['log_binding']

# train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# models to evaluate
models = {
    "RandomForest": RandomForestRegressor(n_estimators=100,min_samples_leaf=5, random_state=42),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.1),
    "SVR": SVR(kernel='rbf', C=1.0, epsilon=0.2),
    "XGBoost": XGBRegressor(n_estimators=100, random_state=42, verbosity=0),
    "LightGBM": LGBMRegressor(n_estimators=100, random_state=42)
}

# Create results directory if it doesn't exist
os.makedirs("results", exist_ok=True)
results = []

# Train and evaluate each model 
# Also generate scatter plots of true vs predicted values
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results.append((name, mse, rmse, mae, r2))


    plt.figure(figsize=(10,8))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('True -log10(binding affinity)')
    plt.ylabel('Predicted binding affinity')
    plt.title(f'True vs Predicted Values for {name}')
    plt.tight_layout()
    plt.savefig(f"results/{name}_scatter.png", dpi=600)
    plt.close()

results_df = pd.DataFrame(results, columns=["Model", "MSE", "RMSE", "MAE", "R2"])
results_df.to_csv("results/model_scores.csv", index=False)