import streamlit as st
import pandas as pd
import os
from io import BytesIO
import zipfile

st.set_page_config(page_title="دمج أسماء من ملفات Excel", layout="centered")

st.title("📑 دمج أسماء من عدة ملفات Excel")

st.write("قم برفع جميع الملفات (كل ملف يحتوي اسم واحد) وسيتم دمجها في ملف Excel واحد.")

# رفع الملفات
uploaded_files = st.file_uploader("اختر ملفات Excel", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    all_names = []

    for file in uploaded_files:
        try:
            df = pd.read_excel(file)
            # نفترض أن الاسم موجود في العمود الأول
            first_col = df.columns[0]
            all_names.append(df[first_col].iloc[0])
        except Exception as e:
            st.error(f"خطأ في قراءة الملف {file.name}: {e}")

    if all_names:
        result_df = pd.DataFrame({"الأسماء": all_names})

        st.subheader("📋 الأسماء المدمجة")
        st.dataframe(result_df)

        # تجهيز الملف للتحميل
        output = BytesIO()
        result_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="📥 تحميل ملف الأسماء المدمجة",
            data=output,
            file_name="merged_names.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )