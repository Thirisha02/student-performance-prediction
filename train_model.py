import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
data = pd.read_csv("data/students.csv")

# Input features
X = data[
    [
        "study_hours",
        "attendance",
        "previous_marks",
        "assignment_score",
        "internal_marks"
    ]
]

# Target
y = data["performance"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = DecisionTreeClassifier(random_state=42)

# Train model
model.fit(X_train, y_train)

# Predict test data
predictions = model.predict(X_test)

# Calculate actual accuracy
accuracy = accuracy_score(y_test, predictions)

print("Model trained successfully!")
print("Actual Accuracy:", accuracy)

# Save model and accuracy
model_data = {
    "model": model,
    "accuracy": accuracy
}

with open("model.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("Model and accuracy saved successfully!")