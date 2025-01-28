import os
import tempfile
from datetime import datetime

from .garmin.client import GarminClient
from .coros.client import CorosClient

SYNC_CONFIG = {
    'GARMIN_AUTH_DOMAIN': '',
    'GARMIN_EMAIL': '',
    'GARMIN_PASSWORD': '',
    'GARMIN_NEWEST_NUM': 0,
    "COROS_EMAIL": '',
    "COROS_PASSWORD": '',
}

# start time を比較し、同期していないCorosのアクティビティのリストを返します。
# それぞれのアクティビティは昇順でソートされているので、
# coros_activities の先頭から比較して、garmin_activities に含まれているアクティビティを検出した時点で比較を終了します。
def unsynced_coros_activities(garmin_activities, coros_activities):
    unsynced_activities = []
    garmin_activity = garmin_activities[0]
    for coros_activity in coros_activities:
        coros_activity_start_time = datetime.fromtimestamp(coros_activity['startTime']).strftime('%Y-%m-%d %H:%M:%S')
        if garmin_activity['startTimeGMT'] == coros_activity_start_time:
            break
        else:
            unsynced_activities.append(coros_activity)
    return unsynced_activities

def upload_coros_activity_to_garmin(garmin_client, coros_client, coros_activity):
    name = coros_activity['name']
    id = coros_activity['labelId']
    sport_type = coros_activity['sportType']
    print(f"--> Download: {id}: {name} ({sport_type})")
    
    # テンポラリファイルを作成
    with tempfile.NamedTemporaryFile(delete=False, suffix='.fit') as temp_file:
        file =  coros_client.downloadActivitie(id, sport_type)
        temp_file.write(file.data)
        temp_file.flush()
        temp_file_path = temp_file.name
        upload_status =garmin_client.upload_activity(temp_file_path)
        print(f"{id}.fit upload status {upload_status}")

def main():
    for k in SYNC_CONFIG:
        if os.getenv(k):
            v = os.getenv(k)
            SYNC_CONFIG[k] = v
    
    garmin_client = GarminClient(SYNC_CONFIG['GARMIN_EMAIL'], SYNC_CONFIG['GARMIN_PASSWORD'], SYNC_CONFIG['GARMIN_AUTH_DOMAIN'], SYNC_CONFIG['GARMIN_NEWEST_NUM'])
    coros_client = CorosClient(SYNC_CONFIG['COROS_EMAIL'], SYNC_CONFIG['COROS_PASSWORD'])

    garmin_activities = garmin_client.getActivities(0, 10)
    coros_activities = coros_client.getActivities(10, 1)

    print("--> garmin_activities")
    for garmin_activity in garmin_activities:
        print(garmin_activity['startTimeGMT'])

    print("--> coros_activities")
    for coros_activity in coros_activities['data']['dataList']:
        start_time = datetime.fromtimestamp(coros_activity['startTime']).strftime('%Y-%m-%d %H:%M:%S')
        print(start_time)

    print("--> sync activities")
    for coros_activity in unsynced_coros_activities(garmin_activities, coros_activities['data']['dataList']):
        upload_coros_activity_to_garmin(garmin_client, coros_client, coros_activity)

if __name__ == '__main__':
    main()
