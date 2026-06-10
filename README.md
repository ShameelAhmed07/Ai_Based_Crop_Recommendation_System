# 🌾 AI-Based Crop Recommendation System

An intelligent web application that recommends the most suitable crop to cultivate based on soil type, weather conditions, and seasonal data — built using Python, Flask, and a Decision Tree machine learning model.

---

## 📌 Problem Statement

Farmers in Pakistan often lack access to data-driven guidance when deciding which crop to plant. Poor crop selection leads to low yields, wasted resources, and financial losses. This system aims to solve that by providing instant, AI-powered crop recommendations based on real agricultural parameters.

---

## 🚀 Features

- 🌡️ Takes temperature, rainfall, soil type, and season as input
- 🤖 Predicts the best crop using a trained Decision Tree Classifier
- 🌐 Bilingual output — English & Urdu (e.g., گندم / Wheat)
- 📊 Shows model confidence score with every prediction
- 🖥️ Clean, interactive web interface (HTML/CSS/JS frontend)
- 🔗 REST API powered by Flask

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| ML Model | Decision Tree Classifier (scikit-learn) |
| Backend | Flask + Flask-CORS |
| Frontend | HTML, CSS, JavaScript |
| Data Processing | Pandas, NumPy |
| Model Persistence | Pickle |
| Dataset | Custom CSV (900 samples, 6 features) |

---

## 🌱 Supported Crops

Wheat · Rice · Cotton · Maize · Sugarcane · Barley · Gram · Potato · Mung · Sorghum

---

## 📥 Input Parameters

| Parameter | Description | Example |
|---|---|---|
| `temp` | Temperature in °C | 27.5 |
| `rain` | Rainfall in mm | 600 |
| `soilType` | Type of soil | Loamy, Alluvial, Clay |
| `season` | Crop season | Rabi, Kharif |

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Algorithm | Decision Tree Classifier |
| Train/Test Split | 80% / 20% |
| Dataset Size | 900 samples |
| Criterion | Gini Impurity |
| Max Depth | 5 (to prevent overfitting) |
| Accuracy Range | 60–85% (Optimal) |

The model is tuned with `max_depth=5`, `min_samples_split=30`, and `min_samples_leaf=10` to ensure generalization and avoid overfitting.

---

## 📁 Project Structure

```
Ai-Based-Crop-Recommendation-System/
│
├── app.py                  # Flask backend & ML model training
├── model_enhancer.py       # Model monitoring & performance tracking
├── crop_data.csv           # Dataset (900 samples)
├── crop_model.pkl          # Saved trained model
├── label_encoders.pkl      # Saved label encoders
├── index.html              # Frontend UI
├── style.css               # Styling
├── script.js               # Frontend logic
└── requirements.txt        # Python dependencies
```

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/ShameelAhmed07/Ai-Based-Crop-Recommendation-System.git
cd Ai-Based-Crop-Recommendation-System
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Flask server
```bash
python app.py
```

### 4. Open the app
Open `index.html` in your browser, or navigate to:
```
http://localhost:5001
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check if server is running |
| GET | `/api/model-info` | Get model accuracy & status |
| GET | `/api/dataset-info` | Get dataset statistics |
| POST | `/api/predict` | Get crop recommendation |

### Sample API Request
```json
POST /api/predict
{
  "temp": 27.5,
  "rain": 600,
  "soilType": "Loamy",
  "season": "Rabi"
}
```

### Sample API Response
```json
{
  "crop": "Wheat",
  "crop_bilingual": "گندم / Wheat",
  "confidence": 91.5,
  "model_accuracy": 78.33,
  "all_probabilities": {
    "Wheat": 91.5,
    "Rice": 3.2,
    "Cotton": 5.3
  }
}
```

---

## 👨‍💻 Author

**Shameel Ahmed**
Student — Sir Syed University of Engineering & Technology (SSUET)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/Shameel-Ahmed)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/ShameelAhmed07)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
