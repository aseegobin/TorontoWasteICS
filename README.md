# TorontoSolidWasteICS

Inspired by the out of date https://laurenarcher.github.io/iCalTOWaste/ and https://github.com/nautmichio/TorontoSolidWasteICS. I forked the project to generate Google Calendar events from the [toronto open data website](https://open.toronto.ca/dataset/solid-waste-pickup-schedule/). All data is from there so if its wrong there, its wrong in my calendars too.

# Run with code

1. `virtualenv env`
2. `source env/bin/activate`
3. `pip install -r requirements.txt`
4. `python garbage.py 2022`
  - Generates garbage collection events in an `.ics` file where you can import it to your Google Calendar
  - There will be an `.ics` file for every TOWaste collection day
  - You will need to know which day of the week is your collection day to know which calendar to import
5. Import your applicable schedule `.ics` file to your calendar and you should see a new all-day event every week for the waste collection

# Calendar files

If you don't want to run it by code and generate the files yourself, you can download your appropriate `.ics` file from the year folders directly in the repo.

## Confirmation

Use your address to confirm you have the correct schedule: https://www.toronto.ca/services-payments/recycling-organics-garbage/houses/collection-schedule/

Also using the district lookup you can cross reference for the correct `.ics` file to use: https://www.toronto.ca/services-payments/recycling-organics-garbage/houses/collection-schedule/2022-curbside-collection-maps/
