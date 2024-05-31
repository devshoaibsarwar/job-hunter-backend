from djongo import models
from .utils import make_ngrams

class Job(models.Model):
    post_id = models.CharField(max_length=255, unique=True)
    job_name = models.CharField(max_length=255, null=False)
    company_name = models.CharField(max_length=255)
    job_full_text = models.TextField()
    post_url = models.URLField()
    post_apply_url = models.URLField()
    company_url = models.URLField(null=True)
    company_industry = models.CharField(max_length=255, null=True)
    minimum_compensation = models.CharField(max_length=50, null=True)
    maximum_compensation = models.CharField(max_length=50, null=True)
    compensation_type = models.CharField(max_length=50, null=True)
    job_hours = models.CharField(max_length=50, null=True)
    role_seniority = models.CharField(max_length=50, null=True)
    minimum_education = models.CharField(max_length=255, null=True, blank=True)
    office_location = models.CharField(max_length=255, null=True)
    post_html = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    job_published_at = models.DateTimeField(null=True)
    last_indexed = models.DateTimeField()
    ngrams = models.TextField()

    def save(self, *args, **kwargs):
        self.ngrams = ' '.join(make_ngrams(self.job_name))
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.job_name