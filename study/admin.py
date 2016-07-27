from django.contrib import admin
from study.models import *


admin.site.register(Study)
admin.site.register(Member)
admin.site.register(Like)
admin.site.register(Notice)
admin.site.register(Calender)
admin.site.register(CalenderCategory)
admin.site.register(Reference)
admin.site.register(ReferenceComment)
admin.site.register(ReferenceFile)
admin.site.register(Question)
admin.site.register(QuestionComment)
admin.site.register(QuestionFile)