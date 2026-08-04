import streamlit as st
import pandas as pd
import subprocess
import os
import glob


# Configuration

PROJECT_ROOT = r"C:\Users\AdMin\BigDataTest"

JOB_DIR = os.path.join(PROJECT_ROOT, "job")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


# Job Display Name

JOB_NAMES = {
    "count_students_by_course": "Thống kê số lượng sinh viên theo môn học",
    "avg_score_per_course": "Tính điểm trung bình theo môn học",
    "grade_distribution": "Thống kê phân bố điểm chữ",
    "pass_fail_per_course": "Thống kê số lượng Đạt / Trượt theo môn học",
    "top_n_fail_rate": "Top N môn học có tỷ lệ trượt cao nhất",
    "students_by_course_and_score_range": "Tìm sinh viên theo môn học và khoảng điểm",
}


# Streamlit Config

st.set_page_config(page_title="Hệ thống quản lý sinh viên", page_icon="📊", layout="wide")

st.title("📊 Hệ thống quản lý sinh viên")


# Load Available Jobs

def get_jobs():

    if not os.path.exists(JOB_DIR):
        return []

    jobs = []

    for item in os.listdir(JOB_DIR):

        path = os.path.join(JOB_DIR, item)

        if os.path.isdir(path):
            jobs.append(item)

    jobs.sort()

    return jobs


# Run Hadoop Job

def run_job(job_name, arguments=None):

    if arguments is None:
        arguments = []

    if job_name == "students_by_course_and_score_range":

        command = ["run_job2.cmd", job_name] + arguments

        result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, shell=True)

    elif job_name == "top_n_fail_rate":

        command = ["run_job_top_n_fail_rate.cmd"] + arguments

        result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, shell=True)

    else:

        command = ["run_job.py", job_name]

        result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, shell=True)

    return result

# Sidebar

st.sidebar.header("🔍 Công cụ tìm kiếm")


available_jobs = get_jobs()

job_display_list = []

for job in available_jobs:
    job_display_list.append(JOB_NAMES.get(job, job))


if job_display_list:

    selected_display = st.sidebar.selectbox("Chức năng", job_display_list)

    selected_job = None

    for key, value in JOB_NAMES.items():

        if value == selected_display:
            selected_job = key
            break

else:

    selected_job = None

    st.sidebar.warning("Không tìm thấy chức năng.")


# Search Parameters

course_id = ""

start_score = 0.0

end_score = 10.0

top_n = 10


if selected_job == "students_by_course_and_score_range":

    st.sidebar.divider()

    st.sidebar.subheader("Điều kiện tìm kiếm")

    COURSE_IDS = [
        "251AI1", "251AI2", "251AI3",
        "251CN1", "251CN2", "251CN3",
        "251DB1", "251DB2", "251DB3",
        "251DM1", "251DM2", "251DM3",
        "251DS1", "251DS2", "251DS3",
        "251ML1", "251ML2", "251ML3",
        "251OOP1", "251OOP2", "251OOP3",
        "251OS1", "251OS2", "251OS3",
        "251SE1", "251SE2", "251SE3",
        "251WP1", "251WP2", "251WP3"
    ]

    course_dropdown = st.sidebar.selectbox("Chọn mã môn học", [""] + COURSE_IDS)

    course_id = course_dropdown

    start_score = st.sidebar.number_input("Điểm bắt đầu", min_value=0.0, max_value=10.0, value=0.0, step=1.0)

    end_score = st.sidebar.number_input("Điểm kết thúc", min_value=0.0, max_value=10.0, value=10.0, step=1.0)


elif selected_job == "top_n_fail_rate":

    st.sidebar.divider()

    st.sidebar.subheader("Điều kiện tìm kiếm")

    top_n = st.sidebar.number_input("Chọn Top N môn học có tỷ lệ trượt cao nhất", min_value=1, max_value=30, value=5, step=1)

# Run Button

run_button = st.sidebar.button("▶ Tìm kiếm")


# Run Job

if run_button:

    if selected_job == "students_by_course_and_score_range" and course_id == "":

        st.sidebar.error("Vui lòng chọn hoặc nhập mã môn học.")

    else:

        with st.spinner("⏳ Đang thực hiện Hadoop Streaming, vui lòng đợi..."):

            if selected_job == "students_by_course_and_score_range":

                result = run_job(selected_job, [course_id, str(start_score), str(end_score)])

            elif selected_job == "top_n_fail_rate":

                result = run_job(selected_job, [str(top_n)])

            else:

                result = run_job(selected_job)

        if result.returncode == 0:

            st.success("✅ Thực hiện thành công.")

        else:

            st.error("❌ Thực hiện thất bại.")

            st.code(result.stdout)

            if result.stderr:

                st.code(result.stderr)
# Read Hadoop Output

def load_result(job_name):

    result_folder = os.path.join(OUTPUT_DIR, job_name)

    files = glob.glob(os.path.join(result_folder, "part-*"))

    if not files:
        return None

    data = []

    for file in files:

        if job_name == "count_students_by_course":

            temp = pd.read_csv(file, sep="\t", header=None, names=["CourseID", "StudentCount"])

        elif job_name == "avg_score_per_course":

            temp = pd.read_csv(file, sep="\t", header=None, names=["CourseID", "AverageScore"])

        elif job_name == "grade_distribution":

            temp = pd.read_csv(file, sep="\t", header=None, names=["LetterGrade", "StudentCount"])

        elif job_name == "pass_fail_per_course":

            temp = pd.read_csv(file, sep="\t", header=None, names=["CourseID", "Pass", "Fail"])

        elif job_name == "top_n_fail_rate":

            temp = pd.read_csv(file, sep="\t", header=None, names=["CourseID", "FailRate"])

        elif job_name == "students_by_course_and_score_range":

            temp = pd.read_csv(file, sep="\t", header=None, names=["StudentID", "LastName", "FirstName"])

        else:

            temp = pd.read_csv(file, sep="\t", header=None, names=["Key", "Value"])

        data.append(temp)

    df = pd.concat(data, ignore_index=True)

    return df


# Main Content

if selected_job:

    st.header(f"📋 {JOB_NAMES.get(selected_job, selected_job)}")

    st.info("Kết quả sẽ được đọc từ thư mục Output sau khi Hadoop Streaming hoàn thành.")

    df = load_result(selected_job)

    if df is None:

        st.warning("⚠ Chưa tìm thấy dữ liệu. Hãy thực hiện chức năng trước.")

    else:

        # Count Students By Course

        if selected_job == "count_students_by_course":

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Tổng số môn học", len(df))

            with col2:
                st.metric("Tổng số lượt đăng ký", int(df["StudentCount"].sum()))

            st.subheader("📋 Danh sách số lượng sinh viên theo môn học")

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Biểu đồ")

            chart_df = df.set_index("CourseID")

            st.bar_chart(chart_df)


        # Average Score Per Course

        elif selected_job == "avg_score_per_course":

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Tổng số môn học", len(df))

            with col2:
                st.metric("Điểm trung bình chung", round(df["AverageScore"].mean(), 2))

            st.subheader("📋 Điểm trung bình theo môn học")

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Biểu đồ")

            chart_df = df.set_index("CourseID")

            st.bar_chart(chart_df)


        # Grade Distribution

        elif selected_job == "grade_distribution":

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Số mức điểm", len(df))

            with col2:
                st.metric("Tổng số sinh viên", int(df["StudentCount"].sum()))

            st.subheader("📋 Phân bố điểm chữ")

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Biểu đồ")

            chart_df = df.set_index("LetterGrade")

            st.bar_chart(chart_df)


        # Pass Fail Per Course

        elif selected_job == "pass_fail_per_course":

            st.metric("Tổng số môn học", len(df))

            st.subheader("📋 Thống kê Đạt / Trượt theo môn học")

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Biểu đồ")

            chart_df = df.set_index("CourseID")

            st.bar_chart(chart_df)


        # Top N Fail Rate

        elif selected_job == "top_n_fail_rate":

            st.metric("Số môn học", len(df))

            st.subheader("📋 Top môn học có tỷ lệ trượt cao nhất")

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Biểu đồ")

            chart_df = df.set_index("CourseID")

            st.bar_chart(chart_df)


        # Students By Course And Score Range

        elif selected_job == "students_by_course_and_score_range":

            st.metric("Số sinh viên tìm được", len(df))

            st.subheader("📋 Danh sách sinh viên")

            st.dataframe(df, use_container_width=True)


        # Default

        else:

            if "Value" in df.columns:

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Tổng số bản ghi", len(df))

                try:

                    total_value = int(pd.to_numeric(df["Value"], errors="coerce").sum())

                    with col2:
                        st.metric("Tổng giá trị", total_value)

                except:
                    pass

            st.subheader("📋 Kết quả")

            st.dataframe(df, use_container_width=True)

            if "Key" in df.columns and "Value" in df.columns:

                try:

                    st.subheader("📈 Biểu đồ")

                    chart_df = df.set_index("Key")

                    st.bar_chart(chart_df)

                except:
                    pass

else:

    st.info("👈 Vui lòng chọn một chức năng ở thanh bên trái.")