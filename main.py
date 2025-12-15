import wx
import hashlib
import time
import os
import datetime

# ---------------- CONFIG ----------------
USERS_FILE = "users.txt"
LOG_FILE = "login_logs.txt"

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

MAX_ATTEMPTS = 6
LOCK_TIME = 30  # seconds

failed_attempts = {}
locked_users = {}

# ---------------- COLORS ----------------
BG = "#0E0E10"
CARD = "#18181B"
TEXT = "#FFFFFF"
SUBTEXT = "#ADADB8"
ACCENT = "#9146FF"
INPUT_BG = "#000000"
ERROR = "#EF5350"
SUCCESS = "#66BB6A"
WARN = "#FFB74D"

# ---------------- UTILS ----------------
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def user_exists(username):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE) as f:
        return any(username == line.split(",")[0] for line in f)

def log_attempt(username, success):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{username},{success},{timestamp}\n")

def password_strength_score(pw):
    score = 0
    if len(pw) >= 8: score += 20
    if any(c.isupper() for c in pw): score += 20
    if any(c.islower() for c in pw): score += 20
    if any(c.isdigit() for c in pw): score += 20
    if any(c in "!@#$%^&*()_+" for c in pw): score += 20
    return score

# ---------------- ADMIN PANEL ----------------
class AdminPanel(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Admin Panel", size=(600, 450))
        self.SetIcon(wx.Icon("admin.ico", wx.BITMAP_TYPE_ICO))

        panel = wx.Panel(self)
        v = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Admin Dashboard")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.logs = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        btn_logs = wx.Button(panel, label="Load Login Logs")
        btn_logs.Bind(wx.EVT_BUTTON, self.load_logs)

        v.Add(title, 0, wx.ALL | wx.CENTER, 10)
        v.Add(btn_logs, 0, wx.ALL | wx.CENTER, 5)
        v.Add(self.logs, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(v)
        self.Show()

    def load_logs(self, e):
        try:
            with open(LOG_FILE) as f:
                self.logs.SetValue(f.read())
        except:
            self.logs.SetValue("No logs found.")

# ---------------- ADMIN LOGIN ----------------
class AdminLogin(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Admin Login", size=(300, 220))
        self.SetIcon(wx.Icon("admin.ico", wx.BITMAP_TYPE_ICO))

        p = wx.Panel(self)
        v = wx.BoxSizer(wx.VERTICAL)

        v.Add(wx.StaticText(p, label="Admin Username"), 0, wx.ALL, 6)
        self.u = wx.TextCtrl(p)
        v.Add(self.u, 0, wx.EXPAND | wx.ALL, 6)

        v.Add(wx.StaticText(p, label="Admin Password"), 0, wx.ALL, 6)
        self.pw = wx.TextCtrl(p, style=wx.TE_PASSWORD)
        v.Add(self.pw, 0, wx.EXPAND | wx.ALL, 6)

        btn = wx.Button(p, label="Login")
        btn.Bind(wx.EVT_BUTTON, self.login)
        v.Add(btn, 0, wx.ALL | wx.CENTER, 10)

        p.SetSizer(v)
        self.Show()

    def login(self, e):
        if self.u.GetValue() == ADMIN_USER and self.pw.GetValue() == ADMIN_PASS:
            AdminPanel()
            self.Close()
        else:
            wx.MessageBox("Invalid admin credentials")

# ---------------- MAIN AUTH UI ----------------
class AuthFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Cybersecurity System", size=(520, 540))
        self.SetIcon(wx.Icon("app.ico", wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(BG)
        self.Centre()

        self.root = wx.Panel(self)
        self.root.SetBackgroundColour(BG)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.root.SetSizer(self.sizer)

        self.lock_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_lock_timer, self.lock_timer)

        self.show_login()
        self.Show()

    # ---------- LOGIN ----------
    def show_login(self):
        self.sizer.Clear(True)

        card = wx.Panel(self.root)
        card.SetBackgroundColour(CARD)
        cs = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(card, label="Log into your account")
        title.SetForegroundColour(TEXT)
        title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # Username
        lbl_user = wx.StaticText(card, label="Username")
        lbl_user.SetForegroundColour(SUBTEXT)
        self.login_user = wx.TextCtrl(card, size=(-1, 32))
        self.login_user.SetBackgroundColour(INPUT_BG)
        self.login_user.SetForegroundColour(TEXT)

        # Password
        lbl_pass = wx.StaticText(card, label="Password")
        lbl_pass.SetForegroundColour(SUBTEXT)
        self.login_pass = wx.TextCtrl(card, style=wx.TE_PASSWORD, size=(-1, 32))
        self.login_pass.SetBackgroundColour(INPUT_BG)
        self.login_pass.SetForegroundColour(TEXT)

        self.attempts_lbl = wx.StaticText(card, label=f"Attempts left: {MAX_ATTEMPTS}")
        self.attempts_lbl.SetForegroundColour(SUBTEXT)

        btn_login = wx.Button(card, label="Log In", size=(-1, 36))
        btn_login.Bind(wx.EVT_BUTTON, self.login)

        signup_link = wx.StaticText(card, label="Don't have an account? Sign up")
        signup_link.SetForegroundColour(ACCENT)
        signup_link.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        signup_link.Bind(wx.EVT_LEFT_DOWN, lambda e: self.show_signup())

        admin_link = wx.StaticText(card, label="Admin Login")
        admin_link.SetForegroundColour(SUBTEXT)
        admin_link.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        admin_link.Bind(wx.EVT_LEFT_DOWN, lambda e: AdminLogin())

        cs.Add(title, 0, wx.ALL | wx.CENTER, 15)
        cs.Add(lbl_user, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)
        cs.Add(self.login_user, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        cs.Add(lbl_pass, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        cs.Add(self.login_pass, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        cs.Add(self.attempts_lbl, 0, wx.ALL | wx.CENTER, 10)
        cs.Add(btn_login, 0, wx.EXPAND | wx.ALL, 20)
        cs.Add(signup_link, 0, wx.ALL | wx.CENTER, 8)
        cs.Add(admin_link, 0, wx.ALL | wx.CENTER, 5)

        card.SetSizer(cs)
        self.sizer.AddStretchSpacer()
        self.sizer.Add(card, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddStretchSpacer()
        self.root.Layout()

    # ---------- SIGNUP ----------
    def show_signup(self):
        self.sizer.Clear(True)

        card = wx.Panel(self.root)
        card.SetBackgroundColour(CARD)
        cs = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(card, label="Create an account")
        title.SetForegroundColour(TEXT)
        title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        lbl_user = wx.StaticText(card, label="Username")
        lbl_user.SetForegroundColour(SUBTEXT)
        self.signup_user = wx.TextCtrl(card, size=(-1, 32))
        self.signup_user.SetBackgroundColour(INPUT_BG)
        self.signup_user.SetForegroundColour(TEXT)

        self.user_status = wx.StaticText(card, label="")
        self.user_status.SetForegroundColour(ERROR)

        lbl_pass = wx.StaticText(card, label="Password")
        lbl_pass.SetForegroundColour(SUBTEXT)
        self.signup_pass = wx.TextCtrl(card, style=wx.TE_PASSWORD, size=(-1, 32))
        self.signup_pass.SetBackgroundColour(INPUT_BG)
        self.signup_pass.SetForegroundColour(TEXT)

        self.strength_bar = wx.Gauge(card, range=100)
        self.strength_text = wx.StaticText(card, label="Password strength")
        self.strength_text.SetForegroundColour(SUBTEXT)

        self.signup_user.Bind(wx.EVT_TEXT, self.check_username)
        self.signup_pass.Bind(wx.EVT_TEXT, self.update_password_strength)

        btn_create = wx.Button(card, label="Sign Up", size=(-1, 36))
        btn_create.Bind(wx.EVT_BUTTON, self.create_account)

        back_link = wx.StaticText(card, label="Back to login")
        back_link.SetForegroundColour(SUBTEXT)
        back_link.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        back_link.Bind(wx.EVT_LEFT_DOWN, lambda e: self.show_login())

        cs.Add(title, 0, wx.ALL | wx.CENTER, 15)
        cs.Add(lbl_user, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)
        cs.Add(self.signup_user, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        cs.Add(self.user_status, 0, wx.LEFT | wx.BOTTOM, 20)
        cs.Add(lbl_pass, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        cs.Add(self.signup_pass, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        cs.Add(self.strength_bar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        cs.Add(self.strength_text, 0, wx.LEFT | wx.BOTTOM, 20)
        cs.Add(btn_create, 0, wx.EXPAND | wx.ALL, 20)
        cs.Add(back_link, 0, wx.ALL | wx.CENTER, 10)

        card.SetSizer(cs)
        self.sizer.AddStretchSpacer()
        self.sizer.Add(card, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddStretchSpacer()
        self.root.Layout()

    # ---------- LOGIC (unchanged) ----------
    def check_username(self, e):
        name = self.signup_user.GetValue().strip()
        if not name:
            self.user_status.SetLabel("")
        elif user_exists(name):
            self.user_status.SetLabel("Username already exists")
            self.user_status.SetForegroundColour(ERROR)
        else:
            self.user_status.SetLabel("Username available")
            self.user_status.SetForegroundColour(SUCCESS)

    def update_password_strength(self, e):
        pw = self.signup_pass.GetValue()
        score = password_strength_score(pw)
        self.strength_bar.SetValue(score)

        if score < 40:
            self.strength_text.SetLabel("Password strength: Weak")
            self.strength_text.SetForegroundColour(ERROR)
        elif score < 80:
            self.strength_text.SetLabel("Password strength: Medium")
            self.strength_text.SetForegroundColour(WARN)
        else:
            self.strength_text.SetLabel("Password strength: Strong")
            self.strength_text.SetForegroundColour(SUCCESS)

    def create_account(self, e):
        u = self.signup_user.GetValue().strip()
        p = self.signup_pass.GetValue()
        if not u or not p or user_exists(u):
            return

        if password_strength_score(p) < 80:
            res = wx.MessageBox(
                "Your password is weak or medium.\nDo you want to continue anyway?",
                "Weak Password Warning",
                wx.YES_NO | wx.ICON_WARNING
            )
            if res != wx.YES:
                return

        with open(USERS_FILE, "a") as f:
            f.write(f"{u},{hash_password(p)}\n")

        wx.MessageBox("Account created successfully")
        self.show_login()

    def login(self, e):
        u = self.login_user.GetValue().strip()
        p = self.login_pass.GetValue()

        if not user_exists(u):
            wx.MessageBox("No account found with this username.\nPlease sign up.",
                          "User Not Found", wx.OK | wx.ICON_WARNING)
            return

        if u in locked_users:
            self.lock_timer.Start(1000)
            return

        success = False
        with open(USERS_FILE) as f:
            for line in f:
                uu, pp = line.strip().split(",")
                if uu == u and pp == hash_password(p):
                    success = True

        log_attempt(u, success)

        if success:
            failed_attempts[u] = 0
            self.attempts_lbl.SetLabel("Login successful")
        else:
            failed_attempts[u] = failed_attempts.get(u, 0) + 1
            left = MAX_ATTEMPTS - failed_attempts[u]
            self.attempts_lbl.SetLabel(f"Attempts left: {left}")
            if failed_attempts[u] >= MAX_ATTEMPTS:
                locked_users[u] = time.time() + LOCK_TIME
                self.lock_timer.Start(1000)

    def update_lock_timer(self, event):
        u = self.login_user.GetValue().strip()
        if u not in locked_users:
            self.lock_timer.Stop()
            return

        remaining = int(locked_users[u] - time.time())
        if remaining <= 0:
            del locked_users[u]
            self.attempts_lbl.SetLabel(f"Attempts left: {MAX_ATTEMPTS}")
            self.lock_timer.Stop()
        else:
            self.attempts_lbl.SetLabel(
                f"Account locked. Try again after {remaining} seconds"
            )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app = wx.App()
    AuthFrame()
    app.MainLoop()
