import datetime
from azan_player import AzanPlayer
from salah_timings import SalahTiming


from apscheduler.schedulers.background import BackgroundScheduler
import datetime

class AzanScheduler:
    def __init__(self) -> object:
        self.salah_timings = SalahTiming()
        self.azan_player = AzanPlayer()
        
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()
        self.schedule_next_job()
    
    def schedule_next_job(self):
        time = self.salah_timings.get_next_salah()
        if not time:
            raise Exception("Time not present")
        time = time.split(":")
        current_date = datetime.datetime.now()
        current_date = current_date.replace(hour=int(time[0]), minute=int(time[1]), second=0, microsecond=0)
        self.scheduler.add_job(self.play_azan,'date',run_date = current_date)
    
    def get_scheduled_job_list(self):
        return str(self.scheduler.get_jobs()[0].trigger)
    
    def play_azan(self):
        print ("Azaan Started")
        self.azan_player.play()
        print ("Azaan Ended")
        self.schedule_next_job()

