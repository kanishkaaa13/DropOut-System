import kagglehub
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
import os

def load_kaggle_dataset():
    # Downloads the dataset and returns the path to the version folder
    path = kagglehub.dataset_download("adilshamim8/predict-students-dropout-and-academic-success")
    
    # Construct the full path
    csv_path = os.path.join(path, "students_dropout_academic_success.csv")
    
    print(f"Loading dataset from: {csv_path}")
    
    # CHANGE: Changed sep=';' to sep=',' based on your terminal output
    df = pd.read_csv(csv_path, sep=',') 
    
    # Clean whitespace just in case
    df.columns = df.columns.str.strip()
    
    return df

def preprocess(df: pd.DataFrame):
    # YOUR OUTPUT SHOWS: The column name is lowercase "target"
    target_col = "target" 
    
    if target_col not in df.columns:
        # Fallback in case it's capitalized in a different version
        potential_targets = [col for col in df.columns if col.lower() == 'target']
        if not potential_targets:
            raise KeyError(f"Target column not found. Columns: {df.columns.tolist()}")
        target_col = potential_targets[0]

    y = df[target_col]
    X = df.drop(columns=[target_col])

    # ... (rest of your existing preprocess code)

    # Identify numerical and categorical features
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )

    categorical_transformer = Pipeline(
        steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ]
    )

    return X, y, preprocessor

def build_model(preprocessor):
    # Ensemble: RF + MLP
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        class_weight="balanced",
        random_state=42,
    )
    mlp = MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="relu",
        solver="adam",
        max_iter=300,
        random_state=42,
    )

    # Wrap in imbalanced-learn pipeline to apply SMOTE
    rf_model = ImbPipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=42)),
            ("rf", rf),
        ]
    )

    mlp_model = ImbPipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=42)),
            ("mlp", mlp),
        ]
    )

    return rf_model, mlp_model

def train_and_save():
    df = load_kaggle_dataset()
    X, y, preprocessor = preprocess(df)

    # Use stratify=y to maintain class proportions in split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    rf_pipe, mlp_pipe = build_model(preprocessor)

    print("Training Random Forest...")
    rf_pipe.fit(X_train, y_train)
    
    print("Training MLP (Neural Network)...")
    mlp_pipe.fit(X_train, y_train)

    # Evaluate individually
    def eval_model(pipe, name):
        y_pred = pipe.predict(X_test)
        print(f"\n=== {name} Classification Report ===")
        print(classification_report(y_test, y_pred))

    eval_model(rf_pipe, "Random Forest")
    eval_model(mlp_pipe, "MLP")

    # Save artifacts for the API
    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(rf_pipe, "artifacts/rf_model.joblib")
    joblib.dump(mlp_pipe, "artifacts/mlp_model.joblib")
    print("\nModels saved successfully in artifacts/")

if __name__ == "__main__":
    train_and_save()