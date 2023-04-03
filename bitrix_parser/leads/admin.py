from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email',
                    'password',
                    'uuid',
                    'period_activation',
                    'activation_status_verbose',)
    list_filter = ('status_activation',)


admin.site.register(User, UserAdmin)
