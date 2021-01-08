from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import TimeStampedModel

User = get_user_model()


class Job(TimeStampedModel):
    title = models.CharField(verbose_name=_("title"), blank=False)
    content = models.TextField(verbose_name=_("content"))
    est_time = models.DateTimeField()
    location = models.CharField(max_length=250, verbose_name=_("location"))

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")


class Activity(TimeStampedModel):
    LIKE = "L"
    SAVE = "S"
    ACTIVITY_TYPES = (
        (LIKE, "Like"),
        (SAVE, "Save"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities", blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    activity_type = models.CharField(verbose_name=_("activity type"), max_length=10, choices=ACTIVITY_TYPES,
                                     blank=False)

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")


class JobActivity(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_activity")
    hires = models.PositiveIntegerField(verbose_name=_("hires"))
    interviews = models.PositiveIntegerField(verbose_name=_("interviews"))

    class Meta:
        verbose_name = _("job activity")
        verbose_name_plural = _("job activities")


class Invite(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs_invites")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="invites")

    class Meta:
        verbose_name = _("invite")
        verbose_name_plural = _("invites")


class Interview(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interviews")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="interviews")

    class Meta:
        verbose_name = "interview"
        verbose_name_plural = "interviews"


class Proposal(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="proposals")
    title = models.CharField(max_length=255, verbose_name=_("title"), blank=False)
    description = models.TextField(blank=False)
    files = ArrayField(models.FileField(upload_to="jobs/proposals", blank=True))
    links = ArrayField(models.CharField(max_length=255, blank=True), size=4)

    class Meta:
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")


# TODO: make no sense keeping this table
class Requirement(models.Model):
    name = models.CharField(max_length=100)
    option = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("requirement")
        verbose_name_plural = _("requirements")
