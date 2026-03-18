"""
Gradient Boosting model for body composition prediction using scikit-learn.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import matplotlib.pyplot as plt
from pathlib import Path


class GradientBoostingModel:
    """Multi-output Gradient Boosting for BodyFat% and MuscleMass prediction."""
    
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=5):
        """
        Initialize the Gradient Boosting model.
        
        Args:
            n_estimators: Number of boosting stages
            learning_rate: Learning rate shrinks the contribution of each tree
            max_depth: Maximum depth of the individual regression estimators
        """
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.model = MultiOutputRegressor(
            GradientBoostingRegressor(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=42
            )
        )
        self.metrics = {}
        
    def tune_hyperparameters(self, X_train, y_train):
        """Tune hyperparameters using grid search."""
        print("Tuning Gradient Boosting hyperparameters...")
        
        param_grid = {
            'estimator__n_estimators': [50, 100, 200],
            'estimator__learning_rate': [0.01, 0.1, 0.2],
            'estimator__max_depth': [3, 5, 7]
        }
        
        grid_search = GridSearchCV(
            self.model, param_grid, cv=3,
            scoring='neg_mean_squared_error',
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        best_params = grid_search.best_params_
        print(f"  Best parameters: {best_params}")
        
        # Update model with best parameters
        self.n_estimators = best_params['estimator__n_estimators']
        self.learning_rate = best_params['estimator__learning_rate']
        self.max_depth = best_params['estimator__max_depth']
        
        self.model = grid_search.best_estimator_
        
    def train(self, X_train, y_train, tune=False):
        """Train the model."""
        print("Training Gradient Boosting model...")
        
        if tune:
            self.tune_hyperparameters(X_train, y_train)
        else:
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
        print(f"Gradient Boosting - {dataset_name} Set Metrics")
        print(f"{'='*60}")
        
        for target, metrics in self.metrics[dataset_name].items():
            print(f"\n{target}:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")
    
    def get_feature_importance(self, feature_names):
        """Get feature importance for each target."""
        importances = {}
        target_names = ['BodyFatPct', 'MuscleMass_kg']
        
        for i, target in enumerate(target_names):
            importance = self.model.estimators_[i].feature_importances_
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importance
            }).sort_values('Importance', ascending=False)
            
            importances[target] = importance_df
        
        return importances
    
    def plot_feature_importance(self, feature_names, save_path=None, top_n=15):
        """Plot feature importance."""
        importances = self.get_feature_importance(feature_names)
        target_names = ['Body Fat %', 'Muscle Mass (kg)']
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        for i, (ax, target_name) in enumerate(zip(axes, target_names)):
            target_key = list(importances.keys())[i]
            imp_df = importances[target_key].head(top_n)
            
            ax.barh(range(len(imp_df)), imp_df['Importance'])
            ax.set_yticks(range(len(imp_df)))
            ax.set_yticklabels(imp_df['Feature'])
            ax.set_xlabel('Importance')
            ax.set_title(f'Top {top_n} Features - {target_name}')
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Feature importance plot saved to {save_path}")
        
        plt.show()
    
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
            ax.set_title(f'{target_name} - Gradient Boosting')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Predictions plot saved to {save_path}")
        
        plt.show()
    
    def save(self, filepath):
        """Save the trained model."""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load a trained model."""
        model = GradientBoostingModel()
        model.model = joblib.load(filepath)
        return model


def train_gradient_boosting(X_train, X_test, y_train, y_test, feature_names=None, tune=False, save_dir=None):
    """
    Train and evaluate a Gradient Boosting model.
    
    Args:
        X_train, X_test: Feature matrices
        y_train, y_test: Target matrices
        feature_names: List of feature names
        tune: Whether to tune hyperparameters
        save_dir: Directory to save model and plots
        
    Returns:
        Trained model
    """
    model = GradientBoostingModel()
    
    # Train
    model.train(X_train, y_train, tune=tune)
    
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
        
        model.save(save_dir / 'gradient_boosting_model.pkl')
        model.plot_predictions(X_test, y_test, save_dir / 'gradient_boosting_predictions.png')
        
        if feature_names:
            model.plot_feature_importance(feature_names, save_dir / 'gradient_boosting_feature_importance.png')
        
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
        
        metrics_df.to_csv(save_dir / 'gradient_boosting_metrics.csv', index=False)
        
        # Save feature importance
        if feature_names:
            importances = model.get_feature_importance(feature_names)
            for target, imp_df in importances.items():
                filename = f'gradient_boosting_importance_{target.replace(" ", "_")}.csv'
                imp_df.to_csv(save_dir / filename, index=False)
    
    return model
