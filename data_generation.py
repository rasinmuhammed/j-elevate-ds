import csv
import random

# Define departments, roles, and their corresponding skills
departments = {
    "Data Engineering": {
        "Senior Data Engineer": [
            "Python Programming",
            "SQL",
            "Data Warehousing",
            "ETL",
            "Cloud Computing",
            "Spark",
            "Hadoop",
            "Data Modeling",
        ],
        "Data Engineer": [
            "Python Programming",
            "SQL",
            "Data Warehousing",
            "ETL",
            "Cloud Computing",
        ],
        "Junior Data Engineer": ["Python Programming", "SQL", "ETL"],
        "ETL Developer": ["Python Programming", "SQL", "ETL", "Data Warehousing"],
        "Data Architect": [
            "Data Modeling",
            "Data Warehousing",
            "Cloud Computing",
            "Data Governance",
            "Big Data",
        ],
    },
    "Data Science": {
        "Senior Data Scientist": [
            "Python Programming",
            "R Programming",
            "Machine Learning",
            "Deep Learning",
            "Statistics",
            "Data Visualization",
            "Cloud Computing",
        ],
        "Data Scientist": [
            "Python Programming",
            "Machine Learning",
            "Statistics",
            "Data Visualization",
        ],
        "Junior Data Scientist": ["Python Programming", "Machine Learning", "Statistics"],
        "Machine Learning Engineer": [
            "Python Programming",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
        ],
        "Data Analyst": ["SQL", "Data Visualization", "Excel", "Data Analysis"],
    },
    "Full Stack Development": {
        "Senior Full Stack Developer": [
            "JavaScript",
            "HTML",
            "CSS",
            "React",
            "Node.js",
            "Python Programming",
            "Databases",
            "DevOps",
        ],
        "Full Stack Developer": [
            "JavaScript",
            "HTML",
            "CSS",
            "React",
            "Node.js",
            "Databases",
        ],
        "Junior Full Stack Developer": ["JavaScript", "HTML", "CSS", "React"],
        "Frontend Developer": ["JavaScript", "HTML", "CSS", "React", "Angular", "Vue.js"],
        "Backend Developer": ["Node.js", "Python Programming", "Java", "Databases"],
    },
    "Core Consulting": {
        "Senior Business Analyst": [
            "Business Analysis",
            "Data Analysis",
            "SQL",
            "Project Management",
            "Problem Solving",
            "Communication",
        ],
        "Business Analyst": [
            "Business Analysis",
            "Data Analysis",
            "SQL",
            "Problem Solving",
            "Communication",
        ],
        "Junior Business Analyst": ["Business Analysis", "Data Analysis"],
        "Management Consultant": [
            "Strategy",
            "Business Analysis",
            "Project Management",
            "Leadership",
        ],
        "Strategy Consultant": [
            "Strategy",
            "Business Analysis",
            "Data Analysis",
            "Leadership",
            "Communication",
        ],
    },
}

# Load Coursera data (replace 'Coursera.csv' with your actual filename)
coursera_courses = []
with open("Coursera.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        coursera_courses.append(row)

# Function to generate a random employee profile
def generate_employee(employee_id):
    department = random.choice(list(departments.keys()))
    role = random.choice(list(departments[department].keys()))
    num_skills = min(random.randint(2, 5), len(departments[department][role]))  # Ensure k is not larger than the skill list
    user_skills = random.sample(departments[department][role], k=num_skills) 
    points = random.randint(100, 300)  # Simulate skill level
    return employee_id, department, role, user_skills, points

# Function to recommend courses based on skills and level
def recommend_courses(user_skills, level, department, num_courses=5):
    recommended = []
    potential_courses = [
        c
        for c in coursera_courses
        if any(s in c["skills"] for s in user_skills)
        and (level.lower() in c["level"].lower() or "mixed" in c["level"].lower())
    ]
    if department.lower() in ["data engineering", "data science"]:
        potential_courses = [
            c
            for c in potential_courses
            if "programming" in c["skills"].lower()
            or "python" in c["skills"].lower()
            or "sql" in c["skills"].lower()
        ]
    # Prioritize courses that teach new skills
    potential_courses.sort(
        key=lambda c: len(set(eval(c["skills"])) - set(user_skills)), reverse=True
    )
    recommended = potential_courses[:num_courses]
    return recommended

# Generate synthetic training data
def generate_training_data(num_employees, output_filename):
    with open(output_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "employeeID",
                "courseId",
                "partner",
                "course",
                "expected_skills",
                "rating",
                "level",
                "certificateType",
                "duration",
                "designation",
                "userSkills",
                "points",
                "department",
            ]
        )

        for i in range(num_employees):
            employee_id = f"EMP{random.randint(1000000000000000, 9999999999999999)}"
            (
                employee_id,
                department,
                role,
                user_skills,
                points,
            ) = generate_employee(employee_id)
            recommended_courses = recommend_courses(
                user_skills, level=role.split()[0], department=department
            )  # Use the first word of the role as level indicator

            for course in recommended_courses:
                writer.writerow(
                    [
                        employee_id,
                        course["course"].replace(",", ""),
                        course["partner"],
                        course["course"].replace(",", ""),
                        course["skills"],
                        course["rating"],
                        course["level"].strip(),
                        course["certificatetype"].strip(),
                        course["duration"].strip(),
                        role,
                        str(user_skills),
                        points,
                        department,
                    ]
                )


# Example usage: Generate a CSV file with 100,000 employee-course recommendations
generate_training_data(5000, "training_data.csv") 