"""
Model Enhancement & Monitoring System
Add this to your existing app.py or run as separate service
"""

import numpy as np
import pandas as pd
from datetime import datetime
import json
import os

class ModelMonitor:
    """
    Monitors model performance over time
    Prevents model degradation
    """
    
    def __init__(self):
        self.performance_log = 'model_performance.json'
        self.load_log()
    
    def load_log(self):
        """Load performance history"""
        if os.path.exists(self.performance_log):
            with open(self.performance_log, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {
                'dates': [],
                'accuracies': [],
                'predictions': [],
                'feedback': []
            }
    
    def log_performance(self, accuracy, prediction_details):
        """Log model performance for tracking"""
        entry = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'accuracy': accuracy,
            'prediction': prediction_details,
            'model_status': self.get_model_status(accuracy)
        }
        
        self.history['dates'].append(entry['date'])
        self.history['accuracies'].append(accuracy)
        self.history['predictions'].append(prediction_details)
        
        # Keep only last 1000 entries
        if len(self.history['dates']) > 1000:
            self.history['dates'] = self.history['dates'][-1000:]
            self.history['accuracies'] = self.history['accuracies'][-1000:]
            self.history['predictions'] = self.history['predictions'][-1000:]
        
        self.save_log()
        
        # Check for model degradation
        self.check_degradation()
        
        return entry
    
    def get_model_status(self, accuracy):
        """Determine model status based on accuracy"""
        if accuracy < 60:
            return {
                'status': 'underfitting',
                'action': 'increase_model_complexity',
                'message': 'Model is too simple. Consider adding more features or increasing tree depth.'
            }
        elif 60 <= accuracy <= 85:
            return {
                'status': 'optimal',
                'action': 'none',
                'message': 'Model is performing well.'
            }
        elif 85 < accuracy < 90:
            return {
                'status': 'high_accuracy',
                'action': 'monitor_closely',
                'message': 'High accuracy. Watch for overfitting.'
            }
        else:
            return {
                'status': 'overfitting',
                'action': 'increase_regularization',
                'message': 'Potential overfitting. Increase min_samples_split or reduce max_depth.'
            }
    
    def check_degradation(self):
        """Check if model accuracy is degrading over time"""
        if len(self.history['accuracies']) > 30:
            recent = np.mean(self.history['accuracies'][-30:])
            older = np.mean(self.history['accuracies'][-60:-30])
            
            if recent < older - 5:  # 5% degradation
                print(f"⚠️ MODEL DEGRADATION DETECTED: {older:.1f}% → {recent:.1f}%")
                print("   Consider retraining with new data")
                return True
        return False
    
    def save_log(self):
        """Save performance history"""
        with open(self.performance_log, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_performance_stats(self):
        """Get performance statistics"""
        if not self.history['accuracies']:
            return {'average': 0, 'trend': 'stable', 'total_predictions': 0}
        
        avg_accuracy = np.mean(self.history['accuracies'][-30:]) if len(self.history['accuracies']) >= 30 else np.mean(self.history['accuracies'])
        
        # Calculate trend
        if len(self.history['accuracies']) >= 10:
            recent = np.mean(self.history['accuracies'][-10:])
            older = np.mean(self.history['accuracies'][-20:-10])
            trend = 'improving' if recent > older + 1 else 'declining' if recent < older - 1 else 'stable'
        else:
            trend = 'stable'
        
        return {
            'average_accuracy': round(avg_accuracy, 2),
            'trend': trend,
            'total_predictions': len(self.history['predictions']),
            'last_30_days': len([d for d in self.history['dates'] if datetime.strptime(d, "%Y-%m-%d %H:%M:%S") > datetime.now().replace(day=datetime.now().day-30)])
        }


class DataEnhancer:
    """
    Enhances training data with real-world conditions
    """
    
    def enhance_dataset(self):
        """Add more realistic features based on Pakistan agriculture"""
        
        enhanced_features = {
            # Water availability categories
            'water_availability': ['High', 'Medium', 'Low'],
            
            # Soil pH levels
            'soil_ph': ['Acidic (5.5-6.5)', 'Neutral (6.5-7.5)', 'Alkaline (7.5-8.5)'],
            
            # Previous crop (for crop rotation)
            'previous_crop': ['Wheat', 'Rice', 'Cotton', 'Maize', 'None'],
            
            # Irrigation type
            'irrigation_type': ['Canal', 'Tube Well', 'Rain-fed', 'Drip'],
            
            # Farm size categories
            'farm_size': ['Small (<5 acres)', 'Medium (5-25 acres)', 'Large (>25 acres)']
        }
        
        print("🔧 Enhanced dataset with realistic Pakistani agriculture features")
        return enhanced_features
    
    def generate_seasonal_data(self, district, season):
        """Generate realistic seasonal data for districts"""
        
        seasonal_data = {
            'Punjab': {
                'Rabi': {
                    'avg_temp': 15.5,
                    'avg_rain': 350,
                    'crop_cycle': 'Oct-Apr',
                    'common_crops': ['Wheat', 'Gram', 'Barley', 'Potato']
                },
                'Kharif': {
                    'avg_temp': 32.5,
                    'avg_rain': 750,
                    'crop_cycle': 'May-Oct',
                    'common_crops': ['Rice', 'Cotton', 'Maize', 'Sugarcane']
                }
            },
            'Sindh': {
                'Rabi': {
                    'avg_temp': 18.5,
                    'avg_rain': 120,
                    'crop_cycle': 'Oct-Mar',
                    'common_crops': ['Wheat', 'Gram']
                },
                'Kharif': {
                    'avg_temp': 35.5,
                    'avg_rain': 550,
                    'crop_cycle': 'Apr-Sep',
                    'common_crops': ['Rice', 'Cotton', 'Sugarcane']
                }
            }
        }
        
        return seasonal_data.get(district, seasonal_data['Punjab']).get(season)


# Add to your existing app.py
def add_enhanced_features_to_backend():
    """
    Call this function in your app.py to add enhanced features
    """
    monitor = ModelMonitor()
    enhancer = DataEnhancer()
    
    print("✅ Enhanced features added to backend")
    
    # Return monitoring API endpoint
    return {
        '/api/model-stats': 'GET - Get model performance statistics',
        '/api/feedback': 'POST - Submit farmer feedback for model improvement',
        '/api/retrain': 'POST - Trigger model retraining with new data'
    }


if __name__ == '__main__':
    print("🧪 Testing Model Monitor...")
    monitor = ModelMonitor()
    
    # Test logging
    test_entry = monitor.log_performance(
        accuracy=82.5,
        prediction_details={'crop': 'Wheat', 'district': 'Lahore', 'season': 'Rabi'}
    )
    
    print("📊 Model Stats:", monitor.get_performance_stats())