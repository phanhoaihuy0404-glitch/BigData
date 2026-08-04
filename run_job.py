import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Configuration 
HADOOP_HOME = Path(r"D:\hadoop\hadoop-3.3.6")
JAVA_HOME = Path(r"D:\Java11")
PYTHON = r"C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe"
PROJECT_ROOT = Path(r"C:\Users\AdMin\BigDataTest")

STREAMING_JAR = HADOOP_HOME / "share" / "hadoop" / "tools" / "lib" / "hadoop-streaming-3.3.6.jar"

DEFAULT_NUM_REDUCERS = 2


def build_env():
    import os
    env = os.environ.copy()
    env["PATH"] = f"{HADOOP_HOME / 'bin'};{JAVA_HOME / 'bin'};{env.get('PATH', '')}"
    return env


def run(cmd, cwd=None, env=None, check=True, capture=False):
    cmdline = subprocess.list2cmdline([str(c) for c in cmd])
    print(f"\n$ {cmdline}")
    result = subprocess.run(
        cmdline, cwd=cwd, env=env, shell=True,
        capture_output=capture, text=True,
    )
    if capture:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
    if check and result.returncode != 0:
        print(f"\n[FAIL] Lenh that bai (exit code {result.returncode})")
        sys.exit(1)
    return result


def main():
    parser = argparse.ArgumentParser(description="Chay Hadoop Streaming job tren Enrollment.csv")
    parser.add_argument("job_name", help="Ten job trong thu muc job/<job_name>")
    parser.add_argument("--reducers", type=int, default=DEFAULT_NUM_REDUCERS,
                         help=f"So luong reducer (mac dinh {DEFAULT_NUM_REDUCERS})")
    args = parser.parse_args()

    job_name = args.job_name
    num_reducers = args.reducers

    job_dir = PROJECT_ROOT / "job" / job_name
    local_input = PROJECT_ROOT / "data" / "output" / "Enrollment.csv"
    local_output = PROJECT_ROOT / "output" / job_name

    hdfs_input = "/input/Enrollment.csv"
    hdfs_output = f"/output/{job_name}"

    env = build_env()

    # ------------------------------------------------------------
    # Check job
    # ------------------------------------------------------------
    mapper_py = job_dir / "mapper.py"
    reducer_py = job_dir / "reducer.py"
    if not mapper_py.exists():
        print("\n[FAIL] mapper.py not found")
        sys.exit(1)
    if not reducer_py.exists():
        print("\n[FAIL] reducer.py not found")
        sys.exit(1)

    # Export MongoDB
    print("\n" + "=" * 60)
    print("Export MongoDB")
    print("=" * 60)
    run([PYTHON, "-m", "mongodb.export_data"], cwd=PROJECT_ROOT, env=env)
    print("\n[OK] MongoDB export completed")

    # Upload CSV to HDFS
    print("\n" + "=" * 60)
    print("Upload CSV To HDFS")
    print("=" * 60)
    print("Removing old input...")
    run(["hdfs", "dfs", "-rm", "-f", hdfs_input], env=env, check=False)

    print("Uploading CSV...")
    run(["hdfs", "dfs", "-put", str(local_input), "/input"], env=env)

    print("\nVerify HDFS input:")
    run(["hdfs", "dfs", "-ls", "/input"], env=env, check=False)

    # ------------------------------------------------------------
    # Remove Old Output (retry toi da 10 lan)
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Remove Old Output (khong dua vao exit code cua -test -e
    # vi hdfs.cmd tren Windows thuong khong tra ve dung exit code)
    # ------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Remove Old Output")
    print("=" * 60)

    def output_exists():
        result = run(["hdfs", "dfs", "-ls", "/output/"], env=env, check=False, capture=True)
        combined = (result.stdout or "") + (result.stderr or "")
        return job_name in combined and hdfs_output in combined

    run(["hdfs", "dfs", "-rm", "-r", "-f", "-skipTrash", hdfs_output],
        env=env, check=False, capture=True)

    for attempt in range(1, 11):
        if not output_exists():
            break
        print(f"Output directory still exists, waiting and retrying... {attempt}/10")
        run(["hdfs", "dfs", "-rm", "-r", "-f", "-skipTrash", hdfs_output],
            env=env, check=False, capture=True)
        time.sleep(1)
    else:
        print("[FAIL] Could not confirm output directory deletion after 10 retries")
        sys.exit(1)

    if local_output.exists():
        shutil.rmtree(local_output)

    print("\n[OK] Old output removed")

    # Hadoop Streaming
    print("\n" + "=" * 60)
    print("Hadoop Streaming")
    print("=" * 60)
    print(f"\nJob      : {job_name}")
    print(f"Mapper   : {mapper_py}")
    print(f"Reducer  : {reducer_py}")
    print(f"Input    : {hdfs_input}")
    print(f"Output   : {hdfs_output}")
    print(f"Reducers : {num_reducers}")

    csv_parser = PROJECT_ROOT / "parser_1" / "csv_parser.py"

    run([
        "hadoop", "jar", str(STREAMING_JAR),
        "-D", f"mapreduce.job.reduces={num_reducers}",
        "-file", "mapper.py",
        "-file", "reducer.py",
        "-file", str(csv_parser),
        "-input", hdfs_input,
        "-output", hdfs_output,
        "-mapper", f"{PYTHON} mapper.py",
        "-reducer", f"{PYTHON} reducer.py",
    ], cwd=job_dir, env=env)

    copied_parser = job_dir / "csv_parser.py"
    if copied_parser.exists():
        copied_parser.unlink()

    # Download Result
    print("\n" + "=" * 60)
    print("Download Result")
    print("=" * 60)
    local_output.mkdir(parents=True, exist_ok=True)
    run(["hdfs", "dfs", "-get", f"{hdfs_output}/*", str(local_output)], env=env)

    # Display Result - duyet qua TAT CA cac file part-*
    print("\n" + "=" * 60)
    part_files = sorted(local_output.glob("part-*"))
    if part_files:
        print(f"Result (tat ca {len(part_files)} file part-*):\n")
        print("="*60)
        for f in part_files:
            print(f"{f.name}")
            print(f.read_text(encoding="utf-8", errors="replace"))
    else:
        print("[FAIL] khong tim thay file part-* nao")

    print("\n" + "_" * 60)
    print("Finished")
    print("_" * 60)


if __name__ == "__main__":
    main()