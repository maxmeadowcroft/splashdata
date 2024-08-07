# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProjectForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Project
import pandas as pd


@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    df = pd.read_csv(project.csv_file.path)
    # Add logic for sorting and displaying data
    context = {
        'project': project,
        'dataframe': df.to_html(classes='table table-striped'),
    }
    return render(request, 'myapp/project_detail.html', context)


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'myapp/create_project.html', {'form': form})

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    # Add logic to handle CSV processing and display
    return render(request, 'myapp/project_detail.html', {'project': project})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
