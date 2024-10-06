# Getting ready to collect data

## Prepping an environment

These instructions assume you are using linux and have python3 installed

First create and activate a python virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

Then install requirements from requirements file (BeautifulSoup and requests)

```
python -m pip install -r requirements.txt
```

## Getting the exam date data

TODO: currently just manually make the json file. just put `exam_schedule.json` in the same folder as `main.py`

## Getting ready to query the SoC

The main file needs an active session token to talk to the schedule of classes website.
It is easy to obtain this token.

These steps have been written assuming you are using the google chrome browser, they may vary if you are using another browser.

1. Open [https://navigator.cnu.edu/StudentScheduleofClasses/](https://navigator.cnu.edu/StudentScheduleofClasses/) in chrome

2. Open up chrome dev tools (CTRL+SHIFT+I, right click and open dev tools, etc.)

3. Switch to the "Network" tab at the top

4. Scroll to the bottom of the schedule of classes website and click "Search"

5. Once the page loads, look in the chrome dev tools window for the entry labeled "StudentScheduleofClasses/" or "socresults.aspx" and click on one (either will work, it doesn't matter which one you pick)

6. Scroll down to the "Request Headers" section and find where it says "Cookie:"

7. In that line, find where it says `ASP.NET_SessionId=XXXXXXXXXXXXXXXXXXXXXXXX`. The Xs are placeholders for the session token in this example

8. Copy that session token (just the Xs part)

9. Open main.py in some text editor (all we are doing is pasting in that session token, so we don't need anything fancy)

10. Find the line near the top that starts `cookie={'ASP.NET_SessionId': 'XXXXXXXXXXXXXXXXXXXXXXXX'}`

11. Replace the Xs with your session token

INFO: Session tokens are valid for 20 minutes, only change after a longer time (this time is not currently known). After 20 minutes you should just need to click "Search" on the SoC website to make you session token valid again.

## Running the program

Now that everything is prepped, all you need to do is run the file `main.py`

```
python3 main.py
```

And it should pop out a JSON file with all the info
