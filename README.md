# 🎓 Student Performance Prediction System

An AI-based web application that predicts student academic performance using Machine Learning.

## 📌 Project Overview

The Student Performance Prediction System uses student academic data such as study hours, attendance, previous marks, assignment scores, and internal marks to predict performance as:

- 🟢 High
- 🟡 Medium
- 🔴 Low

The system also identifies students who may be at academic risk and provides recommendations for improvement.

## 🚀 Features

- 🤖 Machine Learning based performance prediction
- 📊 Interactive Streamlit dashboard
- 🗄️ SQLite database integration
- 🚨 At-Risk Student Detection
- 🔎 Student Search
- 📈 Performance Distribution Charts
- 📝 Prediction History
- 📥 Downloadable Student Reports
- 📚 Dataset Overview
- 💡 Academic improvement recommendations

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Streamlit
- SQLite
- Pickle

## 🤖 Machine Learning Model

### Decision Tree Classifier

The model uses the following features:

1. Study Hours
2. Attendance
3. Previous Exam Marks
4. Assignment Score
5. Internal Exam Marks

The model predicts the student's academic performance category.

> Note: The current dataset is a small demo dataset. The reported test accuracy is based on this dataset and should be re-evaluated using a larger real-world dataset.

## 📂 Project Structure

```text
student performance prediction/
│
├── data/
│   └── students.csv
│
├── app.py
├── train_model.py
├── database.py
├── model.pkl
├── students.db
├── requirements.txt
└── README.md