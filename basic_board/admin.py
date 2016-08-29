from django.contrib import admin
from basic_board.models import *

admin.site.register(BasicBoard)
admin.site.register(BasicBoardComment)
admin.site.register(BasicBoardFile)