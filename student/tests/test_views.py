from django.urls import reverse
from django.conf import settings


def test_home_view_logged_student(sample_database, student_log_in):
    url = '/'
    client = student_log_in
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('student:items_view')


def test_home_view_logged_techer(sample_database, teacher_log_in):
    url = '/'
    client = teacher_log_in
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('teacher:home')
    assert client.session['current_academic_year'] == '2023-2024'


def test_home_view_not_logged(client, db):
    url = '/'
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL


def test_item_view(sample_database, student_log_in):
    url1 = reverse('student:home')
    url2 = reverse('student:items_view')
    client = student_log_in
    response = client.get(url1)
    response = client.get(url2)
    assert response.status_code == 200
    assert '<p>John Doe</p>' in response.content.decode('UTF-8')
    assert 'Science' in response.content.decode('UTF-8')
    assert client.session['current_academic_year'] == '2023-2024'
    assert client.session['is_student'] is True
    assert client.session['is_teacher'] is False


def test_item_view_not_logged(client, db):
    url = reverse('student:items_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL + '?next=' + url


def test_reunions_view(sample_database, student_log_in):
    url1 = reverse('student:home')
    url2 = reverse('student:reunions_view')
    client = student_log_in
    response = client.get(url1)
    response = client.get(url2)
    assert response.status_code == 200
    assert '<p>John Doe</p>' in response.content.decode('UTF-8')
    assert '<h2>Reunions for your level in this academic year:</h2>' in response.content.decode('UTF-8')
    assert 'No reunions found' in response.content.decode('UTF-8')
    assert client.session['current_academic_year'] == '2023-2024'
    assert client.session['is_student'] is True
    assert client.session['is_teacher'] is False


def test_reunions_view_not_logged(client, db):
    url = reverse('student:reunions_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL + '?next=' + url


def test_reunion_detail_view(sample_database, student_log_in):
    url1 = reverse('student:home')
    url2 = reverse('student:reunion-detail', args=[1])
    client = student_log_in
    response = client.get(url1)
    response = client.get(url2)
    assert response.status_code == 200
    assert '<p>John Doe</p>' in response.content.decode('UTF-8')
    assert 'Lessons' in response.content.decode('UTF-8')
    assert 'Math' in response.content.decode('UTF-8')
    assert client.session['current_academic_year'] == '2023-2024'
    assert client.session['is_student'] is True
    assert client.session['is_teacher'] is False


def test_reunion_detail_view_not_logged(client, db):
    url = reverse('student:reunion-detail', args=[1])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL + '?next=' + url
