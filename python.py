# Create a Python file called create_requirements.py
requirements_content = """flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
joblib==1.3.2"""

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

print("✅ requirements.txt created successfully!")