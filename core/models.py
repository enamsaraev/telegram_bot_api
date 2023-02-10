from django.db import models


class Budjet(models.Model):
    """Money budjet model"""

    name = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Expense category model"""

    codename = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255)
    aliases = models.TextField()

    def __str__(self) -> str:
        return self.codename


class Expense(models.Model):
    """Base expense model"""

    category = models.ForeignKey(
        'Category',
        verbose_name='expenses',
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    expense_text = models.TextField()

    def __str__(self) -> str:
        return str(self.id)
