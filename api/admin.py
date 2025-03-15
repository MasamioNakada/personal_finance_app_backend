from django.contrib import admin
from .models import Budget, Category, Tag, Transaction, FinancialGoal, ChangeLog, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(FinancialGoal)
admin.site.register(ChangeLog)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('phone_number',) 

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def phone_number(self, obj):
        return obj.userprofile.phone_number if hasattr(obj, 'userprofile') else ""

    phone_number.short_description = "Phone Number"
    
    # Agregarlo en la lista de usuarios para verlo en el listado
    list_display = UserAdmin.list_display + ("phone_number",)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)