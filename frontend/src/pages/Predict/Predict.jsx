import { useState } from 'react';
import { useTheme } from '../../hooks/useTheme';
import { useToast } from '../../components/Toast Notifications/ToastContext';
import { SearchableDropdown } from '../../components';
import apiService from '../../services/api';
import styles from './Predict.module.css';

const Predict = () => {
  const { theme } = useTheme();
  const { showToast } = useToast();
  
  const [formData, setFormData] = useState({
    Age: '',
    Sex: '',
    Height_cm: '',
    Weight_kg: '',
    Wrist_cm: '',
    Waist_cm: '',
    Hip_cm: '',
    Neck_cm: '',
    UpperArm_cm: '',
    Thigh_cm: '',
    Calf_cm: '',
    Forearm_cm: '',
    Chest_cm: '',
    Shoulder_cm: '',
    Ankle_cm: '',
    Bicep_cm: ''
  });

  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('all');

  const modelOptions = [
    { value: 'all', label: 'All Models' },
    { value: 'linear_regression', label: 'Linear Regression' },
    { value: 'lasso_regression', label: 'Lasso Regression' },
    { value: 'gradient_boosting', label: 'Gradient Boosting' },
    { value: 'xgboost', label: 'XGBoost' },
    { value: 'neural_network', label: 'Neural Network' }
  ];

  const sexOptions = [
    { value: 'Male', label: 'Male' },
    { value: 'Female', label: 'Female' },
    { value: 'M', label: 'M' },
    { value: 'F', label: 'F' },
    { value: 'MALE', label: 'MALE' },
    { value: 'FEMALE', label: 'FEMALE' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSexChange = (option) => {
    setFormData(prev => ({
      ...prev,
      Sex: option.value
    }));
  };

  const handleModelChange = (option) => {
    setSelectedModel(option.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPredictions(null);

    try {
      // Convert form data to numbers where applicable
      const processedData = {};
      Object.keys(formData).forEach(key => {
        if (key === 'Sex') {
          processedData[key] = formData[key];
        } else if (formData[key] !== '') {
          processedData[key] = parseFloat(formData[key]);
        }
      });

      let result;
      if (selectedModel === 'all') {
        result = await apiService.predictAll(processedData);
      } else {
        result = await apiService.predict(selectedModel, processedData);
      }

      setPredictions(result);
      showToast('success', 'Success', 'Predictions generated successfully!');
    } catch (error) {
      showToast('error', 'Prediction Failed', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      Age: '',
      Sex: '',
      Height_cm: '',
      Weight_kg: '',
      Wrist_cm: '',
      Waist_cm: '',
      Hip_cm: '',
      Neck_cm: '',
      UpperArm_cm: '',
      Thigh_cm: '',
      Calf_cm: '',
      Forearm_cm: '',
      Chest_cm: '',
      Shoulder_cm: '',
      Ankle_cm: '',
      Bicep_cm: ''
    });
    setPredictions(null);
  };

  const fillSampleData = () => {
    setFormData({
      Age: '35',
      Sex: 'Male',
      Height_cm: '175',
      Weight_kg: '80',
      Wrist_cm: '17',
      Waist_cm: '90',
      Hip_cm: '100',
      Neck_cm: '38',
      UpperArm_cm: '32',
      Thigh_cm: '60',
      Calf_cm: '38',
      Forearm_cm: '28',
      Chest_cm: '100',
      Shoulder_cm: '45',
      Ankle_cm: '23',
      Bicep_cm: '35'
    });
    // Form is visually filled, no need for notification
  };

  const renderPredictionResults = () => {
    if (!predictions) return null;

    if (selectedModel === 'all' && predictions.models) {
      return (
        <div className={styles.resultsGrid}>
          {Object.entries(predictions.models).map(([modelName, data]) => (
            <div key={modelName} className={styles.resultCard}>
              <h3 className={styles.modelTitle}>{modelName.replace(/_/g, ' ').toUpperCase()}</h3>
              <div className={styles.predictionValues}>
                <div className={styles.valueItem}>
                  <span className={styles.valueLabel}>Body Fat %</span>
                  <span className={styles.valueNumber}>
                    {data.body_fat_percentage?.toFixed(1) || 'N/A'}%
                  </span>
                </div>
                <div className={styles.valueItem}>
                  <span className={styles.valueLabel}>Muscle Mass</span>
                  <span className={styles.valueNumber}>
                    {data.muscle_mass?.toFixed(1) || 'N/A'} kg
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      );
    } else {
      return (
        <div className={styles.singleResult}>
          <h3 className={styles.resultTitle}>Prediction Results</h3>
          <div className={styles.bigValues}>
            <div className={styles.bigValueItem}>
              <span className={styles.bigValueLabel}>Body Fat Percentage</span>
              <span className={styles.bigValueNumber}>
                {predictions.body_fat_percentage?.toFixed(1) || 'N/A'}%
              </span>
            </div>
            <div className={styles.bigValueItem}>
              <span className={styles.bigValueLabel}>Muscle Mass</span>
              <span className={styles.bigValueNumber}>
                {predictions.muscle_mass?.toFixed(1) || 'N/A'} kg
              </span>
            </div>
          </div>
        </div>
      );
    }
  };

  return (
    <div className={styles.container} data-theme={theme}>
      <div className={styles.header}>
        <h1 className={styles.title}>Body Composition Prediction</h1>
        <p className={styles.subtitle}>
          Enter your body measurements to get AI-powered predictions
        </p>
      </div>

      <div className={styles.content}>
        <div className={styles.formSection}>
          <div className={styles.formCard}>
            <div className={styles.formHeader}>
              <h2 className={styles.formTitle}>Input Measurements</h2>
              <div className={styles.formActions}>
                <button
                  type="button"
                  className={styles.btnSmall}
                  onClick={fillSampleData}
                >
                  Fill Sample
                </button>
                <button
                  type="button"
                  className={styles.btnSmall}
                  onClick={handleReset}
                >
                  Reset
                </button>
              </div>
            </div>

            <form onSubmit={handleSubmit} className={styles.form}>
              {/* Model Selection */}
              <div className={styles.formGroup}>
                <label className={styles.label}>Select Model</label>
                <SearchableDropdown
                  options={modelOptions}
                  value={modelOptions.find(opt => opt.value === selectedModel)}
                  onChange={handleModelChange}
                  placeholder="Choose a model..."
                />
              </div>

              {/* Basic Info */}
              <div className={styles.sectionDivider}>
                <span className={styles.sectionLabel}>Basic Information</span>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Age *</label>
                  <input
                    type="number"
                    name="Age"
                    value={formData.Age}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 35"
                    required
                    min="1"
                    max="120"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Sex *</label>
                  <SearchableDropdown
                    options={sexOptions}
                    value={sexOptions.find(opt => opt.value === formData.Sex)}
                    onChange={handleSexChange}
                    placeholder="Select sex..."
                  />
                </div>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Height (cm) *</label>
                  <input
                    type="number"
                    name="Height_cm"
                    value={formData.Height_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 175"
                    required
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Weight (kg) *</label>
                  <input
                    type="number"
                    name="Weight_kg"
                    value={formData.Weight_kg}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 80"
                    required
                    step="0.1"
                  />
                </div>
              </div>

              {/* Body Measurements */}
              <div className={styles.sectionDivider}>
                <span className={styles.sectionLabel}>Body Measurements (cm)</span>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Waist</label>
                  <input
                    type="number"
                    name="Waist_cm"
                    value={formData.Waist_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 90"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Hip</label>
                  <input
                    type="number"
                    name="Hip_cm"
                    value={formData.Hip_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 100"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Neck</label>
                  <input
                    type="number"
                    name="Neck_cm"
                    value={formData.Neck_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 38"
                    step="0.1"
                  />
                </div>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Chest</label>
                  <input
                    type="number"
                    name="Chest_cm"
                    value={formData.Chest_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 100"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Shoulder</label>
                  <input
                    type="number"
                    name="Shoulder_cm"
                    value={formData.Shoulder_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 45"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Wrist</label>
                  <input
                    type="number"
                    name="Wrist_cm"
                    value={formData.Wrist_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 17"
                    step="0.1"
                  />
                </div>
              </div>

              {/* Arms and Legs */}
              <div className={styles.sectionDivider}>
                <span className={styles.sectionLabel}>Arms & Legs (cm)</span>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Upper Arm</label>
                  <input
                    type="number"
                    name="UpperArm_cm"
                    value={formData.UpperArm_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 32"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Forearm</label>
                  <input
                    type="number"
                    name="Forearm_cm"
                    value={formData.Forearm_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 28"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Bicep</label>
                  <input
                    type="number"
                    name="Bicep_cm"
                    value={formData.Bicep_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 35"
                    step="0.1"
                  />
                </div>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Thigh</label>
                  <input
                    type="number"
                    name="Thigh_cm"
                    value={formData.Thigh_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 60"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Calf</label>
                  <input
                    type="number"
                    name="Calf_cm"
                    value={formData.Calf_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 38"
                    step="0.1"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Ankle</label>
                  <input
                    type="number"
                    name="Ankle_cm"
                    value={formData.Ankle_cm}
                    onChange={handleInputChange}
                    className={styles.input}
                    placeholder="e.g., 23"
                    step="0.1"
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className={styles.submitBtn}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className={styles.spinner}></span>
                    Predicting...
                  </>
                ) : (
                  'Get Predictions'
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Results Section */}
        {predictions && (
          <div className={styles.resultsSection}>
            <div className={styles.resultsCard}>
              {renderPredictionResults()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Predict;
