from django.contrib import admin

from core.models import (
    Budjet, Category, Expense
)


admin.site.register(Budjet)
admin.site.register(Category)
admin.site.register(Expense)
