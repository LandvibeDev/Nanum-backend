from django.contrib import admin
from study.models import *


admin.site.register(Study)
admin.site.register(StudyMember)
admin.site.register(StudyLike)
admin.site.register(StudyNotice)
admin.site.register(Calender)
admin.site.register(CalenderCategory)
admin.site.register(HomeWork)
admin.site.register(HomeWorkComment)
admin.site.register(HomeWorkCommentFile)
admin.site.register(HomeWorkFile)
admin.site.register(HomeWorkReComment)
admin.site.register(Reference)
admin.site.register(ReferenceComment)
admin.site.register(ReferenceFile)
admin.site.register(Question)
admin.site.register(QuestionComment)
admin.site.register(QuestionFile)