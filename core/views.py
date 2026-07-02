# Author : w2105627
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .models import AuditLog, Team, Dependency, TeamContact, Organisation, Department, Meeting
from django.db.models import Q
from .forms import DepartmentForm, MeetingForm, TeamForm
from django.shortcuts import redirect





def root(request):
    if request.user.is_authenticated:
        return redirect('core:teams')

    return redirect('accounts:login')

@login_required
def teams(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    teams = Team.objects.filter(
        Q(team_name__icontains=q) |
        Q(department__department_name__icontains=q) |
        Q(team_leader__full_name__icontains=q) |
        Q(status__icontains=q)
    )

    return render(request, 'core/teams.html', {'teams': teams, 'q': q})

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)

        if form.is_valid():
            team = form.save()
            form.save_dependencies(team)
            log_team_action(
                request.user,
                'CREATE_TEAM',
                team,
                f'Created team: {team.team_name}',
            )
            messages.success(request, 'Team created.')
            return redirect('core:team_detail', team_id=team.id)
    else:
        form = TeamForm()

    return render(request, 'core/create_team.html', {'form': form})

@login_required
def organisation(request):
    organisations = Organisation.objects.all()

    return render(request, 'core/organisation.html', {'organisations': organisations})

@login_required
def departments(request):
    departments = Department.objects.all()

    return render(request, 'core/departments.html', {'departments': departments})


@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Department created.')
            return redirect('core:departments')
    else:
        form = DepartmentForm()

    return render(request, 'core/create_department.html', {'form': form})

@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    upstream = Dependency.objects.filter(downstream_team=team)
    downstream = Dependency.objects.filter(upstream_team=team)

    contact = TeamContact.objects.filter(team=team).first()
    meetings = team.meetings.all()
    repositories = team.repositories.all()
    return render(request, 'core/team_detail.html', {
        'team': team,
        'upstream': upstream,
        'downstream': downstream,
        'contact': contact,
        'meetings': meetings,
        'repositories': repositories
    })


@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)

        if form.is_valid():
            team = form.save()
            form.save_dependencies(team, replace=True)
            log_team_action(
                request.user,
                'EDIT_TEAM',
                team,
                f'Edited team: {team.team_name}',
            )
            messages.success(request, 'Team updated.')
            return redirect('core:team_detail', team_id=team.id)
    else:
        form = TeamForm(instance=team)

    return render(request, 'core/edit_team.html', {'form': form, 'team': team})

# Creates an audit log entry for team changes.
def log_team_action(user, action_type, team, details):
    AuditLog.objects.create(
        user=user,
        team=team,
        action_type=action_type,
        audit_details=details,
    )

@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == 'POST':
        team_id = team.id
        team_name = team.team_name
        log_team_action(
            request.user,
            'DELETE_TEAM',
            team,
            f'Deleted team: {team_name}',
        )
        team.delete()
        messages.success(request, 'Team deleted.')
        return redirect('core:teams')

    return render(request, 'core/delete_team.html', {'team': team})


@login_required
def schedule_meeting(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by_user = request.user
            meeting.team = team
            meeting.save()

            messages.success(request, 'Meeting scheduled.')
            return redirect('core:team_detail', team_id=team.id)
    else:
        form = MeetingForm()

    return render(request, 'core/schedule.html', {'form': form, 'team': team})


@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)

        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated.')
            return redirect('core:team_detail', team_id=meeting.team.id)
    else:
        form = MeetingForm(instance=meeting)

    return render(request, 'core/edit_meeting.html', {
        'form': form,
        'meeting': meeting,
    })


@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    team_id = meeting.team.id

    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted.')
        return redirect('core:team_detail', team_id=team_id)

    return render(request, 'core/delete_meeting.html', {'meeting': meeting})
