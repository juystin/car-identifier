import xml.etree.ElementTree as ET
from datetime import datetime
import pytz
import math

FRAMES_PER_SECOND = 15

def get_start_time(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    start_time = root.find('StartTime')

    return convert_utc_to_est(convert_to_sql_readable_time(start_time.text))

def convert_to_sql_readable_time(time):
    time_values = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_time = time_values.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_time

def convert_utc_to_est(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")
    utc_time = pytz.utc.localize(utc_time)
    est_time = utc_time.astimezone(pytz.timezone('US/Eastern'))
    formatted_time = est_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_time

def add_frame_offset_to_time(time, frame_offset):
    time = time.split(' ')
    date = time[0]
    time = time[1].split(':')
    seconds = int(time[2]) + math.floor(frame_offset / FRAMES_PER_SECOND)
    minutes = int(time[1])
    hours = int(time[0])

    while seconds >= 60:
        minutes += 1
        seconds -= 60

    while minutes >= 60:
        hours += 1
        minutes -= 60

    if hours >= 24:
        hours = hours % 24

    return f"{date} {hours:02}:{minutes:02}:{seconds:02}"