from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page

# Register your models here.
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    #list_display = ('title', 'order')
    

admin.site.register(Page, PageAdmin)
