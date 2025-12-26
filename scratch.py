import datetime as dt
from dotenv import load_dotenv
from pathlib import Path

create_time = dt.datetime.now().date()
print(create_time, type(create_time))

today = dt.date.today()
print(today, type(today))


# BASEDIR = Path(__file__).resolve().arent
# envdir = BASEDIR / ".env"
# if envdir.exists():
#     load_dotenv()

# tifa@seventh.heaven >> cloudstrife123
# cloud@shinra.corp >> tifalockhart123
# barret@seventh.heaven >> maryissocute123
# aerith@gains.borough >> zackisfair123