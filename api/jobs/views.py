from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from django.db.models import Q
from .utils import make_ngrams

@api_view(['GET'])
def job_search(request):
    job_title = request.query_params.get('query', None)

    try:
        if job_title:
            query_ngrams = ' '.join(make_ngrams(job_title))

            jobs = Job.objects.filter(Q(ngrams__icontains=query_ngrams))
        else:
            jobs = Job.objects.all()

        job_list = [{"id": str(job.id), "job_name": job.job_name, "company_name": job.company_name} for job in jobs]

        if not job_list:
            return Response({'message': 'No jobs found', 'data': []}, status=status.HTTP_404_NOT_FOUND)

        return Response({'data': job_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
