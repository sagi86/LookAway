
## 📂 File Guide

These BAT files make it easy to run or control the reminder without typing Python commands:

| File name | Purpose |
|-----------|---------|
| **start_eye_break_reminder.bat** | Starts the reminder in **normal mode** (with sound). Use this if you want the 20-minute reminder with chimes. |
| **start_eye_break_reminder_quiet.bat** | Starts the reminder in **quiet mode** (no sounds). Useful if you’re in a meeting or don’t want audio alerts. |
| **stop_eye_break_reminder.bat** | Stops the reminder completely. Can be used if you want to turn it off before shutting down your PC. |

> 💡 You can place a shortcut to `start_eye_break_reminder.bat` or `start_eye_break_reminder_quiet.bat` in your Windows **Startup** folder to have it run automatically when you log in.


# 20/20/20 Eye Break Reminder (Windows)

This is a **Windows** tool that reminds you to follow the **20/20/20 rule**:  
> Every 20 minutes, look at something ~20 feet away for 20 seconds.

It shows a **large, centered popup** on your active monitor, stays **on top of other windows**, and counts down the 20 seconds for you.

---

## ✨ Features
- **Multi-monitor awareness** — popup appears on the monitor where your mouse is.
- **Resets after screen lock/unlock** — timer restarts after you return from locking your PC.
- **Snooze** and **Skip** buttons.
- **Stop** button or external stop file to end the reminder loop.
- **Quiet mode** to disable sounds.
- **Portable** — can be run from any folder, no installation required.
- **BAT files** for easy launch without opening a console.

---

## 📦 Requirements

You need **Python** installed on your computer (version 3.8 or newer).  
If you’re not sure, check:
```bat
py --version
````

or

```bat
python --version
```

If you don’t have Python:

1. Download from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. During installation, check **"Add Python to PATH"**.
3. Finish install.

---

## 📥 Installation

1. **Download** or copy these files into a folder of your choice:

   * `eye_break_popup.pyw` (the main script)
   * `start_eye_break_reminder.bat` (normal mode)
   * `start_eye_break_reminder_quiet.bat` (quiet mode — no sound)
   * `stop_eye_break_reminder.bat` (to stop the reminder loop)

2. **(Optional)** Create a shortcut to `start_eye_break_reminder.bat` in your Windows Startup folder:

   * Press `Win + R`
   * Type:

     ```
     shell:startup
     ```
   * Press Enter.
   * Place the shortcut there — the reminder will start automatically when you log in.

---

## ▶️ How to Run

* **Normal mode:** double-click `start_eye_break_reminder.bat`
* **Quiet mode:** double-click `start_eye_break_reminder_quiet.bat`
* **Stop the reminder:** double-click `stop_eye_break_reminder.bat` or press **Stop (Exit)** on any popup.

---

## 🔧 Controls

Inside the popup:

* **Snooze** — delays the reminder by a few minutes.
* **Skip** — closes the popup until the next scheduled reminder.
* **Stop (Exit)** — ends the reminder loop completely.

Outside the popup:

* Create a file called `STOP_20BREAK.flag` in the script folder to stop the reminder.
* Create a file called `QUIET_20BREAK.flag` in the script folder to mute sounds (remove it to unmute).

---

## 📚 How It Works

* Runs a timer in the background.

* Every `INTERVAL_MINUTES` (default: 20) it:

  1. Detects your active monitor.
  2. Shows a centered, always-on-top popup.
  3. Plays a gentle chime (unless in quiet mode).
  4. Counts down `BREAK_SECONDS` (default: 20 seconds).
  5. Plays an ending chime (unless in quiet mode).

* If your PC is **locked**, the timer pauses and restarts when you unlock.

---

## 🛠 Changing Settings

To adjust:

* **Interval between reminders**
* **Break duration**
* **Snooze time**
* **Popup size**

Open `eye_break_popup.pyw` in any text editor (Notepad works) and look for:

```python
INTERVAL_MINUTES = 20
BREAK_SECONDS    = 20
SNOOZE_MINUTES   = 5
WINDOW_SIZE      = (560, 300)
```

Change the numbers, save, and restart the script.

---

## 🆘 Troubleshooting

**Python not found:**

* Make sure Python is installed and added to PATH.
* Try replacing `py -3w` in the `.bat` file with the full path to your `pythonw.exe`
  (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python311\pythonw.exe`).

**Popup doesn’t appear after locking/unlocking:**

* Make sure you didn’t stop the reminder loop.
* Check if `STOP_20BREAK.flag` exists — delete it if you want to resume.

**Sounds don’t play:**

* Ensure you’re not in quiet mode (`QUIET_20BREAK.flag` missing).
* Check if your speakers are on.

---

## 📄 License

Free to use, modify, and share. No warranty.

---

