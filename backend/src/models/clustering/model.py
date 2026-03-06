"""
Clustering model for body type categorization.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class BodyTypeClusteringModel:
    """Clustering model to categorize body types."""
    
    def __init__(self, n_clusters=5, algorithm='kmeans'):
        """
        Initialize clustering model.
        
        Args:
            n_clusters: Number of clusters (for KMeans)
            algorithm: 'kmeans' or 'dbscan'
        """
        self.n_clusters = n_clusters
        self.algorithm = algorithm
        self.model = None
        self.scaler = StandardScaler()
        self.labels = None
        self.metrics = {}
        self.cluster_profiles = None
        
    def find_optimal_clusters(self, X, max_clusters=10):
        """
        Find optimal number of clusters using elbow method and silhouette score.
        
        Args:
            X: Feature matrix
            max_clusters: Maximum number of clusters to try
        """
        print("Finding optimal number of clusters...")
        
        inertias = []
        silhouette_scores = []
        K_range = range(2, max_clusters + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        
        # Plot results
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        axes[0].plot(K_range, inertias, 'bo-')
        axes[0].set_xlabel('Number of Clusters (k)')
        axes[0].set_ylabel('Inertia')
        axes[0].set_title('Elbow Method')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(K_range, silhouette_scores, 'ro-')
        axes[1].set_xlabel('Number of Clusters (k)')
        axes[1].set_ylabel('Silhouette Score')
        axes[1].set_title('Silhouette Score vs. Number of Clusters')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Recommend optimal k
        best_k = K_range[np.argmax(silhouette_scores)]
        print(f"  Recommended number of clusters: {best_k}")
        print(f"  Silhouette score: {max(silhouette_scores):.4f}")
        
        return best_k
    
    def train(self, X, find_optimal=False):
        """
        Train the clustering model.
        
        Args:
            X: Feature matrix
            find_optimal: Whether to find optimal number of clusters first
        """
        print(f"Training {self.algorithm.upper()} clustering model...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        if find_optimal and self.algorithm == 'kmeans':
            optimal_k = self.find_optimal_clusters(X_scaled)
            self.n_clusters = optimal_k
        
        # Train model
        if self.algorithm == 'kmeans':
            self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        elif self.algorithm == 'dbscan':
            self.model = DBSCAN(eps=0.5, min_samples=5)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        
        self.labels = self.model.fit_predict(X_scaled)
        
        # Calculate metrics
        if len(np.unique(self.labels)) > 1:
            self.metrics['silhouette'] = silhouette_score(X_scaled, self.labels)
            self.metrics['davies_bouldin'] = davies_bouldin_score(X_scaled, self.labels)
            self.metrics['calinski_harabasz'] = calinski_harabasz_score(X_scaled, self.labels)
        
        print("✅ Training complete!")
        print(f"  Number of clusters found: {len(np.unique(self.labels))}")
        
        if self.metrics:
            print("\nClustering Metrics:")
            print(f"  Silhouette Score: {self.metrics['silhouette']:.4f}")
            print(f"  Davies-Bouldin Index: {self.metrics['davies_bouldin']:.4f}")
            print(f"  Calinski-Harabasz Index: {self.metrics['calinski_harabasz']:.2f}")
    
    def create_cluster_profiles(self, X, feature_names, target_data=None):
        """
        Create profiles for each cluster.
        
        Args:
            X: Original feature matrix
            feature_names: List of feature names
            target_data: Optional target data (BodyFatPct, MuscleMass_kg)
        """
        df = pd.DataFrame(X, columns=feature_names)
        df['Cluster'] = self.labels
        
        if target_data is not None:
            df['BodyFatPct'] = target_data[:, 0]
            df['MuscleMass_kg'] = target_data[:, 1]
        
        # Calculate cluster statistics
        profiles = []
        for cluster_id in sorted(df['Cluster'].unique()):
            if cluster_id == -1:  # Noise points in DBSCAN
                continue
            
            cluster_data = df[df['Cluster'] == cluster_id]
            profile = {
                'Cluster': cluster_id,
                'Size': len(cluster_data),
                'Size_Pct': len(cluster_data) / len(df) * 100
            }
            
            # Add mean values for key features
            key_features = feature_names[:5] if len(feature_names) > 5 else feature_names
            for feat in key_features:
                profile[f'{feat}_mean'] = cluster_data[feat].mean()
            
            if target_data is not None:
                profile['BodyFatPct_mean'] = cluster_data['BodyFatPct'].mean()
                profile['MuscleMass_kg_mean'] = cluster_data['MuscleMass_kg'].mean()
            
            profiles.append(profile)
        
        self.cluster_profiles = pd.DataFrame(profiles)
        
        return self.cluster_profiles
    
    def assign_body_type_names(self):
        """Assign meaningful names to clusters based on their characteristics."""
        if self.cluster_profiles is None:
            print("Create cluster profiles first!")
            return
        
        # Sort clusters by body fat percentage
        if 'BodyFatPct_mean' in self.cluster_profiles.columns:
            sorted_profiles = self.cluster_profiles.sort_values('BodyFatPct_mean')
            
            body_type_names = ['Athletic', 'Fit', 'Average', 'Stocky', 'High Body Fat']
            n_clusters = len(sorted_profiles)
            
            # Assign names based on available clusters
            if n_clusters <= len(body_type_names):
                names = body_type_names[:n_clusters]
            else:
                names = [f'Type_{i}' for i in range(n_clusters)]
            
            cluster_to_name = dict(zip(sorted_profiles['Cluster'].values, names))
            self.cluster_profiles['BodyType'] = self.cluster_profiles['Cluster'].map(cluster_to_name)
            
            return cluster_to_name
        
        return None
    
    def plot_clusters_2d(self, X, save_path=None, features_to_plot=None):
        """
        Plot clusters in 2D using first two principal components or specified features.
        
        Args:
            X: Feature matrix
            save_path: Path to save plot
            features_to_plot: Tuple of (feature_idx1, feature_idx2) to plot
        """
        from sklearn.decomposition import PCA
        
        X_scaled = self.scaler.transform(X)
        
        if features_to_plot is not None:
            X_plot = X_scaled[:, features_to_plot]
            xlabel = f'Feature {features_to_plot[0]}'
            ylabel = f'Feature {features_to_plot[1]}'
        else:
            # Use PCA for dimensionality reduction
            pca = PCA(n_components=2)
            X_plot = pca.fit_transform(X_scaled)
            xlabel = f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)'
            ylabel = f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)'
        
        plt.figure(figsize=(10, 7))
        scatter = plt.scatter(X_plot[:, 0], X_plot[:, 1], 
                            c=self.labels, cmap='viridis', 
                            alpha=0.6, edgecolors='k', s=50)
        plt.colorbar(scatter, label='Cluster')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(f'Body Type Clustering ({self.algorithm.upper()})')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Cluster plot saved to {save_path}")
        
        plt.show()
    
    def plot_cluster_heatmap(self, save_path=None):
        """Plot heatmap of cluster profiles."""
        if self.cluster_profiles is None:
            print("Create cluster profiles first!")
            return
        
        # Select numeric columns for heatmap
        numeric_cols = self.cluster_profiles.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col not in ['Cluster', 'Size', 'Size_Pct']]
        
        if len(numeric_cols) == 0:
            print("No numeric features to plot!")
            return
        
        heatmap_data = self.cluster_profiles[numeric_cols]
        
        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_data.T, annot=True, fmt='.2f', cmap='coolwarm', 
                   xticklabels=self.cluster_profiles['Cluster'].values,
                   yticklabels=numeric_cols)
        plt.xlabel('Cluster')
        plt.ylabel('Feature (Mean)')
        plt.title('Cluster Profiles Heatmap')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Heatmap saved to {save_path}")
        
        plt.show()
    
    def predict(self, X):
        """Predict cluster labels for new data."""
        X_scaled = self.scaler.transform(X)
        
        if self.algorithm == 'kmeans':
            return self.model.predict(X_scaled)
        elif self.algorithm == 'dbscan':
            # DBSCAN doesn't have predict method, use fit_predict on combined data
            print("Note: DBSCAN doesn't support prediction on new data")
            return None
    
    def save(self, filepath):
        """Save the trained model."""
        save_data = {
            'model': self.model,
            'scaler': self.scaler,
            'labels': self.labels,
            'metrics': self.metrics,
            'cluster_profiles': self.cluster_profiles,
            'n_clusters': self.n_clusters,
            'algorithm': self.algorithm
        }
        joblib.dump(save_data, filepath)
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load a trained model."""
        save_data = joblib.load(filepath)
        model = BodyTypeClusteringModel(
            n_clusters=save_data['n_clusters'],
            algorithm=save_data['algorithm']
        )
        model.model = save_data['model']
        model.scaler = save_data['scaler']
        model.labels = save_data['labels']
        model.metrics = save_data['metrics']
        model.cluster_profiles = save_data['cluster_profiles']
        return model


def perform_clustering(X_train, y_train, feature_names, n_clusters=5, save_dir=None):
    """
    Perform clustering analysis on body measurements.
    
    Args:
        X_train: Feature matrix
        y_train: Target matrix (BodyFatPct, MuscleMass_kg)
        feature_names: List of feature names
        n_clusters: Number of clusters
        save_dir: Directory to save results
        
    Returns:
        Trained clustering model
    """
    model = BodyTypeClusteringModel(n_clusters=n_clusters, algorithm='kmeans')
    
    # Train
    model.train(X_train, find_optimal=True)
    
    # Create cluster profiles
    profiles = model.create_cluster_profiles(X_train, feature_names, y_train)
    print("\n" + "="*60)
    print("Cluster Profiles")
    print("="*60)
    print(profiles.to_string(index=False))
    
    # Assign body type names
    body_type_mapping = model.assign_body_type_names()
    if body_type_mapping:
        print("\n" + "="*60)
        print("Body Type Categories")
        print("="*60)
        for cluster_id, name in body_type_mapping.items():
            size = profiles[profiles['Cluster'] == cluster_id]['Size'].values[0]
            print(f"  {name} (Cluster {cluster_id}): {size} people")
    
    # Create visualizations
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(exist_ok=True, parents=True)
        
        model.save(save_dir / 'clustering_model.pkl')
        model.plot_clusters_2d(X_train, save_dir / 'clustering_2d.png')
        model.plot_cluster_heatmap(save_dir / 'clustering_heatmap.png')
        
        # Save profiles
        if model.cluster_profiles is not None:
            model.cluster_profiles.to_csv(save_dir / 'cluster_profiles.csv', index=False)
    
    return model
