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
        "presentation_skills", "content", "ability_to_answer", "presenting_idea",
        "Final_Score", "Date"
    ])
    df.to_csv(DATA_FILE, index=False)

st.title("📊 نظام تقييم المشاريع")

# 📍 تعريف المعايير المشتركة
common_criteria = {
    "presentation_skills": ("Presentation Skills", 5),
    "content": ("Content", 5),
    "ability_to_answer": ("Ability to Answer Questions", 5),
    "presenting_idea": ("Presenting Idea Properly", 5)
}

# 📍 تعريف معايير المدرب لكل كورس
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
        "dl_submit_on_time": ("Submit on Time", 10),
        "dl_discussion_time": ("Discussion Time", 10),
        "dl_accuracy": ("Accuracy & Implementation", 30),
        "dl_analysis": ("Analysis & Explanation", 15),
        "dl_code_org": ("Code Organization & Structure", 5),
        "dl_deployment": ("Deployment the Model", 10)
    },
    "Dart": {
        "dl_submit_on_time": ("Submit on Time", 10),
        "dl_discussion_time": ("Discussion Time", 10),
        "dl_accuracy": ("OOP", 30),
        "dl_analysis": ("Function rec", 15),
        "dl_code_org": ("Code Organization & Structure", 5),

    }
}

# 🖊 إدخال بيانات أساسية
course = st.selectbox("اختر الكورس:", list(trainer_criteria.keys()))
student = st.text_input("📝 اسم الطالب:")
evaluators = ["رند", "محمد", "جود", "أنسام"]
evaluator = st.selectbox("اختر اسم المقيّم:", evaluators)

# 🔹 إدخال المعايير المشتركة
st.subheader("📍 التقييمات المشتركة (من جميع المقيمين)")
scores = {}
for key, (label, max_val) in common_criteria.items():
    scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)

# 🔹 إدخال معايير المدرب إذا كان المقيّم رند
if evaluator == "رند":
    st.subheader("📍 تقييم المدرب")
    for key, (label, max_val) in trainer_criteria[course].items():
        scores[key] = st.number_input(f"{label} (0-{max_val})", 0.0, float(max_val), step=0.5)
else:
    # لو مش المدرب، نضع القيم None حتى تبقى الأعمدة موجودة
    for key in trainer_criteria[course].keys():
        scores[key] = None

# 💾 حفظ التقييم
if st.button("💾 حفظ التقييم"):
    if student.strip() == "":
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

# 📋 عرض التقييمات
st.subheader("📋 جميع التقييمات")
df = pd.read_csv(DATA_FILE)
st.dataframe(df)

# 📊 حساب النتيجة النهائية
st.subheader("📊 النتيجة النهائية لكل طالب")
final_results = []
for student_name in df["Student"].unique():
    student_data = df[df["Student"] == student_name]
    course_type = student_data.iloc[0]["Course"]

    # متوسط تقييم المقيمين (من 20)
    peer_avg = student_data[list(common_criteria.keys())].mean().mean()

    # تقييم المدرب (من 80)
    trainer_data = student_data[(student_data["Evaluator"] == "رند") & (student_data["Course"] == course_type)]
    trainer_score = 0
    if not trainer_data.empty:
        trainer_row = trainer_data.iloc[0]
        trainer_score = sum([
            trainer_row[k] or 0
            for k in trainer_criteria[course_type].keys()
        ])

    final_score = round(peer_avg + trainer_score, 2)
    final_results.append({
        "Student": student_name,
        "Course": course_type,
        "Peer Avg (20)": round(peer_avg, 2),
        "Trainer Score (80)": trainer_score,
        "Final Score (100)": final_score
    })

final_df = pd.DataFrame(final_results)
st.dataframe(final_df)
