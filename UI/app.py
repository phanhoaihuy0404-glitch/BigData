import streamlit as st
import pandas as pd
import os
import glob


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = r"C:\Users\AdMin\BigDataTest"

JOB_DIR = os.path.join(
    PROJECT_ROOT,
    "job"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "output"
)


# ============================================================
# Streamlit Config
# ============================================================

st.set_page_config(
    page_title="Student Management Big Data",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# Title
# ============================================================

st.title("📊 Chương trình quản lý sinh viên ")



# ============================================================
# Load Available Jobs
# ============================================================

def get_jobs():

    if not os.path.exists(JOB_DIR):
        return []

    jobs = []

    for item in os.listdir(JOB_DIR):

        path = os.path.join(
            JOB_DIR,
            item
        )

        if os.path.isdir(path):
            jobs.append(item)

    return jobs



# ============================================================
# Read Hadoop Output
# ============================================================

def load_result(job_name):

    result_folder = os.path.join(
        OUTPUT_DIR,
        job_name
    )


    files = glob.glob(
        os.path.join(
            result_folder,
            "part-*"
        )
    )


    if not files:
        return None


    data = []


    for file in files:

        temp = pd.read_csv(
            file,
            sep="\t",
            header=None,
            names=[
                "Key",
                "Value"
            ]
        )

        data.append(temp)



    df = pd.concat(
        data,
        ignore_index=True
    )


    return df



# ============================================================
# Sidebar
# ============================================================

st.sidebar.header(
    "⚙ Job Control"
)


jobs = get_jobs()


if jobs:

    selected_job = st.sidebar.selectbox(
        "Select Hadoop Job",
        jobs
    )

else:

    selected_job = None

    st.sidebar.warning(
        "No job found"
    )



run_button = st.sidebar.button(
    "▶ Run Job"
)



# ============================================================
# Main Content
# ============================================================


if selected_job:


    st.header(
        f"Job Result: {selected_job}"
    )


    st.info(
        "Chương trình đang tìm kiếm, kết quả sẽ được hiển thị bên dưới nếu tìm thấy dữ liệu."
    )



    df = load_result(
        selected_job
    )


    if df is not None:


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Total Records",
                len(df)
            )


        with col2:

            st.metric(
                "Total Value",
                int(df["Value"].sum())
            )



        st.subheader(
            "📋 Data Table"
        )


        st.dataframe(
            df,
            use_container_width=True
        )



        st.subheader(
            "📈 Chart"
        )


        chart_df = df.set_index(
            "Key"
        )


        st.bar_chart(
            chart_df
        )


    else:


        st.warning(
            "Không tìm thấy dữ liệu kết quả. Vui lòng chạy lại job để tạo dữ liệu."
        )



else:


    st.warning(
        "Vui lòng chọn một job"
    )