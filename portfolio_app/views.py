from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse, Http404
import os
from .models import Profile, Skill, Project, ContactMessage


def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    contact_messages = ContactMessage.objects.all()   # for admin inbox

    # Group skills by category label
    skill_categories = {}
    for skill in skills:
        cat = skill.get_category_display()
        skill_categories.setdefault(cat, []).append(skill)

    context = {
        'profile': profile,
        'skill_categories': skill_categories,
        'projects': projects,
        'contact_messages': contact_messages,
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if all([name, email, subject, message]):
            ContactMessage.objects.create(
                name=name, email=email,
                subject=subject, message=message
            )
            messages.success(request, 'Message sent! I will get back to you soon.')
        else:
            messages.error(request, 'Please fill in all fields.')

    return redirect('home')


def download_resume(request):
    profile = Profile.objects.first()
    if profile and profile.resume:
        path = profile.resume.path
        if os.path.exists(path):
            return FileResponse(open(path, 'rb'), content_type='application/pdf',
                                as_attachment=True, filename='Akshaya_Resume.pdf')
    raise Http404("Resume not available.")