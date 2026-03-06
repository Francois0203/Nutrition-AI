"""
Lasso Regression model for body composition prediction with L1 regularization.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import matplotlib.pyplot as plt
from pathlib import Path


class LassoRegressionModel:
    """Multi-output Lasso Regression with feature selection via L1 regularization."""
    
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.model = MultiOutputRegressor(Lasso(alpha=alpha, max_iter=10000))
        self.metrics = {}
        self.best_alpha = alpha
        
    def tune_hyperparameters(self, X_train, y_train, alphas=None):
        """Tune the alpha hyperparameter using grid search."""
        if alphas is None:
            alphas = [0.001, 0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0]
        
        print("Tuning Lasso alpha hyperparameter...")
        
        # Tune separately for each output
        best_alphas = []
        for i, target_name in enumerate(['BodyFatPct', 'MuscleMass_kg']):
            lasso = Lasso(max_iter=10000)
            param_grid = {'alpha': alphas}
            
            grid_search = GridSearchCV(
                lasso, param_grid, cv=5, 
                scoring='neg_mean_squared_error', 
                n_jobs=-1
            )
            
            grid_search.fit(X_train, y_train[:, i])
            best_alpha = grid_search.best_params_['alpha']
            best_alphas.append(best_alpha)
            
            print(f"  {target_name}: Best alpha = {best_alpha:.4f}")
        
        # Use average of best alphas
        self.best_alpha = np.mean(best_alphas)
        print(f"Using alpha = {self.best_alpha:.4f}")
        
        # Reinitialize model with best alpha
        self.model = MultiOutputRegressor(Lasso(alpha=self.best_alpha, max_iter=10000))
        
    def train(self, X_train, y_train, tune=True):
        """Train the model."""
        print("Training Lasso Regression model...")
        
        if tune:
            self.tune_hyperparameters(X_train, y_train)
        
        self.model.fit(X_train, y_train)
        print("✅ Training complete!")
        
        # Report feature sparsity
        n_features_used = []
        for estimator in self.model.estimators_:
            n_features_used.append(np.sum(estimator.coef_ != 0))
        print(f"Features used: {n_features_used} out of {X_train.shape[1]}")
        
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
        print(f"Lasso Regression - {dataset_name} Set Metrics")
        print(f"{'='*60}")
        
        for target, metrics in self.metrics[dataset_name].items():
            print(f"\n{target}:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")
    
    def get_feature_importance(self, feature_names):
        """Get feature importance (absolute coefficients) for each target."""
        importances = {}
        target_names = ['BodyFatPct', 'MuscleMass_kg']
        
        for i, target in enumerate(target_names):
            coefs = np.abs(self.model.estimators_[i].coef_)
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': coefs
            }).sort_values('Importance', ascending=False)
            
            importances[target] = importance_df
        
        return importances
    
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
            ax.set_title(f'{target_name} - Lasso Regression (α={self.best_alpha:.4f})')
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
        model = LassoRegressionModel()
        model.model = joblib.load(filepath)
        return model


def train_lasso_regression(X_train, X_test, y_train, y_test, feature_names=None, save_dir=None):
    """
    Train and evaluate a Lasso Regression model.
    
    Args:
        X_train, X_test: Feature matrices
        y_train, y_test: Target matrices
        feature_names: List of feature names
        save_dir: Directory to save model and plots
        
    Returns:
        Trained model
    """
    model = LassoRegressionModel()
    
    # Train with hyperparameter tuning
    model.train(X_train, y_train, tune=True)
    
    # Evaluate
    train_metrics = model.evaluate(X_train, y_train, "Train")
    test_metrics = model.evaluate(X_test, y_test, "Test")
    
    # Print results
    model.print_metrics("Train")
    model.print_metrics("Test")
    
    # Feature importance
    if feature_names:
        print("\n" + "="*60)
        print("Top 10 Most Important Features")
        print("="*60)
        importances = model.get_feature_importance(feature_names)
        for target, imp_df in importances.items():
            print(f"\n{target}:")
            print(imp_df.head(10).to_string(index=False))
    
    # Save if directory provided
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(exist_ok=True, parents=True)
        
        model.save(save_dir / 'lasso_regression_model.pkl')
        model.plot_predictions(X_test, y_test, save_dir / 'lasso_regression_predictions.png')
        
        # Save metrics
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
        
        metrics_df.to_csv(save_dir / 'lasso_regression_metrics.csv', index=False)
        
        # Save feature importance
        if feature_names:
            importances = model.get_feature_importance(feature_names)
            for target, imp_df in importances.items():
                filename = f'lasso_feature_importance_{target.replace(" ", "_")}.csv'
                imp_df.to_csv(save_dir / filename, index=False)
    
    return model
