from django.urls import reverse


def test_change_password_view_get(sample_database, student_log_in):
    client = student_log_in
    url = reverse('users:change_password')
    response = client.get(url)
    assert 'Change Password for user1@example.com' in response.content.decode('UTF-8')


def test_change_academic_year_get(sample_database, student_log_in):
    client = student_log_in
    url = reverse('users:change_academic_year')
    response = client.get(url)
    assert 'Change current academic year' in response.content.decode('UTF-8')


def test_change_academic_year_post(sample_database, student_log_in):
    client = student_log_in
    url = reverse('users:change_academic_year')
    data = {
        "current_academic_year": '1'
    }
    response = client.post(url, data=data)
    assert client.session['current_academic_year'] == '2022-2023'
    assert response.status_code == 302


def test_change_password_view_post(sample_database, student_log_in):
    client = student_log_in
    url = reverse('users:change_password')
    response = client.post(url, {
        'old_password': 'password1',
        'new_password1': 'newtestpass123',
        'new_password2': 'newtestpass123'
    })
    assert response.status_code == 302

    # Wylogowanie użytkownika i zalogowanie z nowym hasłem
    client.logout()
    response = client.login(email='user1@example.com', password='newtestpass123')
    assert response is True
