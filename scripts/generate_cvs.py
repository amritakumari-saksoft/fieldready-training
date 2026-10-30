import json
from pathlib import Path

OUTPUT_DIR = Path("data/synthetic_cvs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

first_names = [
    "Priya",
    "Rahul",
    "Ananya",
    "Arjun",
    "Neha",
    "Rohan",
    "Sneha",
    "Vikram",
    "Aisha",
    "Karan",
    "Meera",
    "Aditya",
    "Pooja",
    "Dev",
    "Isha",
    "Kabir",
    "Riya",
    "Nikhil",
    "Tara",
    "Aman",
]

last_names = [
    "Sharma",
    "Verma",
    "Rao",
    "Mehta",
    "Singh",
    "Gupta",
    "Patel",
    "Nair",
    "Khan",
    "Malhotra",
    "Iyer",
    "Joshi",
    "Kapoor",
    "Shah",
    "Bose",
    "Sethi",
    "Das",
    "Kulkarni",
    "Menon",
    "Jain",
]

skill_sets = [
    ["Python", "SQL"],
    ["Java", "Spring Boot"],
    ["JavaScript", "React"],
    ["Python", "FastAPI"],
    ["Docker", "Kubernetes"],
]

education_options = [
    ["B.Tech Computer Science"],
    ["B.Sc Information Technology"],
    ["MCA"],
    ["B.E Computer Engineering"],
]

ground_truth = []

for index in range(20):
    cv_id = f"cv_{index + 1:02d}"
    name = f"{first_names[index]} {last_names[index]}"
    email = f"{first_names[index].lower()}.{last_names[index].lower()}@example.com"
    phone = f"90000{index:05d}"
    skills = skill_sets[index % len(skill_sets)]
    education = education_options[index % len(education_options)]
    experience = float(index % 7)

    cv_text = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Skills: {', '.join(skills)}\n"
        f"Education: {', '.join(education)}\n"
        f"Professional Experience: {experience:g} years\n"
    )

    (OUTPUT_DIR / f"{cv_id}.txt").write_text(cv_text, encoding="utf-8")

    ground_truth.append(
        {
            "cv_id": cv_id,
            "full_name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "education": education,
            "experience_years": experience,
        }
    )

Path("data/ground_truth.json").write_text(
    json.dumps(ground_truth, indent=2),
    encoding="utf-8",
)
