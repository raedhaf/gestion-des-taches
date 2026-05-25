from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Task, Team

class CustomUserCreationForm(UserCreationForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False, label="Choisir une équipe")
    new_team_name = forms.CharField(max_length=100, required=False, label="Ou créer une nouvelle équipe")

    class Meta:
        model = User
        fields = ('email', 'name', 'team', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        # On sauvegarde d'abord l'utilisateur pour qu’il ait un ID
        if commit:
            user.save()

        if self.cleaned_data.get('new_team_name'):
            team, created = Team.objects.get_or_create(name=self.cleaned_data['new_team_name'])
            if created:
                team.created_by = user  # Maintenant user est sauvegardé donc OK
                team.save()
            user.team = team
        else:
            user.team = self.cleaned_data.get('team')

        if commit:
            user.save()  # deuxième save pour mettre à jour user.team
            if user.team:
                user.team.members.add(user)

        return user



class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'is_private', 'assigned_users', 'assigned_teams']
        widgets = {
            'assigned_users': forms.CheckboxSelectMultiple,
            'assigned_teams': forms.CheckboxSelectMultiple,
        }
