
import httplib2
import os
from datetime import datetime
from rfc3339 import rfc3339

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import helpers

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

ROOT_UID  = 0

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Daily Schedule Planner'
service = None
today_events = []


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def find_overlapping_event(event_times):
    global today_events
    new_time = {
        "start": event_times[0],
        "end": event_times[1],
    }

    for event in today_events:
        # Each event time is a string in the format (example) '2018-04-10T17:00:00+03:00'
        # We just need the time. Extract it
        if not event.get("start") or not event.get("end"):
            continue
        
        e_start = event["start"]["dateTime"].split("+")[0].split("T")[1].split(":")
        e_end = event["end"]["dateTime"].split("+")[0].split("T")[1].split(":")

        e_time = {
            "start": helpers.hour_to_datetime(int(e_start[0]), int(e_start[1])),
            "end": helpers.hour_to_datetime(int(e_end[0]), int(e_end[1])),
        }

        # If e_end is later than start_datetime and e_start is earlier than end_datetime
        # Which means if the events overlap
        if new_time["start"] < e_time["end"] and new_time["end"] > e_time["start"] \
                or e_time["start"] < new_time["start"] < new_time["end"] < e_time["end"]:
            return event

    return None


def add_event(event_times, description):
    global service
    start_datetime, end_datetime = event_times
    result = service.events().insert(calendarId="primary",
                                     body={
                                        "summary": description,
                                        "start": {
                                            "timeZone": "Asia/Jerusalem",
                                            "dateTime": rfc3339(start_datetime)
                                        },
                                        "end": {
                                            "timeZone": "Asia/Jerusalem",
                                            "dateTime": rfc3339(end_datetime)
                                        }
                                     }).execute()


def init():
    global service
    global today_events
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    midnight = datetime.time(0, 0)
    today = datetime.date.today()
    tommorow = today + datetime.timedelta(days=1)
    last_midnight = datetime.datetime.combine(today, midnight)
    this_midnight = datetime.datetime.combine(tommorow, midnight)

    today_events = service.events().list(calendarId="primary",
                                         timeMin=rfc3339(last_midnight),
                                         timeMax=rfc3339(this_midnight)
                                         ).execute()["items"]


def main():
    pass


if os.geteuid() != ROOT_UID:
	exit("You must be root in order to run this.")

init()
if __name__ == "__main__":
	main()
