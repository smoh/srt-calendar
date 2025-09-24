"""Generate an iCalendar file for booked trains.


This script contains a placeholder function `fetch_booked_trains()` where you should
plug in your logic to fetch booked train data (API, scraping, file parse, etc.).


It writes `calendar.ics` to the current working directory. When used by the workflow,
it will be moved into the token-named folder for publishing.


Usage:
python src/generate_ics.py --out calendar.ics --token <TOKEN>


"""

from icecream import ic
from ics import Calendar, Event
from datetime import datetime
import argparse
import os
import json
from SRT import SRT


attr_names = [
    "reservation_number",
    "total_cost",
    "seat_count",
    "train_code",
    "train_name",
    "train_number",
    "dep_date",  # in TTTTMMDD format
    "dep_time",  # in HHMMSS format
    "dep_station_code",
    "dep_station_name",
    "arr_time",
    "arr_station_code",
    "arr_station_name",
    "payment_date",
    "payment_time",
    "paid",
]


# Get iso string from dep_date and dep_time
def to_iso(date, time):
    seoul_offset = "+09:00"
    return f"{date[:4]}-{date[4:6]}-{date[6:]}T{time[:2]}:{time[2:4]}:{time[4:]}{seoul_offset}"


def process_reservation(r):
    return dict(
        train_number=r.train_number,
        departure_iso=to_iso(r.dep_date, r.dep_time),
        arrival_iso=to_iso(r.dep_date, r.arr_time),
        from_station=r.dep_station_name,
        to_station=r.arr_station_name,
        seat=", ".join(f"{t.car}-{t.seat}" for t in r._tickets if t.seat),
        booking_ref=r.reservation_number,
    )


def fetch_booked_trains_from_srt(IDEN, PASSWORD, debug=False):
    """Placeholder. Replace this with real fetch logic.

    Return a list of dicts, each with keys:
    - train_number
    - departure_iso (ISO 8601 local or with TZ)
    - arrival_iso
    - from_station
    - to_station
    - seat (optional)
    - booking_ref (optional)
    """
    if debug:
        ic("Debug mode: using static data")
        with open(os.path.join(os.path.dirname(__file__), "sample_trains.json")) as f:
            reservations = json.load(f)
        return [process_reservation(r) for r in reservations]

    ic("Fetching booked trains from SRT")
    srt = SRT(IDEN, PASSWORD)
    reservations = srt.get_reservations()
    ic(reservations)
    if not reservations:
        ic("No reservations found.")
        return []

    return [process_reservation(r) for r in reservations]


def create_calendar(trips):
    c = Calendar()
    for t in trips:
        e = Event()
        title = f"SRT {t.get('train_number','').strip('0 ')} {t.get('from_station','')}→{t.get('to_station','')}: {t.get('seat', '?')}"
        e.name = title
        # Parse ISO datetimes robustly
        e.begin = t["departure_iso"]
        e.end = t["arrival_iso"]
        desc_lines = []
        if t.get("seat"):
            desc_lines.append(f"Seat: {t['seat']}")
        if t.get("booking_ref"):
            desc_lines.append(f"Booking ref: {t['booking_ref']}")
        e.description = "\n".join(desc_lines)
        # Add unique UID so Google updates correctly
        if t.get("booking_ref"):
            e.uid = f"{t['booking_ref']}@train-calendar"
        c.events.add(e)
    return c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=str,
        default="calendar.ics",
        help="Output .ics file path",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Token (not used in file but workflow moves file into token folder)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    IDEN = os.getenv("SRT_IDEN")
    PASSWORD = os.getenv("SRT_PASSWORD")
    if not IDEN or not PASSWORD:
        raise ValueError("SRT_IDEN and SRT_PASSWORD environment variables must be set.")

    trips = []
    trips = fetch_booked_trains_from_srt(IDEN, PASSWORD, debug=args.debug)

    cal = create_calendar(trips)
    with open(args.out, "w", encoding="utf-8") as f:
        f.writelines(cal)
    print(f"Wrote {args.out} with {len(cal.events)} events.")


if __name__ == "__main__":
    main()
