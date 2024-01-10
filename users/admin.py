from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'email_confirm_key',)
    list_filter = ()
    search_fields = ('email', 'phone',)
