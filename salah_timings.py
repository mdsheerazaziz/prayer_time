import datetime
import requests
import csv

SALAH_NAME_INDEX_MAPPING = {"fajr": 1, "dhuhr": 3, "asr": 4, "maghrib": 5, "isha": 6} 
SHOW_SALAH_TIMES_FOR = ["fajr", "dhuhr", "asr", "maghrib", "isha"]

class SalahTiming:
    # https://docs.google.com/spreadsheet/ccc?key={YOUR_SHEET_ID}&output=csv
    DEFAULT_CSV_LINK = "https://docs.google.com/spreadsheet/ccc?key=1Kd6DN-NDeL0zUUfuH08jwHmQL0PW6SSELM281zIpWaw&output=csv"
    def __init__(self, csv_url=DEFAULT_CSV_LINK):
        self.csv = csv_url

    def download_google_sheet(self):
        response = requests.get(url=self.csv)
        open('google.csv', 'wb').write(response.content)

    def get_today_salah_time(self):
        today_date = datetime.date.today().strftime("%d/%m/%Y")
        with open('google.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                if lines[0] == today_date:
                    return lines
        return None
    
    def get_next_salah(self):
        try:
            self.download_google_sheet()
        except:
            pass
        current_time = datetime.datetime.now().strftime("%H:%M")
        salah_times = self.get_today_salah_time()
        if not salah_times:
            return None
        filtered_times = []
        for salah_name in SHOW_SALAH_TIMES_FOR:
            filtered_times.append(salah_times[SALAH_NAME_INDEX_MAPPING[salah_name]])

        for filtered_time in filtered_times:
            if (current_time < filtered_time):
                return filtered_time

        return None