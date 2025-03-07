from django.contrib import admin
from .models import Budget, Category, Tag, Transaction, FinancialGoal, ChangeLog

# @admin.register(Budget)
# class BudgetAdmin(admin.ModelAdmin):
#     list_display = ('user', 'month', 'total_budget')
#     search_fields = ('name',)

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(FinancialGoal)
admin.site.register(ChangeLog)