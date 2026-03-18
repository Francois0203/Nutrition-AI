/**
 * API Service for Nutrition AI Backend
 * Handles all HTTP requests to the ML models backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

class ApiService {
  /**
   * Generic fetch wrapper with error handling
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(error.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  /**
   * Get prediction from a specific model
   * @param {string} modelName - Name of the model (e.g., 'linear_regression', 'xgboost')
   * @param {object} measurements - Body measurements data
   */
  async predict(modelName, measurements) {
    return this.request(`/predict/${modelName}`, {
      method: 'POST',
      body: JSON.stringify({ measurements }),
    });
  }

  /**
   * Get predictions from all available models
   * @param {object} measurements - Body measurements data
   */
  async predictAll(measurements) {
    return this.request('/predict/all', {
      method: 'POST',
      body: JSON.stringify({ measurements }),
    });
  }

  /**
   * Get model comparison metrics
   */
  async getModelComparison() {
    return this.request('/models/comparison');
  }

  /**
   * Get detailed information about a specific model
   * @param {string} modelName - Name of the model
   */
  async getModelInfo(modelName) {
    return this.request(`/models/${modelName}`);
  }

  /**
   * Get feature importance for models that support it
   * @param {string} modelName - Name of the model
   */
  async getFeatureImportance(modelName) {
    return this.request(`/models/${modelName}/features`);
  }

  /**
   * Get list of all available models
   */
  async getAvailableModels() {
    return this.request('/models');
  }

  /**
   * Get data statistics and distributions
   */
  async getDataStats() {
    return this.request('/data/stats');
  }

  /**
   * Health check endpoint
   */
  async healthCheck() {
    return this.request('/health');
  }

  /**
   * Validate input measurements
   * @param {object} measurements - Body measurements to validate
   */
  async validateMeasurements(measurements) {
    return this.request('/validate', {
      method: 'POST',
      body: JSON.stringify({ measurements }),
    });
  }
}

export default new ApiService();
