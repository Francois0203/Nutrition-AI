"""
Neural Network model for body composition prediction using TensorFlow/Keras.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
import json


class NeuralNetworkModel:
    """Multi-output Neural Network for BodyFat% and MuscleMass prediction."""
    
    def __init__(self, input_dim, hidden_layers=[128, 64, 32], dropout_rate=0.3):
        """
        Initialize the neural network.
        
        Args:
            input_dim: Number of input features
            hidden_layers: List of hidden layer sizes
            dropout_rate: Dropout rate for regularization
        """
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.dropout_rate = dropout_rate
        self.model = None
        self.history = None
        self.metrics = {}
        self.build_model()
        
    def build_model(self):
        """Build the neural network architecture."""
        model = keras.Sequential()
        
        # Input layer
        model.add(layers.Input(shape=(self.input_dim,)))
        
        # Hidden layers with dropout
        for i, units in enumerate(self.hidden_layers):
            model.add(layers.Dense(units, activation='relu', name=f'hidden_{i+1}'))
            model.add(layers.Dropout(self.dropout_rate, name=f'dropout_{i+1}'))
        
        # Output layer (2 outputs: BodyFatPct, MuscleMass_kg)
        model.add(layers.Dense(2, activation='linear', name='output'))
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=100, batch_size=32):
        """
        Train the neural network.
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data (optional)
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        print("Training Neural Network model...")
        print(f"Architecture: {self.input_dim} -> {' -> '.join(map(str, self.hidden_layers))} -> 2")
        
        # Callbacks
        callback_list = [
            callbacks.EarlyStopping(
                monitor='val_loss' if X_val is not None else 'loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss' if X_val is not None else 'loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6,
                verbose=1
            )
        ]
        
        # Train
        validation_data = (X_val, y_val) if X_val is not None else None
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callback_list,
            verbose=1
        )
        
        print("✅ Training complete!")
        
    def evaluate(self, X, y, dataset_name="Test"):
        """Evaluate the model and return metrics."""
        predictions = self.model.predict(X, verbose=0)
        
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
        print(f"Neural Network - {dataset_name} Set Metrics")
        print(f"{'='*60}")
        
        for target, metrics in self.metrics[dataset_name].items():
            print(f"\n{target}:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")
    
    def plot_training_history(self, save_path=None):
        """Plot training history."""
        if self.history is None:
            print("No training history available")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Loss plot
        axes[0].plot(self.history.history['loss'], label='Train Loss')
        if 'val_loss' in self.history.history:
            axes[0].plot(self.history.history['val_loss'], label='Val Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss (MSE)')
        axes[0].set_title('Training History - Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # MAE plot
        axes[1].plot(self.history.history['mae'], label='Train MAE')
        if 'val_mae' in self.history.history:
            axes[1].plot(self.history.history['val_mae'], label='Val MAE')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('MAE')
        axes[1].set_title('Training History - MAE')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Training history plot saved to {save_path}")
        
        plt.show()
    
    def plot_predictions(self, X, y, save_path=None):
        """Plot actual vs predicted values."""
        predictions = self.model.predict(X, verbose=0)
        target_names = ['Body Fat %', 'Muscle Mass (kg)']
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        for i, (ax, target_name) in enumerate(zip(axes, target_names)):
            ax.scatter(y[:, i], predictions[:, i], alpha=0.5, edgecolors='k')
            ax.plot([y[:, i].min(), y[:, i].max()], 
                   [y[:, i].min(), y[:, i].max()], 
                   'r--', lw=2, label='Perfect Prediction')
            ax.set_xlabel(f'Actual {target_name}')
            ax.set_ylabel(f'Predicted {target_name}')
            ax.set_title(f'{target_name} - Neural Network')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Predictions plot saved to {save_path}")
        
        plt.show()
    
    def save(self, filepath):
        """Save the trained model."""
        self.model.save(filepath)
        
        # Save config
        config = {
            'input_dim': self.input_dim,
            'hidden_layers': self.hidden_layers,
            'dropout_rate': self.dropout_rate
        }
        config_path = Path(filepath).parent / 'nn_config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load a trained model."""
        model = NeuralNetworkModel(input_dim=1)  # Placeholder
        model.model = keras.models.load_model(filepath)
        
        # Load config
        config_path = Path(filepath).parent / 'nn_config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                model.input_dim = config['input_dim']
                model.hidden_layers = config['hidden_layers']
                model.dropout_rate = config['dropout_rate']
        
        return model


def train_neural_network(X_train, X_test, y_train, y_test, epochs=100, batch_size=32, save_dir=None):
    """
    Train and evaluate a Neural Network model.
    
    Args:
        X_train, X_test: Feature matrices
        y_train, y_test: Target matrices
        epochs: Number of training epochs
        batch_size: Batch size for training
        save_dir: Directory to save model and plots
        
    Returns:
        Trained model
    """
    # Use 20% of training data for validation
    val_split = int(0.8 * len(X_train))
    X_val = X_train[val_split:]
    y_val = y_train[val_split:]
    X_train_subset = X_train[:val_split]
    y_train_subset = y_train[:val_split]
    
    # Initialize model
    model = NeuralNetworkModel(
        input_dim=X_train.shape[1],
        hidden_layers=[128, 64, 32],
        dropout_rate=0.3
    )
    
    # Print model summary
    print("\nModel Architecture:")
    model.model.summary()
    
    # Train
    model.train(
        X_train_subset, y_train_subset,
        X_val, y_val,
        epochs=epochs,
        batch_size=batch_size
    )
    
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
        
        model.save(save_dir / 'neural_network_model.keras')
        model.plot_training_history(save_dir / 'nn_training_history.png')
        model.plot_predictions(X_test, y_test, save_dir / 'nn_predictions.png')
        
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
        
        metrics_df.to_csv(save_dir / 'neural_network_metrics.csv', index=False)
    
    return model
