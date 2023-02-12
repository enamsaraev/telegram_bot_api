from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from telegram_message_api.managers import (
    ExpenseManager, CategoryManager
)
from django.contrib.auth import get_user_model


class BaseUser(APIView):

    def post(self, request, *args, **kwargs):
        """User authentication"""

        user_email = request.data['user_email']
        user_password = request.data['user_password']
        user_chat_id = request.data['user_chat_id']

        user = get_user_model().objects.filter(
            email=user_email, 
            password=user_password,
            chat_id=user_chat_id,
        ).exists()

        if user:
            return Response(status=status.HTTP_200_OK)
        
        else:
            get_user_model().objects.create_user(
                email=user_email, 
                password=user_password,
                chat_id=user_chat_id,
            )
            return Response(status=status.HTTP_200_OK)


class BaseCategory(APIView):

    def get(self, request, *args, **kwargs):
        """Return all categories from db"""

        data = CategoryManager(
            chat_id=request.data['user_chat_id'],
        ).get_current_categories()

        return Response({'msg': [data]}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Add an category to the db"""

        user_chat_id = request.data['user_chat_id']
        messege_category = request.data['category']
        messege_aliases = request.data['category_aliases']
        
        CategoryManager(chat_id=user_chat_id).add_data(
            codename=messege_category,
            aliases=messege_aliases
        )

        return Response({'msg': 'Категория сохранена'}, status=status.HTTP_200_OK)


class BaseExpense(APIView):

    def post(self, request, *args, **kwargs):
        """Add an expense to the db"""

        user_chat_id = request.data['user_chat_id']
        messege_text = request.data['msg_text']

        ExpenseManager(
            chat_id=user_chat_id
        ).add_data(text=messege_text)

        return Response({'msg': 'Запись сохранена'}, status=status.HTTP_200_OK)
        
