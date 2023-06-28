from _decimal import Decimal

from django.urls import reverse
from django.conf import settings

from student.models import Student, Item
from teacher.models import Rating, Teacher, Lesson, Exam, StudentExam


def test_teacher_home_view(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    url2 = reverse('teacher:home')
    client = teacher_log_in
    response = client.get(url1)
    response = client.get(url2)
    assert response.status_code == 200
    content = response.content.decode('UTF-8')
    assert 'Teacher First' in content
    assert content.count('John') == 1
    assert content.count('Science') == 1
    assert client.session['current_academic_year'] == '2023-2024'
    assert client.session['is_student'] is False
    assert client.session['is_teacher'] is True


def test_teacher_home_view_not_logged(client):
    url = reverse('teacher:home')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL + '?next=' + reverse('teacher:home')


def test_rating_create_view(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)
    student = Student.objects.get(pk=1)
    teacher = Teacher.objects.get(pk=1)
    item = Item.objects.get(pk=2)
    url = reverse('teacher:rating-create')
    form_data = {
        'student': student.pk,
        'teacher': teacher.pk,
        'item': item.pk,  # Replace with the correct item ID
        'date': '2023-06-27',
        'value': '4.5',
        'notice': 'Test notice',
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 302  # Should redirect after successful form submission
    assert Rating.objects.count() == 11


def test_rating_create_view_when_student_is_logged(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)
    student = Student.objects.get(pk=1)
    teacher = Teacher.objects.get(pk=1)
    item = Item.objects.get(pk=2)
    url = reverse('teacher:rating-create')
    form_data = {
        'student': student.pk,
        'teacher': teacher.pk,
        'item': item.pk,  # Replace with the correct item ID
        'date': '2023-06-27',
        'value': '4.5',
        'notice': 'Test notice',
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200  # Should redirect after successful form submission
    assert Rating.objects.count() == 10


def test_rating_update(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)
    student = Student.objects.get(pk=1)
    teacher = Teacher.objects.get(pk=1)
    item = Item.objects.get(pk=2)
    url = reverse('teacher:rating-update', args=[1])
    form_data = {
        'student': student.pk,
        'teacher': teacher.pk,
        'item': item.pk,  # Replace with the correct item ID
        'date': '2023-06-27',
        'value': '5.0',
        'notice': 'Test notice updated',
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    updated_rating = Rating.objects.get(pk=1)
    assert updated_rating.notice == 'Test notice updated'


def test_rating_update_when_user_is_student(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)
    student = Student.objects.get(pk=1)
    teacher = Teacher.objects.get(pk=1)
    item = Item.objects.get(pk=2)
    url = reverse('teacher:rating-update', args=[1])
    form_data = {
        'student': student.pk,
        'teacher': teacher.pk,
        'item': item.pk,  # Replace with the correct item ID
        'date': '2023-06-27',
        'value': '5.0',
        'notice': 'Test notice updated',
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    updated_rating = Rating.objects.get(pk=1)
    is_updated = updated_rating.notice == 'Test notice updated'
    assert is_updated is False


def test_lesson_create_view(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)
    url = reverse('teacher:lesson-create')
    data = {
        'localization': '1',
        'item': '2',
        'level': '1',
        'reunion': '2',
        'present_students': ['1'],
        'topic': 'Test Topic',
        'date_time': '2023-06-27 12:00:00',
        'references': '',
        'teacher': '1'
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert Lesson.objects.count() == 3


def test_lesson_create_view_when_student_is_logged(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)
    url = reverse('teacher:lesson-create')
    data = {
        'localization': '1',
        'item': '2',
        'level': '1',
        'reunion': '2',
        'present_students': ['1'],
        'topic': 'Test Topic',
        'date_time': '2023-06-27 12:00:00',
        'references': '',
        'teacher': '1'
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert Lesson.objects.count() == 2


def test_lesson_update(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)

    url = reverse('teacher:lesson-update', args=[1])
    data = {
        'localization': '2',  # update value different from stored in sample database
        'item': '2',
        'level': '1',
        'reunion': '2',
        'present_students': ['1'],
        'topic': 'Test Topic',
        'date_time': '2023-06-27 12:00:00',
        'references': '',
        'teacher': '1'
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    updated_lesson = Lesson.objects.get(pk=1)
    assert updated_lesson.localization.pk == 2


def test_lesson_update_when_student_is_logged(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)

    url = reverse('teacher:lesson-update', args=[1])
    data = {
        'localization': '2',  # update value different from stored in sample database
        'item': '2',
        'level': '1',
        'reunion': '2',
        'present_students': ['1'],
        'topic': 'Test Topic',
        'date_time': '2023-06-27 12:00:00',
        'references': '',
        'teacher': '1'
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    updated_lesson = Lesson.objects.get(pk=1)
    assert updated_lesson.localization.pk == 1


def test_exam_create_view_when_student_is_logged(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)
    url = reverse('teacher:exam-create')
    data = {
        'academic_year': '2',
        'localization': '1',
        'item': '2',
        'date_time': '2023-06-27 12:00:00',
        'students': ['1'],
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert Exam.objects.count() == 2


def test_exam_create_view(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)
    url = reverse('teacher:exam-create')
    data = {
        'academic_year': '2',  # Replace with valid academic year ID
        'localization': '1',  # Replace with valid localization ID
        'item': '2',  # Replace with valid item ID
        'date_time': '2023-06-27 12:00:00',
        'students': ['1'],  # Replace with valid student IDs
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert Exam.objects.count() == 3


def test_exam_update_when_student_is_logged(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)

    url = reverse('teacher:exam-update', args=[2])
    data = {
        'academic_year': '2',
        'localization': '1',
        'item': '2',
        'date_time': '2023-06-27 12:00:00',
        'students': ['1'],
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    updated_exam = Exam.objects.get(pk=2)
    assert updated_exam.localization.pk == 2


def test_exam_update(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)

    url = reverse('teacher:exam-update', args=[2])
    data = {
        'academic_year': '2',
        'localization': '1',
        'item': '2',
        'date_time': '2023-06-27 12:00:00',
        'students': ['1'],
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    updated_exam = Exam.objects.get(pk=2)
    assert updated_exam.localization.pk == 1


def test_studentexam_update(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    client = teacher_log_in
    response = client.get(url1)

    url = reverse('teacher:exam-rating-update', args=[3])
    data = {
        'student': '1', 'exam': '2', 'rating': 4.5, 'is_passed': True
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    updated_studentexam = StudentExam.objects.get(pk=3)
    assert updated_studentexam.rating == 4.5


def test_studentexam_update_when_student_is_logged(sample_database, student_log_in):
    url1 = reverse('student:home')
    client = student_log_in
    response = client.get(url1)

    url = reverse('teacher:exam-rating-update', args=[3])
    data = {
        'student': '1', 'exam': '2', 'rating': 4.5, 'is_passed': True
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    updated_studentexam = StudentExam.objects.get(pk=3)
    assert updated_studentexam.rating == Decimal('4.20')


def test_teacher_lessons_view(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    url2 = reverse('teacher:lessons')
    client = teacher_log_in
    response = client.get(url1)
    response = client.get(url2)
    assert response.status_code == 200
    content = response.content.decode('UTF-8')
    assert 'Teacher First' in content
    assert content.count('Introduction to Science') == 1
    assert client.session['current_academic_year'] == '2023-2024'
    assert client.session['is_student'] is False
    assert client.session['is_teacher'] is True


def test_teacher_lessons_view_not_logged(client):
    url = reverse('teacher:lessons')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL + '?next=' + reverse('teacher:lessons')


def test_teacher_lessons_view(sample_database, teacher_log_in):
    url1 = reverse('student:home')
    url2 = reverse('teacher:exams')
    client = teacher_log_in
    response = client.get(url1)
    response = client.get(url2)
    assert response.status_code == 200
    content = response.content.decode('UTF-8')
    assert 'Teacher First' in content
    assert content.count('Science') == 1  # item2 should appear
    assert content.count('John Doe') == 1 # student1 is accessed to exam
    assert client.session['current_academic_year'] == '2023-2024'
    assert client.session['is_student'] is False
    assert client.session['is_teacher'] is True

def test_teacher_exams_view_not_logged(client):
    url = reverse('teacher:exams')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL + '?next=' + reverse('teacher:exams')