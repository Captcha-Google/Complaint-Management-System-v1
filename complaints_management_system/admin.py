from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as OrigAdminUser

admin.site.site_header = 'COMPLAINT MANAGEMENT SYSTEM | CONTROL PANEL'
admin.site.site_title = 'AKSYON KAAGAPAY KABARANGAY: COMPLAINT MANAGEMENT SYSTEM'

class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_type','date_added')

class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('case_no','complainant','respondent','complaint_status','complaint_type','hearing_schedule','date_complaint')
    list_filter = ['date_complaint','complaint_status','complaint_type']

class UserAdmin(OrigAdminUser):
    fieldsets = (
        *OrigAdminUser.fieldsets,
        (
            'Entity & Position',
            {
                'fields': (
                    'entity',
                    'position',
                ),
            }
        ),
    )
    list_display = ('username','first_name','last_name','entity','email','is_active')
    list_filter  = ['is_active','entity']

admin.site.register(Position,PositionAdmin)
admin.site.register(Complainant)
admin.site.register(Complaints,ComplaintsAdmin)
admin.site.register(Entities)
admin.site.register(Respondents)
admin.site.register(Purok)
admin.site.register(User,UserAdmin)
