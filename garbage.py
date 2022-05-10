import urllib.request
import json
import sys
from datetime import datetime, timedelta
from ics import Calendar, Event, DisplayAlarm
# Get the dataset metadata by passing package_id to the package_search endpoint
# For example, to retrieve the metadata for this dataset:

def proc_sched(sched):
        cal={}
        for record in sched:
                #Sometimes there are spaces in the Key Names
                item = {k.replace(' ', ''): v for k, v in record.items()}
                #Sometimes there are spaces in the calendar types
                cal_type = item["Calendar"].replace(" ","")
                if cal_type not in cal:
                        cal[cal_type]={}
                if "WeekStarting" in item.keys():
                        cal[cal_type].update({item["WeekStarting"] :gen_pickup(item)})
                else:
                        cal[cal_type].update({item["Week Starting"] :gen_pickup(item)})        
        return cal

def get_id_list(year):
        url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
        params = { "id": "7b70189a-aede-42f1-b092-8708fa4f5fc3"}
        response = urllib.request.urlopen(url, data=bytes(json.dumps(params), encoding="utf-8"))
        package = json.loads(response.read())
        idlist = []
        for keys in package['result']['resources']:
                # resource with url_type of `datastore` has the ID for the event data we care about
                if keys["datastore_active"] and keys["url_type"] == "datastore":
                        # the `name` key is something like: pickup-schedule-2022, so find the one that matches the year we care about
                        if year in keys["name"]:
                                idlist.append(keys["id"])
        return idlist

def get_cal(id):
        url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search"
        cal = list()
        total = 1
        offset = 0
        while offset < total:
                p = { "id": id,"offset": offset }
                r = urllib.request.urlopen(url, data=bytes(json.dumps(p), encoding="utf-8"))
                data = json.loads(r.read())
                if data["success"]:
                        total = data["result"]["total"]
                        for record in data["result"]["records"]:
                                cal.append(record)
                        #default ckan limit is 100
                        offset+=100
                else: 
                        break
        return cal

def create_ics(cal):
        for cal_type in cal:
                c = Calendar()
                for date in cal[cal_type]:
                        e = Event()
                        date_obj = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
                        e.begin = date_obj
                        e.name = "TOWaste - " + cal[cal_type][date]
                        e.description = "Pickup for: " + cal[cal_type][date]
                        e.transparent = True
                        e.make_all_day()

                        # trigger alert at 9pm the night before
                        # NOTE: doesn't always work with Google Calendar: https://stackoverflow.com/a/35876769
                        alarm = DisplayAlarm()
                        alarm.trigger = timedelta(hours=-int(3))

                        e.alarms = [alarm]
                        c.events.add(e)
                filename=cal_type+"_"+date_obj.strftime("%Y")+".ics"   
                print("Creating ICS for", cal_type, "Filename:", filename)
                with open(filename,'w') as f:
                        f.write(str(c))

def gen_pickup(list_val):
        list_pickup = list()
        if list_val["GreenBin"] != '0':
                list_pickup.append("Green Bin")
        if list_val["Garbage"] != '0':
                list_pickup.append("Garbage")        
        if list_val["Recycling"] != '0':
                list_pickup.append("Recycling")
        if list_val["YardWaste"] != '0':
                list_pickup.append("Yard Waste")
        if list_val["ChristmasTree"] != '0':
                list_pickup.append("Christmas Tree")
        str_list = ', '.join(list_pickup)
        return str_list

def main():
        if len(sys.argv) < 2:
                print('must provide year: `python garbage.py YEAR`')
                return
        year = sys.argv[1]
        print('Generating for year:', year)
        cal = list()
        for id in get_id_list(year):
                cal = get_cal(id)
                sorted_cal = proc_sched(cal)
                create_ics(sorted_cal)
main()
