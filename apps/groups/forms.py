from django import forms
from django.utils.text import slugify
from .models import PrivateGroup
from apps.tournaments.models import Tournament

class CreateGroupForm(forms.ModelForm):
    tournament = forms.ModelChoiceField(queryset=Tournament.objects.all())

    class Meta:
        model = PrivateGroup
        fields = ("name", "tournament")

    def save(self, owner, commit=True):
        group = super().save(commit=False)
        group.owner = owner
        group.slug = slugify(self.cleaned_data["name"])
        if commit:
            group.save()
        return group

class JoinGroupForm(forms.Form):
    invite_code = forms.CharField(max_length=12)

    def clean_invite_code(self):
        return self.cleaned_data["invite_code"].strip().upper()
