from _decimal import Decimal

import pytest
from django.utils import timezone
from random import randint
from datetime import timedelta

from student.models import AcademicYear, Level, Item, Student, StudentItemYear
from teacher.models import Teacher, TeacherItemYear, Rating, Localization, Lesson, Reunion, Exam, StudentExam


@pytest.fixture
def sample_database(db, django_user_model):
    # Create users
    User = django_user_model

    user1 = User.objects.create_user(email='user1@example.com', password='password1', first_name='John',
                                     last_name='Doe')
    user2 = User.objects.create_user(email='user2@example.com', password='password2', first_name='Jane',
                                     last_name='Smith')
    user3 = User.objects.create_user(email='user3@example.com', password='password3', first_name='Alice',
                                     last_name='Johnson')

    user4 = User.objects.create_user(email='user4@example.com', password='password4', first_name='Teacher',
                                     last_name='First')
    user5 = User.objects.create_user(email='user5@example.com', password='password5', first_name='Teacher',
                                     last_name='Second')
    user6 = User.objects.create_user(email='user6@example.com', password='password6', first_name='Teacher',
                                     last_name='Third')

    # Create academic years
    academic_year1 = AcademicYear.objects.create(name='2022-2023', started_at=timezone.now(),
                                                 finished_at=timezone.now() + timedelta(days=365))
    academic_year2 = AcademicYear.objects.create(name='2023-2024', started_at=timezone.now() + timedelta(days=365),
                                                 finished_at=timezone.now() + timedelta(days=730))

    # Create levels
    level1 = Level.objects.create(level_number=1)
    level2 = Level.objects.create(level_number=2)

    # Create items
    item1 = Item.objects.create(name='Math')
    item2 = Item.objects.create(name='Science')

    # Create students
    student1 = Student.objects.create(user=user1, phone='1234567890',
                                      birth_date=timezone.now(), confession=Student.Confession.NOT_DEFINED,
                                      education=Student.Education.HIGHER, address='123 Street, City',
                                      workplace='ABC Company', comments='Lorem ipsum dolor sit amet', level=level1,
                                      index='1')

    student2 = Student.objects.create(user=user2, phone='9876543210',
                                      birth_date=timezone.now(), confession=Student.Confession.ORTHODOX,
                                      education=Student.Education.SECONDARY, address='456 Street, City',
                                      workplace='XYZ Company', comments='Lorem ipsum dolor sit amet', level=level2,
                                      index='2')
    student3 = Student.objects.create(user=user3, phone='5555555555',
                                      birth_date=timezone.now(), confession=Student.Confession.GREEK_CATHOLIC,
                                      education=Student.Education.VOCATIONAL, address='789 Street, City',
                                      workplace='PQR Company', comments='Lorem ipsum dolor sit amet', level=level1,
                                      index='3')

    student1.academic_years.add(academic_year1, academic_year2)
    student2.academic_years.add(academic_year2)
    student3.academic_years.add(academic_year1)

    # Create student-item-year relationships
    StudentItemYear.objects.create(student=student1, item=item1, academic_year=academic_year1)
    StudentItemYear.objects.create(student=student1, item=item2, academic_year=academic_year2)

    # Create teachers
    teacher1 = Teacher.objects.create(user=user4, phone='1234567890', degree=Teacher.Degree.MASTER)
    teacher2 = Teacher.objects.create(user=user5, phone='9876543210', degree=Teacher.Degree.DOCTOR)
    teacher3 = Teacher.objects.create(user=user6, phone='5555555555', degree=Teacher.Degree.PROFESSOR)

    # Create teacher-item-year relationships
    TeacherItemYear.objects.create(teacher=teacher1, item=item1, academic_year=academic_year1)
    TeacherItemYear.objects.create(teacher=teacher2, item=item2, academic_year=academic_year2)
    TeacherItemYear.objects.create(teacher=teacher1, item=item2, academic_year=academic_year2)

    # Create ratings
    ratings = []
    for i in range(10):
        student = Student.objects.order_by('?').first()
        teacher = Teacher.objects.order_by('?').first()
        item = Item.objects.order_by('?').first()
        date = timezone.now() + timedelta(days=i)
        value = randint(1, 5)
        notice = f"Rating {i + 1}"
        rating = Rating.objects.create(student=student, teacher=teacher, item=item, date=date, value=value,
                                       notice=notice)
        ratings.append(rating)

    # Create lessons
    # Create localizations
    localization1 = Localization.objects.create(name='Classroom 1', address='123 Classroom Street, City')
    localization2 = Localization.objects.create(name='Classroom 2', address='456 Classroom Street, City')
    # Create reunions
    reunion1 = Reunion.objects.create(academic_year=academic_year1, level=level1, start_at=timezone.now(),
                                      finish_at=timezone.now() + timedelta(days=30))
    reunion2 = Reunion.objects.create(academic_year=academic_year2, level=level2,
                                      start_at=timezone.now() + timedelta(days=365),
                                      finish_at=timezone.now() + timedelta(days=395))
    lesson1 = Lesson.objects.create(localization=localization1, item=item1, level=level1, reunion=reunion1,
                                    topic='Introduction to Math', date_time=timezone.now(), teacher=teacher1)
    lesson2 = Lesson.objects.create(localization=localization2, item=item2, level=level2, reunion=reunion2,
                                    topic='Introduction to Science', date_time=timezone.now(), teacher=teacher1)

    # Add students to lessons
    lesson1.present_students.add(student1, student2)
    lesson2.present_students.add(student2, student3)

    # Create exams
    exam1 = Exam.objects.create(academic_year=academic_year1, localization=localization1, item=item1,
                                date_time=timezone.now())
    exam2 = Exam.objects.create(academic_year=academic_year2, localization=localization2, item=item2,
                                date_time=timezone.now() + timedelta(days=365))

    # Add students to exams
    student_exam1 = StudentExam.objects.create(student=student1, exam=exam1, rating=Decimal('4.5'), is_passed=True)
    student_exam2 = StudentExam.objects.create(student=student2, exam=exam1, rating=Decimal('3.7'), is_passed=False)
    student_exam3 = StudentExam.objects.create(student=student1, exam=exam2, rating=Decimal('4.2'), is_passed=True)
    student_exam4 = StudentExam.objects.create(student=student3, exam=exam2, rating=Decimal('3.9'), is_passed=True)
    return True


@pytest.fixture
def student_log_in(sample_database, client):
    if sample_database:
        client.login(email='user1@example.com', password='password1')
    return client


@pytest.fixture
def teacher_log_in(sample_database, client):
    if sample_database:
        client.login(email='user4@example.com', password='password4')
    return client
