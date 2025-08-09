# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# مسار ملف حفظ التقييمات
DATA_FILE = "evaluations.csv"

# ---- بيانات الشركة ----
COMPANY_NAME = "SDK Training Company"
COMPANY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/SDK_Logo.svg/1200px-SDK_Logo.svg.png"  # رابط شعار افتراضي - يمكن تغييره

# ---- المعايير المشتركة ----
common_criteria = {
    "presentation_skills": ("Presentation Skills", 5),
    "content": ("Content", 5),
    "ability_to_answer": ("Ability to Answer Questions", 5),
    "presenting_idea": ("Presenting Idea Properly", 5)
}

# ---- معايير المدربين حسب الكورسات ----
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

# ---- انشاء ملف CSV اذا لم يكن موجود ----
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Course", "Student", "Evaluator",
        *common_criteria.keys(),
        *sum([list(c.keys()) for c in trainer_criteria.values()], []),
        "Final_Score", "Date"
    ])
    df.to_csv(DATA_FILE, index=False)

# --- صفحة التطبيق ---

# عرض شعار واسم الشركة
st.image(COMPANY_LOGO, width=150)
st.title(f"نظام تقييم المشاريع - {COMPANY_NAME}")

# قائمة أسماء المقيمين
evaluators = ["رند", "محمد", "جود", "أنسام"]

# القائمة الجانبية لتبديل الصفحات
page = st.sidebar.selectbox("القائمة", ["تقييم مشروع", "عرض التقييمات"])

if page == "تقييم مشروع":
    st.header("📝 تسجيل تقييم جديد")

    # بيانات الإدخال
    course = st.selectbox("اختر الكورس:", list(trainer_criteria.keys()))
    student = st.text_input("اسم الطالب:")
    evaluator = st.selectbox("اختر اسم المقيّم:", evaluators)

    # إدخال تقييمات المعايير المشتركة
    st.subheader("التقييمات المشتركة (من جميع المقيمين)")
    scores = {}
    for key, (label, max_val) in common_criteria.items():
        scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)

    # إدخال تقييمات المدرب حسب الكورس واسم المقيّم
    if evaluator == "رند":
        st.subheader("تقييمات المدرب رند")
        for key, (label, max_val) in trainer_criteria.get(course, {}).items():
            scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
    elif evaluator == "جود":
        # جود لها معايير خاصة بالكورسات Dart, Flutter.2, Flutter.3
        if course in ["Dart", "Flutter.2", "Flutter.3"]:
            st.subheader("تقييمات المدرب جود")
            for key, (label, max_val) in trainer_criteria[course].items():
                scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
        else:
            # لو جود لم تقم بالتقييم (معايير غير موجودة للكورس)
            for key in trainer_criteria.get(course, {}).keys():
                scores[key] = None
    elif evaluator == "محمد":
        # محمد معايير Front End, React js, Mern
        if course in ["Front End", "React js", "Mern"]:
            st.subheader("تقييمات المدرب محمد")
            for key, (label, max_val) in trainer_criteria[course].items():
                scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
        else:
            for key in trainer_criteria.get(course, {}).keys():
                scores[key] = None
    else:
        # أنسام أو غيرهم لا تقييم مدرب
        for key in trainer_criteria.get(course, {}).keys():
            scores[key] = None

    # حفظ التقييم
    if st.button("💾 حفظ التقييم"):
        if not student.strip():
            st.warning("⚠️ يرجى إدخال اسم الطالب.")
        else:
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

elif page == "عرض التقييمات":
    st.header("📋 عرض تقييمات الطلاب حسب الكورس")

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame()

    selected_course = st.selectbox("اختر الكورس لعرض تقييماته:", list(trainer_criteria.keys()))

    if df.empty:
        st.info("لا توجد بيانات تقييمات لعرضها.")
    else:
        df_course = df[df["Course"] == selected_course]

        if df_course.empty:
            st.warning(f"لا توجد تقييمات مسجلة للكورس: {selected_course}")
        else:
            # أعمدة المعايير المشتركة
            common_cols = list(common_criteria.keys())
            # أعمدة معايير الكورس المختار فقط
            course_cols =
