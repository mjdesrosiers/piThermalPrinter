import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# from printer_server import send_message_to_server

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_upcoming_info(days=30):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + "Z"
        print("Getting the upcoming 10 events")
        calendars = service.calendarList().list().execute().get("items", [])
        events_total = []
        if calendars:
            for calendar in calendars:
                events_result = (
                    service.events()
                    .list(
                        calendarId=calendar['id'],
                        timeMin=now,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])
                events_total.extend(events)

        if not events_total:
            print("No upcoming events found.")
            return

        def get_date(item):
            return item["start"].get("dateTime", item["start"].get("date"))

        events_total.sort(key=get_date)

        starts_and_summaries = []
        # Prints the start and name of the next 10 events
        for event in events:
            start = get_date(event)
            print(start, event["summary"])
            starts_and_summaries.append((start, event["summary"]))
        return starts_and_summaries

    except HttpError as error:
        print(f"An error occurred: {error}")

def format_upcoming_info(info):
    days = [item[0][0:11] for item in info]
    message = ""
    for day in days:
        message += day + '\n'
        all_days = []
        specific = []
        for (time, summary) in info:
            if day in time:
                if "T" not in time:
                    all_days.append(summary)
                else:
                    specific.append((time.split("T")[1], summary))
        for item in all_days:
            message += "  " + item + "\n"
        for (time, item) in specific:
            message += "  " + time + " : " + item + "\n"
    return message


if __name__ == "__main__":
    info = get_upcoming_info()
    message = format_upcoming_info(info)
    # send_message_to_server(message)
