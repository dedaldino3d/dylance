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

    def create(self, validated_data):
        if 'request' in self.context:
            user = self.context['request'].user
            validated_data.update({
                user: user
            })
