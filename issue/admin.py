from django.contrib import admin
from issue.models import *
# Register your models here.

admin.site.register(Issue)
admin.site.register(IssueComment)
admin.site.register(IssueFile)
admin.site.register(IssueLike)
admin.site.register(IssueTag)