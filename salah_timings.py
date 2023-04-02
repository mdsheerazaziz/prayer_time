import datetime
import requests
import csv

SALAH_NAME_INDEX_MAPPING = {"fajr": 1, "dhuhr": 3, "asr": 4, "maghrib": 5, "isha": 6}
SHOW_SALAH_TIMES_FOR = ["fajr", "dhuhr", "asr", "maghrib", "isha"]


class SalahTiming:
    # https://docs.google.com/spreadsheet/ccc?key={YOUR_SHEET_ID}&output=csv
    DEFAULT_CSV_LINK = "https://docs.google.com/spreadsheet/ccc?key=1Kd6DN-NDeL0zUUfuH08jwHmQL0PW6SSELM281zIpWaw" \
                       "&output=csv"

    def __init__(self, csv_url=DEFAULT_CSV_LINK):
        self.csv = csv_url

    def download_google_sheet(self):
        response = requests.get(url=self.csv)
        open('google.csv', 'wb').write(response.content)

    @staticmethod
    def get_salah_time_by_date(today_date):
        # Today date in -> today_date = datetime.date.today().strftime("%d/%m/%Y")
        with open('google.csv', mode='r') as file:
            csv_file = csv.reader(file)
            for lines in csv_file:
                if lines[0] == today_date:
                    return lines
        return None

    def get_next_salah(self, current_date=datetime.date.today().strftime("%d/%m/%Y"),
                       current_time=datetime.datetime.now().strftime("%H:%M"), count=0):
        # noinspection PyBroadException
        try:
            self.download_google_sheet()
        except:
            pass
        salah_times = self.get_salah_time_by_date(current_date)
        if not salah_times:
            return None
        filtered_times = []
        for salah_name in SHOW_SALAH_TIMES_FOR:
            filtered_times.append(salah_times[SALAH_NAME_INDEX_MAPPING[salah_name]])
        for filtered_time in filtered_times:
            if current_time < filtered_time:
                return current_date, filtered_time
        if count < 1:
            # Try for next day incase it Isha Prayer
            next_day = (datetime.date.today() + datetime.timedelta(1)).strftime("%d/%m/%Y")
            count += 1
            return self.get_next_salah(next_day, "00:00", count)
        return None
