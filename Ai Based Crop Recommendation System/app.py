"""
Crop Recommendation System - Backend Server
Flask API with scikit-learn Decision Tree Model

Requirements:
pip install flask flask-cors pandas numpy scikit-learn
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# GLOBAL VARIABLES

model = None
label_encoders = {}
model_accuracy = 0
feature_names = ['temp', 'rain', 'soilType', 'season']
crop_names_urdu = {
    'Wheat': 'گندم / Wheat',
    'Rice': 'چاول / Rice',
    'Cotton': 'کپاس / Cotton',
    'Maize': 'مکئی / Maize',
    'Sugarcane': 'گنا / Sugarcane',
    'Barley': 'جَو / Barley',
    'Gram': 'چنا / Gram',
    'Potato': 'آلو / Potato',
    'Mung': 'مونگ / Mung',
    'Sorghum': 'جوار / Sorghum'
}

# CSV DATASET LOADING 
def load_csv_dataset():
    print("Loading dataset from CSV file...")
    try:
        # Load CSV file
        df = pd.read_csv('crop_data.csv')
        
        print(f"CSV dataset loaded: {len(df)} samples")
        print(f"Columns found: {list(df.columns)}")
        
        # Show dataset statistics
        print(f"\nDataset Statistics:")
        print(f"   Total samples: {len(df)}")
        print(f"   Crop distribution:")
        crop_counts = df['crop'].value_counts()
        for crop, count in crop_counts.items():
            percentage = (count / len(df)) * 100
            print(f"     {crop}: {count} samples ({percentage:.1f}%)")
        
        print(f"\nFeature Ranges:")
        print(f"   Temperature: {df['temp'].min():.1f} to {df['temp'].max():.1f}°C")
        print(f"   Rainfall: {df['rain'].min():.0f} to {df['rain'].max():.0f} mm")
        print(f"   Soil types: {df['soilType'].nunique()} types")
        print(f"   Seasons: {df['season'].unique().tolist()}")
        
        # Shuffle data
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        return df
        
    except FileNotFoundError:
        print("ERROR: crop_data.csv not found!")
        print("   Creating a sample CSV file...")
        return create_sample_csv_dataset()
    except Exception as e:
        print(f"Error loading CSV: {e}")
        print("   Creating a sample CSV file...")
        return create_sample_csv_dataset()

# MACHINE LEARNING MODEL 

def train_model():
    global model, label_encoders, model_accuracy
    
    print("\n" + "="*70)
    print("TRAINING MACHINE LEARNING MODEL FROM CSV DATASET")
    print("="*70)
    
    df = load_csv_dataset()  # load kary ga csv file
    
    # Feature Selection: imp feature use kary ga
    print("\nSelected Features: temp, rain, soilType, season")
    print("   (Removed: humidity - correlated, sunshine - irrelevant)")
    
    # features and target prepared
    X = df[feature_names].copy()
    y = df['crop']
    
    # Encode categorical variables ML ky liye 
    print("\nEncoding categorical features...")
    label_encoders['soilType'] = LabelEncoder()
    label_encoders['season'] = LabelEncoder()
    
    X['soilType'] = label_encoders['soilType'].fit_transform(X['soilType'])
    X['season'] = label_encoders['season'].fit_transform(X['season'])
    
    # Train/Test Split (80/20)
    print("\nSplitting data: 80% training, 20% testing")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y  # ✅ Maintain class balance
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    print("   ✅ Completely separate datasets (no data leakage)")
    
    # Create Decision Tree with proper hyperparameters
    print("\nBuilding Decision Tree Classifier...")
    print("   Hyperparameters (prevent overfitting):")
    print("   - max_depth: 5")
    print("   - min_samples_split: 30")
    print("   - min_samples_leaf: 10")
    print("   - criterion: gini")
    
    model = DecisionTreeClassifier(
        max_depth=5,              # Prevent overfitting
        min_samples_split=30,     # Avoid tiny splits
        min_samples_leaf=10,      # Ensure generalization
        criterion='gini',         # Gini impurity
        random_state=42
    )
    
    # Train model on training data ONLY
    print("\nTraining model...")
    model.fit(X_train, y_train)
    
    # Evaluate on TEST data 
    print("\nEvaluating model on TEST dataset...")
    train_accuracy = model.score(X_train, y_train) * 100
    test_accuracy = model.score(X_test, y_test) * 100
    model_accuracy = test_accuracy
    
    print(f"   Training Accuracy: {train_accuracy:.2f}%")
    print(f"   Testing Accuracy: {test_accuracy:.2f}%")
    
    # Check for overfitting/underfitting
    print("\nModel Status:")
    if test_accuracy < 60:
        print(f"   UNDERFITTING ({test_accuracy:.1f}% < 60%)")
        print("   → Model is too simple, not learning patterns")
    elif 60 <= test_accuracy <= 85:
        print(f"   OPTIMAL ({test_accuracy:.1f}% in 60-85% range)")
        print("   → Model is well-balanced and ready for production")
    elif 85 < test_accuracy < 90:
        print(f"   HIGH ACCURACY ({test_accuracy:.1f}% in 85-90% range)")
        print("   → Model is performing well, acceptable")
    else:
        print(f"   OVERFITTING RISK ({test_accuracy:.1f}% > 90%)")
        print("   → Model may be memorizing training data")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    for idx, row in feature_importance.iterrows():
        print(f"   {row['feature']}: {row['importance']:.3f}")
    
    # Save model
    print("\nSaving model...")
    with open('crop_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('label_encoders.pkl', 'wb') as f:
        pickle.dump(label_encoders, f)
    
    print("="*70)
    print("MODEL TRAINING COMPLETE FROM CSV DATASET")
    print("="*70)
    
    return model, model_accuracy

# API ENDPOINTS 

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """
    model ki info or statistics lega
    """
    global model_accuracy
    
    if model_accuracy < 60:
        status = "underfitting"
        message = "Underfitting (< 60%)"
    elif 60 <= model_accuracy <= 85:
        status = "optimal"
        message = "Optimal (60-85%)"
    elif 85 < model_accuracy < 90:
        status = "high"
        message = "High (85-90%)"
    else:
        status = "overfitting"
        message = "Overfitting (> 90%)"
    
    return jsonify({
        'accuracy': round(model_accuracy, 2),
        'status': status,
        'message': message,
        'features': feature_names,
        'total_crops': 10,
        'data_source': 'CSV Dataset'
    })

@app.route('/api/predict', methods=['POST'])
def predict_crop():
    """
    Predict crop based on input parameters
    """
    try:
        data = request.json
        # Validate input
        required_fields = ['temp', 'rain', 'soilType', 'season']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Prepare input data
        input_df = pd.DataFrame([{
            'temp': float(data['temp']),
            'rain': float(data['rain']),
            'soilType': data['soilType'],
            'season': data['season']
        }])
        
        # Encode categorical features
        input_df['soilType'] = label_encoders['soilType'].transform(input_df['soilType'])
        input_df['season'] = label_encoders['season'].transform(input_df['season'])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Get confidence (probability of predicted class)
        confidence = float(max(prediction_proba) * 100)
        
        # Get bilingual name
        crop_name = crop_names_urdu.get(prediction, prediction)
        
        print(f"Prediction: {prediction} (Confidence: {confidence:.1f}%)")
        
        return jsonify({
            'crop': prediction,
            'crop_bilingual': crop_name,
            'confidence': round(confidence, 2),
            'model_accuracy': round(model_accuracy, 2),
            'all_probabilities': {
                crop: round(float(prob) * 100, 2) 
                for crop, prob in zip(model.classes_, prediction_proba)
            }
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_accuracy': round(model_accuracy, 2),
        'data_source': 'CSV Dataset'
    })

@app.route('/api/dataset-info', methods=['GET'])
def dataset_info():
    """
    Get information about the dataset
    """
    try:
        if os.path.exists('crop_data.csv'):
            df = pd.read_csv('crop_data.csv')
            return jsonify({
                'dataset': 'crop_data.csv',
                'samples': len(df),
                'crops': int(df['crop'].nunique()),
                'columns': list(df.columns),
                'size_kb': round(os.path.getsize('crop_data.csv') / 1024, 2)
            })
        else:
            return jsonify({
                'dataset': 'Not found',
                'message': 'CSV file will be created when training'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MAIN 

if __name__ == '__main__':
    print("\n" + "="*70)
    print("CROP RECOMMENDATION SYSTEM ")
    print("="*70)
    
    # Check if model exists
    if os.path.exists('crop_model.pkl') and os.path.exists('label_encoders.pkl'):
        print("\nLoading existing model...")
        with open('crop_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        
        # Quick evaluation to get accuracy - USE CSV NOW
        print("Evaluating with CSV dataset...")
        df = load_csv_dataset()  # CHANGED FROM: generate_balanced_training_data()
        X = df[feature_names].copy()
        y = df['crop']
        X['soilType'] = label_encoders['soilType'].transform(X['soilType'])
        X['season'] = label_encoders['season'].transform(X['season'])
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model_accuracy = model.score(X_test, y_test) * 100
        print(f"Model loaded! Accuracy: {model_accuracy:.2f}%")
    else:
        print("\nNo existing model found. Training new model from CSV...")
        train_model()
    
    print("\n" + "="*70)
    print("Starting Flask Server...")
    print("="*70)
    print("\nAPI Endpoints:")
    print("   GET  /api/health        - Health check")
    print("   GET  /api/model-info    - Model information")
    print("   GET  /api/dataset-info  - Dataset information")
    print("   POST /api/predict       - Crop prediction")
    print("\nUsing dataset: crop_data.csv")
    print("Server running at: http://localhost:5000")
    print("="*70 + "\n")
    
    # Run Flask server
    app.run(debug=True, host='0.0.0.0', port=5001)