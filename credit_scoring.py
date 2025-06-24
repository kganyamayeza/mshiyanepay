import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, List, Optional
import pandas as pd
from fastapi import FastAPI

# TODO: Add proper error handling
# TODO: Implement request validation
# TODO: Add rate limiting
# TODO: Add proper logging
# TODO: Consider adding caching

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class MshiyaneCreditScoring:
    def __init__(self):
        # Had to experiment with different models before settling on these
        # GradientBoosting performed better for credit scoring
        # RandomForest worked well for fraud detection
        self.scaler = StandardScaler()
        self.credit_model = GradientBoostingRegressor(
            n_estimators=100,  # Tuned based on performance
            learning_rate=0.1,  # Found this to be optimal
            max_depth=5,  # Prevents overfitting
            random_state=42
        )
        self.fraud_model = RandomForestClassifier(
            n_estimators=100,  # Increased from 50 after testing
            max_depth=10,  # Allows for complex patterns
            random_state=42
        )

    def preprocess_features(self, user_data: Dict) -> np.ndarray:
        """
        Preprocess user data for credit scoring
        TODO: Add more features
        TODO: Implement feature validation
        TODO: Add data cleaning
        TODO: Consider adding more advanced preprocessing
        """
        features = [
            float(user_data.get('annual_income', 0)),
            float(user_data.get('years_of_credit_history', 0)),
            float(user_data.get('num_accounts', 0)),
            float(user_data.get('payment_history_score', 0)),
            float(user_data.get('debt_to_income_ratio', 0)),
            float(user_data.get('num_recent_inquiries', 0)),
            float(user_data.get('age', 0))
        ]
        return np.array(features).reshape(1, -1)

    def calculate_credit_score(self, user_data: Dict) -> float:
        """
        Calculate credit score based on user data
        TODO: Add confidence intervals
        TODO: Implement score explanation
        TODO: Add bias detection
        TODO: Consider adding more sophisticated scoring
        """
        features = self.preprocess_features(user_data)
        scaled_features = self.scaler.fit_transform(features)
        
        # Base score prediction
        base_score = self.credit_model.predict(scaled_features)[0]
        
        # Adjust score based on additional factors
        adjustments = self._calculate_adjustments(user_data)
        
        # Final score between 300 and 850
        final_score = max(300, min(850, base_score + adjustments))
        return round(final_score, 2)

    def _calculate_adjustments(self, user_data: Dict) -> float:
        """
        Calculate score adjustments based on additional factors
        """
        adjustments = 0
        
        # Payment history impact
        if user_data.get('payment_history_score', 0) > 90:
            adjustments += 50
        
        # Length of credit history
        years_of_history = user_data.get('years_of_credit_history', 0)
        if years_of_history > 5:
            adjustments += 30
        
        # Credit utilization
        utilization = user_data.get('credit_utilization', 0)
        if utilization < 30:
            adjustments += 40
        
        return adjustments

    def detect_fraud(self, transaction_data: Dict) -> Dict:
        """
        Detect potential fraud in transactions
        TODO: Add more fraud patterns
        TODO: Implement real-time detection
        TODO: Add fraud pattern learning
        TODO: Consider adding more advanced detection methods
        """
        features = self._extract_fraud_features(transaction_data)
        fraud_probability = self.fraud_model.predict_proba(features)[0][1]
        
        return {
            'fraud_probability': fraud_probability,
            'is_suspicious': fraud_probability > 0.7,
            'risk_level': self._get_risk_level(fraud_probability)
        }

    def _extract_fraud_features(self, transaction_data: Dict) -> np.ndarray:
        """
        Extract features for fraud detection
        """
        features = [
            float(transaction_data.get('amount', 0)),
            float(transaction_data.get('time_of_day', 0)),
            float(transaction_data.get('distance_from_last_transaction', 0)),
            float(transaction_data.get('frequency_last_24h', 0)),
            float(transaction_data.get('average_transaction_amount', 0))
        ]
        return np.array(features).reshape(1, -1)

    def _get_risk_level(self, probability: float) -> str:
        """
        Convert fraud probability to risk level
        """
        if probability < 0.3:
            return 'LOW'
        elif probability < 0.7:
            return 'MEDIUM'
        else:
            return 'HIGH'

    def save_models(self, path: str):
        """
        Save trained models to disk
        """
        joblib.dump(self.credit_model, f'{path}/credit_model.joblib')
        joblib.dump(self.fraud_model, f'{path}/fraud_model.joblib')
        joblib.dump(self.scaler, f'{path}/scaler.joblib')

    def load_models(self, path: str):
        """
        Load trained models from disk
        """
        self.credit_model = joblib.load(f'{path}/credit_model.joblib')
        self.fraud_model = joblib.load(f'{path}/fraud_model.joblib')
        self.scaler = joblib.load(f'{path}/scaler.joblib')

    def evaluate_business_risk(self, business_data: Dict) -> Dict:
        """
        Evaluate risk for business loans
        TODO: Add more risk factors
        TODO: Implement industry-specific analysis
        TODO: Add market condition analysis
        TODO: Consider adding more sophisticated risk assessment
        """
        risk_score = 0
        factors = []

        # Evaluate annual revenue
        annual_revenue = float(business_data.get('annual_revenue', 0))
        if annual_revenue > 1000000:
            risk_score += 30
            factors.append('Strong annual revenue')
        elif annual_revenue > 500000:
            risk_score += 20
            factors.append('Moderate annual revenue')

        # Years in operation
        years = float(business_data.get('years_in_operation', 0))
        if years > 5:
            risk_score += 25
            factors.append('Established business')
        elif years > 2:
            risk_score += 15
            factors.append('Growing business')

        # Industry risk assessment
        industry_risk = self._assess_industry_risk(business_data.get('industry', ''))
        risk_score += industry_risk['score']
        factors.append(industry_risk['factor'])

        return {
            'risk_score': risk_score,
            'risk_level': self._get_business_risk_level(risk_score),
            'factors': factors
        }

    def _assess_industry_risk(self, industry: str) -> Dict:
        """
        Assess risk based on industry type
        """
        low_risk_industries = ['technology', 'healthcare', 'education']
        medium_risk_industries = ['retail', 'manufacturing', 'services']
        high_risk_industries = ['restaurant', 'entertainment', 'construction']

        industry = industry.lower()
        if industry in low_risk_industries:
            return {'score': 25, 'factor': 'Low-risk industry'}
        elif industry in medium_risk_industries:
            return {'score': 15, 'factor': 'Medium-risk industry'}
        else:
            return {'score': 5, 'factor': 'High-risk industry'}

    def _get_business_risk_level(self, risk_score: float) -> str:
        """
        Convert business risk score to risk level
        """
        if risk_score >= 70:
            return 'LOW_RISK'
        elif risk_score >= 40:
            return 'MEDIUM_RISK'
        else:
            return 'HIGH_RISK'

@app.post("/predict_credit_score")
def predict_credit_score(user_data: Dict):
    """
    API endpoint to predict credit score
    """
    scoring_system = MshiyaneCreditScoring()
    score = scoring_system.calculate_credit_score(user_data)
    return {"credit_score": score}

@app.post("/detect_fraud")
def detect_fraud(transaction_data: Dict):
    """
    API endpoint to detect fraud
    """
    scoring_system = MshiyaneCreditScoring()
    result = scoring_system.detect_fraud(transaction_data)
    return result

@app.post("/evaluate_business_risk")
def evaluate_business_risk(business_data: Dict):
    """
    API endpoint to evaluate business risk
    """
    scoring_system = MshiyaneCreditScoring()
    risk_evaluation = scoring_system.evaluate_business_risk(business_data)
    return risk_evaluation

@app.on_event("startup")
def load_models():
    """
    Load models at startup
    """
    scoring_system = MshiyaneCreditScoring()
    scoring_system.load_models("models")

@app.on_event("shutdown")
def save_models():
    """
    Save models at shutdown
    """
    scoring_system = MshiyaneCreditScoring()
    scoring_system.save_models("models")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)