from django.contrib import admin

from .models import User, UserInfo, Avatar

admin.site.site_header = "User Administration"
admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(Avatar)