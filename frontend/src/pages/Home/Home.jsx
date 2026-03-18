import { useEffect } from 'react';
import { useTheme } from '../../hooks/useTheme';
import apiService from '../../services/api';
import styles from './Home.module.css';

const Home = ({ onNavigate }) => {
  const { theme } = useTheme();

  useEffect(() => {
    // Load data stats if available
    const loadStats = async () => {
      try {
        await apiService.getDataStats();
      } catch (error) {
        console.log('Stats not available yet:', error.message);
      }
    };

    loadStats();
  }, []);

  return (
    <div className={styles.container} data-theme={theme}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.title}>
            <span className={styles.gradient}>Nutrition AI</span>
          </h1>
          <p className={styles.subtitle}>
            Advanced Machine Learning for Body Composition Analysis
          </p>
          <p className={styles.description}>
            Predict body fat percentage and muscle mass using state-of-the-art ML models
            trained on comprehensive body measurement data.
          </p>
          <div className={styles.buttonGroup}>
            <button
              className={`${styles.btn} ${styles.btnPrimary}`}
              onClick={() => onNavigate('/predict')}
            >
              Get Predictions
            </button>
            <button
              className={`${styles.btn} ${styles.btnSecondary}`}
              onClick={() => onNavigate('/models')}
            >
              View Models
            </button>
          </div>
        </div>

        {/* Animated Background Elements */}
        <div className={styles.backgroundElements}>
          <div className={styles.orb1}></div>
          <div className={styles.orb2}></div>
          <div className={styles.orb3}></div>
        </div>
      </section>

      {/* Features Section */}
      <section className={styles.features}>
        <h2 className={styles.sectionTitle}>Key Features</h2>
        <div className={styles.featureGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🧠</div>
            <h3 className={styles.featureTitle}>6 ML Models</h3>
            <p className={styles.featureDescription}>
              Multiple algorithms including Linear Regression, XGBoost, Neural Networks, and more
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📊</div>
            <h3 className={styles.featureTitle}>Accurate Predictions</h3>
            <p className={styles.featureDescription}>
              Trained on comprehensive body measurement data for reliable results
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🔍</div>
            <h3 className={styles.featureTitle}>Model Insights</h3>
            <p className={styles.featureDescription}>
              Understand how predictions are made with feature importance analysis
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>⚡</div>
            <h3 className={styles.featureTitle}>Real-time Results</h3>
            <p className={styles.featureDescription}>
              Get instant predictions from all models simultaneously
            </p>
          </div>
        </div>
      </section>

      {/* Models Overview */}
      <section className={styles.modelsOverview}>
        <h2 className={styles.sectionTitle}>Available Models</h2>
        <div className={styles.modelsList}>
          <div className={styles.modelItem}>
            <div className={styles.modelBadge}>Linear</div>
            <span className={styles.modelName}>Linear Regression</span>
          </div>
          <div className={styles.modelItem}>
            <div className={styles.modelBadge}>Lasso</div>
            <span className={styles.modelName}>Lasso Regression</span>
          </div>
          <div className={styles.modelItem}>
            <div className={styles.modelBadge}>GB</div>
            <span className={styles.modelName}>Gradient Boosting</span>
          </div>
          <div className={styles.modelItem}>
            <div className={styles.modelBadge}>XGB</div>
            <span className={styles.modelName}>XGBoost</span>
          </div>
          <div className={styles.modelItem}>
            <div className={styles.modelBadge}>NN</div>
            <span className={styles.modelName}>Neural Network</span>
          </div>
          <div className={styles.modelItem}>
            <div className={styles.modelBadge}>K-M</div>
            <span className={styles.modelName}>Clustering (K-Means)</span>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={styles.cta}>
        <h2 className={styles.ctaTitle}>Ready to analyze your body composition?</h2>
        <p className={styles.ctaDescription}>
          Input your body measurements and get instant predictions powered by AI
        </p>
        <button
          className={`${styles.btn} ${styles.btnPrimary} ${styles.btnLarge}`}
          onClick={() => onNavigate('/predict')}
        >
          Start Prediction
        </button>
      </section>
    </div>
  );
};

export default Home;
