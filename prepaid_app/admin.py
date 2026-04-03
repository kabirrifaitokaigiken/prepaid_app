from django.contrib import admin
from .models import Prepaid, TopUp, History

admin.site.register(Prepaid)
admin.site.register(TopUp)
admin.site.register(History)