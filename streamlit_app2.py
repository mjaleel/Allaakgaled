import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="دمج أسماء من ملفات Excel", layout="centered")

st.title("📑 دمج أسماء من عدة ملفات Excel")

st.write("قم برفع جميع الملفات (كل ملف يحتوي أسماء في عمود واحد) وسيتم دمجها في ملف Excel واحد.")

# رفع الملفات
uploaded_files = st.file_uploader("اختر ملفات Excel", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    all_names = []

    for file in uploaded_files:
        try:
            # نجرب نقرأ الملف مع رؤوس أعمدة
            df = pd.read_excel(file)

            if "الاسم" in df.columns:  
                # إذا عنده عمود اسمه 'الاسم'
                names = df["الاسم"].dropna().astype(str).tolist()
            else:
                # إذا ماكو عمود 'الاسم' نجرب نقرأ العمود الأول
                # بعض الملفات قد تكون بدون header
                try:
                    df_noheader = pd.read_excel(file, header=None)
                    names = df_noheader.iloc[:, 0].dropna().astype(str).tolist()
                except:
                    names = df[df.columns[0]].dropna().astype(str).tolist()

            all_names.extend(names)

        except Exception as e:
            st.error(f"⚠️ خطأ في قراءة الملف {file.name}: {e}")

    if all_names:
        result_df = pd.DataFrame({"الاسم": all_names})

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
