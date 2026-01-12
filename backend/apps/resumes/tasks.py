from celery import shared_task
from .models import Resume
from .services.text_extractor import extract_resume_text
from apps.resumes.services.skill_extractor import extract_skills
from apps.resumes.services.ats_scoring import compute_ats_score
from apps.jobs.models import Job
from apps.applications.models import Application


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10,
    retry_kwargs={"max_retries": 3},
)
def parse_resume_task(self, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)

        text = extract_resume_text(resume.file.path)
        resume.extracted_text = text

        skills = extract_skills(text)
        resume.extracted_skills = skills

        ats_score, ats_feedback = compute_ats_score(text)
        resume.ats_score = ats_score
        resume.ats_feedback = ats_feedback

        resume.is_parsed = True
        resume.parse_error = None
        resume.save()

    except Exception as e:
        resume.parse_error = str(e)
        resume.is_parsed = False
        resume.save()
        raise e
