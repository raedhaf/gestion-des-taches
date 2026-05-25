from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, User, Team
from .forms import TaskForm, CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('task_list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(
    Q(is_private=False) |
    Q(created_by=request.user) |
    Q(assigned_users=request.user) |
    Q(assigned_teams__in=request.user.teams.all())
    ).distinct()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def team_profile(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    tasks = Task.objects.filter(assigned_teams=team, is_private=False)
    return render(request, 'team_profile.html', {'team': team, 'tasks': tasks})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Tâche modifiée avec succès.")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.created_by != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette tâche.")
    else:
        task.delete()
        messages.success(request, "Tâche supprimée.")
    return redirect('task_list')



@login_required
def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            team, created = Team.objects.get_or_create(name=name)
            if created or not team.created_by:
                team.created_by = request.user
                team.save()
            team.members.add(request.user)
            messages.success(request, f"Équipe '{name}' créée et vous avez été ajouté.")
            return redirect('team_profile', team_id=team.id)
        else:
            messages.error(request, "Le nom de l'équipe ne peut pas être vide.")
    return render(request, 'team/create_team.html')





@login_required
@require_POST
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.members.all():
        team.members.add(request.user)
        messages.success(request, f"Vous avez rejoint l'équipe {team.name}.")
    else:
        messages.info(request, f"Vous êtes déjà membre de l'équipe {team.name}.")
    return redirect('team_profile', team_id=team.id)

@login_required
@require_POST
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user in team.members.all():
        team.members.remove(request.user)
        messages.success(request, f"Vous avez quitté l'équipe {team.name}.")
    else:
        messages.info(request, f"Vous n'êtes pas membre de l'équipe {team.name}.")
    return redirect('team_profile', team_id=team.id)

@login_required
def team_profile(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    tasks = Task.objects.filter(assigned_teams=team, is_private=False)
    members = team.members.all()
    is_member = request.user in members
    return render(request, 'team/team_profile.html', {
        'team': team,
        'tasks': tasks,
        'members': members,
        'is_member': is_member,
    })


@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(assigned_users=user_profile, is_private=False)
    teams = user_profile.teams.all()
    return render(request, 'team/user_profile.html', {
        'user_profile': user_profile,
        'tasks': tasks,
        'teams': teams,
    })


@login_required
def team_list(request):
    teams = Team.objects.all()
    user = request.user
    return render(request, 'team/team_list.html', {'teams': teams, 'user': user})
