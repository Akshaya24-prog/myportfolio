from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.conf import settings
import os
import json
import functools
from .models import Profile, Skill, Project, ContactMessage, Education


def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    contact_messages = ContactMessage.objects.all()
    education = Education.objects.all()

    skill_categories = {}
    for skill in skills:
        cat = skill.get_category_display()
        skill_categories.setdefault(cat, []).append(skill)

    context = {
        'profile': profile,
        'skill_categories': skill_categories,
        'projects': projects,
        'contact_messages': contact_messages,
        'education': education,
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


def _require_admin(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('portfolio_admin'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return func(request, *args, **kwargs)
    return wrapper


def _parse_json(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse({'error': 'Invalid JSON'}, status=400)


def api_admin_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    data, err = _parse_json(request)
    if err:
        return err
    if (data.get('username', '').strip() == settings.PORTFOLIO_ADMIN_USER and
            data.get('password', '') == settings.PORTFOLIO_ADMIN_PASS):
        request.session['portfolio_admin'] = True
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


def api_admin_logout(request):
    request.session.pop('portfolio_admin', None)
    return JsonResponse({'success': True})


@_require_admin
def api_add_skill(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    data, err = _parse_json(request)
    if err:
        return err
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    skill = Skill.objects.create(name=name, category=data.get('category', 'other'))
    return JsonResponse({
        'id': skill.id,
        'name': skill.name,
        'category': skill.category,
        'category_display': skill.get_category_display(),
    })


@_require_admin
def api_delete_skill(request, pk):
    try:
        Skill.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Skill.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


@_require_admin
def api_add_project(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    data, err = _parse_json(request)
    if err:
        return err
    title = data.get('title', '').strip()
    if not title:
        return JsonResponse({'error': 'Title is required'}, status=400)
    short_desc = data.get('short_description', '').strip()
    project = Project.objects.create(
        title=title,
        short_description=short_desc,
        description=data.get('description', short_desc).strip() or short_desc,
        tech_stack=data.get('tech_stack', '').strip(),
        github_url=data.get('github_url', '').strip(),
        live_url=data.get('live_url', '').strip(),
        status=data.get('status', 'completed'),
    )
    return JsonResponse({
        'id': project.id,
        'title': project.title,
        'short_description': project.short_description,
        'tech_list': project.get_tech_list(),
        'github_url': project.github_url,
        'live_url': project.live_url,
        'status': project.status,
        'status_display': project.get_status_display(),
    })


@_require_admin
def api_delete_project(request, pk):
    try:
        Project.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


@_require_admin
def api_update_bio(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    data, err = _parse_json(request)
    if err:
        return err
    bio = data.get('bio', '').strip()
    profile = Profile.objects.first()
    if not profile:
        return JsonResponse({'error': 'No profile found. Create one via /admin first.'}, status=404)
    profile.bio = bio
    profile.save()
    return JsonResponse({'success': True, 'bio': bio})


def _edu_to_dict(edu):
    return {
        'id': edu.id,
        'institution': edu.institution,
        'degree': edu.degree,
        'start_date': edu.start_date,
        'end_date': edu.end_date,
    }


@_require_admin
def api_add_education(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    data, err = _parse_json(request)
    if err:
        return err
    institution = data.get('institution', '').strip()
    if not institution:
        return JsonResponse({'error': 'Institution is required'}, status=400)
    edu = Education.objects.create(
        institution=institution,
        degree=data.get('degree', '').strip(),
        start_date=data.get('start_date', '').strip(),
        end_date=data.get('end_date', 'Present').strip() or 'Present',
    )
    return JsonResponse(_edu_to_dict(edu))


@_require_admin
def api_edit_education(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    data, err = _parse_json(request)
    if err:
        return err
    try:
        edu = Education.objects.get(pk=pk)
    except Education.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    edu.institution = data.get('institution', edu.institution).strip()
    edu.degree = data.get('degree', edu.degree).strip()
    edu.start_date = data.get('start_date', edu.start_date).strip()
    edu.end_date = data.get('end_date', edu.end_date).strip() or 'Present'
    edu.save()
    return JsonResponse(_edu_to_dict(edu))


@_require_admin
def api_delete_education(request, pk):
    try:
        Education.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Education.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
