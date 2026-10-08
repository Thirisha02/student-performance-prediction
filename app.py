import streamlit as st
import pickle
import pandas as pd
import sqlite3

# -----------------------------
# Load trained model
# -----------------------------
with open("model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
accuracy = model_data["accuracy"]


# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_csv("data/students.csv")


# -----------------------------
# Database connection
# -----------------------------
def get_connection():
    return sqlite3.connect("students.db")


# -----------------------------
# Save prediction
# -----------------------------
def save_prediction(
    name,
    study_hours,
    attendance,
    previous_marks,
    assignment_score,
    internal_marks,
    performance
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (
            student_name,
            study_hours,
            attendance,
            previous_marks,
            assignment_score,
            internal_marks,
            performance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        study_hours,
        attendance,
        previous_marks,
        assignment_score,
        internal_marks,
        performance
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Get predictions
# -----------------------------
def get_predictions():
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🎓 Student Performance Prediction")

st.write(
    "An AI-based system to predict student academic performance."
)


# ============================================================
# GET SAVED DATA
# ============================================================

saved_data = get_predictions()


# ============================================================
# DASHBOARD
# ============================================================

st.subheader("📊 Performance Dashboard")

total_predictions = len(saved_data)

high_count = len(
    saved_data[saved_data["performance"] == "High"]
)

medium_count = len(
    saved_data[saved_data["performance"] == "Medium"]
)

low_count = len(
    saved_data[saved_data["performance"] == "Low"]
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Predictions",
        total_predictions
    )

with col2:
    st.metric(
        "🟢 High",
        high_count
    )

with col3:
    st.metric(
        "🟡 Medium",
        medium_count
    )

with col4:
    st.metric(
        "🔴 Low",
        low_count
    )


st.divider()


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.subheader("📚 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Students",
        len(data)
    )

with col2:
    st.metric(
        "Average Attendance",
        f"{data['attendance'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Average Study Hours",
        f"{data['study_hours'].mean():.1f}"
    )


st.divider()


# ============================================================
# STUDENT INPUT
# ============================================================

st.subheader("👤 Enter Student Details")

name = st.text_input(
    "Student Name"
)

study_hours = st.number_input(
    "Daily Study Hours",
    min_value=0.0,
    max_value=24.0,
    value=2.0
)

attendance = st.number_input(
    "Attendance Percentage",
    min_value=0.0,
    max_value=100.0,
    value=75.0
)

previous_marks = st.number_input(
    "Previous Exam Marks",
    min_value=0.0,
    max_value=100.0,
    value=50.0
)

assignment_score = st.number_input(
    "Assignment Score",
    min_value=0.0,
    max_value=100.0,
    value=50.0
)

internal_marks = st.number_input(
    "Internal Exam Marks",
    min_value=0.0,
    max_value=100.0,
    value=50.0
)


# ============================================================
# MODEL INFORMATION
# ============================================================

st.info(
    f"🤖 Model Accuracy: {accuracy * 100:.0f}%"
)


# ============================================================
# PREDICTION
# ============================================================

if st.button(
    "🔮 Predict Performance",
    use_container_width=True
):

    if name.strip() == "":
        st.warning(
            "⚠️ Please enter the student name."
        )

    else:

        prediction = model.predict([[
            study_hours,
            attendance,
            previous_marks,
            assignment_score,
            internal_marks
        ]])

        result = prediction[0]


        # Save prediction
        save_prediction(
            name,
            study_hours,
            attendance,
            previous_marks,
            assignment_score,
            internal_marks,
            result
        )


        # Success messages
        st.success(
            "✅ Prediction completed successfully!"
        )

        st.success(
            "💾 Prediction saved to database!"
        )


        # Student name
        st.write("### 👤 Student Name")

        st.write(name)


        # Prediction result
        st.write("### 📊 Predicted Performance")


        if result == "High":

            st.success(
                "🟢 High Performance"
            )

            st.success(
                "🌟 Good Academic Performance"
            )

            st.write(
                "💡 Keep maintaining the current study habits and performance."
            )


        elif result == "Medium":

            st.warning(
                "🟡 Medium Performance"
            )

            st.warning(
                "⚠️ Needs Improvement"
            )

            st.write(
                "💡 Student should improve consistency, attendance and academic performance."
            )


        else:

            st.error(
                "🔴 Low Performance"
            )

            st.error(
                "⚠️ At Risk Student"
            )

            st.write(
                "💡 Student should improve attendance, study hours and marks."
            )


# ============================================================
# REFRESH DATA
# ============================================================

saved_data = get_predictions()


# ============================================================
# AT-RISK STUDENTS
# ============================================================

st.divider()

st.subheader("🚨 At-Risk Students")

at_risk_students = saved_data[
    saved_data["performance"] == "Low"
]

st.metric(
    "🔴 Total At-Risk Students",
    len(at_risk_students)
)

if len(at_risk_students) > 0:

    st.warning(
        "⚠️ These students may need academic support."
    )

    st.dataframe(
        at_risk_students,
        use_container_width=True
    )

else:

    st.success(
        "🎉 No At-Risk students found!"
    )


# ============================================================
# STUDENT SEARCH
# ============================================================

st.divider()

st.subheader("🔎 Search Student")

search_name = st.text_input(
    "Enter student name to search"
)


if search_name.strip() != "":

    search_result = saved_data[
        saved_data["student_name"].str.contains(
            search_name,
            case=False,
            na=False
        )
    ]

    if len(search_result) > 0:

        st.success(
            f"✅ {len(search_result)} record(s) found."
        )

        st.dataframe(
            search_result,
            use_container_width=True
        )


        # -----------------------------
        # Download Student Report
        # -----------------------------

        csv_report = search_result.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Student Report",
            data=csv_report,
            file_name=f"{search_name}_student_report.csv",
            mime="text/csv"
        )


    else:

        st.warning(
            "❌ No student found with that name."
        )


# ============================================================
# DATASET PERFORMANCE DISTRIBUTION
# ============================================================

st.divider()

st.subheader(
    "📈 Dataset Performance Distribution"
)

performance_counts = data[
    "performance"
].value_counts()

st.bar_chart(
    performance_counts
)


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.divider()

st.subheader(
    "🗄️ Prediction History"
)

if len(saved_data) > 0:

    st.dataframe(
        saved_data,
        use_container_width=True
    )

else:

    st.info(
        "No predictions saved yet."
    )


# ============================================================
# PREDICTION HISTORY CHART
# ============================================================

if len(saved_data) > 0:

    st.subheader(
        "📊 Prediction History Chart"
    )

    history_counts = saved_data[
        "performance"
    ].value_counts()

    st.bar_chart(
        history_counts
    )


# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

st.divider()

st.subheader(
    "🤖 Machine Learning Model"
)

st.write(
    "Model Used: Decision Tree Classifier"
)

st.write(
    f"Test Accuracy: {accuracy * 100:.0f}%"
)

st.write(
    "Features Used: Study Hours, Attendance, Previous Marks, Assignment Score and Internal Marks."
)


# ============================================================
# PROJECT SUMMARY
# ============================================================

st.divider()

st.subheader("💡 Project Summary")

st.write(
    """
This system uses machine learning to predict student academic
performance based on study hours, attendance, previous marks,
assignment scores and internal marks.

The system stores prediction results in an SQLite database,
provides a dashboard, identifies at-risk students, allows
student searching and provides downloadable student reports.
"""
)