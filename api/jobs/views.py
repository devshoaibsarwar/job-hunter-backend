from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from authentication.models import User

@api_view(['GET'])
def job_search(request):
    """
    Job Search Flow
    - Get job_title from query parameters
    - Perform a case-insensitive search in the MongoDB jobs collection
    - Return a list of matching job postings
    """

    job_title = request.query_params.get('query', None)

    try:    
        print(Job.objects.all())
        if job_title:
            jobs = Job.objects.filter(job_name__icontains=job_title)
        else:
            jobs = Job.objects.all()

        job_list = [{"id": str(job.id), "job_name": job.job_name, "company_name": job.company_name} for job in jobs]

        if not job_list:
            return Response({'message': 'No jobs found', 'data': []}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'data': job_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)