import datetime
import pytz
import time
import math
import tkinter as tk
from tkinter import ttk
import scalarcore as sc  # 🔗 Scalar harmonic ratio and constants

SECONDS_IN_STANDARD_DAY = 86400
HARMONIC_DAY_SECONDS = SECONDS_IN_STANDARD_DAY * float(sc.HARMONIC_DAY_LENGTH)

# Reference epoch for driftless harmonic time
REFERENCE_EPOCH = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

# Converts UTC time to harmonic time with fixed reference epoch
def get_harmonic_time(timezone_str='UTC'):
    timezone = pytz.timezone(timezone_str)
    now = datetime.datetime.now(pytz.UTC)
    delta_seconds = (now - REFERENCE_EPOCH).total_seconds()
    harmonic_seconds = delta_seconds / float(sc.HARMONIC_DAY_LENGTH)
    harmonic_seconds_today = harmonic_seconds % SECONDS_IN_STANDARD_DAY

    h_hours = int(harmonic_seconds_today // 3600)
    h_minutes = int((harmonic_seconds_today % 3600) // 60)
    h_seconds = int(harmonic_seconds_today % 60)

    # Drift calculation
    local_now = datetime.datetime.now(timezone)
    seconds_since_midnight = (local_now - local_now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    drift = seconds_since_midnight - harmonic_seconds_today

    return h_hours, h_minutes, h_seconds, drift

# GUI setup
def update_clock():
    h, m, s, drift = get_harmonic_time(tz_choice.get())
    harmonic_time_str = f"Harmonic Time: {h:02d}:{m:02d}:{s:02d}"
    drift_str = f"Drift from UTC: {drift:+.2f} sec"

    label.config(text=harmonic_time_str)
    drift_label.config(text=drift_str)
    root.after(1000, update_clock)

root = tk.Tk()
root.title("Harmonic Clock")

frame = ttk.Frame(root, padding=20)
frame.grid()

label = ttk.Label(frame, font=("Helvetica", 28))
label.grid(row=0, column=0, columnspan=2)

drift_label = ttk.Label(frame, font=("Helvetica", 12))
drift_label.grid(row=1, column=0, columnspan=2, pady=5)

tz_label = ttk.Label(frame, text="Timezone:")
tz_label.grid(row=2, column=0, sticky="e")

tz_choice = ttk.Combobox(frame, values=sorted(pytz.all_timezones), width=30)
tz_choice.set("UTC")
tz_choice.grid(row=2, column=1, sticky="w")

update_clock()
root.mainloop()

