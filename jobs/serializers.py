from rest_framework.serializers import ModelSerializer
from users.serializers import SmallUserSerializer
from .models import Job, Proposal


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ("created_at", "updated_at", "user", "id")


class DetailJobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ("created_at", "updated_at", "user", "id")


class ProposalSerializer(ModelSerializer):
    user = SmallUserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = '__all__'
        read_only_fields = ("created_at", "updated_at", "user", "id", "job")
