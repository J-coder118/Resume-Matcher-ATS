import json
import os
from typing import List

import nltk
import pandas as pd

from scripts.similarity.get_score import *
from scripts.utils import get_filenames_from_dir
from scripts.utils.logger import init_logging_config

from config import PROCESSED_RESUMES_PATH, PROCESSED_JOB_DESCRIPTIONS_PATH

init_logging_config()
cwd = find_path("Resume-Score")
config_path = os.path.join(cwd, "scripts", "similarity")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def tokenize_string(input_string):
    tokens = nltk.word_tokenize(input_string)
    return tokens

resume_names = get_filenames_from_dir(PROCESSED_RESUMES_PATH)
job_description = get_filenames_from_dir(PROCESSED_JOB_DESCRIPTIONS_PATH)

# Dictionary to store scores and file names
scores = {}

for resume in resume_names:
    resume_dict = read_json(PROCESSED_RESUMES_PATH + resume)
    job_dict = read_json(PROCESSED_JOB_DESCRIPTIONS_PATH + job_description)
    resume_keywords = resume_dict["extracted_keywords"]
    job_description_keywords = job_dict["extracted_keywords"]

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    final_result = get_score(resume_string, jd_string)
    for r in final_result:
        print(r.score)
        scores[resume] = r.score
    print(f"Processing resume: {resume}")
    print(f"Processing job description: {job_description}")

# Function to get the maximum score and corresponding file name
def get_max_score():
    if not scores:
        return None, None
    
    max_score = max(scores.values())
    max_file = next(filename for filename, score in scores.items() if score == max_score)
    return max_score, max_file

max_score, max_file = get_max_score()
if max_score is not None:
    print(f"The maximum score is {max_score} in the file {max_file}")
else:
    print("No scores have been added yet.")