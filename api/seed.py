import os
import csv
import django
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from jobs.models import Job

def seed_jobs_from_csv(file_path):
  with open(file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      job = Job(
        post_id=row['post_id'],
        job_name=row['job_name'],
        company_name=row['company_name'],
        job_full_text=row['job_full_text'],
        post_url=row['post_url'],
        post_apply_url=row['post_apply_url'],
        company_url=row['company_url'],
        company_industry=row['Company Industry'],
        minimum_compensation=row['Minimum Compensation'],
        maximum_compensation=row['Maximum Compensation'],
        compensation_type=row['Compensation Type'],
        job_hours=row['Job Hours'],
        role_seniority=row['Role Seniority'],
        minimum_education=row['Minimum Education'],
        office_location=row['Office Location'],
        post_html=row['post_html'],
        city=row['city'],
        region=row['region'],
        country=row['country'],
        job_published_at=datetime.strptime(row['job_published_at'], '%Y-%m-%d %H:%M:%S'),
        last_indexed=datetime.strptime(row['last_indexed'], '%Y-%m-%d %H:%M:%S')
      )
      job.save()

if __name__ == "__main__":
  file_path = './job_post.csv'
  seed_jobs_from_csv(file_path)
