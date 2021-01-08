from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    # TODO: name must be convites (but in english)
    sended = models.PositiveIntegerField(verbose_name=_("sended"))

    class Meta:
        verbose_name = _("job activity")
        verbose_name_plural = _("job activities")


# TODO: adicionar convite


class Skill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=250, verbose_name=_("name"))
    choice = models.CharField(max_length=250, verbose_name=_("choice"))

    class Meta:
        verbose_name = _("skill")
        verbose_name_plural = _("skills")


class Proposal(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="proposals")
    content = models.TextField()

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
