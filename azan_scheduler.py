from azan_player import AzanPlayer
from salah_timings import SalahTiming
from apscheduler.schedulers.background import BackgroundScheduler
import datetime


class AzanScheduler:
    def __init__(self):
        self.salah_timings = SalahTiming()
        self.azan_player = AzanPlayer()

        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()
        self.schedule_next_job()

    def schedule_next_job(self):
        date, time = self.salah_timings.get_next_salah()
        if not time or not date:
            raise Exception("Time/Date not present")
        time = time.split(":")
        date = date.split("/")
        current_date = datetime.datetime.now()
        current_date = current_date.replace(day=int(date[0]), month=int(date[1]), year=int(date[2]),
                                            hour=int(time[0]), minute=int(time[1]), second=0, microsecond=0)
        self.scheduler.add_job(self.play_azan, 'date', run_date=current_date)

    def get_scheduled_job_list(self):
        return str(self.scheduler.get_jobs()[0].trigger)

    def play_azan(self):
        print("Azan Started")
        self.azan_player.play()
        print("Azan Ended")
        self.schedule_next_job()
