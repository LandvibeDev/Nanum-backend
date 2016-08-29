from django.contrib import admin
from study.models import *


admin.site.register(Study)
admin.site.register(StudyMember)
admin.site.register(StudyLike)
admin.site.register(Board)
admin.site.register(Calendar)
admin.site.register(CalendarTag)
admin.site.register(Verification)
admin.site.register(VerificationFile)
