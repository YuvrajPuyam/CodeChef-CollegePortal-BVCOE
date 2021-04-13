from django.contrib import admin

from .models import Contest, rank
from .models import Problem
from .models import Invitation
from .models import CodeChefCookOff
from .models import Submission
from .models import CustomSet
from .models import rank
from .models import pastcontest, pastrank

admin.register(Contest)(admin.ModelAdmin)
admin.register(Problem)(admin.ModelAdmin)
admin.register(Invitation)(admin.ModelAdmin)
admin.register(CodeChefCookOff)(admin.ModelAdmin)
admin.register(Submission)(admin.ModelAdmin)
admin.register(CustomSet)(admin.ModelAdmin)
admin.register(rank)(admin.ModelAdmin)
admin.register(pastrank)(admin.ModelAdmin)
admin.register(pastcontest)(admin.ModelAdmin)