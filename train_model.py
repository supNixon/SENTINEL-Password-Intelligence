from src.analyzer import load_or_train_model
model, status = load_or_train_model()
print(status)
print("Model saved as password_model.joblib")
