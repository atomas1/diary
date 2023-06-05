from django.contrib import admin
from django.contrib.auth.models import User

from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserAdmin(UserAdmin):
    ordering = ['last_name']
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('email',)}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'level',)

    list_filter = ('level',)

    # list_editable = ('subject',)
    # search_fields = ('title', 'overview')
    # prepopulated_fields = {'slug': ('title',)}
    # inlines = (ModuleInline,)
    def user_first_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(AcademicYear)
admin.site.register(Level)
admin.site.register(Item)
admin.site.register(StudentItemYear)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
