import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "evaluations.csv"

# تعريف المعايير المشتركة
common_criteria = {
    "presentation_skills": ("Presentation Skills", 5),
    "content": ("Content", 5),
    "ability_to_answer": ("Ability to Answer Questions", 5),
    "presenting_idea": ("Presenting Idea Properly", 5)
}

# معايير المدربين للكورسات
trainer_criteria = {
    "Python": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "idea": ("Idea", 5),
        "error_handling": ("Error Handling", 5),
        "GUI": ("GUI", 10),
        "Code_OOP": ("Code & OOP", 40)
    },
    "Deep Learning": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "dl_accuracy": ("Accuracy & Implementation", 30),
        "dl_analysis": ("Analysis & Explanation", 15),
        "dl_code_org": ("Code Organization & Structure", 5),
        "dl_deployment": ("Deployment the Model", 10)
    },
    "Machine Learning": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "dl_accuracy": ("Accuracy & Implementation", 30),
        "dl_analysis": ("Analysis & Explanation", 15),
        "dl_code_org": ("Code Organization & Structure", 5),
        "dl_deployment": ("Deployment the Model", 10)
    },
    "Dart": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "idea": ("Idea", 5),
        "error_handling": ("Error Handling", 5),
        "data_collection": ("Data Collection", 5),
        "functions": ("Functions", 5),
        "reusability": ("Reusability", 5)
    },
    "Flutter.3": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling": ("Error Handling", 10)
    },
    "Flutter.2": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "idea": ("Idea", 5),
        "deal_with_data": ("Deal with Data (CRUD)", 25),
        "design": ("Design", 10),
        "validation_auth": ("Validation (Auth)", 15)
    },
    "Front End": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling_mohammed": ("Error Handling", 10)
    },
    "React js": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling_mohammed": ("Error Handling", 10)
    },
    "Mern": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling_mohammed": ("Error Handling", 10)
    }
}

# تحميل البيانات
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame()

st.title("عرض تقييمات الطلاب حسب الكورس")

# اختيار الكورس للعرض
selected_course = st.selectbox("اختر الكورس لعرض تقييماته:", list(trainer_criteria.keys()))

if df.empty:
    st.info("لا توجد بيانات تقييمات لعرضها.")
else:
    # فلترة بيانات الطلاب الذين ينتمون للكورس المختار
    df_course = df[df["Course"] == selected_course]

    if df_course.empty:
        st.warning(f"لا توجد تقييمات مسجلة للكورس: {selected_course}")
    else:
        # الأعمدة الخاصة بالمعايير المشتركة
        common_cols = list(common_criteria.keys())

        # الأعمدة الخاصة بمعايير الكورس المختار
        course_cols = list(trainer_criteria[selected_course].keys())

        # الأعمدة التي نريد عرضها: بيانات الطالب + المعايير المشتركة + معايير الكورس
        cols_to_show = ["Student", "Evaluator"] + common_cols + course_cols

        # تصفية الأعمدة الموجودة فقط (بعض المعايير قد لا تكون مسجلة في كل صف)
        cols_to_show = [col for col in cols_to_show if col in df_course.columns]

        # عرض الجدول
        st.subheader(f"تقييمات الطلاب في كورس {selected_course}")
        st.dataframe(df_course[cols_to_show].reset_index(drop=True))
