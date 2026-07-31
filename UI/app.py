import streamlit as st
import pandas as pd
import subprocess
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

st.title("📊 Student Management Big Data System")


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

    jobs.sort()

    return jobs


# ============================================================
# Run Hadoop Job
# ============================================================

def run_job(job_name, arguments=None):

    if arguments is None:
        arguments = []

    # Job dùng nhiều input
    if job_name == "students_by_course_and_score_range":

        command = [
            "run_job2.cmd",
            job_name
        ] + arguments

    # Các job thông thường
    else:

        command = [
            "run_job.cmd",
            job_name
        ]

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        shell=True
    )

    return result


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

        # ====================================================
        # count_course
        # ====================================================

        if job_name == "count_course":

            temp = pd.read_csv(
                file,
                sep="\t",
                header=None,
                names=[
                    "CourseID",
                    "StudentCount"
                ]
            )

        # students_by_course_and_score_range
        # ====================================================

        elif job_name == "students_by_course_and_score_range":

            temp = pd.read_csv(
                file,
                sep="\t",
                header=None,
                names=[
                    "StudentID",
                    "LastName",
                    "FirstName"
                ]
            )

        # Default
        # ====================================================

        else:

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

st.sidebar.header("⚙ Công cụ tìm kiếm")


jobs = get_jobs()


if jobs:

    selected_job = st.sidebar.selectbox(
        "Các chức năng tìm kiếm",
        jobs
    )

else:
    selected_job = None

    st.sidebar.warning(
        "Không tìm thấy chức năng tìm kiếm. Vui lòng thử lại sau"
    )


# Parameters

course_id = ""

start_score = 0.0

end_score = 100.0


if selected_job == "Tìm học sinh dựa vào khóa học và khoảng điểm (0-10)":

    st.sidebar.markdown("---")

    st.sidebar.subheader("Search Condition")

    course_id = st.sidebar.text_input(
        "Course ID"
    )

    start_score = st.sidebar.number_input("Điểm bắt đầu", min_value=0.0, max_value=10.0, value=0.0,step=1.0 )
    end_score = st.sidebar.number_input("Điểm kết thúc", min_value=0.0, max_value=10.0, value=10.0,step=1.0 )


# Run Button

run_button = st.sidebar.button(
    "▶ Tìm kiếm"
)


if run_button:

    with st.spinner("Đang tìm kiếm ^^ Vui lòng đợi trong chút lát..."):

        if selected_job == "students_by_course_and_score_range":

            result = run_job(
                selected_job,
                [
                    course_id,
                    str(start_score),
                    str(end_score)
                ]
            )

        else:

            result = run_job( selected_job )

    if result.returncode == 0:
        st.success("Tìm kiếm thành công.")

    else:
        st.error("Chạy thất bại.")



# Main Content

if selected_job:

    st.header(
        f"Job: {selected_job}"
    )

    st.info(
        "Chọn điều kiện (nếu có) rồi nhấn Run Job để thực hiện Hadoop Streaming."
    )

    # Chỉ hiển thị kết quả nếu đã có output
    df = load_result(selected_job)

    if df is None:

        st.warning(
            "Không tìm thấy kết quả. Hãy chạy Job trước."
        )

    else:

        # ====================================================
        # count_course
        # ====================================================

        if selected_job == "count_course":

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Total Courses",
                    len(df)
                )

            with col2:

                st.metric(
                    "Total Enrollments",
                    int(df["StudentCount"].sum())
                )

            st.subheader("Course Enrollment")

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader("Enrollment Chart")

            chart_df = df.set_index(
                "CourseID"
            )

            st.bar_chart(
                chart_df
            )

        # ====================================================
        # students_by_course_and_score_range
        # ====================================================

        elif selected_job == "students_by_course_and_score_range":

            st.metric(
                "Matched Students",
                len(df)
            )

            st.subheader("Matched Student List")

            st.dataframe(
                df,
                use_container_width=True
            )

        # ====================================================
        # Default
        # ====================================================

        else:

            if "Value" in df.columns:

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Total Records",
                        len(df)
                    )

                try:

                    total_value = int(
                        pd.to_numeric(
                            df["Value"],
                            errors="coerce"
                        ).sum()
                    )

                    with col2:

                        st.metric(
                            "Total Value",
                            total_value
                        )

                except:

                    pass

            st.subheader("Result")

            st.dataframe(
                df,
                use_container_width=True
            )

            if "Key" in df.columns and "Value" in df.columns:

                try:

                    st.subheader("Chart")

                    chart_df = df.set_index(
                        "Key"
                    )

                    st.bar_chart(
                        chart_df
                    )

                except:

                    pass

else:

    st.warning(
        "Please select a Hadoop Job."
    )