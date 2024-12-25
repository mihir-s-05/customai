import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import joblib
from config import MODEL_STORAGE_PATH, DEFAULT_MODEL_TYPE  # Import configurations
from utils.logger import logger

def train_model(data, labels, model_type=DEFAULT_MODEL_TYPE):
    """
    Train a machine learning model based on the given data and model type.

    Args:
        data (array-like): The input data for training.
        labels (array-like): The target labels for training.
        model_type (str): The type of model to train (default is set in config).

    Returns:
        str: The path to the saved model.
    """
    # Ensure the model storage folder exists
    os.makedirs(MODEL_STORAGE_PATH, exist_ok=True)

    # Select the model type
    if model_type == "linear_regression":
        model = LinearRegression()
    elif model_type == "random_forest":
        model = RandomForestRegressor()
    elif model_type == "svr":
        model = SVR()
    else:
        logger.error(f"Unsupported model type: {model_type}")
        raise ValueError(f"Unsupported model type: {model_type}")

    try:
        # Train the model
        model.fit(data, labels)
        logger.info(f"Model training successful: {model_type}")

        # Save the model
        model_path = os.path.join(MODEL_STORAGE_PATH, f"{model_type}_model.pkl")
        joblib.dump(model, model_path)
        logger.info(f"Model saved at: {model_path}")

        return model_path

    except Exception as e:
        logger.error(f"Model training failed: {str(e)}")
        raise RuntimeError(f"Model training failed: {str(e)}")
