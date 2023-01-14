from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Cinema),
admin.site.register(Movie),
admin.site.register(Shows),
admin.site.register(Bookings),
# ------------Changed------------
admin.site.register(Club),
admin.site.register(CinemaManagerRegister)
# ------------Changed------------
