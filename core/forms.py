# Author : w2105627
from django import forms
from .models import Dependency, Department, Meeting, Team


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_head', 'organisation']


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'meeting_date', 'meeting_description']
class TeamForm(forms.ModelForm):
    depends_on = forms.ModelMultipleChoiceField(
        queryset=Team.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='This team depends on'
    )
    depended_on_by = forms.ModelMultipleChoiceField(
        queryset=Team.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Teams that depend on this team'
    )

    class Meta:
        model = Team
        fields = [
            'team_name',
            'department',
            'team_leader',
            'status',
            'team_description',
            'team_mission',
            'responsibilities',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teams = Team.objects.all().order_by('team_name')
        if self.instance and self.instance.pk:
            teams = teams.exclude(pk=self.instance.pk)

        self.fields['depends_on'].queryset = teams
        self.fields['depended_on_by'].queryset = teams

        if self.instance and self.instance.pk:
            self.fields['depends_on'].initial = Team.objects.filter(
                upstream_dependencies__downstream_team=self.instance,
            )
            self.fields['depended_on_by'].initial = Team.objects.filter(
                downstream_dependencies__upstream_team=self.instance,
            )

    def save_dependencies(self, team, replace=False):
        if replace:
            Dependency.objects.filter(downstream_team=team).delete()
            Dependency.objects.filter(upstream_team=team).delete()

        for upstream_team in self.cleaned_data.get('depends_on', []):
            Dependency.objects.create(
                downstream_team=team,
                upstream_team=upstream_team,
            )

        for downstream_team in self.cleaned_data.get('depended_on_by', []):
            Dependency.objects.create(
                downstream_team=downstream_team,
                upstream_team=team,
            )
