from django.contrib import admin
from .models import Note, Category

admin.site.register(Note)
admin.site.register(Category)


class NotesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
