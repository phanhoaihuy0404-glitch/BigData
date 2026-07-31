use("StudentManagementBigData");

// Top 10 students with the most enrolled courses
db.Enrollment.aggregate([
    {
        $group: {
            _id: "$StudentID",
            TotalCourses: { $sum: 1 }
        }
    },
    {
        $sort: {
            TotalCourses: -1
        }
    },
    {
        $limit: 10
    }
]).forEach(printjson);