"""
Linear Regression model for body composition prediction.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
import joblib
import matplotlib.pyplot as plt
from pathlib import Path


class LinearRegressionModel:
    """Multi-output Linear Regression for BodyFat% and MuscleMass prediction."""
    
    def __init__(self):
        self.model = MultiOutputRegressor(LinearRegression())
        self.metrics = {}
        
    def train(self, X_train, y_train):
        """Train the model."""
        print("Training Linear Regression model...")
        self.model.fit(X_train, y_train)
        print("✅ Training complete!")
        
    def evaluate(self, X, y, dataset_name="Test"):
        """Evaluate the model and return metrics."""
        predictions = self.model.predict(X)
        
        # Calculate metrics for each target
        metrics = {}
        target_names = ['BodyFatPct', 'MuscleMass_kg']
        
        for i, target in enumerate(target_names):
            mse = mean_squared_error(y[:, i], predictions[:, i])
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y[:, i], predictions[:, i])
            r2 = r2_score(y[:, i], predictions[:, i])
            
            metrics[target] = {
                'MSE': mse,
                'RMSE': rmse,
                'MAE': mae,
                'R2': r2
            }
        
        self.metrics[dataset_name] = metrics
        return metrics
    
    def print_metrics(self, dataset_name="Test"):
        """Print evaluation metrics."""
        if dataset_name not in self.metrics:
            print(f"No metrics available for {dataset_name}")
            return
        
        print(f"\n{'='*60}")
        print(f"Linear Regression - {dataset_name} Set Metrics")
        print(f"{'='*60}")
        
        for target, metrics in self.metrics[dataset_name].items():
            print(f"\n{target}:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")
    
    def plot_predictions(self, X, y, save_path=None):
        """Plot actual vs predicted values."""
        predictions = self.model.predict(X)
        target_names = ['Body Fat %', 'Muscle Mass (kg)']
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        for i, (ax, target_name) in enumerate(zip(axes, target_names)):
            ax.scatter(y[:, i], predictions[:, i], alpha=0.5, edgecolors='k')
            ax.plot([y[:, i].min(), y[:, i].max()], 
                   [y[:, i].min(), y[:, i].max()], 
                   'r--', lw=2, label='Perfect Prediction')
            ax.set_xlabel(f'Actual {target_name}')
            ax.set_ylabel(f'Predicted {target_name}')
            ax.set_title(f'{target_name} - Linear Regression')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def save(self, filepath):
        """Save the trained model."""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load a trained model."""
        model = LinearRegressionModel()
        model.model = joblib.load(filepath)
        return model


def train_linear_regression(X_train, X_test, y_train, y_test, save_dir=None):
    """
    Train and evaluate a Linear Regression model.
    
    Args:
        X_train, X_test: Feature matrices
        y_train, y_test: Target matrices
        save_dir: Directory to save model and plots
        
    Returns:
        Trained model
    """
    model = LinearRegressionModel()
    
    # Train
    model.train(X_train, y_train)
    
    # Evaluate
    train_metrics = model.evaluate(X_train, y_train, "Train")
    test_metrics = model.evaluate(X_test, y_test, "Test")
    
    # Print results
    model.print_metrics("Train")
    model.print_metrics("Test")
    
    # Save if directory provided
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(exist_ok=True, parents=True)
        
        model.save(save_dir / 'linear_regression_model.pkl')
        model.plot_predictions(X_test, y_test, save_dir / 'linear_regression_predictions.png')
        
        # Save metrics to file
        metrics_df = pd.DataFrame({
            'Target': [],
            'Dataset': [],
            'MSE': [],
            'RMSE': [],
            'MAE': [],
            'R2': []
        })
        
        for dataset in ['Train', 'Test']:
            for target, metrics in model.metrics[dataset].items():
                metrics_df = pd.concat([metrics_df, pd.DataFrame({
                    'Target': [target],
                    'Dataset': [dataset],
                    'MSE': [metrics['MSE']],
                    'RMSE': [metrics['RMSE']],
                    'MAE': [metrics['MAE']],
                    'R2': [metrics['R2']]
                })], ignore_index=True)
        
        metrics_df.to_csv(save_dir / 'linear_regression_metrics.csv', index=False)
        print(f"Metrics saved to {save_dir / 'linear_regression_metrics.csv'}")
    
    return model
