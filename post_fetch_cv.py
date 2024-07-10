import logging
import os
from linkedin_api import Linkedin
from linkedin_api.utils.helpers import generate_random_id
from config import JOB_DESCRIPTIONS_PATH, RESUMES_PATH

logger = logging.getLogger(__name__)

# LinkedIn API credentials
linkedin_email = "your_linkedin_email"
linkedin_password = "your_linkedin_password"

# Connect to LinkedIn API
api = Linkedin(linkedin_email, linkedin_password)

# Job posting details
job_title = "Software Engineer"
job_description = "We are looking for an experienced Software Engineer to join our team."
job_location = "New York, NY"
job_type = "Full-time"

# Upload the job description PDF to LinkedIn
job_pdf_id = api.upload_file(JOB_DESCRIPTIONS_PATH)

# Post the job on LinkedIn
try:
    job_id = api.post_job(job_title, job_description, job_location, job_type, job_pdf_id)
    print(f"Job posted with ID: {job_id}")
    logging.info(f"Job posted with ID: {job_id}.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    logging.error(f"An error occurred: {str(e)}.")

# Retrieve applicants' CVs
try:
    applicants = api.get_job_applicants(job_id)
    logging.info(f"Retrieved {len(applicants)} job applicants.")
except Exception as e:
    print(f"An error occurred while retrieving job applicants: {str(e)}")
    logging.error(f"An error occurred while retrieving job applicants: {str(e)}.")

for applicant in applicants:
    applicant_id = applicant["id"]
    cv_url = api.get_applicant_cv(applicant_id)
    print(f"Applicant ID: {applicant_id}, CV URL: {cv_url}")

    # Download the CV/Resume and save it to the specified directory
    cv_filename = os.path.join(RESUMES_PATH, f"{applicant_id}.pdf")
    api.download_file(cv_url, cv_filename)
    print(f"CV saved: {cv_filename}")