# SmartHire – Backend (Job Portal & Resume Analyzer)

SmartHire is a backend system built using Django and Django REST Framework that solves the real-world problem of efficient hiring and job matching.
It provides APIs for candidates, recruiters, and administrators to manage jobs, resumes, applications, and intelligent matching between them.

# 🎯 Real-World Problem It Solves

🔴 Problem in Hiring Systems

Recruiters receive hundreds of resumes per job

Manual resume screening is:

Time-consuming

Error-prone

Inconsistent

Candidates apply blindly without knowing job fit

Resume formats and skills are highly inconsistent

🟢 How SmartHire Solves This

Automatically parses resumes

Extracts and normalizes skills

Computes an ATS score

Matches resumes with jobs using rule-based logic

Ranks candidates for recruiters

Recommends jobs to candidates

This reduces manual screening effort and improves quality of hiring decisions.

# 🧠 System Capabilities (Implemented)

👤 User Management

Custom user system with roles:

Candidate

Recruiter

JWT-based authentication

Secure login and token refresh APIs

📄 Resume Processing

Resume upload (PDF / DOCX)

Text extraction from resume files

Skill extraction from resume content

ATS (Applicant Tracking System) score calculation

Resume processing handled asynchronously

💼 Job Management

Recruiters can:

Create jobs

Define required skills

Define experience requirements

Set salary ranges

Jobs store structured skill and experience data

📌 Job Applications

Candidates can apply to jobs

Each application stores:

Candidate

Job

Resume

Application status

Match score

🤝 Resume ↔ Job Matching

Rule-based matching engine

Matching logic considers:

Required skills overlap

Optional skills overlap

Resume ATS score

Final match score is calculated and stored per application

Recruiters can view ranked candidates for a job

🎯 Job Recommendations

Candidates receive job recommendations

Based on resume skills and job requirements

Uses the same rule-based matching logic

# 🛠️ Technologies Used (Only What Is Implemented)
Backend Framework

Python

Django

Django REST Framework

Database

PostgreSQL

Authentication & Security

JWT authentication (SimpleJWT)

Role-based access control

Async Processing

Celery

Redis (message broker)

Resume Processing

File handling for PDF/DOCX

Text extraction utilities

Skill extraction logic

ATS scoring logic

DevOps & Infrastructure

Docker

Docker Compose

Environment-based configuration (.env)

Separation of services (backend, database, redis, celery)

# 👨‍💻 Author

Vishal Gupta
Backend Developer | Django | REST APIs | Scalable Systems


