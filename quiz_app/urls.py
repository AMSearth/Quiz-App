from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-user/', views.create_user, name='create_user'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Teacher URLs
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('add-question/<int:quiz_id>/', views.add_question, name='add_question'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('publish-quiz/<int:quiz_id>/', views.publish_quiz, name='publish_quiz'),
    path('student-results/', views.student_results, name='student_results'),
    path('view-student-result/<int:attempt_id>/', views.view_student_result, name='view_student_result'),
    
    # Student URLs
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('start-quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('take-quiz/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    path('quiz-result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('submit-quiz/<int:attempt_id>/', views.submit_quiz, name='submit_quiz'),
    path('check-time/<int:attempt_id>/', views.check_time, name='check_time'),
] 