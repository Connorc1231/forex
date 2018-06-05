from crontab import CronTab

cron = CronTab(user='Connor_Chen')

job = cron.new(command='/usr/bin/python Documents/forex/write.py', comment="write")

job.minute.every(1)

cron.write()
