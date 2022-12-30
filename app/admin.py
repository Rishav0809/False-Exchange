from django.contrib import admin
from .models import Order
# Register your models here.


class CreatedAt(admin.ModelAdmin):
    readonly_fields=('created',)

admin.site.register(Order,CreatedAt)
