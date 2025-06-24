import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib
from typing import Dict, List, Optional
from datetime import datetime
import json

# TODO: Need to implement model versioning system
# TODO: Add more sophisticated feature engineering
# TODO: Implement A/B testing framework
# TODO: Add model performance monitoring
# TODO: Consider adding more advanced ML models (neural networks?)

class MshiyaneCreditScoringSystem:
    def __init__(self):
        # Had to tune these parameters after initial poor performance
        # XGBoost performed better than RandomForest for our use case
        self.scaler = StandardScaler()
        self.model = XGBRegressor(
            n_estimators=200,  # Increased from 100 after testing
            learning_rate=0.05,  # Reduced to prevent overfitting
            max_depth=6,  # Found this to be optimal after grid search
            subsample=0.8,  # Helps with generalization
            colsample_bytree=0.8,  # Feature sampling for better robustness
            random_state=42
        )
        self.feature_importance = {}
        self.model_version = "1.0.0"  # Need to implement proper versioning
        self.last_training_date = None
        
    def preprocess_features(self, user_data: Dict) -> np.ndarray:
        """
        Enhanced feature preprocessing with more sophisticated features
        TODO: Add more domain-specific features
        TODO: Implement feature selection based on importance
        TODO: Add feature validation
        TODO: Consider adding more advanced feature engineering
        """
        basic_features = [
            float(user_data.get('annual_income', 0)),
            float(user_data.get('years_of_credit_history', 0)),
            float(user_data.get('num_accounts', 0)),
            float(user_data.get('payment_history_score', 0)),
            float(user_data.get('debt_to_income_ratio', 0)),
            float(user_data.get('num_recent_inquiries', 0)),
            float(user_data.get('age', 0))
        ]
        
        # Advanced features
        advanced_features = [
            self._calculate_income_stability(user_data),
            self._analyze_transaction_patterns(user_data),
            self._calculate_savings_ratio(user_data),
            self._assess_employment_stability(user_data),
            self._calculate_behavioral_score(user_data)
        ]
        
        return np.array(basic_features + advanced_features).reshape(1, -1)

    def _calculate_income_stability(self, user_data: Dict) -> float:
        """
        Calculate income stability score based on income history
        """
        income_history = user_data.get('income_history', [])
        if not income_history:
            return 0.0
            
        variations = np.std(income_history) / np.mean(income_history) if income_history else 1.0
        stability_score = 1.0 / (1.0 + variations)
        return min(1.0, stability_score)

    def _analyze_transaction_patterns(self, user_data: Dict) -> float:
        """
        Analyze transaction patterns for consistency and reliability
        """
        transactions = user_data.get('transaction_history', [])
        if not transactions:
            return 0.0
            
        # Analyze transaction regularity
        transaction_amounts = [t.get('amount', 0) for t in transactions]
        transaction_regularity = 1.0 - (np.std(transaction_amounts) / (np.mean(transaction_amounts) + 1e-6))
        return max(0.0, min(1.0, transaction_regularity))

    def _calculate_savings_ratio(self, user_data: Dict) -> float:
        """
        Calculate savings to income ratio
        """
        annual_income = float(user_data.get('annual_income', 0))
        savings = float(user_data.get('savings_amount', 0))
        
        if annual_income == 0:
            return 0.0
            
        savings_ratio = min(1.0, savings / (annual_income + 1e-6))
        return savings_ratio

    def _assess_employment_stability(self, user_data: Dict) -> float:
        """
        Assess employment stability
        """
        employment_history = user_data.get('employment_history', [])
        if not employment_history:
            return 0.0
            
        total_years = sum(job.get('duration_years', 0) for job in employment_history)
        num_jobs = len(employment_history)
        
        if num_jobs == 0:
            return 0.0
            
        avg_tenure = total_years / num_jobs
        stability_score = min(1.0, avg_tenure / 5.0)  # Normalize to 5 years
        return stability_score

    def _calculate_behavioral_score(self, user_data: Dict) -> float:
        """
        Calculate behavioral score based on user activities
        """
        behavior_factors = {
            'on_time_payments': user_data.get('on_time_payment_ratio', 0),
            'savings_frequency': user_data.get('savings_frequency', 0),
            'overdraft_frequency': 1.0 - user_data.get('overdraft_frequency', 0),
            'mobile_app_usage': user_data.get('mobile_app_usage_score', 0)
        }
        
        weights = {
            'on_time_payments': 0.4,
            'savings_frequency': 0.3,
            'overdraft_frequency': 0.2,
            'mobile_app_usage': 0.1
        }
        
        behavioral_score = sum(score * weights[factor] for factor, score in behavior_factors.items())
        return min(1.0, behavioral_score)

    def calculate_credit_score(self, user_data: Dict) -> Dict:
        """
        Calculate enhanced credit score with detailed breakdown
        TODO: Add confidence intervals
        TODO: Implement model explainability
        TODO: Add bias detection
        TODO: Consider adding more sophisticated scoring components
        """
        features = self.preprocess_features(user_data)
        scaled_features = self.scaler.transform(features)
        
        # Base score prediction
        base_score = self.model.predict(scaled_features)[0]
        
        # Calculate component scores
        component_scores = {
            'payment_history': self._calculate_payment_history_score(user_data),
            'credit_utilization': self._calculate_credit_utilization_score(user_data),
            'credit_age': self._calculate_credit_age_score(user_data),
            'income_stability': self._calculate_income_stability(user_data),
            'behavioral': self._calculate_behavioral_score(user_data)
        }
        
        # Apply weights to component scores
        weights = {
            'payment_history': 0.35,
            'credit_utilization': 0.30,
            'credit_age': 0.15,
            'income_stability': 0.10,
            'behavioral': 0.10
        }
        
        weighted_score = sum(score * weights[component] 
                           for component, score in component_scores.items())
        
        # Final score between 300 and 850
        final_score = max(300, min(850, base_score * weighted_score))
        
        return {
            'credit_score': round(final_score, 2),
            'component_scores': component_scores,
            'score_breakdown': {
                component: round(score * 100, 2)
                for component, score in component_scores.items()
            },
            'risk_level': self._get_risk_level(final_score),
            'improvement_tips': self._generate_improvement_tips(component_scores),
            'model_version': self.model_version
        }

    def _calculate_payment_history_score(self, user_data: Dict) -> float:
        """
        Calculate payment history score
        """
        payment_history = user_data.get('payment_history', {})
        on_time_payments = payment_history.get('on_time', 0)
        total_payments = payment_history.get('total', 1)
        late_payments = payment_history.get('late', 0)
        
        if total_payments == 0:
            return 0.0
            
        score = (on_time_payments / total_payments) * (1 - 0.1 * late_payments)
        return max(0.0, min(1.0, score))

    def _calculate_credit_utilization_score(self, user_data: Dict) -> float:
        """
        Calculate credit utilization score
        """
        total_credit = float(user_data.get('total_credit', 0))
        used_credit = float(user_data.get('used_credit', 0))
        
        if total_credit == 0:
            return 0.0
            
        utilization = used_credit / total_credit
        score = 1.0 - min(1.0, utilization)
        return score

    def _calculate_credit_age_score(self, user_data: Dict) -> float:
        """
        Calculate credit age score
        """
        years_of_history = float(user_data.get('years_of_credit_history', 0))
        score = min(1.0, years_of_history / 10.0)  # Normalize to 10 years
        return score

    def _get_risk_level(self, credit_score: float) -> str:
        """
        Determine risk level based on credit score
        """
        if credit_score >= 750:
            return 'EXCELLENT'
        elif credit_score >= 700:
            return 'GOOD'
        elif credit_score >= 650:
            return 'FAIR'
        elif credit_score >= 600:
            return 'POOR'
        else:
            return 'VERY_POOR'

    def _generate_improvement_tips(self, component_scores: Dict) -> List[str]:
        """
        Generate personalized improvement tips based on component scores
        """
        tips = []
        
        if component_scores['payment_history'] < 0.8:
            tips.append("Make all payments on time to improve your payment history")
            
        if component_scores['credit_utilization'] < 0.7:
            tips.append("Try to keep your credit utilization below 30%")
            
        if component_scores['income_stability'] < 0.6:
            tips.append("Maintain stable income sources and keep employment records")
            
        if component_scores['behavioral'] < 0.7:
            tips.append("Use mobile banking regularly and maintain consistent savings")
            
        return tips

    def train_model(self, training_data: pd.DataFrame):
        """
        Train the model with cross-validation
        TODO: Add early stopping
        TODO: Implement hyperparameter tuning
        TODO: Add model validation metrics
        TODO: Consider adding more advanced training techniques
        """
        X = training_data.drop('credit_score', axis=1)
        y = training_data['credit_score']
        
        # Perform cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        
        # Train final model
        self.model.fit(X, y)
        
        # Update feature importance
        self.feature_importance = dict(zip(X.columns, self.model.feature_importances_))
        
        # Update model metadata
        self.last_training_date = datetime.now().isoformat()
        
        return {
            'cv_scores_mean': cv_scores.mean(),
            'cv_scores_std': cv_scores.std(),
            'feature_importance': self.feature_importance
        }

    def save_model(self, path: str):
        """
        Save model and metadata
        TODO: Add model versioning
        TODO: Implement model backup
        TODO: Add model validation before saving
        TODO: Consider adding model compression
        """
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance,
            'model_version': self.model_version,
            'last_training_date': self.last_training_date
        }
        joblib.dump(model_data, f'{path}/enhanced_credit_model.joblib')

    def load_model(self, path: str):
        """
        Load model and metadata
        """
        model_data = joblib.load(f'{path}/enhanced_credit_model.joblib')
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_importance = model_data['feature_importance']
        self.model_version = model_data['model_version']
        self.last_training_date = model_data['last_training_date'] 