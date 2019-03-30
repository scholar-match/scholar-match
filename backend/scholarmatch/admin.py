from django.contrib import admin
from .models import ScholarMatch 

class ScholarMatchAdmin(admin.ModelAdmin):  
  list_display = ('title', 'description', 'completed')
# Register your models here.
admin.site.register(ScholarMatch, ScholarMatchAdmin)
