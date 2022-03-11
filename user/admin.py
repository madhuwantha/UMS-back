# import datetime
#
# from django.contrib import admin
#
# # Register your models here.
# from django_q.models import Schedule
# from django_q.tasks import schedule
# import arrow
# from datetime import datetime
#
#
import arrow


#

#
#
# #
# #
# # Schedule.objects.create(func='print_text',
# #                         args='2,-2',
# #                         schedule_type=Schedule.MINUTES,
# #                         minutes='1',
# #                         repeats='24',
# #                         next_run=arrow.utcnow()
# #                         )
# #
# # # schedule('print_text',
# # #          '3',
# # #          schedule_type=Schedule.MINUTES,
# # #          minutes=5,
# # #          repeats=24,
# # #          next_run=arrow.utcnow().replace(hour=23, minute=12))
#
#
# from django_q.models import Schedule
#
# Schedule.objects.create(
#     func='UMS.user.admin.print_text',  # module and func to run
#     args='2,-2',
#     minutes=1,  # run every 5 minutes
#     repeats=-1,  # keep repeating, repeat forevers
#     next_run=str(arrow.utcnow())
# )
