# TODO: Move mappers/reducers into job folder

## ✅ Step 1: Create new job folders for external mapper/reducer pairs

- [x] `job/job/semester_count/mapper.py` + `reducer.py`
- [x] `job/job/avg_midterm_per_course/mapper.py` + `reducer.py`
- [x] `job/job/course_performance_analytics/mapper.py` + `reducer.py`
- [x] `job/job/lowest_score_per_course/mapper.py` + `reducer.py`
- [x] `job/job/pass_fail_per_course/mapper.py` + `reducer.py`

## ✅ Step 2: Update run_all.cmd

- [x] Fix PROJECT_ROOT path
- [x] Add 5 new jobs to pipeline
- [x] Fix Windows sort.exe memory issue (replaced with Python sort)

## ✅ Step 3: Remove old mapper/reducer files from root level

- [x] Delete `mapper/` files (already moved)
- [x] Delete `reducer/` files (already moved)
- [x] Delete `semester_count.py` root file

## ✅ Step 4: Run tests and verify

- [x] Execute `run_all.cmd` to test all jobs
- [x] All 10 jobs passed successfully!
- [x] average_score.txt now has data (fixed sort issue)
