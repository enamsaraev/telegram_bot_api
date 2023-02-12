from django.urls import path, include

from telegram_message_api.views import BaseExpense, BaseCategory, BaseUser


app_name = 'telegram_message_api'


urlpatterns = [
    path('get_categories/', BaseCategory.as_view(), name='get_categories'),
    path('add_category/', BaseCategory.as_view(), name='add_category'),
    path('add_expense/', BaseExpense.as_view(), name='add_expense'),
    path('registration/', BaseUser.as_view(), name='user_registration'),
]