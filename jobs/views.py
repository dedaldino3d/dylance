from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from users.permissions import IsOwnerOrReadOnly, IsPremium
from .models import Job, Activity, Proposal
from .serializers import JobSerializer, DetailJobSerializer, ProposalSerializer

JOB_ALL = Job.objects.all()


class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return AllowAny()
        return IsAuthenticated()


class RetrieveUpdateDestroyJobAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = DetailJobSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_url_kwarg = ['job_id']


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def save_job(request, job_id):
    user = request.user
    job = get_object_or_404(JOB_ALL, id=job_id)
    job_ct = ContentType.objects.get_for_model(job)
    try:
        Activity.objects.get(content_type=job_ct, object_id=job.id,
                             activity_type=Activity.SAVE, user=user)
    except Activity.DoesNotExist:
        Activity.objects.create(content_object=job, activity_type=Activity.SAVE, user=user)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
@permission_classes([IsAuthenticated])
def unsave_job(request, job_id):
    user = request.user
    job = get_object_or_404(JOB_ALL, id=job_id)
    if job and user is not None:
        job_ct = ContentType.objects.get_for_model(job)
        activity = get_object_or_404(Activity.objects.all(), content_type=job_ct, object_id=job.id,
                                     activity_type=Activity.SAVE, user=user)
        if activity is not None:
            activity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class ListCreateProposal(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = (IsAuthenticated, IsPremium,)
    lookup_url_kwarg = ['job_id']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated(), IsPremium()]
        return IsAuthenticated()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_freelancer:
            return Response(data={'message': "You need to be a freelancer to send a proposal"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        job = get_object_or_404(JOB_ALL, id=self.kwargs['job_id'])
        serializer.save(user=self.request.user, job=job)


class RetrieveUpdateDestroyProposal(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    lookup_url_kwarg = ['proposal_id']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated(), IsPremium(read_only=True)]
        return [permission() for permission in self.permission_classes]
