import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="دمج بيانات من ملفات Excel", layout="centered")

st.title("📑 دمج بيانات من عدة ملفات Excel")

st.write("قم برفع جميع الملفات (كل ملف يحتوي صف كامل من البيانات) وسيتم دمجها في ملف Excel واحد.")

# رفع الملفات
uploaded_files = st.file_uploader("اختر ملفات Excel", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    all_data = []

    for file in uploaded_files:
        try:
            # نقرأ الملف كامل (الملف فيه صفوف وأعمدة)
            df = pd.read_excel(file)

            # نتأكد من وجود بيانات
            if not df.empty:
                all_data.append(df)
            else:
                st.warning(f"⚠️ الملف {file.name} فارغ.")

        except Exception as e:
            st.error(f"⚠️ خطأ في قراءة الملف {file.name}: {e}")

    if all_data:
        # ندمج كل الداتا فريمات
        result_df = pd.concat(all_data, ignore_index=True)

        st.subheader("📋 البيانات المدمجة")
        st.dataframe(result_df)

        # تجهيز الملف للتحميل
        output = BytesIO()
        result_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="📥 تحميل ملف البيانات المدمجة",
            data=output,
            file_name="merged_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
