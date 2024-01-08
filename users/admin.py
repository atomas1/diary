from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def change_password_link(self, obj):
        change_password_url = reverse('admin:auth_user_password_change', args=[obj.id])
        return format_html(f'<a href="{change_password_url}">Change Password</a>')

    change_password_link.short_description = 'Change Password'

    list_display = ('first_name', 'last_name', 'email', 'change_password_link')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'last_name',)
    ordering = ('last_name',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
