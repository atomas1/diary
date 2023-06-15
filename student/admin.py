from django.contrib import admin

from .models import Student, AcademicYear, Level, Item, StudentItemYear


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
