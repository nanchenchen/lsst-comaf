from django.db import models
from django.contrib.auth.models import User
from comaf.apps.metrics.models import Plot

# Create your models here.
class SpaceView(models.Model):
    owner = models.ForeignKey(User)
    plots = models.ManyToManyField(Plot, related_name="space_views", null=True, blank=True, default=None)

    def __unicode__(self):
        return self.workspace.name + " / " + self.owner.name

class MemberSpace(models.Model):
    owner = models.ForeignKey(User)
    space_views = models.ManyToManyField(SpaceView, related_name="member_spaces", null=True, blank=True, default=None)
    plots = models.ManyToManyField(Plot, related_name="member_spaces", null=True, blank=True, default=None)

    def __unicode__(self):
        return self.workspace.name + " / " + self.owner.name


class WorkSpace(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    members = models.ManyToManyField(User, related_name="workspaces", null=True, blank=True, default=None)
    member_spaces = models.ManyToManyField(MemberSpace, related_name="workspaces", null=True, blank=True, default=None)
    space_views = models.ManyToManyField(SpaceView, related_name="workspaces", null=True, blank=True, default=None)
    current_views =models.ForeignKey(SpaceView)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name + " / " + self.owner.name



def add_a_member_to_workspace(workspace, user):
    workspace.members.add(user)
    member_space = MemberSpace(owner=user)
    member_space.save()
    workspace.member_spaces.add(member_space)
    return member_space

def create_a_space_view(member_space):
    space_view = SpaceView(owner=member_space.owner)
    space_view.save()
    member_space.space_views.add(space_view)
    member_space.save()
    member_space.workspace.space_views.add(space_view)
    member_space.workspace.save()
    return space_view