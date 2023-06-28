from student.models import AcademicYear


def set_current_academic_year(request):
    if 'current_academic_year' not in request.session:
        current_academic_year = AcademicYear.objects.all().order_by('-started_at').first()
        if current_academic_year:
            request.session['current_academic_year'] = current_academic_year.name
        else:
            request.session['current_academic_year'] = "No academic year selected"
    # Return a dictionary containing the session variable
    return {'current_academic_year': request.session.get('current_academic_year')}



