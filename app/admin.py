from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User, ForgetPasswordVarify,Booking,UserMessage,PaymentDetail,Room
# Register your models here.


class MyUserAdmin(UserAdmin):
    fieldsets = (
        ('Personal Info',{'fields':('first_name','last_name','phone','email','password','gender')}),
        ('Permission',{'fields':('is_active','is_staff','is_superuser')}),
        ('Important Dates',{'fields':('last_login','date_joined')}),
    )

    add_fieldsets = (
        (None,{'classes':('wide',),'fields':('first_name','last_name','phone','email','password1','password2','gender')}),
    )

    list_display = ('email','first_name','last_name')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(User,MyUserAdmin)
admin.site.register(ForgetPasswordVarify)
admin.site.register(Booking)
admin.site.register(UserMessage)
admin.site.register(PaymentDetail)
admin.site.register(Room)