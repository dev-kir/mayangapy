from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/prayer-times-esolat', methods=['GET'])
def get_prayer_times_esolat():
    url = "https://www.e-solat.gov.my/portalassets/www2/solat.php?kod=TRG01&lang=BM&url=http:/www.islam.gov.my"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        prayer_times = {}
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 2:
                prayer_name = columns[0].text.strip().lower()
                prayer_time = columns[1].text.strip().replace('pm', '').replace('am', '').rstrip(':')
                if prayer_name.lower() in ['asar', 'zohor', 'maghrib', 'isyak']:
                    parsed_time = datetime.strptime(prayer_time, '%I:%M')
                    parsed_time += timedelta(hours=12)
                    prayer_time = parsed_time.strftime('%H:%M')
                else:
                    prayer_time = datetime.strptime(prayer_time, '%I:%M').strftime('%H:%M')
                prayer_times[prayer_name] = prayer_time

        return jsonify(prayer_times)
    else:
        return jsonify({'error': 'Failed to fetch data from the website'}), 500

@app.route('/prayer-times-waktusolat', methods=['GET'])
def get_prayer_times_waktusolat():
    url = "https://www.waktusolat.my/kuala-terengganu"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        prayer_times = {}
        prayer_boxes = soup.select('.salat-times__box')
        for box in prayer_boxes:
            prayer_name = box.select_one('h4').text.strip().lower()
            prayer_time = box.select_one('span').text.strip()
            formatted_time = f"{prayer_time.lower()}"
            prayer_times[prayer_name] = formatted_time

        return jsonify(prayer_times)
    else:
        return jsonify({'error': 'Failed to fetch data from the website'}), 500

@app.route('/prayer-times-waktusolatxyz', methods=['GET'])
def get_prayer_times_waktusolatxyz():
    url = "https://www.waktusolat.xyz/zon/trg01/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        prayer_times = {}
        time_rows = soup.select('.col-6.p-0')
        for i in range(0, len(time_rows), 2):
            prayer_name = time_rows[i].text.strip().lower()
            prayer_time = time_rows[i + 1].text.strip()
            prayer_times[prayer_name] = f"{prayer_time}"

        return jsonify(prayer_times)
    else:
        return jsonify({'error': 'Failed to fetch data from the website'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
