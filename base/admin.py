from django.contrib import admin



from .models import * 


admin.site.register(CustomUser)

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'job_title']
    list_filter = ['profile_visibility', 'theme_preference']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']