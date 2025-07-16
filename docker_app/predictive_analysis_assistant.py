from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime

PREDICTIVE_ANALYSIS_SYSTEM_PROMPT = """
You are PredictiveAnalysisExpert, a specialized assistant for forecasting and predictive modeling.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all analysis and responses.

Your expertise includes:

1. Forecasting Methodologies:
   - Time series analysis (ARIMA, SARIMA, Prophet)
   - Machine learning models (Random Forest, XGBoost, Neural Networks)
   - Ensemble methods and model stacking
   - Bayesian forecasting and uncertainty quantification

2. Data Quality & Feature Engineering:
   - Missing data handling and imputation
   - Outlier detection and treatment
   - Feature selection and dimensionality reduction
   - Cross-validation and backtesting strategies

3. Model Evaluation & Selection:
   - Accuracy metrics (MAE, RMSE, MAPE, SMAPE)
   - Statistical significance testing
   - Model interpretability and explainability
   - Forecast confidence intervals and prediction bands

4. Best Practices:
   - Data preprocessing and normalization
   - Seasonal decomposition and trend analysis
   - External variable integration (economic indicators, events)
   - Real-time model updating and drift detection

Focus on actionable insights with quantified uncertainty and model limitations.
"""

@tool
def predictive_analysis_assistant(query: str) -> str:
    """
    Provide predictive analysis and forecasting expertise with best practices.
    
    Args:
        query: A predictive analysis or forecasting request
        
    Returns:
        Comprehensive forecasting methodology and recommendations
    """
    try:
        print("Routed to Predictive Analysis Assistant")
        enhanced_query = enhance_query_with_realtime(query, "predictive_analysis")

        
        analysis_framework = generate_predictive_framework(query)
        
        formatted_query = f"Provide predictive analysis guidance: {query}\n\nFramework: {analysis_framework}"
        
        predictive_agent = Agent(
            system_prompt=PREDICTIVE_ANALYSIS_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = predictive_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"Predictive analysis error: {str(e)}"

def generate_predictive_framework(query):
    """Generate predictive analysis framework based on query type"""
    query_lower = query.lower()
    
    if any(term in query_lower for term in ['time series', 'sales forecast', 'demand']):
        return """TIME SERIES FORECASTING FRAMEWORK:

Data Preparation:
- Check for stationarity (ADF test, KPSS test)
- Handle missing values (interpolation, forward fill)
- Detect and treat outliers (IQR method, Z-score)
- Seasonal decomposition (STL, X-13ARIMA-SEATS)

Model Selection:
- Classical: ARIMA, SARIMA, Exponential Smoothing
- Modern: Prophet (Facebook), TBATS, State Space Models
- ML-based: LSTM, GRU, Transformer models
- Ensemble: Combine multiple models for robustness

Validation Strategy:
- Time series cross-validation (rolling window)
- Walk-forward analysis
- Out-of-sample testing (last 20% of data)
- Backtesting with multiple forecast horizons

Key Metrics:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- MAPE (Mean Absolute Percentage Error)
- Directional accuracy for trend prediction"""
    
    elif any(term in query_lower for term in ['classification', 'prediction', 'machine learning']):
        return """MACHINE LEARNING PREDICTION FRAMEWORK:

Feature Engineering:
- Domain knowledge integration
- Polynomial and interaction features
- Lag features for temporal data
- Categorical encoding (one-hot, target, embedding)

Model Development:
- Baseline models (logistic regression, decision trees)
- Advanced models (XGBoost, LightGBM, CatBoost)
- Deep learning (neural networks, autoencoders)
- Ensemble methods (voting, stacking, blending)

Cross-Validation:
- Stratified K-fold for classification
- Time-based splits for temporal data
- Nested CV for hyperparameter tuning
- Bootstrap sampling for uncertainty estimation

Performance Optimization:
- Hyperparameter tuning (Bayesian optimization)
- Feature selection (RFE, LASSO, mutual information)
- Model calibration and probability adjustment
- Threshold optimization for business metrics"""
    
    elif any(term in query_lower for term in ['financial', 'market', 'stock', 'price']):
        return """FINANCIAL FORECASTING FRAMEWORK:

Market Data Processing:
- Price normalization and returns calculation
- Volatility clustering detection (GARCH models)
- Market regime identification
- Economic indicator integration

Risk-Adjusted Models:
- Value at Risk (VaR) and Expected Shortfall
- Sharpe ratio optimization
- Maximum drawdown constraints
- Tail risk assessment

Advanced Techniques:
- Monte Carlo simulation
- Black-Scholes and derivatives pricing
- Copula models for dependency structure
- Regime-switching models

Validation Considerations:
- Walk-forward optimization
- Out-of-sample performance decay
- Transaction cost integration
- Market impact modeling"""
    
    else:
        return """GENERAL PREDICTIVE ANALYSIS FRAMEWORK:

Data Quality Assessment:
- Completeness, consistency, accuracy checks
- Distribution analysis and normality tests
- Correlation analysis and multicollinearity
- Data leakage detection and prevention

Model Development Process:
1. Exploratory Data Analysis (EDA)
2. Feature engineering and selection
3. Model training and validation
4. Hyperparameter optimization
5. Model interpretation and explainability
6. Production deployment and monitoring

Best Practices:
- Start simple, then increase complexity
- Use cross-validation for all model selection
- Document assumptions and limitations
- Monitor model performance over time
- Implement automated retraining pipelines
- Maintain prediction confidence intervals

Success Metrics:
- Prediction accuracy on unseen data
- Business impact and ROI measurement
- Model stability and robustness
- Computational efficiency and scalability"""