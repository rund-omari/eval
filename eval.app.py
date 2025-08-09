# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "evaluations.csv"

# إنشاء الملف إذا لم يكن موجود
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Course", "Student", "Evaluator",
        # المعايير المشتركة
        "presentation_skills", "content", "ability_to_answer", "presenting_idea",
        # معايير المدربين (مفتاحية - نملأها كلها لضمان وجود الأعمدة)
        "submit_on_time", "discussion_time", "idea", "error_handling", "data_collection",
        "functions", "reusability", "gui_or_frontend", "clean_code", "good_idea",
        "validation_auth", "deal_with_data_crud", "design", "accuracy_and_implementation",
        "analysis_and_explanation", "code_organization_and_structure", "deployment_the_model",
        "code_oop", "data_description_and_statistical_analysis", "handling_missing_values",
        "visualization", "exploratory_data_analysis", "relationship_identification",
        "outliers_and_scaling", "data_encoding", "streamlit",
        "Final_Score", "Date"
    ])
    df.to_csv(DATA_FILE, index=False)

st.title("📊 نظام تقييم مشاريع شركة SDK")

# شعار الشركة (يمكنك تعديل الرابط لو عندك صورة خاصة)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/SDK_Logo.svg/1200px-SDK_Logo.svg.png", width=150)
st.header("شركة SDK للتدريب")

# المعايير المشتركة (من جميع المقيمين)
common_criteria = {
    "presentation_skills": ("Presentation Skills", 5),
    "content": ("Content", 5),
    "ability_to_answer": ("Ability to Answer Questions", 5),
    "presenting_idea": ("Presenting Idea Properly", 5)
}

# معايير المدربين لكل كورس
trainer_criteria = {
    "Python": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "idea": ("Idea", 5),
        "error_handling": ("Error Handling", 5),
        "gui_or_frontend": ("GUI", 10),
        "code_oop": ("Code & OOP", 40)
    },
    "Deep Learning": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "accuracy_and_implementation": ("Accuracy & Implementation", 30),
        "analysis_and_explanation": ("Analysis & Explanation", 15),
        "code_organization_and_structure": ("Code Organization & Structure", 5),
        "deployment_the_model": ("Deployment the Model", 10)
    },
    "Machine Learning": {  # نفس معايير Deep Learning للمدربة رند
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "accuracy_and_implementation": ("Accuracy & Implementation", 30),
        "analysis_and_explanation": ("Analysis & Explanation", 15),
        "code_organization_and_structure": ("Code Organization & Structure", 5),
        "deployment_the_model": ("Deployment the Model", 10)
    },
    "Data Engineer": {
        "submit_on_time": ("Submit on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "data_description_and_statistical_analysis": ("Data Description and Statistical Analysis", 15),
        "handling_missing_values": ("Handling Missing Values", 5),
        "visualization": ("Visualization", 5),
        "exploratory_data_analysis": ("Exploratory Data Analysis (EDA)", 5),
        "relationship_identification": ("Relationship Identification", 5),
        "outliers_and_scaling": ("Outliers and Scaling", 5),
        "data_encoding": ("Data Encoding (if required)", 10),
        "streamlit": ("Streamlit", 10)
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
        "gui_or_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling": ("Error Handling", 10)
    },
    "Flutter.2": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "idea": ("Idea", 10),
        "deal_with_data_crud": ("Deal with Data (CRUD)", 25),
        "design": ("Design", 10),
        "validation_auth": ("Validation (Auth)", 15)
    },
    "Front End": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_or_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling": ("Error Handling", 10)
    },
    "React js": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_or_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling": ("Error Handling", 10)
    },
    "Mern": {
        "submit_on_time": ("Submit the Project on Time", 10),
        "discussion_time": ("Discussion Time", 10),
        "gui_or_frontend": ("GUI or Front End", 20),
        "clean_code": ("Clean Code", 20),
        "good_idea": ("Good Idea", 10),
        "error_handling": ("Error Handling", 10)
    }
}

# كورسات تخص المدربة رند فقط
randa_courses = ["Python", "Data Engineer", "Deep Learning", "Machine Learning"]

# مقيمي الكورس
evaluators = ["رند", "محمد", "جود", "أنسام"]

# الشريط الجانبي للاختيار بين الإدخال والعرض
st.sidebar.title("القائمة")
page = st.sidebar.selectbox("اختر الصفحة", ["إدخال تقييم", "عرض تقييمات"])

if page == "إدخال تقييم":
    st.header("إدخال تقييم جديد")

    course = st.selectbox("اختر الكورس:", list(trainer_criteria.keys()))
    student = st.text_input("📝 اسم الطالب:")
    evaluator = st.selectbox("اختر اسم المقيّم:", evaluators)

    # التقييمات المشتركة (من جميع المقيمين)
    st.subheader("📍 التقييمات المشتركة (من جميع المقيمين)")
    scores = {}
    for key, (label, max_val) in common_criteria.items():
        scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)

    # تقييمات المدربين
    if evaluator == "رند":
        if course in randa_courses:
            st.subheader("📍 تقييمات المدرب رند")
            for key, (label, max_val) in trainer_criteria[course].items():
                scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
        else:
            st.info("رند لا تقوم بتقييم هذا الكورس.")
            for key in trainer_criteria.get(course, {}).keys():
                scores[key] = None

    elif evaluator == "جود":
        if course in ["Dart", "Flutter.2", "Flutter.3"]:
            st.subheader("📍 تقييمات المدرب جود")
            for key, (label, max_val) in trainer_criteria[course].items():
                scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
        else:
            for key in trainer_criteria.get(course, {}).keys():
                scores[key] = None

    elif evaluator == "محمد":
        if course in ["Front End", "React js", "Mern"]:
            st.subheader("📍 تقييمات المدرب محمد")
            for key, (label, max_val) in trainer_criteria[course].items():
                scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
        else:
            for key in trainer_criteria.get(course, {}).keys():
                scores[key] = None

    else:
        # أنسام أو غيرهم بدون تقييم مدرب
        for key in trainer_criteria.get(course, {}).keys():
            scores[key] = None

    if st.button("💾 حفظ التقييم"):
        if student.strip() == "":
            st.warning("⚠️ يرجى إدخال اسم الطالب.")
        else:
            # حفظ البيانات
            new_data = {
                "Course": course,
                "Student": student.strip(),
                "Evaluator": evaluator,
                **scores,
                "Final_Score": None,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ تم حفظ التقييم بنجاح!")

elif page == "عرض تقييمات":
    st.header("عرض التقييمات")

    df = pd.read_csv(DATA_FILE)
    if df.empty:
        st.info("لا توجد تقييمات حتى الآن.")
    else:
        course_selected = st.selectbox("اختر الكورس لعرض تقييماته:", sorted(df["Course"].unique()))
        df_course = df[df["Course"] == course_selected]

        # الأعمدة المشتركة للعرض
        common_cols = list(common_criteria.keys())

        # الأعمدة الخاصة بالكورس فقط
        course_cols = list(trainer_criteria.get(course_selected, {}).keys())

        # الأعمدة الأساسية للعرض
        cols_to_show = ["Student", "Evaluator"] + common_cols + course_cols

        # تصفية الأعمدة الموجودة فقط
        cols_to_show = [col for col in cols_to_show if col in df_course.columns]

        st.dataframe(df_course[cols_to_show].reset_index(drop=True))

        # حساب النتيجة النهائية لكل طالب في الكورس المحدد
        st.subheader("📊 النتائج النهائية للطلاب في هذا الكورس")
        final_results = []
        for student_name in df_course["Student"].unique():
            student_data = df_course[df_course["Student"] == student_name]

            # متوسط تقييم المقيمين (من المعايير المشتركة، مجموع 20)
            peer_avg = student_data[list(common_criteria.keys())].mean().mean()

            # تقييم المدرب (حسب المقيّم رند، جود أو محمد والمعايير الخاصة)
            trainer_score = 0

            for evaluator_name in evaluators:
                trainer_data = student_data[student_data["Evaluator"] == evaluator_name]
                if trainer_data.empty:
                    continue

                # حساب مجموع نقاط المدرب بحسب المعايير
                criteria_keys = list(trainer_criteria.get(course_selected, {}).keys())
                criteria_sum = 0
                max_sum = 0
                for key in criteria_keys:
                    if pd.notna(trainer_data.iloc[0].get(key)):
                        criteria_sum += trainer_data.iloc[0][key]
                        max_sum += trainer_criteria[course_selected][key][1]

                if max_sum > 0:
                    trainer_score += (criteria_sum / max_sum) * 20  # نوزعها على 20 نقطة

            # المجموع النهائي (peer 20 + trainer 20) = 40 كحد أقصى
            final_score = peer_avg + trainer_score

            final_results.append((student_name, round(final_score, 2)))

        # عرض النتائج النهائية
        final_df = pd.DataFrame(final_results, columns=["Student", "Final Score"])
        st.table(final_df.sort_values(by="Final Score", ascending=False).reset_index(drop=True))
