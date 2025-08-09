# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 11:13:43 2025

@author: SDK
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "evaluations.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Course", "Student", "Evaluator",
        "presentation_skills", "content", "ability_to_answer", "presenting_idea",
        # معايير Python
        "submit_on_time", "discussion_time", "idea", "error_handling", "GUI", "Code_OOP",
        # معايير Deep Learning
        "dl_submit_on_time", "dl_discussion_time", "dl_accuracy", "dl_analysis", "dl_code_org", "dl_deployment",
        "Final_Score", "Date"
    ])
    df.to_csv(DATA_FILE, index=False)

st.title("📊 نظام تقييم المشاريع")

# اختيار الكورس
course = st.selectbox("اختر الكورس:", ["Python", "Deep Learning"])

# إدخال اسم الطالب يدويًا
student = st.text_input("📝 اسم الطالب:")

# اختيار اسم المقيّم
evaluators = ["رند", "محمد", "جود", "أنسام"]
evaluator = st.selectbox("اختر اسم المقيّم:", evaluators)

# التقييمات المشتركة (20 نقطة)
st.subheader("📍 التقييمات المشتركة (من جميع المقيمين)")
presentation_skills = st.number_input("Presentation Skills (0-5)", 0.0, 5.0, step=0.5)
content = st.number_input("Content (0-5)", 0.0, 5.0, step=0.5)
ability_to_answer = st.number_input("Ability to Answer Questions (0-5)", 0.0, 5.0, step=0.5)
presenting_idea = st.number_input("Presenting Idea Properly (0-5)", 0.0, 5.0, step=0.5)

# معايير المدرب حسب الكورس
# Python
submit_on_time = discussion_time = idea_score = error_handling = gui_score = code_oop = None
# Deep Learning
dl_submit_on_time = dl_discussion_time = dl_accuracy = dl_analysis = dl_code_org = dl_deployment = None

if evaluator == "رند":
    st.subheader("📍 تقييم المدرب")
    if course == "Python":
        submit_on_time = st.number_input("Submit on Time (0-10)", 0.0, 10.0, step=0.5)
        discussion_time = st.number_input("Discussion Time (0-10)", 0.0, 10.0, step=0.5)
        idea_score = st.number_input("Idea (0-5)", 0.0, 5.0, step=0.5)
        error_handling = st.number_input("Error Handling (0-5)", 0.0, 5.0, step=0.5)
        gui_score = st.number_input("GUI (0-10)", 0.0, 10.0, step=0.5)
        code_oop = st.number_input("Code & OOP (0-40)", 0.0, 40.0, step=1.0)

    elif course == "Deep Learning":
        dl_submit_on_time = st.number_input("Submit on Time (0-10)", 0.0, 10.0, step=0.5)
        dl_discussion_time = st.number_input("Discussion Time (0-10)", 0.0, 10.0, step=0.5)
        dl_accuracy = st.number_input("Accuracy & Implementation (0-30)", 0.0, 30.0, step=0.5)
        dl_analysis = st.number_input("Analysis & Explanation (0-15)", 0.0, 15.0, step=0.5)
        dl_code_org = st.number_input("Code Organization & Structure (0-5)", 0.0, 5.0, step=0.5)
        dl_deployment = st.number_input("Deployment the Model (0-10)", 0.0, 10.0, step=0.5)

# حفظ التقييم
if st.button("💾 حفظ التقييم"):
    if student.strip() == "":
        st.warning("⚠️ يرجى إدخال اسم الطالب.")
    else:
        new_data = {
            "Course": course,
            "Student": student.strip(),
            "Evaluator": evaluator,
            "presentation_skills": presentation_skills,
            "content": content,
            "ability_to_answer": ability_to_answer,
            "presenting_idea": presenting_idea,
            "submit_on_time": submit_on_time,
            "discussion_time": discussion_time,
            "idea": idea_score,
            "error_handling": error_handling,
            "GUI": gui_score,
            "Code_OOP": code_oop,
            "dl_submit_on_time": dl_submit_on_time,
            "dl_discussion_time": dl_discussion_time,
            "dl_accuracy": dl_accuracy,
            "dl_analysis": dl_analysis,
            "dl_code_org": dl_code_org,
            "dl_deployment": dl_deployment,
            "Final_Score": None,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ تم حفظ التقييم بنجاح!")

# عرض التقييمات
st.subheader("📋 جميع التقييمات")
df = pd.read_csv(DATA_FILE)
st.dataframe(df)

# حساب النتيجة النهائية لكل طالب
st.subheader("📊 النتيجة النهائية لكل طالب")
final_results = []
for student_name in df["Student"].unique():
    student_data = df[df["Student"] == student_name]
    course_type = student_data.iloc[0]["Course"]

    # متوسط تقييم المقيمين (من 20)
    peer_avg = student_data[["presentation_skills", "content", "ability_to_answer", "presenting_idea"]].mean().mean()

    # تقييم المدرب (من 80)
    trainer_data = student_data[(student_data["Evaluator"] == "رند") & (student_data["Course"] == course_type)]
    trainer_score = 0
    if not trainer_data.empty:
        trainer_row = trainer_data.iloc[0]
        if course_type == "Python":
            trainer_score = sum([
                trainer_row["submit_on_time"] or 0,
                trainer_row["discussion_time"] or 0,
                trainer_row["idea"] or 0,
                trainer_row["error_handling"] or 0,
                trainer_row["GUI"] or 0,
                trainer_row["Code_OOP"] or 0
            ])
        elif course_type == "Deep Learning":
            trainer_score = sum([
                trainer_row["dl_submit_on_time"] or 0,
                trainer_row["dl_discussion_time"] or 0,
                trainer_row["dl_accuracy"] or 0,
                trainer_row["dl_analysis"] or 0,
                trainer_row["dl_code_org"] or 0,
                trainer_row["dl_deployment"] or 0
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
