import { useTheme } from '../../hooks/useTheme';
import styles from './About.module.css';

const About = () => {
  const { theme } = useTheme();

  return (
    <div className={styles.container} data-theme={theme}>
      <div className={styles.hero}>
        <h1 className={styles.title}>How It Works</h1>
        <p className={styles.subtitle}>
          Understanding the machine learning pipeline behind body composition prediction
        </p>
      </div>

      {/* Data Collection */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div className={styles.iconBox}>📊</div>
          <h2 className={styles.sectionTitle}>Data Collection</h2>
        </div>
        <div className={styles.content}>
          <p className={styles.text}>
            The models are trained on a comprehensive dataset containing body measurements from diverse individuals. 
            Each record includes 16 different measurements:
          </p>
          <div className={styles.measurementsList}>
            <div className={styles.measurementGroup}>
              <h4 className={styles.groupTitle}>Basic Measurements</h4>
              <ul className={styles.list}>
                <li>Age & Sex</li>
                <li>Height & Weight</li>
              </ul>
            </div>
            <div className={styles.measurementGroup}>
              <h4 className={styles.groupTitle}>Body Circumferences</h4>
              <ul className={styles.list}>
                <li>Waist, Hip, Chest</li>
                <li>Neck, Shoulder</li>
                <li>Wrist, Ankle</li>
              </ul>
            </div>
            <div className={styles.measurementGroup}>
              <h4 className={styles.groupTitle}>Limb Measurements</h4>
              <ul className={styles.list}>
                <li>Upper Arm, Forearm, Bicep</li>
                <li>Thigh, Calf</li>
              </ul>
            </div>
          </div>
          <p className={styles.text}>
            Target variables: <strong>Body Fat Percentage</strong> and <strong>Muscle Mass (kg)</strong>
          </p>
        </div>
      </section>

      {/* Preprocessing */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div className={styles.iconBox}>🔧</div>
          <h2 className={styles.sectionTitle}>Data Preprocessing</h2>
        </div>
        <div className={styles.content}>
          <div className={styles.stepsList}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>1</div>
              <div className={styles.stepContent}>
                <h4 className={styles.stepTitle}>Feature Engineering</h4>
                <p className={styles.stepText}>
                  Creating derived features like BMI, body ratios, and proportions to enhance model understanding
                </p>
              </div>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>2</div>
              <div className={styles.stepContent}>
                <h4 className={styles.stepTitle}>Handling Missing Data</h4>
                <p className={styles.stepText}>
                  Imputation strategies for missing measurements using statistical methods and domain knowledge
                </p>
              </div>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>3</div>
              <div className={styles.stepContent}>
                <h4 className={styles.stepTitle}>Multicollinearity Reduction</h4>
                <p className={styles.stepText}>
                  Removing highly correlated features to prevent model instability and improve generalization
                </p>
              </div>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>4</div>
              <div className={styles.stepContent}>
                <h4 className={styles.stepTitle}>Outlier Detection</h4>
                <p className={styles.stepText}>
                  Identifying and handling outliers that could skew model predictions
                </p>
              </div>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>5</div>
              <div className={styles.stepContent}>
                <h4 className={styles.stepTitle}>Feature Scaling</h4>
                <p className={styles.stepText}>
                  Normalizing features to ensure all measurements contribute equally to predictions
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Model Training */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div className={styles.iconBox}>🧠</div>
          <h2 className={styles.sectionTitle}>Model Training</h2>
        </div>
        <div className={styles.content}>
          <p className={styles.text}>
            Multiple machine learning algorithms are trained and compared to find the best approach:
          </p>
          <div className={styles.modelsGrid}>
            <div className={styles.modelBox}>
              <h4 className={styles.modelBoxTitle}>Linear Regression</h4>
              <p className={styles.modelBoxText}>
                Fast baseline model using linear relationships between features
              </p>
            </div>
            <div className={styles.modelBox}>
              <h4 className={styles.modelBoxTitle}>Lasso Regression</h4>
              <p className={styles.modelBoxText}>
                Automatic feature selection with L1 regularization
              </p>
            </div>
            <div className={styles.modelBox}>
              <h4 className={styles.modelBoxTitle}>Gradient Boosting</h4>
              <p className={styles.modelBoxText}>
                Ensemble method building multiple decision trees sequentially
              </p>
            </div>
            <div className={styles.modelBox}>
              <h4 className={styles.modelBoxTitle}>XGBoost</h4>
              <p className={styles.modelBoxText}>
                Optimized gradient boosting with advanced regularization
              </p>
            </div>
            <div className={styles.modelBox}>
              <h4 className={styles.modelBoxTitle}>Neural Network</h4>
              <p className={styles.modelBoxText}>
                Deep learning model capturing complex non-linear patterns
              </p>
            </div>
            <div className={styles.modelBox}>
              <h4 className={styles.modelBoxTitle}>K-Means Clustering</h4>
              <p className={styles.modelBoxText}>
                Unsupervised learning for body type categorization
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Evaluation */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div className={styles.iconBox}>📈</div>
          <h2 className={styles.sectionTitle}>Model Evaluation</h2>
        </div>
        <div className={styles.content}>
          <p className={styles.text}>
            Models are evaluated using multiple metrics on a held-out test set:
          </p>
          <div className={styles.metricsGrid}>
            <div className={styles.metricBox}>
              <h4 className={styles.metricBoxTitle}>MAE</h4>
              <p className={styles.metricBoxText}>
                Mean Absolute Error - Average magnitude of prediction errors
              </p>
            </div>
            <div className={styles.metricBox}>
              <h4 className={styles.metricBoxTitle}>RMSE</h4>
              <p className={styles.metricBoxText}>
                Root Mean Square Error - Penalizes larger errors more heavily
              </p>
            </div>
            <div className={styles.metricBox}>
              <h4 className={styles.metricBoxTitle}>R² Score</h4>
              <p className={styles.metricBoxText}>
                Coefficient of determination - How well the model fits the data (0-1)
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Prediction */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div className={styles.iconBox}>🎯</div>
          <h2 className={styles.sectionTitle}>Making Predictions</h2>
        </div>
        <div className={styles.content}>
          <div className={styles.pipeline}>
            <div className={styles.pipelineStep}>
              <div className={styles.pipelineIcon}>1</div>
              <p className={styles.pipelineText}>Enter your body measurements</p>
            </div>
            <div className={styles.pipelineArrow}>→</div>
            <div className={styles.pipelineStep}>
              <div className={styles.pipelineIcon}>2</div>
              <p className={styles.pipelineText}>Data is preprocessed and normalized</p>
            </div>
            <div className={styles.pipelineArrow}>→</div>
            <div className={styles.pipelineStep}>
              <div className={styles.pipelineIcon}>3</div>
              <p className={styles.pipelineText}>Models generate predictions</p>
            </div>
            <div className={styles.pipelineArrow}>→</div>
            <div className={styles.pipelineStep}>
              <div className={styles.pipelineIcon}>4</div>
              <p className={styles.pipelineText}>Results displayed with confidence</p>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Stack */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div className={styles.iconBox}>⚙️</div>
          <h2 className={styles.sectionTitle}>Technical Stack</h2>
        </div>
        <div className={styles.content}>
          <div className={styles.techGrid}>
            <div className={styles.techCard}>
              <h4 className={styles.techTitle}>Backend</h4>
              <ul className={styles.techList}>
                <li>Python</li>
                <li>Scikit-learn</li>
                <li>XGBoost</li>
                <li>TensorFlow/Keras</li>
                <li>Pandas & NumPy</li>
              </ul>
            </div>
            <div className={styles.techCard}>
              <h4 className={styles.techTitle}>Frontend</h4>
              <ul className={styles.techList}>
                <li>React</li>
                <li>CSS Modules</li>
                <li>Fetch API</li>
                <li>Responsive Design</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
