# eye_break_popup.pyw
import os, sys, time, threading, ctypes
import tkinter as tk
from tkinter import ttk

# ---------------- Settings ----------------
INTERVAL_MINUTES = 20       # remind every 20 minutes
BREAK_SECONDS    = 20       # 20/20/20: look away for 20 seconds
SNOOZE_MINUTES   = 5
WINDOW_SIZE      = (560, 300)
TITLE            = "20/20/20 Eye Break"
MESSAGE          = "Look ~20 feet away (~6 meters) for"
# ------------------------------------------

# Args / flags
QUIET = ("--quiet" in sys.argv) or ("--no-sound" in sys.argv)

# Paths (same folder as this script)
APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
STOP_FLAG = os.path.join(APP_DIR, "STOP_20BREAK.flag")
QUIET_FLAG = os.path.join(APP_DIR, "QUIET_20BREAK.flag")  # create/delete to toggle quiet on the fly

# ---- Windows API (ctypes) for multi-monitor & lock detection ----
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_cursor_monitor_rect():
    """Return (left, top, right, bottom) of the monitor under the mouse cursor."""
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    MONITOR_DEFAULTTONEAREST = 2
    monitor = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTONEAREST)
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                    ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
    class MONITORINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("rcMonitor", RECT),
                    ("rcWork", RECT), ("dwFlags", ctypes.c_ulong)]
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    user32.GetMonitorInfoW(monitor, ctypes.byref(mi))
    r = mi.rcMonitor
    return (r.left, r.top, r.right, r.bottom)

def is_workstation_locked():
    """
    Detect locked workstation by trying to switch to the input desktop.
    If SwitchDesktop fails, Windows is typically locked.
    """
    UOI_NAME = 2
    DESKTOP_SWITCHDESKTOP = 0x0100
    hdesk = user32.OpenInputDesktop(0, False, DESKTOP_SWITCHDESKTOP)
    if not hdesk:
        return True  # cannot open input desktop -> locked
    res = user32.SwitchDesktop(hdesk)
    user32.CloseDesktop(hdesk)
    return not bool(res)

# ---- Sound (optional) ----
def chime_start():
    if QUIET or os.path.exists(QUIET_FLAG):
        return
    try:
        import winsound
        winsound.Beep(880, 140)
        winsound.Beep(988, 140)
    except Exception:
        pass

def chime_end():
    if QUIET or os.path.exists(QUIET_FLAG):
        return
    try:
        import winsound
        winsound.Beep(740, 120)
        winsound.Beep(659, 120)
    except Exception:
        pass

# ---- App ----
def center_on_monitor(win, w, h):
    L, T, R, B = get_cursor_monitor_rect()
    mw, mh = (R - L), (B - T)
    x = L + max(0, (mw - w) // 2)
    y = T + max(0, (mh - h) // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

class EyeBreakApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.stop_requested = False

        # Start scheduler
        self.scheduler_thread = threading.Thread(target=self.scheduler_loop, daemon=True)
        self.scheduler_thread.start()

        # initial small info popup so you know it's running
        self.root.after(400, self.show_popup, True, True)

    # elapsed timer that resets after unlock
    def scheduler_loop(self):
        interval = INTERVAL_MINUTES * 60
        elapsed = 0
        last_locked = False
        poll = 1  # seconds

        while True:
            if os.path.exists(STOP_FLAG) or self.stop_requested:
                # optional: delete stop flag so next run starts clean
                try: os.remove(STOP_FLAG)
                except: pass
                break

            locked = is_workstation_locked()
            if locked:
                last_locked = True
                elapsed = 0  # ensure a fresh interval after unlock
            else:
                if last_locked:
                    # just unlocked: start fresh
                    last_locked = False
                    elapsed = 0

                elapsed += poll
                if elapsed >= interval:
                    elapsed = 0
                    self.root.after(0, self.show_popup)

            time.sleep(poll)

        # exit the Tk loop
        self.root.after(0, self.root.quit)

    def show_popup(self, manual=False, initial=False):
        popup = tk.Toplevel(self.root)
        popup.title(TITLE)
        popup.attributes("-topmost", True)
        try:
            popup.wm_attributes("-toolwindow", 1)
        except Exception:
            pass
        popup.lift()
        popup.focus_force()
        popup.resizable(False, False)

        w, h = WINDOW_SIZE
        popup.update_idletasks()
        center_on_monitor(popup, w, h)

        frm = ttk.Frame(popup, padding=18)
        frm.pack(expand=True, fill="both")

        head = ttk.Label(frm, text="👀 Time for an eye break", font=("Segoe UI", 20, "bold"))
        head.pack(pady=(0, 8))

        sub = ttk.Label(frm, text=f"{MESSAGE} {BREAK_SECONDS} seconds.", font=("Segoe UI", 12))
        sub.pack(pady=(0, 12))

        countdown_lbl = ttk.Label(frm, text=f"{BREAK_SECONDS}", font=("Segoe UI", 40, "bold"))
        countdown_lbl.pack(pady=6)

        btn_row = ttk.Frame(frm)
        btn_row.pack(pady=12)

        def on_snooze():
            popup.destroy()
            threading.Thread(target=self._snooze_timer, args=(SNOOZE_MINUTES,), daemon=True).start()

        def on_skip():
            popup.destroy()

        def on_stop():
            self.stop_requested = True
            popup.destroy()

        snooze_btn = ttk.Button(btn_row, text=f"Snooze {SNOOZE_MINUTES} min", command=on_snooze)
        snooze_btn.grid(row=0, column=0, padx=6)

        skip_btn = ttk.Button(btn_row, text="Skip", command=on_skip)
        skip_btn.grid(row=0, column=1, padx=6)

        stop_btn = ttk.Button(btn_row, text="Stop (Exit)", command=on_stop)
        stop_btn.grid(row=0, column=2, padx=6)

        # status row: shows quiet mode and control hints
        quiet_on = QUIET or os.path.exists(QUIET_FLAG)
        status = ttk.Label(frm, text=f"Quiet: {'ON' if quiet_on else 'OFF'}   •   "
                                     f"To toggle quiet: create/delete {os.path.basename(QUIET_FLAG)}   •   "
                                     f"To stop anytime: create {os.path.basename(STOP_FLAG)}",
                           font=("Segoe UI", 9))
        status.pack(pady=(6, 0))

        chime_start()
        self._start_countdown(popup, countdown_lbl)

        def keep_on_top():
            try:
                popup.lift()
                popup.attributes("-topmost", True)
            except Exception:
                pass
            popup.after(1500, keep_on_top)
        keep_on_top()

    def _start_countdown(self, popup, label):
        start = time.time()
        def tick():
            if not popup.winfo_exists():
                return
            elapsed = int(time.time() - start)
            remaining = max(0, BREAK_SECONDS - elapsed)
            label.configure(text=str(remaining))
            if remaining > 0:
                label.after(250, tick)
            else:
                chime_end()
                done = ttk.Label(popup, text="All set ✔  Blink a few times and relax your shoulders.",
                                 font=("Segoe UI", 11))
                done.pack(pady=(6, 2))
                popup.after(2500, popup.destroy)
        tick()

    def _snooze_timer(self, minutes):
        # pause the scheduler by waiting "minutes" with lock-awareness
        target = minutes * 60
        waited = 0
        while waited < target and not self.stop_requested and not os.path.exists(STOP_FLAG):
            if not is_workstation_locked():
                waited += 1
            time.sleep(1)
        self.root.after(0, self.show_popup)

    def run(self):
        try:
            print(f"{TITLE} running: every {INTERVAL_MINUTES} minutes.")
        except Exception:
            pass
        self.root.mainloop()

if __name__ == "__main__":
    EyeBreakApp().run()
