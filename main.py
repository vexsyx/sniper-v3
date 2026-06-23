import sys
import os
import json
import configparser
import re
import time
import random
import requests
from requests import RequestException
import urllib.request
from urllib.parse import urlparse, parse_qs
import tempfile
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QLineEdit, QCheckBox, QComboBox,
    QStackedWidget, QTabWidget, QTextEdit, QScrollArea, QFrame, QSizePolicy,
    QAbstractItemView, QFormLayout, QGroupBox, QDialog, QTreeWidget, 
    QTreeWidgetItem, QHeaderView, QProgressBar, QMessageBox, QTableWidget, 
    QTableWidgetItem, QInputDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout, 
    QDialog, QPushButton, QLabel, QLineEdit, QWidget, QHeaderView, QFileDialog,
    QColorDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QTimer, QSize, QStandardPaths, QRect, QPoint, QUrl, QEvent, QRectF, QByteArray, QMetaObject, Q_ARG, QEventLoop
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QFontDatabase, QPainter, QBrush, QPen, QLinearGradient, QPainterPath, QColor, QRegion, QTransform, QIntValidator
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
import webbrowser
import psutil
import discord
from discord.ext import commands
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from datetime import datetime, timedelta
import platform
import subprocess
import threading
import pyautogui
from pynput import keyboard as pynput_keyboard
from pynput.keyboard import Controller as KeyboardController
from queue import Queue
import shutil
import concurrent.futures
import getpass
import base64
import gc
import websockets

if platform.system() == "Windows":
    from win11toast import toast
    import win32gui
    import win32con
    import win32api
    import win32process
    import winreg
    import ctypes
    import ctypes.wintypes
    ctypes.windll.user32.SetProcessDPIAware()

if platform.system() == "Darwin":
    import Quartz  # type: ignore
    from Foundation import NSBundle  # type: ignore

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

APP_NAME = "sol-sniper"
BASE_DIR = Path(os.getcwd())
SETTINGS_DIR = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)) / APP_NAME
SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

def send_to_existing_instance(args):
    socket = QLocalSocket()
    socket.connectToServer(APP_NAME)
    if socket.waitForConnected(500):
        data = json.dumps({"argv": args}).encode("utf-8")
        socket.write(data)
        socket.flush()
        socket.waitForBytesWritten(500)
        socket.disconnectFromServer()
        return True
    return False

KEYWORDS_FILE = SETTINGS_DIR / "keywords.json"
SERVERS_FILE = SETTINGS_DIR / "servers.json"
CONFIG_FILE = SETTINGS_DIR / "sniper_config.ini"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"
DATA_FILE = SETTINGS_DIR / "currentKeyword.json"
LOGS_DIR = SETTINGS_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
ACCOUNTS_DIR = SETTINGS_DIR / "accounts"
ACCOUNTS_DIR.mkdir(parents=True, exist_ok=True)

ROBLOX_COOKIES_PATH = Path(os.path.expanduser("~/AppData/Local/Roblox/LocalStorage/RobloxCookies.dat"))
ROBLOX_APPSTORAGE_PATH = Path(os.path.expanduser("~/AppData/Local/Roblox/LocalStorage/appStorage.json"))

ASSETS = {
    "snipercat.png": "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/snipercat.png",
    "yeswe.png": "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/yeswe.png",
    "solsniper.png": "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/solsniper.png",
    "font.ttf": "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/font.ttf",
    "vex.png": "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/vex.png"
}

DISCORD_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#fff" viewBox="0 0 16 16">
    <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/>
</svg>"""
ROBLOX_SVG = b"""<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1"
id="svg10" inkscape:version="0.92.3 (2405546, 2018-03-11)" sodipodi:docname="Roblox_2017_O_Icon_final_-_Red.svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:svg="http://www.w3.org/2000/svg"
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 302.7 302.7"
style="enable-background:new 0 0 302.7 302.7;" xml:space="preserve">
<style type="text/css">
.st0{fill:#FFFFFF;}
</style>
<sodipodi:namedview  bordercolor="#666666" borderopacity="1" gridtolerance="10" guidetolerance="10" id="namedview12" inkscape:current-layer="svg10" inkscape:cx="151.36" inkscape:cy="151.36" inkscape:pageopacity="0" inkscape:pageshadow="2" inkscape:window-height="1017" inkscape:window-maximized="1" inkscape:window-width="1920" inkscape:window-x="-8" inkscape:window-y="-8" inkscape:zoom="2.6030655" objecttolerance="10" pagecolor="#ffffff" showgrid="false">
</sodipodi:namedview>
<path id="path20" inkscape:connector-curvature="0" class="st0" d="M120.5,271.7c-110.9-28.6-120-31-119.9-31.5
C0.7,239.6,62.1,0.5,62.2,0.4c0,0,54,13.8,119.9,30.8s120,30.8,120.1,30.8c0.2,0,0.2,0.4,0.1,0.9c-0.2,1.5-61.5,239.3-61.7,239.5
C240.6,302.5,186.5,288.7,120.5,271.7z M174.9,158c3.2-12.6,5.9-23.1,6-23.4c0.1-0.5-2.3-1.2-23.2-6.6c-12.8-3.3-23.5-5.9-23.6-5.8
c-0.3,0.3-12.1,46.6-12,46.7c0.2,0.2,46.7,12.2,46.8,12.1C168.9,180.9,171.6,170.6,174.9,158L174.9,158z"/>
</svg>
"""
GITHUB_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#fff" viewBox="0 0 16 16">
    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.22 2.2.82a7.65 7.65 0 0 1 2-.27c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.19 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
</svg>"""
WEBSITE_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" class="bi bi-globe-americas" viewBox="0 0 16 16">
  <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0M2.04 4.326c.325 1.329 2.532 2.54 3.717 3.19.48.263.793.434.743.484q-.121.12-.242.234c-.416.396-.787.749-.758 1.266.035.634.618.824 1.214 1.017.577.188 1.168.38 1.286.983.082.417-.075.988-.22 1.52-.215.782-.406 1.48.22 1.48 1.5-.5 3.798-3.186 4-5 .138-1.243-2-2-3.5-2.5-.478-.16-.755.081-.99.284-.172.15-.322.279-.51.216-.445-.148-2.5-2-1.5-2.5.78-.39.952-.171 1.227.182.078.099.163.208.273.318.609.304.662-.132.723-.633.039-.322.081-.671.277-.867.434-.434 1.265-.791 2.028-1.12.712-.306 1.365-.587 1.579-.88A7 7 0 1 1 2.04 4.327Z"/>
</svg>"""
EDIT_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" class="bi bi-pencil-square" viewBox="0 0 16 16">
  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
</svg>"""
EYE_OPEN_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" class="bi bi-eye-fill" viewBox="0 0 16 16">
  <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
  <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
</svg>"""
EYE_CLOSED_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" class="bi bi-eye-slash-fill" viewBox="0 0 16 16">
  <path d="m10.79 12.912-1.614-1.615a3.5 3.5 0 0 1-4.474-4.474l-2.06-2.06C.938 6.278 0 8 0 8s3 5.5 8 5.5a7 7 0 0 0 2.79-.588M5.21 3.088A7 7 0 0 1 8 2.5c5 0 8 5.5 8 5.5s-.939 1.721-2.641 3.238l-2.062-2.062a3.5 3.5 0 0 0-4.474-4.474z"/>
  <path d="M5.525 7.646a2.5 2.5 0 0 0 2.829 2.829zm4.95.708-2.829-2.83a2.5 2.5 0 0 1 2.829 2.829zm3.171 6-12-12 .708-.708 12 12z"/>
</svg>"""


PRIVATE_SERVER_PATTERN = re.compile(r'https://www\.roblox\.com/games/(\d+)/.+\?privateserverlinkcode=([\w-]+)', re.IGNORECASE)
SHARE_CODE_PATTERN = re.compile(r'https://www\.roblox\.com/share\?code=([a-f0-9]+)&type=server', re.IGNORECASE)
DEEPLINK_PATTERN = re.compile(r'https://www\.roblox\.com/games/start\?placeid=(\d+)(?:&launchdata=([^&]+))?', re.IGNORECASE)
URL_PATTERN = re.compile(r'(?:(?:https?|roblox)://[^\s<>"]+|www\.[^\s<>"]+\.[^\s<>"]+|(?:ro\.pro|ropro\.io|join-rbx\.vexsys\.site)/[^\s<>"]+)', re.IGNORECASE)
ROPRO_PATTERN = re.compile(r'https?://(?:www\.)?(?:ro\.pro|ropro\.io)/(?:join/)?([a-zA-Z0-9]+)', re.IGNORECASE)
REDIRECT_GAME_PATTERN = re.compile(r'launchdata=(\d+)/([a-f0-9\-]+)', re.IGNORECASE)
JOIN_RBX_PUBLIC_PATTERN = re.compile(r'https?://join-rbx\.vexsys\.site/public\?placeid=(\d+)&gameinstanceid=([A-Za-z0-9\-]+)', re.IGNORECASE)
JOIN_RBX_PRIVATE_SHARE_PATTERN = re.compile(r'https?://join-rbx\.vexsys\.site/private\?share_code=([A-Za-z0-9]+)', re.IGNORECASE)
JOIN_RBX_PRIVATE_SERVER_PATTERN = re.compile(r'https?://join-rbx\.vexsys\.site/private\?placeid=(\d+)&link_code=([A-Za-z0-9\-]+)', re.IGNORECASE)

CURRENT_VERSION = "3.0.0"
IS_BETA_VERSION = True
BETA_VERSION = 7
IS_PRE_RELEASE = False
LOCKED_PRE_RELEASE = False
PRE_RELEASE_VERSION = 0
# raw version strings use the following format: 3.0.0-beta7-pre4, 3.0.0-beta7 or 3.0.0 depending on the version and whether its a pre release or not
# ^ also only used for version control
RAW_VERSION_STR = f"{CURRENT_VERSION}-beta{BETA_VERSION}-pre{PRE_RELEASE_VERSION}" if IS_BETA_VERSION and IS_PRE_RELEASE else (f"{CURRENT_VERSION}-beta{BETA_VERSION}" if IS_BETA_VERSION else CURRENT_VERSION)

SOL_SNIPER_SERVER_ID = "1271189425459826699"
SNIPERMEOW_CHANNELS = []
try:
    response = requests.get("https://raw.githubusercontent.com/vexsyx/sniper-v3/main/snipermeow_channels.json", timeout=10)
    if response.status_code == 200:
        SNIPERMEOW_CHANNELS = response.json()
except Exception as e:
    print(f"Error fetching sol sniper channels: {e}")

GLOBALMEOW_CHANNELS = []
try:
    response = requests.get("https://raw.githubusercontent.com/vexsyx/sniper-v3/main/globalmeow_channels.json", timeout=10)
    if response.status_code == 200:
        GLOBALMEOW_CHANNELS = response.json()
except Exception as e:
    print(f"Error fetching globalmeow channels: {e}")


CONFIG_DATA = {
    "token": "",
    "glitchsniping": False,
    "dreamsniping": False,
    "cybersniping": False,
    "singularitysniping": False,
    "jestersniping": False,
    "voidcoinsniping": False,
    "close_roblox_before_joining": False,
    "leave_game_before_joining": False,
    "minimize_other_windows": False,
    "auto_pause_sniper": True,
    "only_join_sols_links": True,
    "snipe_ropro_links": True,
    "snipe_joinrbx_links": True,
    "snipe_roseal_links": True,
    "snipe_fishstrap_links": True,
    "ignore_messages_that_respond": False,
    "pause_duration": 120,
    "pause_duration_glitched": 180,
    "pause_duration_dreamspace": 180,
    "pause_duration_cyberspace": 720,
    "pause_duration_singularity": 1200,
    "pause_duration_jester": 120,
    "pause_duration_void_coin": 120,
    "override_protocol_enabled": False,
    "override_protocol_path": "",
    "override_protocol_type": "",
    "override_protocol_version": "",
    "open_roblox": "-",
    "open_roblox_toggle": True,
    "stop_sniper": "[",
    "stop_sniper_toggle": True,
    "toggle_sniper": "f4",
    "toggle_sniper_toggle": True,
    "loading_asset_skipper": "f5",
    "loading_asset_skipper_toggle": False,
    "main_menu_skipper": "f6",
    "main_menu_skipper_toggle": False,
    "toast_notifications": True,
    "use_discord_app": True,
    "stillbackground": False,
    "semi_transparent_background": False,
    "gradient_theme": True,
    "advanced_mode": False,
    "dismissed_notices": {
        "handout_channel_warning": False,
        "handout_channel_warning_launch": False,
        "missing_maincord_warning": False,
        "locked_pre_release_warning": False
    },
    "hide_from_board": False,
}

config = configparser.ConfigParser()
url_pattern = re.compile(r'https?://[^\s]+')
game_pattern = r"https:\/\/www\.roblox\.com\/games\/(\d+)\/[^?]+\?privateServerLinkCode=(\d+)"
share_pattern = r"https:\/\/www\.roblox\.com\/share\?code=([a-f0-9]+)&type=([A-Za-z]+)"
timer_running = False
sniper_active = False
sniper_paused = False
pause_end_time = None
loading_asset_skipper_active = False
main_menu_skipper_active = False
restart_roblox_on_next_snipe = False

blockedUsers = []
processing_hotkey_assignment = False

executor = ThreadPoolExecutor(max_workers=4)
config_lock = Lock()

class UsernameFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.username = getpass.getuser()
        self.username_lower = self.username.lower()
        self.username_capitalized = self.username.capitalize()
        self.username_upper = self.username.upper()
    
    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            original_msg = record.msg
            record.msg = original_msg.replace(self.username, '*' * len(self.username))
            record.msg = record.msg.replace(self.username_lower, '*' * len(self.username))
            record.msg = record.msg.replace(self.username_capitalized, '*' * len(self.username))
            record.msg = record.msg.replace(self.username_upper, '*' * len(self.username))
            
            pattern = re.compile(r'(\\Users\\|/Users/|\\user\\|/user/)' + re.escape(self.username) + r'(\\|/|$)')
            record.msg = pattern.sub(r'\1' + '*' * len(self.username) + r'\2', record.msg)
            pattern_lower = re.compile(r'(\\Users\\|/Users/|\\user\\|/user/)' + re.escape(self.username_lower) + r'(\\|/|$)')
            record.msg = pattern_lower.sub(r'\1' + '*' * len(self.username) + r'\2', record.msg)
        
        return True

def sanitize_text(text):
    if not isinstance(text, str):
        return text
    
    username = getpass.getuser()
    username_lower = username.lower()
    username_capitalized = username.capitalize()
    username_upper = username.upper()
    
    # replace all case variations of the username
    result = text.replace(username, '*' * len(username))
    result = result.replace(username_lower, '*' * len(username))
    result = result.replace(username_capitalized, '*' * len(username))
    result = result.replace(username_upper, '*' * len(username))
    
    # handle path patterns like C:\Users\username\ or /Users/username/
    pattern = re.compile(r'(\\Users\\|/Users/|\\user\\|/user/)' + re.escape(username) + r'(\\|/|$)')
    result = pattern.sub(r'\1' + '*' * len(username) + r'\2', result)
    pattern_lower = re.compile(r'(\\Users\\|/Users/|\\user\\|/user/)' + re.escape(username_lower) + r'(\\|/|$)')
    result = pattern_lower.sub(r'\1' + '*' * len(username) + r'\2', result)
    
    return result

class LogSignalEmitter(QThread):
    log_signal = pyqtSignal(str, str, str)
    
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def run(self):
        while True:
            try:
                timestamp, level, message = self.queue.get(timeout=0.1)
                self.log_signal.emit(timestamp, level, message)
            except:
                pass

log_emitter = LogSignalEmitter()

class GUILoggingHandler(logging.Handler):
    def emit(self, record):
        try:
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            level = record.levelname
            message = record.getMessage()
            message = sanitize_text(message)
            log_emitter.queue.put((timestamp, level, message))
        except Exception:
            self.handleError(record)

def cleanup_old_logs():
    log_files = sorted(LOGS_DIR.glob("*.log"), key=os.path.getmtime, reverse=True)
    for log_file in log_files[6:]:
        try:
            log_file.unlink()
        except Exception as e:
            logging.error(f"Failed to delete old log file {log_file}: {e}")

def setup_logging():
    global log_filename
    log_filename = datetime.now().strftime("%m-%d-%Y %H-%M-%S.log")
    
    logging.root.handlers.clear()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(str(LOGS_DIR / log_filename), encoding="utf-8"),
            logging.StreamHandler(),
            GUILoggingHandler()
        ]
    )
    
    username_filter = UsernameFilter()
    for handler in logging.root.handlers:
        handler.addFilter(username_filter)
    
    cleanup_old_logs()

def register_protocol():
    if platform.system() == "Windows":
        try:
            key_path = r"SOFTWARE\Classes\solsniper"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:Sol Sniper Protocol")
                winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

            command_path = rf"{key_path}\shell\open\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{sys.executable}" "%1"')
            logging.info("Registered solsniper:// as executable protocol")
        except Exception as e:
            logging.error(f"Failed to register protocol: {e}")
    else:
        logging.info("Current OS not windows, skipping protocol creation/overriding for solsniper://")

class AssetDownloadDialog(QDialog):
    update_signal = pyqtSignal(str, str, int, int)
    error_signal = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Checking & Downloading Assets")
        self.setFixedSize(500, 375)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.download_canceled = False
        self.failed_assets = []
        
        self.setup_ui()
        self.apply_rounded_corners()
        
        self.update_signal.connect(self.do_update_progress)
        self.error_signal.connect(self.do_show_error_message)

    def apply_rounded_corners(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        
    def setup_ui(self):
        if CONFIG_DATA["stillbackground"]:
            self.bg_widget = StarryBackgroundStill(self)
        else:
            self.bg_widget = StarryBackground(self)
        self.bg_widget.setGeometry(0, 0, self.width(), int(self.height() * 1.25))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_bar = ModernTitleBar(self)
        title_bar.title.setText("Checking Assets")
        layout.addWidget(title_bar)
        
        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        self.status_label = QLabel("Checking and downloading assets...")
        self.status_label.setStyleSheet("font-size: 18px; color: #e0e0e0;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        content_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 6px;
                text-align: center;
                color: white;
                height: 24px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                border-radius: 5px;
            }
        """)
        self.progress_bar.setMaximum(len(ASSETS))
        content_layout.addWidget(self.progress_bar)
        
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(5)
        self.history_labels = []
        for i in range(3):
            label = QLabel("")
            label.setStyleSheet(f"font-size: {12 - i * 2}px; color: {'#e0e0e0' if i == 0 else '#888888'};")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self.history_labels.append(label)
            self.history_layout.addWidget(label)
        
        content_layout.addLayout(self.history_layout)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedHeight(35)
        if CONFIG_DATA["gradient_theme"]:
            self.cancel_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        self.cancel_btn.clicked.connect(self.cancel_download)
        content_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(content_frame)
        
    def cancel_download(self):
        self.download_canceled = True
        self.close()
        
    def do_update_progress(self, asset_name, status, completed, total):
        if total is not None:
            self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(completed)
        
        for i in range(2, 0, -1):
            self.history_labels[i].setText(self.history_labels[i-1].text())
            self.history_labels[i].setStyleSheet(f"font-size: {12 - i * 2}px; color: #888888;")
        
        status_color = "#e0e0e0" if status in ("Downloaded", "Updated", "Done") else "#888888"
        display_text = f"{asset_name} ({status})"
        self.history_labels[0].setText(display_text)
        self.history_labels[0].setStyleSheet(f"font-size: 12px; color: {status_color};")
        
    def update_progress(self, asset_name, status, completed, total=None):
        self.update_signal.emit(asset_name, status, completed, total if total is not None else -1)
        
    def do_show_error_message(self, failed_assets):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Failed Assets")
        error_dialog.setFixedSize(500, 438)
        error_dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        error_dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        if CONFIG_DATA["stillbackground"]:
            bg_widget = StarryBackgroundStill(error_dialog)
        else:
            bg_widget = StarryBackground(error_dialog)
        bg_widget.setGeometry(0, 0, error_dialog.width(), int(error_dialog.height() * 1.25))
        
        layout = QVBoxLayout(error_dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_bar = ModernTitleBar(error_dialog)
        title_bar.title.setText("Failed Assets")
        layout.addWidget(title_bar)
        
        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        error_label = QLabel("The following assets failed to download/check:")
        error_label.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        error_label.setWordWrap(True)
        content_layout.addWidget(error_label)
        
        error_text = "\n".join([f"• {name}: {err}" for name, err in failed_assets])
        error_details = QTextEdit()
        error_details.setPlainText(error_text)
        error_details.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        error_details.setReadOnly(True)
        content_layout.addWidget(error_details)
        
        button_layout = QHBoxLayout()
        
        retry_btn = QPushButton("Redownload Failed Assets")
        retry_btn.setFixedHeight(35)
        if CONFIG_DATA["gradient_theme"]:
            retry_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            retry_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        retry_btn.clicked.connect(lambda: self.redownload_failed(failed_assets, error_dialog))
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(35)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                font-weight: 500;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        close_btn.clicked.connect(error_dialog.close)
        
        button_layout.addWidget(retry_btn)
        button_layout.addWidget(close_btn)
        content_layout.addLayout(button_layout)
        
        layout.addWidget(content_frame)
        error_dialog.exec()
        
    def show_error_message(self, failed_assets):
        self.error_signal.emit(failed_assets)
        
    def redownload_failed(self, failed_assets, parent_dialog):
        parent_dialog.close()
        failed_assets_dict = {name: ASSETS[name] for name, _ in failed_assets if name in ASSETS}
        if failed_assets_dict:
            self.download_assets_subset(failed_assets_dict)
            
    def download_assets_subset(self, assets_dict):
        self.progress_bar.setMaximum(len(assets_dict))
        self.progress_bar.setValue(0)
        self.failed_assets = []
        
        completed = 0
        for filename, url in assets_dict.items():
            if self.download_canceled:
                break
                
            asset_path = SETTINGS_DIR / filename
            status = ""
            try:
                if asset_path.exists():
                    response = requests.get(url, timeout=10)
                    if response.status_code in (403, 429):
                        status = "Rate-Limited"
                        self.failed_assets.append((filename, f"Rate-limited ({response.status_code})"))
                        logging.warning(f"Asset '{filename}' rate-limited with status {response.status_code}")
                        self.update_progress(filename, status, completed, len(assets_dict))
                        completed += 1
                        continue
                    response.raise_for_status()
                    remote_bytes = response.content
                    with open(asset_path, "rb") as f:
                        local_bytes = f.read()
                        if local_bytes == remote_bytes:
                            status = "Done"
                            logging.info(f"Asset '{filename}' is up to date.")
                            self.update_progress(filename, status, completed, len(assets_dict))
                            completed += 1
                            continue
                    status = "Updated"
                    with open(asset_path, "wb") as f:
                        f.write(remote_bytes)
                    logging.info(f"Asset '{filename}' updated.")
                    self.update_progress(filename, status, completed, len(assets_dict))
                    completed += 1
                else:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    status = "Downloaded"
                    with open(asset_path, "wb") as f:
                        f.write(response.content)
                    logging.info(f"Asset '{filename}' downloaded.")
                    self.update_progress(filename, status, completed, len(assets_dict))
                    completed += 1
            except Exception as e:
                status = "Failed"
                self.failed_assets.append((filename, str(e)))
                logging.error(f"Asset '{filename}' failed to download/update: {e}")
                self.update_progress(filename, status, completed, len(assets_dict))
                completed += 1
                
        if self.failed_assets:
            self.show_error_message(self.failed_assets)

def download_assets(window=None):
    download_dialog = AssetDownloadDialog()
    
    def download_task():
        completed = 0
        font_url = ASSETS.get("font.ttf")
        if font_url:
            font_path = SETTINGS_DIR / "font.ttf"
            try:
                logging.info(f"Checking font asset: font.ttf")
                response = requests.get(font_url, timeout=10)
                response.raise_for_status()
                with open(font_path, "wb") as f:
                    f.write(response.content)
                font_id = QFontDatabase.addApplicationFont(str(font_path))
                if font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    if font_families:
                        QApplication.instance().setFont(QFont(font_families[0], 10))
                download_dialog.update_progress("font.ttf", "Downloaded", 1, len(ASSETS))
                completed = 1
                logging.info(f"Font asset downloaded successfully")
            except Exception as e:
                logging.error(f"Failed to download font: {e}")
                download_dialog.failed_assets.append(("font.ttf", str(e)))
                download_dialog.update_progress("font.ttf", "Failed", 1, len(ASSETS))
                completed = 1
        
        asset_items = [(filename, url) for filename, url in ASSETS.items() if filename != "font.ttf"]
        total_assets = len(asset_items)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(check_single_asset, filename, url): filename for filename, url in asset_items}
            
            for future in concurrent.futures.as_completed(futures):
                if download_dialog.download_canceled:
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                completed += 1
                filename, status, error = future.result()
                if error:
                    download_dialog.failed_assets.append((filename, error))
                download_dialog.update_progress(filename, status, completed, total_assets + 1)
        
        if download_dialog.failed_assets and not download_dialog.download_canceled:
            QTimer.singleShot(100, lambda: download_dialog.show_error_message(download_dialog.failed_assets))
        
        if not download_dialog.download_canceled:
            QTimer.singleShot(500, download_dialog.close)
    
    def check_single_asset(filename, url):
        asset_path = SETTINGS_DIR / filename
        try:
            logging.info(f"Checking asset: {filename}")
            if asset_path.exists():
                response = requests.get(url, timeout=10)
                if response.status_code in (403, 429):
                    logging.warning(f"Asset '{filename}' rate-limited with status {response.status_code}")
                    return filename, "Rate-Limited", f"Rate-limited ({response.status_code})"
                response.raise_for_status()
                remote_bytes = response.content
                with open(asset_path, "rb") as f:
                    local_bytes = f.read()
                    if local_bytes == remote_bytes:
                        logging.info(f"Asset '{filename}' is up to date.")
                        return filename, "Done", None
                with open(asset_path, "wb") as f:
                    f.write(remote_bytes)
                logging.info(f"Asset '{filename}' has been updated.")
                return filename, "Updated", None
            else:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(asset_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"Asset '{filename}' has been downloaded.")
                return filename, "Downloaded", None
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code in (403, 429):
                logging.warning(f"Asset '{filename}' rate-limited: {e}")
                return filename, "Rate-Limited", f"Rate-limited ({e.response.status_code})"
            logging.error(f"Asset '{filename}' failed to download: {e}")
            return filename, "Failed", str(e)
        except Exception as e:
            logging.error(f"Asset '{filename}' failed to download/update: {e}")
            return filename, "Failed", str(e)
    
    download_thread = threading.Thread(target=download_task, daemon=False)
    download_thread.start()
    
    download_dialog.exec()
    download_thread.join(timeout=30)
    
    if download_dialog.download_canceled:
        logging.info("Asset download was canceled, continuing with available assets")

    if window:
        window.initialize_ui()
    else:
        logging.error("Window is None, cannot initialize UI")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("An error occurred while initializing the UI. Please restart the application.")
        msg.exec()

def load_settings():
    global CONFIG_DATA
    
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                CONFIG_DATA.update(loaded_data)
            logging.info("Settings loaded from settings.json")
        except Exception as e:
            logging.error(f"Failed to load settings.json: {e}")
    elif CONFIG_FILE.exists():
        if prompt_import_legacy_settings():
            convert_legacy_settings()
        else:
            save_settings()
    else:
        save_settings()
    
    if KEYWORDS_FILE.exists():
        try:
            with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                keywords_data = json.load(f)
                custom_categories = keywords_data.get("custom_categories", [])
                for category in custom_categories:
                    setting_name = f"customcat_{category.replace(' ', '_')}"
                    if setting_name not in CONFIG_DATA:
                        CONFIG_DATA[setting_name] = False
        except:
            pass
    
    if platform.system() != "Windows":
        CONFIG_DATA["override_protocol_enabled"] = False
        CONFIG_DATA["override_protocol_path"] = ""
        CONFIG_DATA["override_protocol_type"] = ""
        CONFIG_DATA["override_protocol_version"] = ""

def prompt_import_legacy_settings():
    msg = QMessageBox()
    msg.setWindowTitle("Import Legacy Settings")
    msg.setText("Legacy settings file found. Would you like to import your settings from the old system?")
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setIcon(QMessageBox.Icon.Question)
    return msg.exec() == QMessageBox.StandardButton.Yes

def convert_legacy_settings():
    global CONFIG_DATA
    try:
        config_legacy = configparser.ConfigParser()
        config_legacy.read(CONFIG_FILE)
        
        if 'sniping' in config_legacy:
            CONFIG_DATA['token'] = config_legacy['sniping'].get('token', '')
            CONFIG_DATA['glitchsniping'] = config_legacy['sniping'].get('glitchsniping', 'False') == 'True'
            CONFIG_DATA['dreamsniping'] = config_legacy['sniping'].get('dreamsniping', 'False') == 'True'
            CONFIG_DATA['cybersniping'] = config_legacy['sniping'].get('cybersniping', 'False') == 'True'
            CONFIG_DATA['jestersniping'] = config_legacy['sniping'].get('jestersniping', 'False') == 'True'
            CONFIG_DATA['voidcoinsniping'] = config_legacy['sniping'].get('voidCoinsniping', 'False') == 'True'
            CONFIG_DATA['close_roblox_before_joining'] = config_legacy['sniping'].get('close_roblox_before_joining', 'False') == 'True'
            CONFIG_DATA['leave_game_before_joining'] = config_legacy['sniping'].get('leave_game_before_joining', 'False') == 'True'
            CONFIG_DATA['minimize_other_windows'] = config_legacy['sniping'].get('minimize_other_windows', 'False') == 'True'
            CONFIG_DATA['auto_pause_sniper'] = config_legacy['sniping'].get('auto_pause_sniper', 'True') == 'True'
            CONFIG_DATA['only_join_sols_links'] = config_legacy['sniping'].get('only_join_sols_links', 'True') == 'True'
            CONFIG_DATA['snipe_ropro_links'] = config_legacy['sniping'].get('snipe_ropro_links', 'True') == 'True'
            CONFIG_DATA['pause_duration'] = int(config_legacy['sniping'].get('pause_duration', 120))
            
            if platform.system() == "Windows":
                CONFIG_DATA['override_protocol_enabled'] = config_legacy['sniping'].get('override_protocol_enabled', 'False') == 'True'
                CONFIG_DATA['override_protocol_path'] = config_legacy['sniping'].get('override_protocol_path', '')
                CONFIG_DATA['override_protocol_type'] = config_legacy['sniping'].get('override_protocol_type', '')
            
            custom_categories = []
            for key in config_legacy['sniping']:
                if key.startswith('customcat_'):
                    if config_legacy['sniping'].get(key) in ['True', 'False']:
                        category_name = key.replace('customcat_', '').replace('_', ' ')
                        is_enabled = config_legacy['sniping'].get(key) == 'True'
                        custom_categories.append(category_name)
                        CONFIG_DATA[key] = is_enabled
        
        if 'Hotkeys' in config_legacy:
            CONFIG_DATA['open_roblox_toggle'] = config_legacy['Hotkeys'].get('open_roblox_toggle', 'True') == 'True'
            CONFIG_DATA['open_roblox'] = config_legacy['Hotkeys'].get('open_roblox', '-')
            CONFIG_DATA['stop_sniper_toggle'] = config_legacy['Hotkeys'].get('stop_sniper_toggle', 'True') == 'True'
            CONFIG_DATA['stop_sniper'] = config_legacy['Hotkeys'].get('stop_sniper', '[')
            CONFIG_DATA['toggle_sniper_toggle'] = config_legacy['Hotkeys'].get('toggle_sniper_toggle', 'True') == 'True'
            CONFIG_DATA['toggle_sniper'] = config_legacy['Hotkeys'].get('toggle_sniper', 'f4')
            CONFIG_DATA['loading_asset_skipper_toggle'] = config_legacy['Hotkeys'].get('loading_asset_skipper_toggle', 'False') == 'True'
            CONFIG_DATA['loading_asset_skipper'] = config_legacy['Hotkeys'].get('loading_asset_skipper', 'f5')
            CONFIG_DATA['main_menu_skipper_toggle'] = config_legacy['Hotkeys'].get('main_menu_skipper_toggle', 'False') == 'True'
            CONFIG_DATA['main_menu_skipper'] = config_legacy['Hotkeys'].get('main_menu_skipper', 'f6')
        
        if 'Settings' in config_legacy:
            CONFIG_DATA['toast_notifications'] = config_legacy['Settings'].get('toast_notifications', 'True') == 'True'
            CONFIG_DATA['stillbackground'] = config_legacy['Settings'].get('stillbackground', 'False') == 'True'
            CONFIG_DATA['semi_transparent_background'] = config_legacy['Settings'].get('semi_transparent_background', 'False') == 'True'
            CONFIG_DATA['gradient_theme'] = config_legacy['Settings'].get('gradient_theme', 'False') == 'True'
            CONFIG_DATA['advanced_mode'] = config_legacy['Settings'].get('advanced_mode', 'False') == 'True'
        
        save_settings()
        logging.info("Successfully migrated legacy settings and saved them to settings.json")
    except Exception as e:
        logging.error(f"Failed to convert legacy settings: {e}")

def save_settings():
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(CONFIG_DATA, f, indent=4)
        logging.info("Settings saved to settings.json")
    except Exception as e:
        logging.error(f"Failed to save settings: {e}")

def get_config(key, default=None):
    return CONFIG_DATA.get(key, default)

def get_pause_duration_for_category(category):
    if category:
        category_key = category.lower().replace(' ', '_')
        return CONFIG_DATA.get(f"pause_duration_{category_key}", 60)
    return CONFIG_DATA.get("pause_duration", 120)

def set_config(key, value):
    CONFIG_DATA[key] = value
    save_settings()

def get_installed_roblox_versions():
    versions = []
    latest_version = None
    
    if platform.system() == 'Darwin':
        roblox_app_path = Path(os.path.expanduser("~/Applications/Roblox.app/Contents/MacOS/Roblox"))
        if roblox_app_path.exists():
            versions.append({
                "name": "Roblox (macOS)",
                "path": str(roblox_app_path),
                "type": "macOS",
                "icon": str(get_app_icon(roblox_app_path))
            })
        
        app_path = Path("/Applications/Roblox.app/Contents/MacOS/Roblox")
        if app_path.exists():
            versions.append({
                "name": "Roblox (System)",
                "path": str(app_path),
                "type": "macOS",
                "icon": str(get_app_icon(app_path))
            })
        
        return versions
    
    if platform.system() != 'Windows':
        return versions
    
    try:
        response = requests.get("https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer", timeout=5)
        if response.status_code == 200:
            data = response.json()
            client_version_upload = data.get("clientVersionUpload", "")
            latest_version = client_version_upload
            
            legacy_path = Path(os.path.expanduser("~/AppData/Local/Roblox/Versions"))
            if legacy_path.exists():
                for version_dir in legacy_path.iterdir():
                    if version_dir.name == client_version_upload:
                        exe_path = version_dir / "RobloxPlayerBeta.exe"
                        if exe_path.exists():
                            versions.append({
                                "name": f"Latest Web Version ({client_version_upload.replace("version-", "")})",
                                "path": str(exe_path),
                                "type": "legacy",
                                "icon": str(get_app_icon(exe_path)),
                                "version": client_version_upload
                            })
                            break

            programfiles_path = Path(r"C:\Program Files (x86)\Roblox\Versions")
            if programfiles_path.exists():
                for version_dir in programfiles_path.iterdir():
                    if version_dir.name == client_version_upload:
                        exe_path = version_dir / "RobloxPlayerBeta.exe"
                        if exe_path.exists():
                            versions.append({
                                "name": f"Latest Web Version ({client_version_upload.replace("version-", "")})",
                                "path": str(exe_path),
                                "type": "legacy",
                                "icon": str(get_app_icon(exe_path)),
                                "version": client_version_upload
                            })
                            break
    except:
        pass
    
    legacy_path = Path(os.path.expanduser("~/AppData/Local/Roblox/Versions"))
    if legacy_path.exists():
        for version_dir in legacy_path.iterdir():
            exe_path = version_dir / "RobloxPlayerBeta.exe"
            if exe_path.exists() and exe_path not in [v["path"] for v in versions] and version_dir.name != latest_version:
                versions.append({
                    "name": f"Web Version ({version_dir.name.replace("version-", "")})",
                    "path": str(exe_path),
                    "type": "legacy",
                    "icon": str(get_app_icon(exe_path)),
                    "version": version_dir.name
                })

    programfiles_path = Path(r"C:\Program Files (x86)\Roblox\Versions")
    if programfiles_path.exists():
        for version_dir in programfiles_path.iterdir():
            exe_path = version_dir / "RobloxPlayerBeta.exe"
            if exe_path.exists() and exe_path not in [v["path"] for v in versions] and version_dir.name != latest_version:
                versions.append({
                    "name": f"Web Version ({version_dir.name.replace("version-", "")})",
                    "path": str(exe_path),
                    "type": "legacy",
                    "icon": str(get_app_icon(exe_path)),
                    "version": version_dir.name
                })
    
    bootstrappers = [
        {
            "name": "Bloxstrap",
            "paths": [
                Path(os.path.expanduser("~/AppData/Local/Bloxstrap/Bloxstrap.exe"))
            ]
        },
        {
            "name": "Fishstrap",
            "paths": [
                Path(os.path.expanduser("~/AppData/Local/Fishstrap/Fishstrap.exe"))
            ]
        }
    ]
    
    for bootstrapper in bootstrappers:
        for bootstrapper_path in bootstrapper["paths"]:
            if bootstrapper_path.exists():
                versions.append({
                    "name": bootstrapper["name"],
                    "path": str(bootstrapper_path),
                    "type": "bootstrapper",
                    "icon": str(get_app_icon(bootstrapper_path)),
                    "version": "N/A"
                })
                break
    
    return versions

def get_app_icon(exe_path):
    exe_path_lower = str(exe_path).lower()
    
    if "roblox.app" in exe_path_lower or "macos" in exe_path_lower or "local\\roblox" in exe_path_lower or "program files" in exe_path_lower:
        return "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/roblox.png"
    elif "windowsapps" in exe_path_lower:
        return "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/windows_store.png"
    elif "local\\bloxstrap" in exe_path_lower or "bloxstrap" in exe_path_lower:
        return "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/bloxstrap.png"
    elif "local\\fishstrap" in exe_path_lower or "fishstrap" in exe_path_lower:
        return "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/fishstrap.png"
    else:
        return "https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/vex.png"

def override_roblox_protocol(roblox_path, roblox_type, roblox_version):
    try:
        if platform.system() == "Darwin":
            plist_path = Path(os.path.expanduser("~/Library/Preferences/com.apple.LaunchServices.plist"))
            logging.info(f"macOS protocol override - would register {roblox_path}")
            return True
        
        key_path = r"SOFTWARE\Classes\roblox"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL: Roblox Protocol")
        
        icon_key_path = rf"{key_path}\DefaultIcon"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, icon_key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, roblox_path)
        
        command_key_path = rf"{key_path}\shell\open\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key_path) as key:
            if roblox_type == "bootstrapper":
                cmd = f'"{roblox_path}" -player "%1"'
            else:
                cmd = f'"{roblox_path}" "%1"'
            
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
        
        return True
    except Exception as e:
        logging.error(f"Failed to override Roblox protocol: {e}")
        return False

def is_roblox_protocol_overridden():
    try:
        if platform.system() == "Darwin":
            return False
        
        key_path = r"SOFTWARE\Classes\roblox\shell\open\command"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, "")
            return True
    except Exception:
        return False

def get_roblox_protocol_target():
    try:
        if platform.system() == "Darwin":
            return None
        
        key_path = r"SOFTWARE\Classes\roblox\shell\open\command"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, "")
            return value
    except Exception:
        return None

def restore_roblox_protocol():
    try:
        if platform.system() == "Darwin":
            return True
        
        key_path = r"SOFTWARE\Classes\roblox"
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"{key_path}\shell\open\command")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"{key_path}\shell\open")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"{key_path}\shell")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, rf"{key_path}\DefaultIcon")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        
        return True
    except Exception as e:
        logging.error(f"Failed to restore Roblox protocol: {e}")
        return False

class RobloxVersionDialog(QDialog):
    def __init__(self, parent=None, allow_custom=False):
        super().__init__(parent)
        self.setWindowTitle("Select Roblox Version")
        self.setFixedSize(550, 400)
        self.selected_version = None
        self.allow_custom = allow_custom
        
        layout = QVBoxLayout(self)
        
        title = QLabel("Select Roblox Version for Protocol Override")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #e0e0e0; margin-bottom: 10px;")
        layout.addWidget(title)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 6px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #4a7bff;
                color: white;
            }
        """)
        layout.addWidget(self.list_widget)
        
        self.no_versions_label = QLabel("No supported Roblox versions found.\n\nYou can:\n1. Specify an executable manually\n2. Download the official Roblox app from ")
        self.no_versions_label.setStyleSheet("font-size: 14px; color: #ff5555; padding: 20px; text-align: center;")
        self.no_versions_label.setWordWrap(True)
        self.no_versions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_versions_label.hide()
        layout.addWidget(self.no_versions_label)
        
        self.download_link = ClickableLabel("https://roblox.com/download", "https://roblox.com/download")
        self.download_link.setStyleSheet("font-size: 14px; color: #4a7bff; text-decoration: underline;")
        self.download_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_link.hide()
        layout.addWidget(self.download_link)
        
        if self.allow_custom:
            self.custom_btn = QPushButton("Browse Custom Executable...")
            self.custom_btn.setFixedHeight(35)
            self.custom_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8a4caf;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #9a5cbf;
                }
            """)
            self.custom_btn.clicked.connect(self.browse_custom_executable)
            layout.addWidget(self.custom_btn)
        
        button_layout = QHBoxLayout()
        self.assign_btn = QPushButton("Select")
        self.assign_btn.setFixedHeight(35)
        self.assign_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a7bff;
                color: white;
                font-weight: 500;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5a8bff;
            }
            QPushButton:disabled {
                background-color: #3a5baf;
            }
        """)
        self.assign_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(35)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                font-weight: 500;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.assign_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.load_roblox_versions()
    
    def load_roblox_versions(self):
        versions = get_installed_roblox_versions()
        
        if not versions:
            self.list_widget.hide()
            self.no_versions_label.show()
            self.download_link.show()
            if hasattr(self, 'custom_btn'):
                self.custom_btn.setEnabled(True)
            self.assign_btn.setEnabled(False)
        else:
            self.no_versions_label.hide()
            self.download_link.hide()
            self.list_widget.show()
            
            for version in versions:
                item = QListWidgetItem(" " + version["name"])
                item.setData(Qt.ItemDataRole.UserRole, version)
                
                try:
                    icon_source = version["icon"]
                    response = requests.get(icon_source, timeout=5)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        icon = QIcon(pixmap)
                        item.setIcon(icon)
                except Exception as e:
                    logging.warning(f"Failed to load icon for {version['name']}: {e}")
                
                self.list_widget.addItem(item)
            
            self.list_widget.setCurrentRow(0)
            self.assign_btn.setEnabled(True)
            if hasattr(self, 'custom_btn'):
                self.custom_btn.setEnabled(True)
    
    def browse_custom_executable(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Roblox Executable",
            "",
            "Executable Files (*.exe);;All Files (*)"
        )
        
        if file_path and Path(file_path).exists():
            custom_version = {
                "name": f"Custom: {Path(file_path).name}",
                "path": file_path,
                "type": "custom",
                "icon": file_path
            }
            
            item = QListWidgetItem(custom_version["name"])
            item.setData(Qt.ItemDataRole.UserRole, custom_version)
            
            try:
                icon = QIcon(file_path)
                item.setIcon(icon)
            except:
                pass
            
            if self.list_widget.isHidden():
                self.list_widget.show()
                self.no_versions_label.hide()
                self.download_link.hide()
            
            self.list_widget.addItem(item)
            self.list_widget.setCurrentRow(self.list_widget.count() - 1)
            self.assign_btn.setEnabled(True)
    
    def get_selected_version(self):
        items = self.list_widget.selectedItems()
        if items:
            return items[0].data(Qt.ItemDataRole.UserRole)
        return None

class SnakeGame(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("sneaky snake")
        self.grid_size = 48
        self.grid_width = 15
        footer_height = 70
        self.grid_height = 12
        self.game_width = self.grid_width * self.grid_size
        self.game_height = self.grid_height * self.grid_size
        self.setFixedSize(self.game_width, self.game_height + footer_height)
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.directions = [(1, 0)]
        self.foods = []
        self.score = 0
        self.game_over = False
        self.pending_direction = (1, 0)
        self.last_direction = (1, 0)

        self.fruit_images = {}
        for name in ("yeswe", "solsniper", "vex"):
            img_path = SETTINGS_DIR / f"{name}.png"
            if img_path.exists():
                self.fruit_images[name] = QPixmap(str(img_path)).scaled(self.grid_size, self.grid_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        seg_path = SETTINGS_DIR / "snipercat.png"
        self.snake_segment = QPixmap(str(seg_path)).scaled(self.grid_size, self.grid_size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation) if seg_path.exists() else None

        for _ in range(5):
            self.foods.append(self.generate_food())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(33)

        self.animating = False
        self.anim_progress = 1.0
        self.anim_duration = 0.13
        self.anim_start_time = None
        self.anim_from = None
        self.anim_to = None
        self.anim_direction = None
        self.anim_tail_from = None
        self.anim_tail_to = None
        self.anim_snake_positions = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.score_label = QLabel(f"Score: {self.score}")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFixedHeight(40)
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold; background-color: #252525; border-top: 2px solid #4a7bff;")

        self.instructions = QLabel("Use WASD or Arrow Keys • Press R to restart")
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions.setFixedHeight(30)
        self.instructions.setStyleSheet("font-size: 13px; color: #888; background-color: #252525;")

        layout.addStretch()
        layout.addWidget(self.score_label)
        layout.addWidget(self.instructions)
        self.setLayout(layout)

        self.game_area_y = 0

        self.game_over_label = QLabel("GAME OVER!\nPress R to restart")
        self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_over_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ff5555; background-color: rgba(0,0,0,0.8); border: 3px solid #ff5555; border-radius: 10px; padding: 16px;")
        self.game_over_label.setFixedSize(520, 140)
        self.game_over_label.setParent(self)
        self.game_over_label.hide()

    def generate_food(self):
        while True:
            food_pos = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
            if all(food_pos != f[0] for f in self.foods) and food_pos not in self.snake:
                fruit_key = random.choice(list(self.fruit_images.keys())) if self.fruit_images else None
                fruit_pixmap = self.fruit_images.get(fruit_key) if fruit_key else None
                return (food_pos, fruit_key, fruit_pixmap)

    def keyPressEvent(self, event):
        if self.game_over:
            if event.key() in [Qt.Key.Key_R, Qt.Key.Key_Space]:
                self.restart_game()
            return

        key = event.key()
        current_direction = self.pending_direction
        snake_len = len(self.snake)

        requested_direction = None
        if key in [Qt.Key.Key_W, Qt.Key.Key_Up]:
            requested_direction = (0, -1)
        elif key in [Qt.Key.Key_S, Qt.Key.Key_Down]:
            requested_direction = (0, 1)
        elif key in [Qt.Key.Key_A, Qt.Key.Key_Left]:
            requested_direction = (-1, 0)
        elif key in [Qt.Key.Key_D, Qt.Key.Key_Right]:
            requested_direction = (1, 0)

        if requested_direction and (requested_direction != tuple(-x for x in current_direction) or snake_len == 1):
            if self.animating:
                progress = self.anim_progress
                if progress >= 0.7:
                    self.anim_progress = 1.0
                    self.animating = False
                    self.snake.insert(0, self.anim_to)
                    food_eaten = False
                    for i, (food_pos, _, _) in enumerate(self.foods):
                        if self.anim_to == food_pos:
                            self.score += 1
                            self.foods.pop(i)
                            self.foods.append(self.generate_food())
                            food_eaten = True
                            self.score_label.setText(f"Score: {self.score}")
                            break
                    if not food_eaten:
                        self.snake.pop()
                        self.directions.pop()
                    self.directions.insert(0, self.anim_direction)
                    self.last_direction = self.anim_direction
                    self.update()
                    self.pending_direction = requested_direction
                    self.update_game()
                    return
            self.pending_direction = requested_direction

    def update_game(self):
        if self.game_over:
            return

        if self.animating:
            elapsed = time.time() - self.anim_start_time
            self.anim_progress = min(elapsed / self.anim_duration, 1.0)
            if self.anim_progress >= 1.0:
                self.animating = False
                self.anim_progress = 1.0
                self.snake.insert(0, self.anim_to)
                food_eaten = False
                for i, (food_pos, _, _) in enumerate(self.foods):
                    if self.anim_to == food_pos:
                        self.score += 1
                        self.foods.pop(i)
                        self.foods.append(self.generate_food())
                        food_eaten = True
                        self.score_label.setText(f"Score: {self.score}")
                        break
                if not food_eaten:
                    self.snake.pop()
                    self.directions.pop()
                self.directions.insert(0, self.anim_direction)
                self.last_direction = self.anim_direction
            self.update()
            return

        self.directions.insert(0, self.pending_direction)
        if len(self.directions) > len(self.snake):
            self.directions.pop()

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.directions[0][0], head_y + self.directions[0][1])

        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height or
            new_head in self.snake):
            self.end_game()
            return

        self.anim_snake_positions = [tuple(seg) for seg in self.snake]
        self.animating = True
        self.anim_progress = 0.0
        self.anim_start_time = time.time()
        self.anim_from = self.snake[0]
        self.anim_to = new_head
        self.anim_direction = self.directions[0]
        self.last_direction = self.anim_direction
        self.update()

    def end_game(self):
        self.game_over = True
        self.timer.stop()
        x = (self.width() - self.game_over_label.width()) // 2
        y = self.game_area_y + (self.game_height // 2) - (self.game_over_label.height() // 2)
        self.game_over_label.move(x, y)
        self.game_over_label.show()
        self.game_over_label.raise_()

    def restart_game(self):
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.directions = [(1, 0)]
        self.pending_direction = (1, 0)
        self.last_direction = (1, 0)
        self.foods = []
        for _ in range(5):
            self.foods.append(self.generate_food())
        self.score = 0
        self.game_over = False
        self.game_over_label.hide()
        self.timer.start(33)
        self.animating = False
        self.anim_progress = 1.0
        self.update()
        self.score_label.setText(f"Score: {self.score}")

    def get_rotation_angle(self, direction):
        if direction == (1, 0): return 0
        if direction == (0, 1): return 90
        if direction == (-1, 0): return 180
        if direction == (0, -1): return 270
        return 0

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        game_area_y = self.game_area_y
        painter.fillRect(0, game_area_y, self.game_width, self.game_height, QBrush(QColor(20, 20, 20)))

        painter.setPen(QColor(40, 40, 40))
        for x in range(0, self.game_width, self.grid_size):
            painter.drawLine(x, game_area_y, x, game_area_y + self.game_height)
        for y in range(game_area_y, game_area_y + self.game_height, self.grid_size):
            painter.drawLine(0, y, self.game_width, y)

        if self.animating and self.snake_segment:
            fx, fy = self.anim_from
            tx, ty = self.anim_to
            dx = tx - fx
            dy = ty - fy
            interp_x = fx + dx * self.anim_progress
            interp_y = fy + dy * self.anim_progress
            rect_x = int(interp_x * self.grid_size)
            rect_y = int(interp_y * self.grid_size + game_area_y)
            angle = self.get_rotation_angle(self.anim_direction)
            transform = QTransform()
            transform.translate(rect_x + self.grid_size // 2, rect_y + self.grid_size // 2)
            transform.rotate(angle)
            transform.translate(-self.grid_size // 2, -self.grid_size // 2)
            painter.save()
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(255, 255, 0), 6))
            painter.drawRect(rect_x, rect_y, self.grid_size, self.grid_size)
            painter.restore()
            rotated_pixmap = self.snake_segment.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(rect_x, rect_y, rotated_pixmap)

            for i in range(1, len(self.anim_snake_positions)):
                fx, fy = self.anim_snake_positions[i]
                tx, ty = self.anim_snake_positions[i - 1]
                interp_x = fx + (tx - fx) * self.anim_progress
                interp_y = fy + (ty - fy) * self.anim_progress
                rect_x = int(interp_x * self.grid_size)
                rect_y = int(interp_y * self.grid_size + game_area_y)
                direction = self.directions[i] if i < len(self.directions) else self.directions[-1]
                angle = self.get_rotation_angle(direction)
                transform = QTransform()
                transform.translate(rect_x + self.grid_size // 2, rect_y + self.grid_size // 2)
                transform.rotate(angle)
                transform.translate(-self.grid_size // 2, -self.grid_size // 2)
                rotated_pixmap = self.snake_segment.transformed(transform, Qt.TransformationMode.SmoothTransformation)
                if i == len(self.anim_snake_positions) - 1:
                    painter.save()
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.setPen(QPen(QColor(74, 123, 255), 4))
                    painter.drawRect(rect_x, rect_y, self.grid_size, self.grid_size)
                    painter.restore()
                painter.drawPixmap(rect_x, rect_y, rotated_pixmap)
        else:
            for i, (x, y) in enumerate(self.snake):
                rect_x = int(x * self.grid_size)
                rect_y = int(y * self.grid_size + game_area_y)
                if self.snake_segment:
                    direction = self.directions[i] if i < len(self.directions) else self.directions[-1]
                    angle = self.get_rotation_angle(direction)
                    transform = QTransform()
                    transform.translate(rect_x + self.grid_size // 2, rect_y + self.grid_size // 2)
                    transform.rotate(angle)
                    transform.translate(-self.grid_size // 2, -self.grid_size // 2)
                    rotated_pixmap = self.snake_segment.transformed(transform, Qt.TransformationMode.SmoothTransformation)
                    if i == 0:
                        painter.save()
                        painter.setBrush(Qt.BrushStyle.NoBrush)
                        painter.setPen(QPen(QColor(255, 255, 0), 6))
                        painter.drawRect(rect_x, rect_y, self.grid_size, self.grid_size)
                        painter.restore()
                    if i == len(self.snake) - 1:
                        painter.save()
                        painter.setBrush(Qt.BrushStyle.NoBrush)
                        painter.setPen(QPen(QColor(74, 123, 255), 4))
                        painter.drawRect(rect_x, rect_y, self.grid_size, self.grid_size)
                        painter.restore()
                    painter.drawPixmap(rect_x, rect_y, rotated_pixmap)
                else:
                    painter.setBrush(QBrush(QColor(255, 255, 0) if i == 0 else QColor(138, 76, 175)))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRect(rect_x, rect_y, self.grid_size, self.grid_size)

        for food_pos, fruit_key, fruit_pixmap in self.foods:
            food_x, food_y = food_pos
            rect_x = int(food_x * self.grid_size)
            rect_y = int(food_y * self.grid_size + game_area_y)
            if fruit_pixmap:
                painter.drawPixmap(rect_x, rect_y, fruit_pixmap)
            else:
                painter.setBrush(QBrush(QColor(255, 100, 100)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(rect_x, rect_y, self.grid_size, self.grid_size)

        painter.setPen(QColor(74, 123, 255))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(0, game_area_y, self.game_width, self.game_height)
        painter.end()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

class StarryBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.star_layers = []
        self.last_window_pos = QPoint(0, 0)
        self.current_offset = QPoint(0, 0)
        self.target_window_pos = QPoint(0, 0)
        self.update_interval = 33
        self.generate_optimized_star_layers()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.smooth_update)
        self.update_timer.start(self.update_interval)
        self.cached_star_positions = []

    def get_window_pos(self):
        return self.window().pos() if self.window() else QPoint(0, 0)

    def generate_optimized_star_layers(self):
        self.star_layers.clear()
        screen_geometry = QApplication.primaryScreen().geometry()
        
        layer_configs = [
            (700, 0.3, 40, (1, 2)),
            (600, 0.5, 80, (1, 4)),
            (500, 0.7, 120, (3, 5)),
            (400, 1.0, 180, (5, 7)),
        ]
        
        for star_count, speed_factor, base_brightness, size_range in layer_configs:
            layer_stars = []
            for _ in range(star_count):
                size = random.randint(size_range[0], size_range[1])
                brightness = base_brightness + random.randint(-15, 15)
                brightness = max(40, min(255, brightness))
                x = random.randint(-500, screen_geometry.width() + 500)
                y = random.randint(-500, screen_geometry.height() + 500)
                layer_stars.append((x, y, size, brightness, speed_factor))
            self.star_layers.append(layer_stars)

    def smooth_update(self):
        current_pos = self.get_window_pos()
        if current_pos != self.target_window_pos:
            self.target_window_pos = current_pos
            dx = self.last_window_pos.x() - current_pos.x()
            dy = self.last_window_pos.y() - current_pos.y()
            if abs(dx) > 2 or abs(dy) > 2:
                self.current_offset += QPoint(dx, dy)
                self.last_window_pos = current_pos
                self.update_cached_star_positions()
                self.update()

    def update_cached_star_positions(self):
        self.cached_star_positions = []
        width, height = self.width(), self.height()
        
        for layer_stars in self.star_layers:
            layer_positions = []
            for x, y, size, brightness, speed_factor in layer_stars:
                parallax_x = self.current_offset.x() * speed_factor
                parallax_y = self.current_offset.y() * speed_factor
                star_x = x + parallax_x - self.last_window_pos.x() * speed_factor
                star_y = y + parallax_y - self.last_window_pos.y() * speed_factor
                
                if (-50 <= star_x <= width + 50 and -50 <= star_y <= height + 50):
                    alpha = int(0.7 * 255)
                    if speed_factor <= 0.5:
                        color = (int(brightness * 0.7), int(brightness * 0.8), brightness, alpha)
                    elif speed_factor <= 0.7:
                        color = (int(brightness * 0.9), int(brightness * 0.95), brightness, alpha)
                    else:
                        color = (brightness, brightness, brightness, alpha)
                    
                    layer_positions.append((star_x, star_y, size, color, speed_factor))
            self.cached_star_positions.append(layer_positions)

    def paintEvent(self, event):
        if not self.cached_star_positions:
            self.update_cached_star_positions()
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        alpha = int(0.7 * 255) if CONFIG_DATA["semi_transparent_background"] == True else 255
        painter.fillRect(self.rect(), QColor(0, 0, 0, alpha))
        painter.setPen(Qt.PenStyle.NoPen)

        for layer in self.cached_star_positions:
            for star_x, star_y, size, color, speed_factor in layer:
                r, g, b, a = color
                painter.setBrush(QBrush(QColor(r, g, b, a)))
                painter.drawEllipse(int(star_x), int(star_y), size, size)

    def update_star_positions(self):
        current_pos = self.get_window_pos()
        dx = self.last_window_pos.x() - current_pos.x()
        dy = self.last_window_pos.y() - current_pos.y()
        if abs(dx) > 1 or abs(dy) > 1:
            self.current_offset += QPoint(dx, dy)
            self.last_window_pos = current_pos
            self.target_window_pos = current_pos
            self.update_cached_star_positions()
            self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_cached_star_positions()
        self.update()

    def set_performance_mode(self, low_performance=True):
        if low_performance:
            self.update_interval = 50
            self.update_timer.setInterval(self.update_interval)
        else:
            self.update_interval = 33
            self.update_timer.setInterval(self.update_interval)
        self.generate_optimized_star_layers()

class StarryBackgroundStill(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.star_layers = []
        self.generate_optimized_star_layers()
        self.cached_star_positions = []
        self.update_cached_star_positions()

    def generate_optimized_star_layers(self):
        self.star_layers.clear()
        screen_geometry = QApplication.primaryScreen().geometry()
        
        layer_configs = [
            (400, 0.3, 40, (1, 2)),
            (300, 0.5, 80, (1, 4)),
            (200, 0.7, 120, (3, 5)),
            (100, 1.0, 180, (5, 7)),
        ]
        
        for star_count, speed_factor, base_brightness, size_range in layer_configs:
            layer_stars = []
            for _ in range(star_count):
                size = random.randint(size_range[0], size_range[1])
                brightness = base_brightness + random.randint(-15, 15)
                brightness = max(40, min(255, brightness))
                x = random.randint(0, screen_geometry.width())
                y = random.randint(0, screen_geometry.height())
                layer_stars.append((x, y, size, brightness, speed_factor))
            self.star_layers.append(layer_stars)

    def update_cached_star_positions(self):
        self.cached_star_positions = []
        width, height = self.width(), self.height()
        
        for layer_stars in self.star_layers:
            layer_positions = []
            for x, y, size, brightness, speed_factor in layer_stars:
                star_x = x
                star_y = y
                
                if (0 <= star_x <= width and 0 <= star_y <= height):
                    alpha = int(0.7 * 255)
                    if speed_factor <= 0.5:
                        color = (int(brightness * 0.7), int(brightness * 0.8), brightness, alpha)
                    elif speed_factor <= 0.7:
                        color = (int(brightness * 0.9), int(brightness * 0.95), brightness, alpha)
                    else:
                        color = (brightness, brightness, brightness, alpha)
                    
                    layer_positions.append((star_x, star_y, size, color, speed_factor))
            self.cached_star_positions.append(layer_positions)

    def paintEvent(self, event):
        if not self.cached_star_positions:
            self.update_cached_star_positions()
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        alpha = int(0.7 * 255) if CONFIG_DATA["semi_transparent_background"] == True else 255
        painter.fillRect(self.rect(), QColor(0, 0, 0, alpha))
        painter.setPen(Qt.PenStyle.NoPen)

        for layer in self.cached_star_positions:
            for star_x, star_y, size, color, speed_factor in layer:
                r, g, b, a = color
                painter.setBrush(QBrush(QColor(r, g, b, a)))
                painter.drawEllipse(int(star_x), int(star_y), size, size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_cached_star_positions()
        self.update()

    def update_star_positions(self):
        return

class GradientFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background: transparent;
            border-radius: 12px;
        """)
        self.start_color = QColor(74, 123, 255, 180)
        self.end_color = QColor(138, 76, 175, 180)
        self.angle = 45

    def paintEvent(self, event):
        if gradient_theme_persist == True:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, self.start_color)
            gradient.setColorAt(1, self.end_color)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect(), 12, 12)
            painter.end()
        else:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QBrush(self.start_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect(), 12, 12)
            painter.end()

class ModernTitleBar(QWidget):
    def __init__(self, parent, is_main_window=False):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        logo = QLabel()
        logo_pixmap = QPixmap(str(SETTINGS_DIR / "snipercat.png"))
        rounded = QPixmap(30, 30)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 30, 30, 8, 8)
        painter.setClipPath(path)
        scaled = logo_pixmap.scaled(30, 30, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        logo.setPixmap(rounded)
        logo.setStyleSheet("background-color: transparent;")
        logo.setCursor(Qt.CursorShape.ArrowCursor)
        logo.mousePressEvent = lambda event: self.parent.open_snake_game()
        layout.addWidget(logo)

        beta_version_text = f" [BETA {BETA_VERSION}]" if IS_BETA_VERSION else ""
        pre_release_text = f" [PRE-RELEASE {PRE_RELEASE_VERSION}]" if IS_PRE_RELEASE else "" 
        self.title = QLabel(f"Sol Sniper V{CURRENT_VERSION}{beta_version_text}{pre_release_text}")
        self.title.setStyleSheet("font-size: 17px; font-weight: 600; color: #e0e0e0; background-color: transparent; margin-left: 4px;")
        layout.addWidget(self.title)
        
        layout.addStretch()

        if is_main_window:
            self.question_btn = QPushButton("?")
            self.question_btn.setFixedSize(30, 30)
            self.question_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3a3a3a;
                    color: #e0e0e0;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 14px;
                    padding-bottom: 2px;  /* nudges text down */
                    text-align: center;   /* keeps text centered */
                }
                QPushButton:hover {
                    background-color: #444;
                }
            """)
            self.question_btn.clicked.connect(self.parent.show_help_menu)
        
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(30, 30)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                padding-bottom: 2px;  /* nudges text down */
                text-align: center;   /* keeps text centered */
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        self.min_btn.clicked.connect(self.parent.showMinimized)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                padding-bottom: 2px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)
        self.close_btn.clicked.connect(self.parent.close)

        layout.addStretch()
        layout.addSpacing(4)
        if is_main_window:
            layout.addWidget(self.question_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.min_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        
        if is_main_window:
            layout.addWidget(self.question_btn)
        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)
        self.setStyleSheet("background-color: #1a1a1a;")

class KeywordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyword Selection")
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Keyword List", "Status"])
        self.tree.setColumnWidth(0, 300)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tree)
        
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add List")
        self.remove_btn = QPushButton("Remove List")
        self.save_btn = QPushButton("Save")
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.remove_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)
        
        self.add_btn.clicked.connect(self.add_keyword_list)
        self.remove_btn.clicked.connect(self.remove_keyword_list)
        self.save_btn.clicked.connect(self.save_keywords)
        self.load_keywords()
        
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 4px;
                border: none;
            }
        """)
    
    def load_keywords(self):
        self.tree.clear()
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        keywords = data
                    else:
                        keywords = data.get("keywords", [])
                    
                    for kw in keywords:
                        item = QTreeWidgetItem(self.tree)
                        item.setText(0, kw['name'])
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            except:
                pass
        else:
            with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                json.dump({"keywords": [], "custom_categories": []}, f)

    def add_keyword_list(self):
        item = QTreeWidgetItem(self.tree)
        item.setText(0, "New Keyword List")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.tree.addTopLevelItem(item)
    
    def remove_keyword_list(self):
        item = self.tree.currentItem()
        if item:
            index = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(index)
    
    def save_keywords(self):
        keywords = []
        custom_categories = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            keyword_name = item.text(0)
            keywords.append({
                "name": keyword_name,
                "ids": []
            })
            if keyword_name not in ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]:
                custom_categories.append(keyword_name)
        
        existing_data = {}
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, dict) and "custom_categories" in existing_data:
                        existing_cats = existing_data.get("custom_categories", [])
                        custom_categories = list(set(custom_categories + existing_cats))
            except:
                pass
        
        data_to_save = {
            "keywords": keywords,
            "custom_categories": custom_categories
        }
        
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4)
        self.accept()

class HeaderWithPlus(QHeaderView):
    def __init__(self, orientation, parent, plus_callback):
        super().__init__(orientation, parent)
        self.plus_callback = plus_callback
        self.setSectionsClickable(True)
        self._plus_rects = {}
        self.setDefaultSectionSize(int(self.defaultSectionSize() * 1.75))

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        btn_size = 18
        x = rect.right() - btn_size - 6
        y = rect.center().y() - btn_size // 2
        plus_rect = QRect(x, y, btn_size, btn_size)
        self._plus_rects[logicalIndex] = plus_rect

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#4a7bff")))
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        painter.drawText(plus_rect, Qt.AlignmentFlag.AlignCenter, "+")
        painter.restore()

    def mousePressEvent(self, event):
        for col, rect in self._plus_rects.items():
            if rect.contains(event.pos()):
                self.plus_callback(col)
                return
        super().mousePressEvent(event)

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(int(size.height()))
        return size

class AddKeywordDialog(QDialog):
    def __init__(self, category, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Keyword to {category}")
        self.setModal(True)
        self.resize(300, 120)
        layout = QVBoxLayout(self)
        self.label = QLabel(f"Enter keyword for {category}:")
        layout.addWidget(self.label)
        self.input = QLineEdit()
        layout.addWidget(self.input)
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
    def get_keyword(self):
        return self.input.text().strip()

class KeywordExportDialog(QDialog):
    def __init__(self, parent=None, keywords_data=None):
        super().__init__(parent)
        self.setWindowTitle("Export Keywords & Blacklists")
        self.setModal(True)
        self.resize(650, 550)
        self.keywords_data = keywords_data or {}
        self.category_checks = {}
        self.advanced_mode = CONFIG_DATA.get("advanced_mode", False)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Select items to export:")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #e0e0e0;")
        layout.addWidget(title)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Item"])
        self.tree.setColumnCount(1)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                outline: none;
            }
            QHeaderView {
                background-color: #3c3c3c;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 8px;
                border: none;
            }
            QTreeWidget::item {
                height: 28px;
                padding: 4px;
                border-bottom: 1px solid #3a3a3a;
            }
        """)

        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = self.keywords_data.get("custom_categories", [])
        all_categories = base_categories + custom_categories

        blacklist_base = ["Global"] + base_categories
        blacklist_categories = blacklist_base + custom_categories

        for category in all_categories:
            cat_item = QTreeWidgetItem()
            cat_check = QCheckBox()
            cat_check.setChecked(True)
            cat_check.setStyleSheet("color: #e0e0e0;")
            self.tree.addTopLevelItem(cat_item)
            self.tree.setItemWidget(cat_item, 0, self.create_category_widget(category, cat_check))

            self.category_checks[category] = {"check": cat_check, "keywords": {}, "blacklist": {}, "regex": None}

            keywords = self.keywords_data.get("keywords", {}).get(category, [])
            if keywords:
                kw_item = QTreeWidgetItem(cat_item)
                kw_item.setExpanded(False)
                kw_check = QCheckBox()
                kw_check.setChecked(True)
                kw_check.setStyleSheet("color: #e0e0e0;")
                self.tree.setItemWidget(kw_item, 0, self.create_check_widget("Keywords", kw_check))
                self.category_checks[category]["keywords_check"] = kw_check
                cat_item.addChild(kw_item)

                for kw in keywords:
                    kw_child_item = QTreeWidgetItem(kw_item)
                    kw_check = QCheckBox()
                    kw_check.setChecked(True)
                    kw_check.setStyleSheet("color: #e0e0e0;")
                    self.tree.setItemWidget(kw_child_item, 0, self.create_keyword_widget(kw, kw_check))
                    self.category_checks[category]["keywords"][kw] = kw_check
                    kw_item.addChild(kw_child_item)

            blacklist = self.keywords_data.get("blacklist", {}).get(category, [])
            if blacklist:
                bl_item = QTreeWidgetItem(cat_item)
                bl_item.setExpanded(False)
                bl_check = QCheckBox()
                bl_check.setChecked(True)
                bl_check.setStyleSheet("color: #e0e0e0;")
                self.tree.setItemWidget(bl_item, 0, self.create_check_widget("Blacklist", bl_check))
                self.category_checks[category]["blacklist_check"] = bl_check
                cat_item.addChild(bl_item)

                for bl in blacklist:
                    bl_child_item = QTreeWidgetItem(bl_item)
                    bl_check = QCheckBox()
                    bl_check.setChecked(True)
                    bl_check.setStyleSheet("color: #e0e0e0;")
                    self.tree.setItemWidget(bl_child_item, 0, self.create_keyword_widget(bl, bl_check))
                    self.category_checks[category]["blacklist"][bl] = bl_check
                    bl_item.addChild(bl_child_item)

            if self.advanced_mode:
                regex_data = self.keywords_data.get("regex", {}).get(category)
                if regex_data:
                    regex_item = QTreeWidgetItem(cat_item)
                    regex_item.setExpanded(False)
                    regex_check = QCheckBox()
                    regex_check.setChecked(True)
                    regex_check.setStyleSheet("color: #e0e0e0;")
                    self.tree.setItemWidget(regex_item, 0, self.create_check_widget("Regex", regex_check))
                    self.category_checks[category]["regex"] = regex_check
                    cat_item.addChild(regex_item)

        for category in blacklist_categories:
            if category in self.category_checks:
                continue
            cat_item = QTreeWidgetItem()
            cat_check = QCheckBox()
            cat_check.setChecked(True)
            cat_check.setStyleSheet("color: #e0e0e0;")
            self.tree.addTopLevelItem(cat_item)
            self.tree.setItemWidget(cat_item, 0, self.create_category_widget(category, cat_check))

            self.category_checks[category] = {"check": cat_check, "keywords": {}, "blacklist": {}, "regex": None}

            blacklist = self.keywords_data.get("blacklist", {}).get(category, [])
            if blacklist:
                bl_item = QTreeWidgetItem(cat_item)
                bl_item.setExpanded(False)
                bl_check = QCheckBox()
                bl_check.setChecked(True)
                bl_check.setStyleSheet("color: #e0e0e0;")
                self.tree.setItemWidget(bl_item, 0, self.create_check_widget("Blacklist", bl_check))
                self.category_checks[category]["blacklist_check"] = bl_check
                cat_item.addChild(bl_item)

                for bl in blacklist:
                    bl_child_item = QTreeWidgetItem(bl_item)
                    bl_check = QCheckBox()
                    bl_check.setChecked(True)
                    bl_check.setStyleSheet("color: #e0e0e0;")
                    self.tree.setItemWidget(bl_child_item, 0, self.create_keyword_widget(bl, bl_check))
                    self.category_checks[category]["blacklist"][bl] = bl_check
                    bl_item.addChild(bl_child_item)

        self.tree.expandAll()
        self.tree.collapseAll()
        for i in range(self.tree.topLevelItemCount()):
            self.tree.expandItem(self.tree.topLevelItem(i))

        layout.addWidget(self.tree)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        button_stylesheet = """
            QPushButton {
                background-color: #4a7bff;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 6px 20px;
            }
            QPushButton:hover {
                background-color: #5a8bff;
            }
        """
        if CONFIG_DATA.get("gradient_theme", True):
            button_stylesheet = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 6px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """

        for btn in buttons.buttons():
            btn.setStyleSheet(button_stylesheet)

        layout.addWidget(buttons)

    def create_category_widget(self, category, checkbox):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(checkbox)
        label = QLabel(category)
        label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        layout.addWidget(label)
        layout.addStretch()
        return widget

    def create_check_widget(self, label, checkbox):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(checkbox)
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(label_widget)
        layout.addStretch()
        return widget

    def create_keyword_widget(self, keyword, checkbox):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(checkbox)
        label = QLabel(keyword)
        label.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(label)
        layout.addStretch()
        return widget

    def get_selected_data(self):
        selection = {"keywords": {}, "blacklist": {}, "regex": {}, "custom_categories": []}

        for category, checks in self.category_checks.items():
            if not checks["check"].isChecked():
                continue

            if category in self.keywords_data.get("custom_categories", []):
                selection["custom_categories"].append(category)

            if "keywords_check" in checks and checks["keywords_check"].isChecked():
                selected_keywords = [kw for kw, check in checks["keywords"].items() if check.isChecked()]
                if selected_keywords:
                    selection["keywords"][category] = selected_keywords

            if "blacklist_check" in checks and checks["blacklist_check"].isChecked():
                selected_blacklist = [bl for bl, check in checks["blacklist"].items() if check.isChecked()]
                if selected_blacklist:
                    selection["blacklist"][category] = selected_blacklist

            if self.advanced_mode and checks["regex"] and checks["regex"].isChecked():
                regex_data = self.keywords_data.get("regex", {}).get(category)
                if regex_data:
                    selection["regex"][category] = regex_data

        return selection

class ServerExportDialog(QDialog):
    def __init__(self, parent=None, servers_data=None):
        super().__init__(parent)
        self.setWindowTitle("Export Servers")
        self.setModal(True)
        self.resize(600, 500)
        self.servers_data = servers_data if isinstance(servers_data, list) else servers_data.get("servers", []) if servers_data else []
        self.server_checks = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Select servers and channels to export:")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #e0e0e0;")
        layout.addWidget(title)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Server"])
        self.tree.setColumnCount(1)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                outline: none;
            }
            QHeaderView {
                background-color: #3c3c3c;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 8px;
                border: none;
            }
            QTreeWidget::item {
                height: 28px;
                padding: 4px;
                border-bottom: 1px solid #3a3a3a;
            }
        """)
        
        if len(self.servers_data) == 0:
            no_servers = QTreeWidgetItem(["No servers available"])
            no_servers.setFlags(no_servers.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.tree.addTopLevelItem(no_servers)
        else:
            for server in self.servers_data:
                server_id = server.get('id')
                server_name = server.get('name', 'Unknown')
                
                srv_item = QTreeWidgetItem()
                srv_check = QCheckBox()
                srv_check.setChecked(True)
                srv_check.setStyleSheet("color: #e0e0e0;")
                self.tree.addTopLevelItem(srv_item)
                self.tree.setItemWidget(srv_item, 0, self.create_server_widget(server_name, srv_check))
                
                self.server_checks[server_id] = {"check": srv_check, "channels": {}}
                
                channels = server.get('channels', [])
                if channels:
                    for channel in channels:
                        channel_id = channel.get('id')
                        channel_name = channel.get('name', 'Unknown')
                        
                        ch_item = QTreeWidgetItem(srv_item)
                        ch_check = QCheckBox()
                        ch_check.setChecked(True)
                        ch_check.setStyleSheet("color: #e0e0e0;")
                        self.tree.setItemWidget(ch_item, 0, self.create_channel_widget(channel_name, ch_check))
                        self.server_checks[server_id]["channels"][channel_id] = ch_check
                        srv_item.addChild(ch_item)

        self.tree.expandAll()
        layout.addWidget(self.tree)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        button_stylesheet = """
            QPushButton {
                background-color: #4a7bff;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 6px 20px;
            }
            QPushButton:hover {
                background-color: #5a8bff;
            }
        """
        
        if CONFIG_DATA.get("gradient_theme", True):
            button_stylesheet = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 6px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """
        
        for btn in buttons.buttons():
            btn.setStyleSheet(button_stylesheet)
        
        layout.addWidget(buttons)

    def create_server_widget(self, name, checkbox):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(checkbox)
        label = QLabel(name)
        label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        layout.addWidget(label)
        layout.addStretch()
        return widget

    def create_channel_widget(self, name, checkbox):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(checkbox)
        label = QLabel(name)
        label.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(label)
        layout.addStretch()
        return widget

    def get_selected_servers(self):
        selection = {}
        
        for server_id, checks in self.server_checks.items():
            srv_check = checks["check"]
            if srv_check.isChecked():
                selected_channels = [ch_id for ch_id, check in checks["channels"].items() if check.isChecked()]
                selection[server_id] = selected_channels
        
        return selection

class ClickableLabel(QLabel):
    def __init__(self, text, url, parent=None):
        super().__init__(text, parent)
        self.url = url
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            webbrowser.open(self.url)
        super().mousePressEvent(event)

class UpdateAvailableDialog(QDialog):
    def __init__(self, parent=None, latest_version="", current_version="", forced=False):
        super().__init__(parent)
        self.latest_version = latest_version
        self.current_version = current_version
        self.forced = forced
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Update Available")
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_bar = ModernTitleBar(self)
        title_bar.title.setText("Update Available")
        layout.addWidget(title_bar)

        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        message = QLabel(f"A new version ({self.latest_version}) is available.\nCurrent version: {self.current_version}.\nDo you want to install it now?")
        message.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        message.setWordWrap(True)
        content_layout.addWidget(message)

        button_layout = QHBoxLayout()
        
        install_btn = QPushButton("Install Update")
        install_btn.setFixedHeight(35)
        if CONFIG_DATA["gradient_theme"]:
            install_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            install_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        install_btn.clicked.connect(self.accept)

        if not self.forced:
            later_btn = QPushButton("Later")
            later_btn.setFixedHeight(35)
            later_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #ff6666;
                }
            """)
            later_btn.clicked.connect(self.reject)
            button_layout.addWidget(later_btn)

        button_layout.addWidget(install_btn)
        content_layout.addLayout(button_layout)

        layout.addWidget(content_frame)

class RequiredUpdateDialog(QDialog):
    def __init__(self, parent=None, latest_version="", reason=""):
        super().__init__(parent)
        self.latest_version = latest_version
        self.reason = reason
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Required Update")
        self.setFixedSize(450, 250)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_bar = ModernTitleBar(self)
        title_bar.title.setText("Required Update")
        layout.addWidget(title_bar)

        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        message = QLabel(f"A required update is available ({self.latest_version}).\n\nReason: {self.reason}\n\nYou must update to continue using Sol Sniper.")
        message.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        message.setWordWrap(True)
        content_layout.addWidget(message)

        button_layout = QHBoxLayout()
        
        update_btn = QPushButton("Update Now")
        update_btn.setFixedHeight(35)
        if CONFIG_DATA["gradient_theme"]:
            update_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        update_btn.clicked.connect(self.accept)

        quit_btn = QPushButton("Quit")
        quit_btn.setFixedHeight(35)
        quit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                font-weight: 500;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        quit_btn.clicked.connect(self.reject)

        button_layout.addWidget(quit_btn)
        button_layout.addWidget(update_btn)
        content_layout.addLayout(button_layout)

        layout.addWidget(content_frame)

class DownloadProgressDialog(QDialog):
    progress_updated = pyqtSignal(int, float)
    download_finished = pyqtSignal(str)
    download_failed = pyqtSignal(str)

    def __init__(self, parent=None, forced=False):
        super().__init__(parent)
        self.forced = forced
        self.download_canceled = False
        self.setup_ui()
        self.progress_updated.connect(self.update_progress)

    def setup_ui(self):
        self.setWindowTitle("Downloading Update")
        self.setFixedSize(400, 180)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_bar = ModernTitleBar(self)
        title_bar.title.setText("Downloading Update")
        layout.addWidget(title_bar)

        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        self.message_label = QLabel("Downloading the latest version. Please wait...")
        self.message_label.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        self.message_label.setWordWrap(True)
        content_layout.addWidget(self.message_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 6px;
                text-align: center;
                color: white;
                height: 24px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                border-radius: 5px;
            }
        """)
        content_layout.addWidget(self.progress_bar)

        self.percent_label = QLabel("0.00%")
        self.percent_label.setStyleSheet("font-size: 12px; color: #e0e0e0;")
        self.percent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.percent_label)

        if not self.forced:
            self.cancel_btn = QPushButton("Cancel")
            self.cancel_btn.setFixedHeight(35)
            self.cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #ff6666;
                }
            """)
            self.cancel_btn.clicked.connect(self.cancel_download)
            content_layout.addWidget(self.cancel_btn)

        layout.addWidget(content_frame)

    def update_progress(self, percent_int, percent_float):
        self.progress_bar.setValue(percent_int)
        self.percent_label.setText(f"{percent_float:.2f}%")

    def cancel_download(self):
        self.download_canceled = True
        self.reject()

class UpdateCompleteDialog(QDialog):
    def __init__(self, parent=None, save_path=""):
        super().__init__(parent)
        self.save_path = save_path
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Update Complete")
        self.setFixedSize(400, 180)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_bar = ModernTitleBar(self)
        title_bar.title.setText("Update Complete")
        layout.addWidget(title_bar)

        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        message = QLabel("The new version has been installed.\nLaunch new version?")
        message.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        message.setWordWrap(True)
        content_layout.addWidget(message)

        button_layout = QHBoxLayout()
        
        launch_btn = QPushButton("Launch")
        launch_btn.setFixedHeight(35)
        if CONFIG_DATA["gradient_theme"]:
            launch_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            launch_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        launch_btn.clicked.connect(self.accept)

        quit_btn = QPushButton("Quit")
        quit_btn.setFixedHeight(35)
        quit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                font-weight: 500;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        quit_btn.clicked.connect(self.reject)

        button_layout.addWidget(quit_btn)
        button_layout.addWidget(launch_btn)
        content_layout.addLayout(button_layout)

        layout.addWidget(content_frame)

class DownloadThread(QThread):
    progress_updated = pyqtSignal(int, float)
    download_finished = pyqtSignal(str)
    download_failed = pyqtSignal(str)

    def __init__(self, download_url, save_path, progress_dialog):
        super().__init__()
        self.download_url = download_url
        self.save_path = save_path
        self.progress_dialog = progress_dialog

    def run(self):
        try:
            with requests.get(self.download_url, stream=True, timeout=30) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(self.save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if self.progress_dialog.download_canceled:
                            self._cleanup_file()
                            self.download_failed.emit("Download canceled by user")
                            return
                            
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0:
                                percent = 100 * downloaded / total_size
                                self.progress_updated.emit(int(percent), percent)
                
                self.download_finished.emit(self.save_path)
                
        except Exception as e:
            self._cleanup_file()
            self.download_failed.emit(str(e))

    def _cleanup_file(self):
        if os.path.exists(self.save_path):
            try:
                os.remove(self.save_path)
            except:
                pass

class RobloxInstallDialog(QDialog):
    update_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool)
    
    def __init__(self, parent=None, latest_version=""):
        super().__init__(parent)
        self.setWindowTitle("Installing Roblox")
        self.setFixedSize(500, 375)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        
        self.latest_version = latest_version
        self.installation_canceled = False
        self.drag_position = None
        
        self.setup_ui()
        self.apply_rounded_corners()
        
        self.update_signal.connect(self.do_update_history)
        self.finish_signal.connect(self.do_finish)
        
        QTimer.singleShot(100, self.start_installation)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()
        
    def apply_rounded_corners(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        
    def setup_ui(self):
        if CONFIG_DATA["stillbackground"]:
            self.bg_widget = StarryBackgroundStill(self)
        else:
            self.bg_widget = StarryBackground(self)
        self.bg_widget.setGeometry(0, 0, self.width(), int(self.height() * 1.25))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_bar = ModernTitleBar(self)
        title_bar.title.setText("Installing Roblox")
        title_bar.min_btn.hide()
        layout.addWidget(title_bar)
        
        content_frame = GradientFrame()
        content_frame.setStyleSheet("border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        self.status_label = QLabel(f"Installing Roblox version {self.latest_version.replace('version-', '')}...")
        self.status_label.setStyleSheet("font-size: 18px; color: #e0e0e0;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        content_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 6px;
                text-align: center;
                color: white;
                height: 24px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                border-radius: 4px;
                margin: 1px;
            }
        """)
        content_layout.addWidget(self.progress_bar)
        
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(5)
        self.history_labels = []
        for i in range(3):
            label = QLabel("")
            label.setStyleSheet(f"font-size: {12 - i * 2}px; color: {'#e0e0e0' if i == 0 else '#888888'};")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self.history_labels.append(label)
            self.history_layout.addWidget(label)
        
        content_layout.addLayout(self.history_layout)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedHeight(35)
        if CONFIG_DATA["gradient_theme"]:
            self.cancel_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff5555, stop:1 #ff5555);
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ff6666, stop:1 #ff6666);
                }
            """)
        else:
            self.cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    color: white;
                    font-weight: 500;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #ff6666;
                }
            """)
        self.cancel_btn.clicked.connect(self.cancel_installation)
        content_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(content_frame)
        
    def do_update_history(self, message):
        for i in range(2, 0, -1):
            self.history_labels[i].setText(self.history_labels[i-1].text())
            self.history_labels[i].setStyleSheet(f"font-size: {12 - i * 2}px; color: #888888;")
        self.history_labels[0].setText(message)
        self.history_labels[0].setStyleSheet("font-size: 12px; color: #e0e0e0;")
        
    def update_history(self, message):
        self.update_signal.emit(message)
        
    def do_finish(self, success):
        if success:
            self.accept()
        else:
            self.reject()
        
    def start_installation(self):
        def install_thread():
            try:
                self.update_history("Downloading Roblox installer...")
                
                installer_url = "https://www.roblox.com/download/client?os=win"
                temp_dir = tempfile.gettempdir()
                installer_path = os.path.join(temp_dir, "RobloxPlayerLauncher.exe")
                
                if os.path.exists(installer_path):
                    os.remove(installer_path)
                
                urllib.request.urlretrieve(installer_url, installer_path)
                self.update_history("Download complete, launching installer...")
                
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = subprocess.SW_HIDE
                
                subprocess.Popen(
                    [installer_path, "--silent", "--no-launch"],
                    shell=False,
                    startupinfo=si
                )
                self.update_history("Installer launched, waiting for completion...")
                
                start_time = time.time()
                timeout_seconds = 300
                
                while time.time() - start_time < timeout_seconds:
                    if self.installation_canceled:
                        self.update_history("Installation canceled by user")
                        self.finish_signal.emit(False)
                        return
                    
                    if self.is_roblox_installed():
                        self.update_history("Installation completed successfully!")
                        self.finish_signal.emit(True)
                        return
                    
                    time.sleep(2)
                
                self.update_history("Installation timeout - please install manually")
                self.finish_signal.emit(False)
                
            except Exception as e:
                logging.error(f"Installation error: {e}")
                self.update_history(f"Installation failed: {str(e)}")
                self.finish_signal.emit(False)
        
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
    
    def is_roblox_installed(self):
        try:
            common_paths = [
                os.path.expanduser(f"~/AppData/Local/Roblox/Versions/{self.latest_version}"),
                rf"C:\Program Files (x86)\Roblox\Versions\{self.latest_version}",
            ]
            
            for version_path in common_paths:
                exe_path = os.path.join(version_path, "RobloxPlayerBeta.exe")
                if os.path.exists(exe_path):
                    return True
            
            bootstrapper_paths = [
                os.path.expanduser("~/AppData/Local/Bloxstrap/Versions"),
                os.path.expanduser("~/AppData/Local/Fishstrap/Versions"),
            ]
            
            for bootstrapper_path in bootstrapper_paths:
                if os.path.exists(bootstrapper_path):
                    for item in os.listdir(bootstrapper_path):
                        if item == self.latest_version:
                            exe_check = os.path.join(bootstrapper_path, item, "RobloxPlayerBeta.exe")
                            if os.path.exists(exe_check):
                                return True
            
            return False
        except Exception:
            return False
    
    def cancel_installation(self):
        self.installation_canceled = True
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                proc_name = proc.info['name'].lower()
                if 'robloxplayerlauncher' in proc_name:
                    proc.kill()
            except:
                pass
        self.close()

class URLCache:
    def __init__(self, ttl_seconds: int = 60):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str):
        if key in self.cache:
            timestamp, value = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
    
    def set(self, key: str, value: str):
        self.cache[key] = (time.time(), value)
    
    def clear(self):
        now = time.time()
        expired = [k for k, (t, _) in self.cache.items() if now - t >= self.ttl]
        for k in expired:
            del self.cache[k]


class KeywordMatcher:
    def __init__(self, keywords_file):
        self.keywords_file = keywords_file
        self.categories_to_check = []
        self.keyword_map = {}
        self.regex_map = {}
        self.blacklist_map = {}
        self._load_keywords()
    
    def _load_keywords(self):
        try:
            with open(self.keywords_file, 'r') as f:
                data = json.load(f)
        except:
            data = {"keywords": {}, "blacklist": {}, "regex": {}, "custom_categories": []}
        
        for category, keywords in data.get("keywords", {}).items():
            self.keyword_map[category] = set(kw.lower() for kw in keywords)
        
        for category, keywords in data.get("blacklist", {}).items():
            self.blacklist_map[category] = set(kw.lower() for kw in keywords)
        
        for category, regex_data in data.get("regex", {}).items():
            pattern = regex_data.get("pattern", "")
            flags_list = regex_data.get("flags", [])
            flags = 0
            if "i" in flags_list:
                flags |= re.IGNORECASE
            if "m" in flags_list:
                flags |= re.MULTILINE
            try:
                self.regex_map[category] = (re.compile(pattern, flags), flags_list)
            except re.error:
                pass
    
    def update_categories(self, config_data):
        self.categories_to_check = []
        
        category_map = {
            "glitchsniping": "Glitched",
            "dreamsniping": "Dreamspace", 
            "cybersniping": "Cyberspace",
            "singularitysniping": "Singularity",
            "jestersniping": "Jester",
            "voidcoinsniping": "Void Coin"
        }
        
        for config_key, category in category_map.items():
            if config_data.get(config_key, False):
                self.categories_to_check.append(category)
        
        for custom_cat in self.keyword_map.keys():
            if custom_cat not in category_map.values():
                setting_name = f"customcat_{custom_cat.replace(' ', '_')}"
                if config_data.get(setting_name, False):
                    self.categories_to_check.append(custom_cat)
    
    def check_keywords(self, content_lower):
        for category in self.categories_to_check:
            keywords = self.keyword_map.get(category)
            if keywords:
                for kw in keywords:
                    if kw in content_lower:
                        return True, category, kw
            
            if category in self.regex_map:
                pattern, _ = self.regex_map[category]
                if pattern.search(content_lower):
                    return True, category, "regex_match"
        
        return False, None, None
    
    def check_blacklist(self, content_lower, matched_category = None) -> bool:
        if "Global" in self.blacklist_map:
            for kw in self.blacklist_map["Global"]:
                if kw in content_lower:
                    return True
        
        if matched_category and matched_category in self.blacklist_map:
            for kw in self.blacklist_map[matched_category]:
                if kw in content_lower:
                    return True
        
        return False
    
    def reload(self):
        self._load_keywords()


class URLExtractor:
    CHAR_TRANSLATION = str.maketrans({
        '[': ' ', ']': ' ', '(': ' ', ')': ' ', '{': ' ', '}': ' ',
        '`': ' ', '~': ' ', '|': ' ', '\n': ' ', '\r': ' ', '\t': ' '
    })
    CONTROL_CHARS_PATTERN = re.compile(r'[\x00-\x1F\x7F-\x9F]')
    UNICODE_PATTERN = re.compile(r'[\u2000-\uFFFF]')
    
    URL_PATTERN = re.compile(
        r'(?:(?:https?|roblox)://[^\s<>"]+|www\.[^\s<>"]+\.[^\s<>"]+|(?:ro\.pro|ropro\.io|join-rbx\.vexsys\.site|roseal\.live|fishstrap\.app)/[^\s<>"]+)',
        re.IGNORECASE
    )
    PRIVATE_SERVER_PATTERN = re.compile(
        r'roblox\.com/games/(\d+)/[^?]+\?(?:private[_-]?server[_-]?link[_-]?code)=([\w-]+)',
        re.IGNORECASE
    )
    SHARE_CODE_PATTERN = re.compile(r'roblox\.com/share\?code=([a-f0-9]+)', re.IGNORECASE)
    DEEPLINK_PATTERN = re.compile(r'roblox\.com/games/start\?placeId=(\d+)', re.IGNORECASE)
    REDIRECT_GAME_PATTERN = re.compile(r'launchData=(\d+)/([a-f0-9\-]+)', re.IGNORECASE)
    ROPRO_PATTERN = re.compile(r'(?:ro\.pro|ropro\.io)/(?:join/)?([a-zA-Z0-9]+)', re.IGNORECASE)
    JOIN_RBX_PUBLIC_PATTERN = re.compile(r'join-rbx\.vexsys\.site/public\?placeid=(\d+)&gameinstanceid=([A-Za-z0-9\-]+)', re.IGNORECASE)
    JOIN_RBX_PRIVATE_SHARE_PATTERN = re.compile(r'join-rbx\.vexsys\.site/private\?share_code=([A-Za-z0-9]+)', re.IGNORECASE)
    JOIN_RBX_PRIVATE_SERVER_PATTERN = re.compile(r'join-rbx\.vexsys\.site/private\?placeid=(\d+)&link_code=([A-Za-z0-9\-]+)', re.IGNORECASE)
    ROSEAL_PATTERN = re.compile(r'roseal\.live/join\?placeId=(\d+)&gameInstanceId=([A-Za-z0-9\-]+)', re.IGNORECASE)
    FISHSTRAP_PATTERN = re.compile(r'fishstrap\.app/v1/joingame\?placeId=(\d+)&gameInstanceId=([A-Za-z0-9\-]+)', re.IGNORECASE)
    
    @staticmethod
    def clean_content(content: str) -> str:
        content = URLExtractor.CONTROL_CHARS_PATTERN.sub('', content)
        content = URLExtractor.UNICODE_PATTERN.sub('', content)
        content = content.translate(URLExtractor.CHAR_TRANSLATION)
        return content.lower()
    
    @staticmethod
    def extract_urls(content: str) -> list:
        return URLExtractor.URL_PATTERN.findall(content)
    
    @staticmethod
    def parse_private_server(url: str):
        match = URLExtractor.PRIVATE_SERVER_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
        return None
    
    @staticmethod
    def parse_share_code(url: str):
        match = URLExtractor.SHARE_CODE_PATTERN.search(url)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def parse_deeplink(url: str):
        match = URLExtractor.DEEPLINK_PATTERN.search(url)
        if match:
            place_id = match.group(1)
            launch_match = URLExtractor.REDIRECT_GAME_PATTERN.search(url)
            if launch_match:
                return place_id, f"{launch_match.group(1)}/{launch_match.group(2)}"
            return place_id, None
        return None
    
    @staticmethod
    def parse_ropro(url: str):
        match = URLExtractor.ROPRO_PATTERN.search(url)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def parse_joinrbx_public(url: str):
        match = URLExtractor.JOIN_RBX_PUBLIC_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
        return None
    
    @staticmethod
    def parse_joinrbx_share(url: str):
        match = URLExtractor.JOIN_RBX_PRIVATE_SHARE_PATTERN.search(url)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def parse_joinrbx_private(url: str):
        match = URLExtractor.JOIN_RBX_PRIVATE_SERVER_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
        return None
    
    @staticmethod
    def parse_roseal(url: str):
        match = URLExtractor.ROSEAL_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
        return None

    @staticmethod
    def parse_fishstrap(url: str):
        match = URLExtractor.FISHSTRAP_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
        return None


class InputNoticeDialog(QDialog):
    def __init__(self, parent=None, title="", message="", placeholder="", accept_text="Submit", cancel_text="Cancel", show_dashboard_btn=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-size: 13px; color: #e0e0e0;")
        layout.addWidget(self.message_label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.input_field)
        
        button_box = QDialogButtonBox()
        if show_dashboard_btn:
            dashboard_btn = button_box.addButton("Go to Dashboard", QDialogButtonBox.ButtonRole.ActionRole)
            dashboard_btn.setStyleSheet("background-color: #1a69d1; color: white; border-radius: 4px; padding: 6px 12px;")
            dashboard_btn.clicked.connect(lambda: webbrowser.open("https://solsniper.vexsys.site/dashboard"))
        accept_btn = button_box.addButton(accept_text, QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_btn = button_box.addButton(cancel_text, QDialogButtonBox.ButtonRole.RejectRole)
        accept_btn.setStyleSheet("background-color: #4a7bff; color: white; border-radius: 4px; padding: 6px 12px;")
        cancel_btn.setStyleSheet("background-color: #ff5555; color: white; border-radius: 4px; padding: 6px 12px;")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_value(self):
        return self.input_field.text().strip()
    
    @staticmethod
    def get_input(parent, title, message, placeholder="", accept_text="Submit", cancel_text="Cancel", show_dashboard_btn=False):
        dialog = InputNoticeDialog(parent, title, message, placeholder, accept_text, cancel_text, show_dashboard_btn)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_value()
        return None

class MainWindow(QMainWindow):
    _pressed_keys = set()
    _key_listener = None
    blacklisted_signal = pyqtSignal(str)
    auth_error_signal = pyqtSignal(str)
    maintenance_signal = pyqtSignal(str)
    version_blocked_signal = pyqtSignal(str, str, str)   # message, required_version, download_url
    error_signal = pyqtSignal(str) 
    kicked_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

    def initialize_ui(self):
        logging.info("Initializing MainWindow")
        beta_version_text = f" [BETA {BETA_VERSION}]" if IS_BETA_VERSION else ""
        pre_release_text = f" [PRE-RELEASE {PRE_RELEASE_VERSION}]" if IS_PRE_RELEASE else ""
        self.setWindowTitle(f"Sol Sniper V{CURRENT_VERSION.strip('.0')}{beta_version_text}{pre_release_text}")
        self.resize(1200, 800)
        self.setFixedSize(1200, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._current_toast_thread = None
        self._toast_cancel_flag = False
        self.custom_category_checkboxes = {}
        self.init_key_listener()
        self.blacklisted_signal.connect(self._on_blacklisted)
        self.auth_error_signal.connect(self._on_auth_error, Qt.ConnectionType.QueuedConnection)
        self.maintenance_signal.connect(self.handle_server_maintenance, Qt.ConnectionType.QueuedConnection)
        self.version_blocked_signal.connect(self.handle_version_blocked, Qt.ConnectionType.QueuedConnection)
        self.error_signal.connect(self.handle_auth_error, Qt.ConnectionType.QueuedConnection)
        self.kicked_signal.connect(self._on_kicked, Qt.ConnectionType.QueuedConnection)
        self.url_cache = URLCache(ttl_seconds=60)
        self.keyword_matcher = KeywordMatcher(KEYWORDS_FILE)
        self.RAW_VERSION_STR = RAW_VERSION_STR

        if platform.system() == 'Darwin':
            self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
            font = self.font()
            font.setPointSize(font.pointSize() + 1)
            self.setFont(font)

        self.default_keywords = {
            "keywords": {
                "Glitched": [
                    "glitch",
                    "glig"
                ],
                "Dreamspace": [
                    "dream"
                ],
                "Cyberspace": [
                    "cyber"
                ],
                "Singularity": [
                    "singul"
                ],
                "Jester": [
                    "jest",
                    "obli",
                    "obi"
                ],
                "Void Coin": [
                    "void",
                    "viod"
                ]
            },
            "blacklist": {
                "Global": [
                    "bait",
                    "fake",
                    "aura",
                    "chill",
                    "stigma",
                    "sol",
                    "zero",
                    "day",
                    "dimensional"
                ],
                "Glitched": [],
                "Dreamspace": [],
                "Cyberspace": [],
                "Singularity": [],
                "Jester": [],
                "Void Coin": []
            }
        }
        self.default_servers = [
            {
                "name": "maincord",
                "id": "1186570213077041233",
                "channels": [
                    {
                        "name": "biomes",
                        "id": "1282542323590496277"
                    },
                    {
                        "name": "merchants",
                        "id": "1282543762425516083"
                    }
                ]
            }
        ]
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("""
            QWidget {
                border-radius: 12px;
            }
        """)
        
        if CONFIG_DATA["stillbackground"] == False:
            self.bg_widget = StarryBackground(self.central_widget)
        elif CONFIG_DATA["stillbackground"] == True:
            self.bg_widget = StarryBackgroundStill(self.central_widget)
        self.bg_widget.setGeometry(0, 0, self.width(), self.height())

        self.drag_start_position = None
        self.initial_window_pos = None
        self.central_widget.setMouseTracking(True)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = ModernTitleBar(self, True)
        self.title_bar.setContentsMargins(10, 10, 10, 0)
        main_layout.addWidget(self.title_bar)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 0, 20)
        content_layout.setSpacing(20)
        
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("background-color: rgba(30, 30, 30, 180); border-radius: 12px;")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        logo = QLabel()
        logo_pixmap = QPixmap(str(SETTINGS_DIR / "snipercat.png"))
        rounded = QPixmap(96, 96)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 96, 96, 24, 24)
        painter.setClipPath(path)
        scaled = logo_pixmap.scaled(96, 96, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        logo.setPixmap(rounded)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("background-color: transparent; margin-bottom: 10px;")
        sidebar_layout.addWidget(logo)
        
        self.sniper_btn = self.create_sidebar_btn("Sniper")
        self.accounts_btn = self.create_sidebar_btn("Accounts")
        self.keywords_btn = self.create_sidebar_btn("Keywords")
        self.servers_btn = self.create_sidebar_btn("Servers")
        self.settings_btn = self.create_sidebar_btn("Miscellaneous")
        self.logs_btn = self.create_sidebar_btn("Logs")
        self.credits_btn = self.create_sidebar_btn("Credits")
        self.dashboard_btn = self.create_sidebar_btn("Dashboard", svg=WEBSITE_SVG, color="#1a69d1", url="https://solsniper.vexsys.site/dashboard")
        self.discord_btn = self.create_sidebar_btn("Discord", svg=DISCORD_SVG, color="#5865F2", url="https://discord.gg/RPcPUp47YD")
        self.github_btn = self.create_sidebar_btn("GitHub", svg=GITHUB_SVG, color="#333", url="https://github.com/vexsyx/sniper-v3")

        sidebar_layout.addWidget(self.sniper_btn)
        sidebar_layout.addWidget(self.accounts_btn)
        sidebar_layout.addWidget(self.keywords_btn)
        sidebar_layout.addWidget(self.servers_btn)
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addWidget(self.logs_btn)
        sidebar_layout.addWidget(self.credits_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.discord_btn)
        sidebar_layout.addWidget(self.github_btn)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_widget.tabBar().setVisible(False)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: rgba(30, 30, 30, 200);
                border-radius: 12px;
            }
        """)
        
        self.sniper_tab = self.create_sniper_tab()
        self.accounts_tab = self.create_accounts_tab()
        self.keywords_tab = self.create_keywords_tab()
        self.servers_tab = self.create_servers_tab()
        self.settings_tab = self.create_settings_tab()
        self.logs_tab = self.create_logs_tab()
        self.credits_tab = self.create_credits_tab()
        
        self.tab_widget.addTab(self.sniper_tab, "Sniper")
        self.tab_widget.addTab(self.accounts_tab, "Accounts")
        self.tab_widget.addTab(self.keywords_tab, "Keywords")
        self.tab_widget.addTab(self.servers_tab, "Servers")
        self.tab_widget.addTab(self.settings_tab, "Miscellaneous")
        self.tab_widget.addTab(self.logs_tab, "Logs")
        self.tab_widget.addTab(self.credits_tab, "Credits")

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.tab_widget)
        main_layout.addLayout(content_layout)
        
        self.setup_connections()
        self.setStyleSheet(self.get_stylesheet())
        self.load_keywords_data()
        self.refresh_custom_categories()

        self.is_processing = False
        self.pause_timer = QTimer(self)
        self.pause_timer.timeout.connect(self.check_pause_status)
        self.pause_timer.start(1000)
        self.hotkey_monitor_running = False
        self.keyboard = KeyboardController()
        if not hasattr(self, 'hotkey_thread') or not self.hotkey_thread:
            self.hotkey_monitor_running = True
            self.hotkey_thread = threading.Thread(
                target=self.start_hotkey_monitor,
                daemon=True
            )
            self.hotkey_thread.start()
        self.url_cache = {}
        self.resolution_cache = {}
        self.last_process_time = 0
        self.process_lock = asyncio.Lock()
        logging.info("MainWindow initialized")

        QTimer.singleShot(500, self.perform_startup_checks)

    def show_help_menu(self):
        logging.info("Showing help menu")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Feature Not Implemented")
        msg.setText("This feature is not fully implemented yet.")
        msg.setInformativeText("For questions and support, please refer to the community Discord server.")
        msg.exec()
        return

    def perform_startup_checks(self):
        self.check_for_updates()
        self.check_maincord_server_exists()
        self.check_handout_channel_on_launch()
        self.check_locked_pre_release()
        self.check_new_roblox_version_on_launch()

    async def init_websocket(self):
        try:
            if not hasattr(self, 'websocket_manager') or self.websocket_manager is None:
                self.websocket_manager = WebsocketManager(self)
            self.websocket_manager.hide_from_board = CONFIG_DATA.get("hide_from_board", False)
            
            auth_token = self.getWSToken()
            if auth_token:
                self.websocket_manager.set_auth_token(auth_token)

            result = await self.websocket_manager.start()
            logging.info("WebSocket manager initialized")
            
            if isinstance(result, tuple) and len(result) == 3:
                return result
            return False, "", 0
        except Exception as e:
            logging.error(f"Failed to initialize WebSocket manager: {e}")
            self.websocket_manager = None
            return False, "", 0

    def is_websocket_healthy(self):
        if not hasattr(self, 'websocket_manager') or self.websocket_manager is None:
            return False
        try:
            return self.websocket_manager.is_healthy()
        except:
            return False

    def getWSToken(self):
        return CONFIG_DATA.get("ws_token", "")

    def check_locked_pre_release(self):
        try:
            if not LOCKED_PRE_RELEASE:
                return
        
            self.show_dismissible_notice(
                "Locked Pre-Release",
                "This is a locked pre-release\n"
                "If you are caught distributing this pre-release, you will have your priviledges revoked.\n"
                "Please refrain from sharing/distributing unreleased versions of Sol Sniper unless you are told you may.",
                "locked_pre_release_warning"
            )
        except Exception as e:
            logging.error(f"Error checking if locked pre-release: {e}")

    def check_maincord_server_exists(self):
        try:
            if not SERVERS_FILE.exists():
                return
            
            with open(SERVERS_FILE, 'r', encoding='utf-8') as f:
                servers = json.load(f)
            
            maincord_exists = False
            for server in servers:
                if server.get('id') == "1186570213077041233":
                    maincord_exists = True
                    break
            
            if not maincord_exists:
                self.show_dismissible_notice(
                    "Maincord Server Missing",
                    "Maincord Server Not Found\n\n"
                    "The maincord server (ID: 1186570213077041233) is missing from your servers list.\n\n"
                    "This server is where most private servers are posted. Without it, you will miss many snipes.\n\n"
                    "Would you like to add the maincord server back?\n\n"
                    "• Name: maincord\n"
                    "• ID: 1186570213077041233\n"
                    "• Channels: biomes (1282542323590496277), merchants (1282543762425516083)",
                    "missing_maincord_warning"
                )
                
                if self.show_missing_maincord_add_dialog():
                    self.add_missing_maincord_server()
        
        except Exception as e:
            logging.error(f"Error checking maincord server: {e}")

    def show_missing_maincord_add_dialog(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Add Maincord Server?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Would you like to add the maincord server back?")
        msg.setInformativeText(
            "This will add the maincord server with its default channels:\n\n"
            "• Server Name: maincord\n"
            "• Server ID: 1186570213077041233\n"
            "• Channels: biomes (1282542323590496277), merchants (1282543762425516083)"
        )
        
        add_btn = msg.addButton("Add Maincord", QMessageBox.ButtonRole.AcceptRole)
        later_btn = msg.addButton("Later", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        return msg.clickedButton() == add_btn

    def add_missing_maincord_server(self):
        maincord_server = {
            "name": "maincord",
            "id": "1186570213077041233",
            "enabled": True,
            "channels": [
                {
                    "name": "biomes",
                    "id": "1282542323590496277"
                },
                {
                    "name": "merchants",
                    "id": "1282543762425516083"
                }
            ]
        }
        
        if not SERVERS_FILE.exists():
            os.makedirs(SERVERS_FILE.parent, exist_ok=True)
            servers = [maincord_server]
        else:
            with open(SERVERS_FILE, "r", encoding="utf-8") as f:
                servers = json.load(f)
            
            for server in servers:
                if server.get("id") == "1186570213077041233":
                    logging.info("Maincord server already exists")
                    return
            
            servers.append(maincord_server)
        
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4)
        
        self.load_servers()
        logging.info("Added missing maincord server back")

    def check_handout_channel_on_launch(self):
        try:
            if not SERVERS_FILE.exists():
                return
            
            with open(SERVERS_FILE, 'r', encoding='utf-8') as f:
                servers = json.load(f)
            
            for server in servers:
                if server.get('id') == "1186570213077041233":
                    for channel in server.get('channels', []):
                        if channel.get('id') == "1282554696032194593":
                            proceed_clicked = self.show_dismissible_notice(
                                "Others Channel Detected",
                                "WARNING: Others Channel Detected\n\n"
                                "You currently have the others channel (ID: 1282554696032194593) enabled in the maincord server.\n\n"
                                "Only handout servers are posted in this channel. Sniping here may cause:\n"
                                "• A ton of false detections\n"
                                "• Wasted snipes on \"LF\" servers\n"
                                "• Unnecessary pauses and cooldowns\n\n"
                                "It is highly recommended to disable this channel for optimal sniping.",
                                "handout_channel_warning_launch"
                            )
                            if not proceed_clicked:
                                return

                            # if proceed_clicked, then remove others channel from maincord server and save settings
                            server['channels'].remove(channel)
                            with open(SERVERS_FILE, "w", encoding="utf-8") as f:
                                json.dump(servers, f, indent=4)
        except Exception as e:
            logging.error(f"Error checking handout channel: {e}")

    def check_new_roblox_version_on_launch(self):
        try:
            if platform.system() != 'Windows':
                return
            
            response = requests.get("https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer", timeout=5)
            if response.status_code != 200:
                return
            
            data = response.json()
            latest_version = data.get("clientVersionUpload", "")
            
            if not latest_version:
                return
            
            current_version = None
            is_version_installed = self.is_roblox_version_installed(latest_version)
            
            if hasattr(self, 'selected_override_version') and self.selected_override_version:
                current_version = self.selected_override_version.get("version") != "N/A"
            
            if not current_version and is_roblox_protocol_overridden():
                target = get_roblox_protocol_target()
                if target:
                    match = re.search(r'versions[\\/]([^\\/]+)[\\/]', target.lower())
                    if match:
                        current_version = match.group(1)
            
            if current_version and current_version != latest_version:
                self.show_roblox_version_outdated_notice(latest_version, current_version, is_version_installed)
            elif not current_version:
                self.show_roblox_version_outdated_notice(latest_version, None, is_version_installed)
                
        except Exception as e:
            logging.error(f"Error checking Roblox version: {e}")

    def is_roblox_version_installed(self, version):
        try:
            logging.info(f"Checking if Roblox version {version} is installed...")
            common_paths = [
                os.path.expanduser(f"~/AppData/Local/Roblox/Versions/{version}"),
                rf"C:\Program Files (x86)\Roblox\Versions\{version}",
            ]
            
            for version_path in common_paths:
                exe_path = os.path.join(version_path, "RobloxPlayerBeta.exe")
                if os.path.exists(exe_path):
                    return True
            
            bootstrapper_paths = [
                os.path.expanduser("~/AppData/Local/Bloxstrap/Versions"),
                os.path.expanduser("~/AppData/Local/Fishstrap/Versions"),
            ]
            
            for bootstrapper_path in bootstrapper_paths:
                if os.path.exists(bootstrapper_path):
                    for item in os.listdir(bootstrapper_path):
                        if item == version:
                            exe_check = os.path.join(bootstrapper_path, item, "RobloxPlayerBeta.exe")
                            if os.path.exists(exe_check):
                                return True
            
            return False
        except Exception as e:
            logging.error(f"Error checking if Roblox version is installed: {e}")
            return False

    def show_roblox_version_outdated_notice(self, latest_version, current_version, is_version_installed):
        dismissed_notices = CONFIG_DATA.get("dismissed_notices", {})
        if dismissed_notices.get("roblox_version_outdated", False):
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Roblox Protocol Outdated")
        msg.setIcon(QMessageBox.Icon.Warning)
        
        if current_version:
            message = (
                f"Your Roblox protocol is pointing to an outdated version of Roblox.\n\n"
                f"Current version: {current_version.replace('version-', '')}\n"
                f"Latest version{'' if is_version_installed else ' (not installed)'}: {latest_version.replace('version-', '')}\n\n"
                f"Using an outdated version will cause:\n"
                f"• Inability to join private servers\n"
                f"• Compatibility issues with the sniper\n"
                f"• Missing out on snipes due to version mismatches\n\n"
                f"What would you like to do?"
            )
            install_btn_text = "Update Roblox"
        else:
            message = (
                f"No Roblox protocol override is currently set.\n\n"
                f"The latest Roblox version is: {latest_version.replace('version-', '')}\n\n"
                f"Setting up protocol override ensures you always join with the correct Roblox version.\n"
                f"This helps prevent:\n"
                f"• Inability to join private servers\n"
                f"• Compatibility issues with the sniper\n"
                f"• Missing out on snipes due to version mismatches\n\n"
                f"What would you like to do?"
            )
            install_btn_text = "Install Roblox"
        
        msg.setText(message)
        
        override_btn = msg.addButton("Override Protocol Now", QMessageBox.ButtonRole.AcceptRole)
        install_btn = msg.addButton(install_btn_text, QMessageBox.ButtonRole.ActionRole)
        later_btn = msg.addButton("Later", QMessageBox.ButtonRole.RejectRole)
        dont_show_checkbox = QCheckBox("Don't show this again")
        msg.setCheckBox(dont_show_checkbox)
        msg.setDefaultButton(install_btn)
        
        msg.exec()
        
        if dont_show_checkbox.isChecked():
            if "dismissed_notices" not in CONFIG_DATA:
                CONFIG_DATA["dismissed_notices"] = {}
            CONFIG_DATA["dismissed_notices"]["roblox_version_outdated"] = True
            self.save_settings()
        
        clicked_button = msg.clickedButton()
        
        if clicked_button == install_btn:
            self.start_roblox_installation(latest_version)
            
        elif clicked_button == override_btn:
            self.show_roblox_version_selection_for_override(latest_version)

    def start_roblox_installation(self, latest_version):
        dialog = RobloxInstallDialog(self, latest_version=latest_version)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = QMessageBox.information(
                self,
                "Installation Complete",
                f"Roblox version {latest_version.replace('version-', '')} has been installed successfully!\n\n"
                f"Would you like to override the protocol to use this version now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if result == QMessageBox.StandardButton.Yes:
                self.find_and_override_new_version(latest_version)
        else:
            if hasattr(dialog, 'installation_canceled') and not dialog.installation_canceled:
                QMessageBox.warning(
                    self,
                    "Installation Failed",
                    f"Failed to install Roblox version {latest_version.replace('version-', '')}.\n\n"
                    f"Please manually install Roblox from https://www.roblox.com/download\n\n"
                    f"Then click 'Override Protocol Now' to set up the protocol."
                )

    def find_and_override_new_version(self, target_version):
        versions = get_installed_roblox_versions()
        
        for version in versions:
            if version.get("version") == target_version:
                self.selected_override_version = version
                self.override_version_label.setText(version["name"])
                
                success = override_roblox_protocol(
                    version["path"],
                    version["type"],
                    version.get("version", "")
                )
                
                if success:
                    self.update_protocol_status()
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Roblox protocol has been overridden to use:\n{version['name']}\n\nVersion: {version.get('version', 'Unknown').replace('version-', '')}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Override Failed",
                        "Failed to override Roblox protocol. Please try running as administrator."
                    )
                return
        
        QMessageBox.warning(
            self,
            "Version Not Found",
            f"Could not find the newly installed version {target_version.replace('version-', '')}.\n\nPlease manually override the protocol using the 'Select Version' button."
        )

    def show_roblox_version_selection_for_override(self, recommended_version):
        dialog = RobloxVersionDialog(self, allow_custom=CONFIG_DATA["advanced_mode"])
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_version = dialog.get_selected_version()
            if selected_version:
                if selected_version.get("version") != recommended_version:
                    is_installed = self.is_roblox_version_installed(selected_version.get("version", ""))
                    
                    warning_msg = f"You selected version: {selected_version.get('version')}\n\n"
                    warning_msg += f"The recommended latest version is: {recommended_version}\n\n"
                    
                    if not is_installed:
                        warning_msg += f"WARNING: The selected version is not installed!\n\n"
                    
                    warning_msg += f"Using an outdated or uninstalled version will cause issues.\n\n"
                    warning_msg += f"Are you sure you want to use this version?"
                    
                    confirm = QMessageBox.question(
                        self,
                        "Version Mismatch",
                        warning_msg,
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if confirm != QMessageBox.StandardButton.Yes:
                        return
                
                self.selected_override_version = selected_version
                self.override_version_label.setText(selected_version["name"])
                
                success = override_roblox_protocol(
                    self.selected_override_version["path"],
                    self.selected_override_version["type"],
                    self.selected_override_version.get("version", "")
                )
                
                if success:
                    self.update_protocol_status()
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Roblox protocol has been overridden to use:\n{selected_version['name']}\n\nVersion: {selected_version.get('version', 'Unknown').replace('version-', '')}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Override Failed",
                        "Failed to override Roblox protocol. Please try running as administrator."
                    )

    def check_for_updates(self):
        try:
            raw_version_str = RAW_VERSION_STR
            logging.info(f"Current Version: {raw_version_str}")
            logging.info("Checking for updates...")
            
            response = requests.get(
                "https://api.github.com/repos/vexsyx/sniper-v3/releases/latest",
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            latest_version = data.get("tag_name", "")
            release_body = data.get("body", "")
            
            logging.info(f"Latest version found: {latest_version}")
            
            if release_body.startswith("<!-- <REQUIRED_UPDATE>") and latest_version and self._is_newer_version(latest_version, raw_version_str):
                reason_start = release_body.find("(")
                reason_end = release_body.find(")", reason_start)
                if reason_start != -1 and reason_end != -1:
                    reason = release_body[reason_start + 1:reason_end]
                    self._show_required_update_dialog(latest_version, reason)
                    return "required_update"
            
            if latest_version and self._is_newer_version(latest_version, raw_version_str):
                self._show_update_dialog(latest_version)
                return "update_available"
            
            logging.info("No updates available")
            return "no_update"
            
        except Exception as e:
            logging.error(f"Failed to check for updates: {str(e)}")
            return "no_update"

    def _is_newer_version(self, latest: str, current: str) -> bool:
        def parse_version(v: str):
            v = v.lstrip('v')
            
            parts = []
            
            # handle pre-release suffix (e.g., -pre4)
            pre_match = re.search(r'-pre(\d+)$', v)
            if pre_match:
                pre_num = int(pre_match.group(1))
                v = v[:pre_match.start()]
                parts.append(('pre', pre_num))
            
            # handle beta suffix (e.g., -beta7)
            beta_match = re.search(r'-beta(\d+)$', v)
            if beta_match:
                beta_num = int(beta_match.group(1))
                v = v[:beta_match.start()]
                parts.insert(0, ('beta', beta_num))
            
            # parse base version (e.g., 3.0.0)
            version_parts = [int(x) for x in v.split('.')]
            
            # return tuple for comparison: (major, minor, patch, beta, pre)
            # beta versions are considered older than final releases
            # pre-releases are considered older than beta releases
            beta_val = parts[0][1] if parts and parts[0][0] == 'beta' else float('inf')
            pre_val = parts[1][1] if len(parts) > 1 and parts[1][0] == 'pre' else float('inf')
            
            return (*version_parts, beta_val, pre_val)
        
        try:
            latest_tuple = parse_version(latest)
            current_tuple = parse_version(current)
            
            return latest_tuple > current_tuple
        except Exception as e:
            logging.error(f"Version comparison error: {e}")
            return False

    def _show_required_update_dialog(self, latest_version, reason):
        dialog = RequiredUpdateDialog(self, latest_version, reason)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._install_update(latest_version, forced=True)
        else:
            QApplication.quit()

    def _show_update_dialog(self, latest_version):
        dialog = UpdateAvailableDialog(self, latest_version, RAW_VERSION_STR)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._install_update(latest_version)

    def _install_update(self, latest_version, forced=False):
        def get_download_url():
            try:
                api_url = "https://api.github.com/repos/vexsyx/sniper-v3/releases/latest"
                resp = requests.get(api_url, timeout=10)
                resp.raise_for_status()
                release = resp.json()
                
                for asset in release.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        return asset["browser_download_url"]
                return None
            except Exception as e:
                logging.error(f"Failed to get download URL: {e}")
                return None

        def choose_save_path():
            default_name = f"Sol Sniper {latest_version}.exe"
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Install Sol Sniper Update",
                default_name,
                "Executable (*.exe)"
            )
            return save_path

        download_url = get_download_url()
        if not download_url:
            self._show_error_dialog("Update Error", "No installer found in the latest release.", forced)
            return

        save_path = choose_save_path()
        if not save_path:
            if forced:
                self._show_error_dialog("Update Required", "You must update to continue using Sol Sniper.", forced, retry=True)
            return

        self._start_download(download_url, save_path, latest_version, forced)

    def _start_download(self, download_url, save_path, latest_version, forced):
        progress_dialog = DownloadProgressDialog(self, forced)
        
        download_thread = DownloadThread(download_url, save_path, progress_dialog)
        download_thread.progress_updated.connect(progress_dialog.progress_updated.emit)
        download_thread.download_finished.connect(lambda path: self._on_download_finished(path, progress_dialog))
        download_thread.download_failed.connect(lambda error: self._on_download_failed(error, progress_dialog, latest_version, forced))
        
        download_thread.start()
        progress_dialog.exec()

    def _on_download_finished(self, save_path, progress_dialog):
        progress_dialog.accept()
        complete_dialog = UpdateCompleteDialog(self, save_path)
        if complete_dialog.exec() == QDialog.DialogCode.Accepted:
            self._launch_new_version(save_path)
        else:
            QApplication.quit()

    def _on_download_failed(self, error, progress_dialog, latest_version, forced):
        progress_dialog.reject()
        if "canceled" in error.lower():
            if forced:
                self._show_error_dialog("Update Required", "You must update to continue using Sol Sniper.", forced, retry=True)
        else:
            self._show_error_dialog("Download Failed", f"Failed to download update: {error}", forced, retry=True)

    def _launch_new_version(self, save_path):
        try:
            if platform.system() == 'Windows':
                os.startfile(save_path)
            else:
                subprocess.Popen([save_path])
            QApplication.quit()
        except Exception as e:
            self._show_error_dialog("Launch Error", f"Could not launch new version: {e}\n\nPlease manually launch: {save_path}", False)

    def _show_error_dialog(self, title, message, forced, retry=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
        
        if retry and forced:
            retry_btn = msg.addButton("Retry", QMessageBox.ButtonRole.AcceptRole)
            quit_btn = msg.addButton("Quit", QMessageBox.ButtonRole.RejectRole)
            msg.exec()
            if msg.clickedButton() == retry_btn:
                self._install_update("latest", forced=True)
            else:
                QApplication.quit()
        else:
            msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
            msg.exec()

    def open_snake_game(self):
        try:
            self.snake_game = SnakeGame(self)
            self.snake_game.exec()
        except Exception as e:
            logging.error(f"Error opening snake game: {e}")
            QMessageBox.warning(self, "Error", "Could not open snake game.")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint()
            self.initial_window_pos = self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_start_position'):
            delta = event.globalPosition().toPoint() - self.drag_start_position
            new_pos = self.initial_window_pos + delta
            self.move(new_pos)

            if hasattr(self, 'bg_widget') and CONFIG_DATA["stillbackground"] == False:
                self.bg_widget.update_star_positions()
                
            event.accept()

    def moveEvent(self, event):
        super().moveEvent(event)
        if hasattr(self, 'bg_widget') and CONFIG_DATA["stillbackground"] == False:
            self.bg_widget.update_star_positions()

    def closeEvent(self, event):
        logging.info("Application closing - performing cleanup")
        
        gc.collect()
        gc.collect()
        
        if hasattr(self, 'local_server'):
            self.local_server.close()
            QLocalServer.removeServer(APP_NAME)
        
        logging.info("Cleanup completed")
        event.accept()

    def handle_hotkeys(self):
        if processing_hotkey_assignment:
            return
        
        try:
            if CONFIG_DATA["open_roblox_toggle"]:
                try:
                    if self.is_key_pressed(CONFIG_DATA["open_roblox"]):
                        logging.info(f"Hotkey pressed: open_roblox_key={CONFIG_DATA['open_roblox']}")
                        self.launch_game(f"roblox://placeID=15532962292")
                        time.sleep(0.5)
                except:
                    pass

            if CONFIG_DATA["stop_sniper_toggle"] and not sniper_paused:
                try:
                    if self.is_key_pressed(CONFIG_DATA["stop_sniper"]):
                        logging.info(f"Hotkey pressed: stop_sniper_key={CONFIG_DATA['stop_sniper']}")
                        try:
                            self.temporarily_pause_sniper(int(CONFIG_DATA["pause_duration"]))
                        except ValueError as e:
                            logging.error(f"Invalid pause duration: {CONFIG_DATA['pause_duration']}, error: {e}")
                        time.sleep(0.5)
                except:
                    pass

            if CONFIG_DATA["toggle_sniper_toggle"]:
                try:
                    if self.is_key_pressed(CONFIG_DATA["toggle_sniper"]):
                        logging.info(f"Hotkey pressed: toggle_sniper_key={CONFIG_DATA['toggle_sniper']}")
                        self.toggle_sniping()
                        time.sleep(0.5)
                except:
                    pass
            
        except Exception as e:
            logging.error(f"Error in handle_hotkeys: {e}")
        
        self.handle_skipper_hotkeys()

    def is_key_pressed(self, key_string):
        try:
            if not MainWindow._pressed_keys:
                return False
                
            if '+' not in key_string:
                key = key_string.lower().strip()
                
                special_keys = {
                    'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
                    'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
                    'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
                    'space': 'space', 'enter': 'enter', 'esc': 'esc',
                    'tab': 'tab', 'backspace': 'backspace', 'delete': 'delete',
                    'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
                    '[': '[', ']': ']', '\\': '\\', ';': ';', "'": "'",
                    ',': ',', '.': '.', '/': '/', '`': '`', '-': '-', '=': '='
                }
                
                if key in special_keys:
                    return special_keys[key] in MainWindow._pressed_keys
                elif len(key) == 1:
                    return key in MainWindow._pressed_keys
                return False
            
            parts = key_string.lower().split('+')
            
            for part in parts[:-1]:
                if part == 'ctrl':
                    if not ('ctrl' in MainWindow._pressed_keys or 
                        'ctrlleft' in MainWindow._pressed_keys or 
                        'ctrlright' in MainWindow._pressed_keys):
                        return False
                elif part == 'shift':
                    if not ('shift' in MainWindow._pressed_keys or 
                        'shiftleft' in MainWindow._pressed_keys or 
                        'shiftright' in MainWindow._pressed_keys):
                        return False
                elif part == 'alt':
                    if not ('alt' in MainWindow._pressed_keys or 
                        'altleft' in MainWindow._pressed_keys or 
                        'altright' in MainWindow._pressed_keys):
                        return False
                elif part in ['win', 'windows', 'meta']:
                    if not ('win' in MainWindow._pressed_keys or 
                        'winleft' in MainWindow._pressed_keys or 
                        'winright' in MainWindow._pressed_keys or 
                        'cmd' in MainWindow._pressed_keys):
                        return False
                else:
                    return False
            
            main_key = parts[-1]
            special_keys = {
                'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
                'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
                'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
                'space': 'space', 'enter': 'enter', 'esc': 'esc',
                'tab': 'tab', 'backspace': 'backspace', 'delete': 'delete',
                'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
            }
            
            if main_key in special_keys:
                return special_keys[main_key] in MainWindow._pressed_keys
            elif len(main_key) == 1:
                return main_key in MainWindow._pressed_keys
            
            return False
            
        except Exception as e:
            logging.error(f"Error checking key press for {key_string}: {e}")
            return False

    def is_roblox_focused(self):
        current_time = time.time()
        if hasattr(self, '_last_focus_check') and (current_time - self._last_focus_check) < 0.5:
            return getattr(self, '_cached_focus_result', True)
        
        self._last_focus_check = current_time
        
        try:
            if platform.system() == 'Windows':
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    window_title = win32gui.GetWindowText(hwnd)
                    if 'Roblox' in window_title:
                        self._cached_focus_result = True
                        return True
                    
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        process = psutil.Process(pid)
                        process_name = process.name().lower()
                        if 'roblox' in process_name or 'RobloxPlayerBeta' in process_name:
                            self._cached_focus_result = True
                            return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                self._cached_focus_result = False
                return False
                
            elif platform.system() == 'Darwin':  # macOS
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                    return frontApp
                end tell
                '''
                
                try:
                    result = subprocess.run(
                        ['osascript', '-e', script], 
                        capture_output=True, 
                        text=True, 
                        timeout=0.2
                    )
                    if result.returncode == 0:
                        front_app = result.stdout.strip().lower()
                        if 'roblox' in front_app:
                            self._cached_focus_result = True
                            return True
                except subprocess.TimeoutExpired:
                    return getattr(self, '_cached_focus_result', True)
                except Exception:
                    pass
                
                try:
                    front_app_pid = Quartz.CGWindowListCopyWindowInfo(
                        Quartz.kCGWindowListOptionOnScreenOnly, 
                        Quartz.kCGNullWindowID
                    )
                    if front_app_pid:
                        for window in front_app_pid:
                            if window.get('kCGWindowLayer', 0) == 0:
                                owner_pid = window.get('kCGWindowOwnerPID')
                                if owner_pid:
                                    try:
                                        proc = psutil.Process(owner_pid)
                                        proc_name = proc.name().lower()
                                        if 'roblox' in proc_name:
                                            self._cached_focus_result = True
                                            return True
                                    except:
                                        pass
                                break
                except ImportError:
                    pass  # pyobjc not installed
                
                self._cached_focus_result = False
                return False
                
            else:  # Linux or other (fucking losers lmao, get a real OS)
                logging.error(f"Feature not supported on {platform.system()}")
                return False
                
        except Exception as e:
            # if any error occurs, default to True to not block hotkey functionality
            logging.debug(f"Error checking Roblox focus: {e}")
            self._cached_focus_result = True
            return True

    def handle_skipper_hotkeys(self):
        global loading_asset_skipper_active, main_menu_skipper_active
        
        try:
            if not self.is_roblox_focused():
                return

            if CONFIG_DATA["loading_asset_skipper_toggle"]:
                if self.is_key_pressed(CONFIG_DATA["loading_asset_skipper"]):
                    if not loading_asset_skipper_active:
                        loading_asset_skipper_active = True
                        threading.Thread(target=self.execute_loading_asset_skipper, daemon=True).start()
                else:
                    loading_asset_skipper_active = False

            if CONFIG_DATA["main_menu_skipper_toggle"]:
                if self.is_key_pressed(CONFIG_DATA["main_menu_skipper"]):
                    if not main_menu_skipper_active:
                        main_menu_skipper_active = True
                        threading.Thread(target=self.execute_main_menu_skipper, daemon=True).start()
                else:
                    main_menu_skipper_active = False
        except Exception as e:
            logging.error(f"Error in handle_skipper_hotkeys: {e}")

    def execute_loading_asset_skipper(self):
        logging.info("Loading Asset Skipper activated")
        global loading_asset_skipper_active
        
        if platform.system() == 'Windows':
            try:
                while loading_asset_skipper_active:
                    try:
                        # backslash (ui nav toggle keybind)
                        self.keyboard.press('\\')
                        self.keyboard.release('\\')
                        time.sleep(0.05)
                        
                        # enter
                        self.keyboard.press(pynput_keyboard.Key.enter)
                        self.keyboard.release(pynput_keyboard.Key.enter)
                        time.sleep(0.05)
                        
                    except Exception as e:
                        logging.error(f"Error in Loading Asset Skipper: {e}")
                        break
            except Exception as e:
                logging.error(f"Error initializing Loading Asset Skipper: {e}")
                while loading_asset_skipper_active:
                    try:
                        pyautogui.press('esc')
                        time.sleep(0.05)
                        pyautogui.press('\\')
                        time.sleep(0.05)
                        pyautogui.press('enter')
                        time.sleep(0.05)
                    except Exception as e:
                        logging.error(f"Error in Loading Asset Skipper (fallback): {e}")
                        break
        
        elif platform.system() == 'Darwin':  # macOS
            try:
                while loading_asset_skipper_active:
                    try:
                        # backslash (ui nav toggle keybind)
                        self.keyboard.press('\\')
                        self.keyboard.release('\\')
                        time.sleep(0.05)
                        
                        # enter
                        self.keyboard.press(pynput_keyboard.Key.enter)
                        self.keyboard.release(pynput_keyboard.Key.enter)
                        time.sleep(0.05)
                        
                    except Exception as e:
                        logging.error(f"Error in Loading Asset Skipper (macOS): {e}")
                        break
            except Exception as e:
                logging.error(f"Error initializing Loading Asset Skipper (macOS): {e}")
                while loading_asset_skipper_active:
                    try:
                        pyautogui.press('esc')
                        time.sleep(0.05)
                        pyautogui.press('\\')
                        time.sleep(0.05)
                        pyautogui.press('enter')
                        time.sleep(0.05)
                    except Exception as e:
                        logging.error(f"Error in Loading Asset Skipper (macOS fallback): {e}")
                        break
        
        else:  # Linux or other (fucking losers lmao, get a real OS)
            logging.error(f"Loading Asset Skipper not supported on {platform.system()}")
        
        logging.info("Loading Asset Skipper deactivated")

    def execute_main_menu_skipper(self):
        logging.info("Main Menu Skipper activated")
        global main_menu_skipper_active
        
        if platform.system() == 'Windows':
            try:
                while main_menu_skipper_active:
                    try:
                        # backslash (ui nav toggle keybind)
                        self.keyboard.press('\\')
                        self.keyboard.release('\\')
                        time.sleep(0.05)
                        
                        # down arrow
                        self.keyboard.press(pynput_keyboard.Key.down)
                        self.keyboard.release(pynput_keyboard.Key.down)
                        time.sleep(0.05)
                        
                        # enter
                        self.keyboard.press(pynput_keyboard.Key.enter)
                        self.keyboard.release(pynput_keyboard.Key.enter)
                        time.sleep(0.05)
                        
                    except Exception as e:
                        logging.error(f"Error in Main Menu Skipper: {e}")
                        break
            except Exception as e:
                logging.error(f"Error initializing Main Menu Skipper: {e}")
                while main_menu_skipper_active:
                    try:
                        pyautogui.press('esc')
                        time.sleep(0.05)
                        pyautogui.press('\\')
                        time.sleep(0.05)
                        pyautogui.press('down')
                        time.sleep(0.05)
                        pyautogui.press('enter')
                        time.sleep(0.05)
                    except Exception as e:
                        logging.error(f"Error in Main Menu Skipper (fallback): {e}")
                        break
        
        elif platform.system() == 'Darwin':  # macOS
            try:
                while main_menu_skipper_active:
                    try:
                        # backslash (ui nav toggle keybind)
                        self.keyboard.press('\\')
                        self.keyboard.release('\\')
                        time.sleep(0.05)
                        
                        # down arrow
                        self.keyboard.press(pynput_keyboard.Key.down)
                        self.keyboard.release(pynput_keyboard.Key.down)
                        time.sleep(0.05)
                        
                        # enter
                        self.keyboard.press(pynput_keyboard.Key.enter)
                        self.keyboard.release(pynput_keyboard.Key.enter)
                        time.sleep(0.05)
                        
                    except Exception as e:
                        logging.error(f"Error in Main Menu Skipper (macOS): {e}")
                        break
            except Exception as e:
                logging.error(f"Error initializing Main Menu Skipper (macOS): {e}")
                while main_menu_skipper_active:
                    try:
                        pyautogui.press('esc')
                        time.sleep(0.05)
                        pyautogui.press('\\')
                        time.sleep(0.05)
                        pyautogui.press('down')
                        time.sleep(0.05)
                        pyautogui.press('enter')
                        time.sleep(0.05)
                    except Exception as e:
                        logging.error(f"Error in Main Menu Skipper (macOS fallback): {e}")
                        break
        
        else:  # Linux or other (fucking losers lmao, get a real OS)
            logging.error(f"Main Menu Skipper not supported on {platform.system()}")
        
        main_menu_skipper_active = False
        logging.info("Main Menu Skipper deactivated")

    def init_key_listener(self):
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    MainWindow._pressed_keys.add(key.char.lower())
                else:
                    key_name = str(key).replace('Key.', '').lower()
                    # map common modifier names since pynput is quirky like that
                    if key_name == 'ctrl_l' or key_name == 'ctrl_r':
                        key_name = 'ctrl'
                    elif key_name == 'alt_l' or key_name == 'alt_r':
                        key_name = 'alt'
                    elif key_name == 'shift_l' or key_name == 'shift_r':
                        key_name = 'shift'
                    elif key_name == 'cmd' or key_name == 'cmd_l' or key_name == 'cmd_r':
                        key_name = 'win'
                    MainWindow._pressed_keys.add(key_name)
            except Exception as e:
                logging.error(f"Error in on_press: {e}")
        
        def on_release(key):
            try:
                if hasattr(key, 'char') and key.char:
                    MainWindow._pressed_keys.discard(key.char.lower())
                else:
                    key_name = str(key).replace('Key.', '').lower()
                    # map common modifier names since pynput is quirky like that
                    if key_name == 'ctrl_l' or key_name == 'ctrl_r':
                        key_name = 'ctrl'
                    elif key_name == 'alt_l' or key_name == 'alt_r':
                        key_name = 'alt'
                    elif key_name == 'shift_l' or key_name == 'shift_r':
                        key_name = 'shift'
                    elif key_name == 'cmd' or key_name == 'cmd_l' or key_name == 'cmd_r':
                        key_name = 'win'
                    MainWindow._pressed_keys.discard(key_name)
            except Exception as e:
                logging.error(f"Error in on_release: {e}")
        
        if MainWindow._key_listener is None:
            MainWindow._key_listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
            MainWindow._key_listener.daemon = True
            MainWindow._key_listener.start()

    def start_hotkey_monitor(self):
        logging.info("Starting hotkey monitor thread")
        self.hotkey_monitor_running = True
        
        while self.hotkey_monitor_running:
            try:
                self.handle_hotkeys()
                time.sleep(0.05)
            except Exception as e:
                logging.error(f"Hotkey monitor error: {e}")
                time.sleep(0.1)

    def find_roblox_executable(self):
        if CONFIG_DATA.get("override_protocol_enabled", False) and hasattr(self, 'selected_override_version'):
            exe_path = self.selected_override_version["path"]
            exe_type = self.selected_override_version.get("type", "")
            exe_version = self.selected_override_version.get("version", "")
            
            if os.path.exists(exe_path):
                if exe_type == "bootstrapper" or "bloxstrap" in exe_path.lower() or "fishstrap" in exe_path.lower():
                    logging.info(f"Override is a bootstrapper: {exe_path}")
                    
                    bootstrapper_dir = os.path.dirname(exe_path)
                    versions_path = os.path.join(bootstrapper_dir, "Versions")
                    
                    if os.path.exists(versions_path):
                        versions = []
                        for item in os.listdir(versions_path):
                            item_path = os.path.join(versions_path, item)
                            if os.path.isdir(item_path):
                                exe_check = os.path.join(item_path, "RobloxPlayerBeta.exe")
                                if os.path.exists(exe_check):
                                    versions.append((os.path.getmtime(exe_check), item, exe_check))
                        
                        if versions:
                            versions.sort(reverse=True)
                            actual_exe = versions[0][2]
                            logging.info(f"Found actual Roblox executable from bootstrapper: {actual_exe}")
                            return actual_exe
                        else:
                            logging.warning(f"No RobloxPlayerBeta.exe found in {versions_path}")
                    else:
                        logging.warning(f"Versions folder not found at {versions_path}")
                
                logging.info(f"Using override executable directly: {exe_path}")
                return exe_path
        
        try:
            key_path = r"SOFTWARE\Classes\roblox\shell\open\command"
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
                    value, _ = winreg.QueryValueEx(key, "")
                    match = re.search(r'"([^"]+\.exe)"', value)
                    if match:
                        exe_path = match.group(1)
                        if os.path.exists(exe_path):
                            if '-player' in value.lower():
                                bootstrapper_dir = os.path.dirname(exe_path)
                                versions_path = os.path.join(bootstrapper_dir, "Versions")
                                if os.path.exists(versions_path):
                                    versions = []
                                    for item in os.listdir(versions_path):
                                        item_path = os.path.join(versions_path, item)
                                        if os.path.isdir(item_path):
                                            exe_check = os.path.join(item_path, "RobloxPlayerBeta.exe")
                                            if os.path.exists(exe_check):
                                                versions.append((os.path.getmtime(exe_check), item, exe_check))
                                    
                                    if versions:
                                        versions.sort(reverse=True)
                                        logging.info(f"Found bootstrapper version: {versions[0][1]}")
                                        return versions[0][2]
                            return exe_path
            except FileNotFoundError:
                pass
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value, _ = winreg.QueryValueEx(key, "")
                match = re.search(r'"([^"]+\.exe)"', value)
                if match:
                    exe_path = match.group(1)
                    if os.path.exists(exe_path):
                        if '-player' in value.lower():
                            bootstrapper_dir = os.path.dirname(exe_path)
                            versions_path = os.path.join(bootstrapper_dir, "Versions")
                            if os.path.exists(versions_path):
                                versions = []
                                for item in os.listdir(versions_path):
                                    item_path = os.path.join(versions_path, item)
                                    if os.path.isdir(item_path):
                                        exe_check = os.path.join(item_path, "RobloxPlayerBeta.exe")
                                        if os.path.exists(exe_check):
                                            versions.append((os.path.getmtime(exe_check), item, exe_check))
                                
                                if versions:
                                    versions.sort(reverse=True)
                                    return versions[0][2]
                        return exe_path
        except Exception as e:
            logging.error(f"Error finding Roblox from protocol: {e}")
        
        common_paths = [
            os.path.expanduser("~/AppData/Local/Roblox/Versions"),
            r"C:\Program Files (x86)\Roblox\Versions",
            os.path.expanduser("~/AppData/Local/Bloxstrap/Versions"),
            os.path.expanduser("~/AppData/Local/Fishstrap/Versions"),
        ]
        
        for versions_path in common_paths:
            if os.path.exists(versions_path):
                versions = []
                for item in os.listdir(versions_path):
                    item_path = os.path.join(versions_path, item)
                    if os.path.isdir(item_path):
                        exe_check = os.path.join(item_path, "RobloxPlayerBeta.exe")
                        if os.path.exists(exe_check):
                            versions.append((os.path.getmtime(exe_check), item, exe_check))
                
                if versions:
                    versions.sort(reverse=True)
                    logging.info(f"Found Roblox version: {versions[0][1]} at {versions[0][2]}")
                    return versions[0][2]
        
        return None

    def launch_game(self, uri):
        global restart_roblox_on_next_snipe
        logging.info(f"Launching game with URI: {uri}")
        
        if platform.system() == 'Windows':
            try:
                if CONFIG_DATA["leave_game_before_joining"] and self.is_roblox_focused():
                    self.execute_leave_game()
                if CONFIG_DATA["close_roblox_before_joining"] or restart_roblox_on_next_snipe:
                    restart_roblox_on_next_snipe = False
                    self.kill_roblox_process()
                
                executable = self.find_roblox_executable()
                
                if executable and os.path.exists(executable):
                    subprocess.Popen(f'"{executable}" "{uri}"', shell=True)
                    logging.info(f"Launched Roblox with direct execution")
                else:
                    os.startfile(uri)
                    logging.info("Launbched Roblox with URI execution")
            except Exception as e:
                logging.error(f"Error launching: {e}")
                try:
                    os.startfile(uri)
                except:
                    pass
        elif platform.system() == 'Darwin':
            if CONFIG_DATA["leave_game_before_joining"]:
                self.execute_leave_game()
            if CONFIG_DATA["close_roblox_before_joining"]:
                self.kill_roblox_process()
            subprocess.Popen(['open', uri])
        else:
            try:
                subprocess.Popen([uri], shell=True)
            except:
                pass

    async def is_roblox_running(self):
        for proc in psutil.process_iter(['name']):
            try:
                if platform.system() == 'Windows':
                    if 'RobloxPlayer' in proc.info['name']:
                        return True, proc
                elif platform.system() == 'Darwin':
                    if 'roblox' in proc.info['name'].lower():
                        return True, proc
            except:
                continue
        return False, None
    
    async def get_roblox_version(self):
        logging.info("Checking Roblox version")
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if platform.system() == 'Windows':
                    if 'RobloxPlayerBeta.exe' in proc.info['name']:
                        logging.info("Detected Roblox Player Beta version")
                        return "RobloxPlayerBeta", proc
                    elif 'Windows10Universal.exe' in proc.info['name']:
                        logging.info("Detected Microsoft Store version")
                        return "Windows10Universal", proc
                elif platform.system() == 'Darwin':
                    process_name = proc.info['name'].lower()
                    if 'roblox' in process_name:
                        logging.info("Detected Roblox process on macOS")
                        return "RobloxMac", proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            await asyncio.sleep(0)
        logging.info("Roblox process not found")
        return None, None

    async def get_log_directory(self, roblox_version):
        if platform.system() == 'Darwin':
            log_dir = Path(os.path.expanduser("~/Library/Logs/Roblox"))
            if log_dir.exists():
                logging.info(f"Using log directory: {log_dir}")
                return log_dir
            else:
                log_dir = Path(os.path.expanduser("~/Library/Application Support/Roblox/logs"))
                if log_dir.exists():
                    return log_dir
                logging.warning(f"Log directory not found: {log_dir}")
                return None
        elif roblox_version == "Windows10Universal":
            log_dir = Path(os.path.expanduser("~/AppData/Local/Packages/ROBLOXCorporation.ROBLOX_55nm5eh3cm0pr/LocalState/logs"))
        else:
            log_dir = Path(os.path.expanduser("~/AppData/Local/Roblox/logs"))
        
        if log_dir.exists():
            logging.info(f"Using log directory: {log_dir}")
            return log_dir
        else:
            logging.warning(f"Log directory not found: {log_dir}")
            return None

    async def find_latest_log_file(self, log_dir):
        try:
            log_files = list(log_dir.glob("*.log"))
            if not log_files:
                logging.warning("No log files found")
                return None, 0
            
            latest_file = None
            latest_time = 0
            
            for log_file in log_files:
                if "studio" in log_file.name.lower():
                    continue
                    
                try:
                    file_time = os.path.getmtime(log_file)
                    if file_time > latest_time:
                        latest_time = file_time
                        latest_file = log_file
                except OSError:
                    continue
            
            if latest_file:
                logging.info(f"Latest log file: {latest_file} (modified: {latest_time})")
                return latest_file, latest_time
            else:
                logging.warning("No suitable log files found")
                return None, 0
                
        except Exception as e:
            logging.error(f"Error finding latest log file: {e}")
            return None, 0

    async def verify_biome_match(self, expected_category, detected_keyword):
        if not expected_category or expected_category not in ["GLITCHED", "DREAMSPACE", "CYBERSPACE", "SINGULARITY"]:
            return True
        
        logging.info(f"Verifying biome match for category: {expected_category}")
        
        await asyncio.sleep(8)
        
        current_biome = await self.get_current_biome()
        if not current_biome:
            logging.warning("Could not determine current biome")
            return True
        
        current_biome_upper = current_biome.strip().upper()
        expected_biome = expected_category
        
        logging.info(f"Expected: {expected_biome}, Got: {current_biome_upper}")
        
        if current_biome_upper != expected_biome:
            logging.info(f"Biome mismatch! Expected {expected_biome}, got {current_biome_upper}. Closing Roblox.")
            await asyncio.get_event_loop().run_in_executor(executor, self.kill_roblox_process)
            self.show_toast("Bait Detected", f"Closed Roblox due to wrong biome.\n\nExpected: {expected_biome}\nGot: {current_biome_upper}\nKeyword: {detected_keyword or 'Unknown'}")
            return False
        
        logging.info("Biome verification successful")
        return True

    async def get_current_biome(self):
        logging.info("Getting current biome from Roblox logs")

        roblox_version, _ = await self.get_roblox_version()
        if not roblox_version:
            logging.warning("Cannot determine Roblox version")
            return None

        log_dir = await self.get_log_directory(roblox_version)
        if not log_dir:
            logging.warning("Log directory not available")
            return None

        for attempt in range(30):
            latest_file, latest_time = await self.find_latest_log_file(log_dir)
            if not latest_file:
                await asyncio.sleep(2)
                continue

            try:
                with open(latest_file, 'r', encoding='utf-8', errors='ignore') as log_file:
                    logs = log_file.readlines()

                for line in reversed(logs[-200:]):
                    if 'BloxstrapRPC' in line and 'SetRichPresence' in line and 'Sol\'s RNG' in line:
                        if '"largeImage":{"hoverText":"' in line:
                            biome = line.split('"largeImage":{"hoverText":"')[1].split('"')[0].strip()
                            logging.info(f"Biome found: {biome}")
                            return biome
                        else:
                            logging.info("RichPresence line found but no biome info yet")
            except Exception as e:
                logging.error(f"Error reading log file on attempt {attempt + 1}: {e}")

            await asyncio.sleep(2)

        logging.warning("Biome detection timeout after 30 attempts")
        return None

    async def resolve_share_code(self, share_code):
        if share_code in self.resolution_cache:
            cache_time, result = self.resolution_cache[share_code]
            if time.time() - cache_time < 300:
                return result
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': f'Roblox/{CONFIG_DATA.get("override_protocol_version", "unknown").replace("version-", "")} SolSniper/{RAW_VERSION_STR}'}
                async with session.post(f'https://api-priv.vexsys.site/api/endpoints/roblox/resolve-link?linkId={share_code}', headers=headers, timeout=5) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.resolution_cache[share_code] = (time.time(), (result.get('placeId'), result.get('privateServerLinkCode')))
                        return result.get('placeId'), result.get('privateServerLinkCode')
            return None, None
        except Exception as e:
            logging.error(f"Error resolving share code: {e}")
            return None, None

    async def resolve_ropro_link(self, ropro_url):
        if ropro_url in self.resolution_cache:
            cache_time, result = self.resolution_cache[ropro_url]
            if time.time() - cache_time < 300:
                return result
        try:
            if 'ro.pro' in ropro_url:
                final_url = ropro_url
            elif 'ropro.io' in ropro_url:
                if '/join/' not in ropro_url:
                    match = re.search(r'ropro\.io/([a-zA-Z0-9]+)', ropro_url)
                    if match:
                        code = match.group(1)
                        final_url = f"https://ropro.io/join/{code}"
                    else:
                        final_url = ropro_url
                else:
                    final_url = ropro_url
            else:
                return None
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
                async with session.get(final_url, headers=headers, allow_redirects=True, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        patterns = [
                            r'window\.location\.replace\("(roblox://experiences/start\?[^"]+)"\)',
                            r'window\.location\.replace\("(roblox://placeID=[^"]+)"\)',
                            r'window\.location\.replace\("(robloxmobile://placeID=[^"]+)"\)',
                            r'(roblox://[^"\s]+)'
                        ]
                        for pattern in patterns:
                            match = re.search(pattern, html)
                            if match:
                                deeplink = match.group(1).replace('robloxmobile://', 'roblox://')
                                self.resolution_cache[ropro_url] = (time.time(), deeplink)
                                return deeplink
                    return None
        except Exception as e:
            logging.error(f"Error resolving ropro link: {e}")
            return None

    def extract_game_id_from_uri(self, uri):
        match = re.search(r'place(?:I|i)d[=:](\d+)', uri)
        if match:
            return match.group(1)
        match = re.search(r'placeId=(\d+)', uri)
        if match:
            return match.group(1)
        return None

    async def build_uri(self, url):
        if url in self.url_cache:
            cache_time, uri = self.url_cache[url]
            if time.time() - cache_time < 60:
                return uri
        
        uri = None
        if match := re.search(r'roblox\.com/games/(\d+)/[^?]+\?(?:private[_-]?server[_-]?link[_-]?code)=([\w-]+)', url, re.IGNORECASE):
            game_id, private_code = match.groups()
            uri = f"roblox://placeId={game_id}&linkCode={private_code}"
        elif match := re.search(r'roblox\.com/share\?code=([a-f0-9]+)', url):
            share_code = match.group(1)
            resolved_game_id, _ = await self.resolve_share_code(share_code)
            uri = f"roblox://navigation/share_links?code={share_code}&type=Server"
        elif match := re.search(r'roblox\.com/games/start\?placeId=(\d+)&launchData=(\d+)/([a-f0-9\-]+)', url):
            place_id, redirect_place_id, game_instance_id = match.groups()
            uri = f"roblox://experiences/start?placeId={redirect_place_id}&gameInstanceId={game_instance_id}"
        elif match := re.search(r'roblox\.com/games/start\?placeId=(\d+)', url):
            place_id = match.group(1)
            uri = f"roblox://placeId={place_id}"
        elif match := re.search(r'roblox://placeId=(\d+)', url):
            uri = url
        elif match := re.search(r'join-rbx\.vexsys\.site/public\?placeid=(\d+)&gameinstanceid=([A-Za-z0-9\-]+)', url, re.IGNORECASE):
            place_id, game_instance_id = match.groups()
            uri = f"roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}"
        elif match := re.search(r'join-rbx\.vexsys\.site/private\?share_code=([A-Za-z0-9]+)', url, re.IGNORECASE):
            share_code = match.group(1)
            uri = f"roblox://navigation/share_links?code={share_code}&type=Server"
        elif match := re.search(r'join-rbx\.vexsys\.site/private\?placeid=(\d+)&link_code=([A-Za-z0-9\-]+)', url, re.IGNORECASE):
            place_id, link_code = match.groups()
            uri = f"roblox://placeId={place_id}&linkCode={link_code}"
        elif match := re.search(r'roseal\.live/join\?placeId=(\d+)&gameInstanceId=([A-Za-z0-9\-]+)', url, re.IGNORECASE):
            place_id, game_instance_id = match.groups()
            uri = f"roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}"
        elif match := re.search(r'(?:ro\.pro|ropro\.io)/(?:join/)?([a-zA-Z0-9]+)', url, re.IGNORECASE):
            if CONFIG_DATA["snipe_ropro_links"]:
                full_url = f"https://ropro.io/join/{match.group(1)}" if 'ropro.io' in url else f"https://ro.pro/{match.group(1)}"
                uri = await self.resolve_ropro_link(full_url)
        
        if uri:
            self.url_cache[url] = (time.time(), uri)
        return uri

    async def process_server_link(self, content, embeds=None, discord_user_id=None, discord_channel_id=None, discord_server_id=None, discord_message_id=None, avatar_url=None, message=None):
        async with self.process_lock:
            if self.is_processing or not sniper_active or sniper_paused:
                return {"success": False, "matched_category": None}
            
            self.is_processing = True
            matched_category = None
            detected_keyword = None
            
            try:
                if not content and not embeds:
                    self.is_processing = False
                    return {"success": False, "matched_category": None}
                
                if embeds and isinstance(embeds, list):
                    embed_parts = []
                    for embed in embeds:
                        if isinstance(embed, dict):
                            if embed.get("title"):
                                embed_parts.append(embed["title"])
                            if embed.get("description"):
                                embed_parts.append(embed["description"])
                            if embed.get("fields"):
                                for field in embed["fields"]:
                                    if field.get("value"):
                                        embed_parts.append(field["value"])
                    if embed_parts:
                        content = f"{content} {' '.join(embed_parts)}" if content else ' '.join(embed_parts)
                
                clean_content = URLExtractor.clean_content(content)

                logging.info(f"Processing message {discord_message_id} in channel {discord_channel_id}: {content}")
                
                urls = URLExtractor.extract_urls(clean_content)
                if not urls:
                    self.is_processing = False
                    return {"success": False, "matched_category": None}
                
                self.keyword_matcher.update_categories(CONFIG_DATA)
                
                allowed, matched_category, detected_keyword = self.keyword_matcher.check_keywords(clean_content)
                
                if not allowed:
                    self.is_processing = False
                    return {"success": False, "matched_category": None}
                
                if self.keyword_matcher.check_blacklist(clean_content, matched_category):
                    self.is_processing = False
                    logging.info(f"Skipping message {discord_message_id} with blacklisted keywords")
                    return {"success": False, "matched_category": None}
                
                uri = None
                game_id = None
                
                for url in urls:
                    result = URLExtractor.parse_private_server(url)
                    if result:
                        game_id, private_code = result
                        uri = f"roblox://placeId={game_id}&linkCode={private_code}"
                        break
                    
                    share_code = URLExtractor.parse_share_code(url)
                    if share_code:
                        resolved_game_id, _ = await self.resolve_share_code(share_code)
                        if resolved_game_id:
                            game_id = resolved_game_id
                        uri = f"roblox://navigation/share_links?code={share_code}&type=Server"
                        break
                    
                    result = URLExtractor.parse_joinrbx_public(url) if CONFIG_DATA["snipe_joinrbx_links"] else None
                    if result:
                        place_id, game_instance_id = result
                        uri = f"roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}"
                        game_id = place_id
                        break
                    
                    result = URLExtractor.parse_joinrbx_private(url) if CONFIG_DATA["snipe_joinrbx_links"] else None
                    if result:
                        place_id, link_code = result
                        uri = f"roblox://placeId={place_id}&linkCode={link_code}"
                        game_id = place_id
                        break
                    
                    share_code = URLExtractor.parse_joinrbx_share(url) if CONFIG_DATA["snipe_joinrbx_links"] else None
                    if share_code:
                        uri = f"roblox://navigation/share_links?code={share_code}&type=Server"
                        game_id = None
                        break
                    
                    result = URLExtractor.parse_roseal(url) if CONFIG_DATA["snipe_roseal_links"] else None
                    if result:
                        place_id, game_instance_id = result
                        uri = f"roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}"
                        game_id = place_id
                        break

                    result = URLExtractor.parse_fishstrap(url) if CONFIG_DATA["snipe_fishstrap_links"] else None
                    if result:
                        place_id, game_instance_id = result
                        uri = f"roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}"
                        game_id = place_id
                        break
                    
                    result = URLExtractor.parse_deeplink(url)
                    if result:
                        place_id, launch_data = result
                        uri = f"roblox://placeId={place_id}"
                        if launch_data:
                            uri += f"&launchData={launch_data}"
                        game_id = place_id
                        break
                    
                    ropro_code = URLExtractor.parse_ropro(url) if CONFIG_DATA["snipe_ropro_links"] else None
                    if ropro_code and CONFIG_DATA.get("snipe_ropro_links", True):
                        full_url = f"https://ropro.io/join/{ropro_code}" if 'ropro.io' in url else f"https://ro.pro/{ropro_code}"
                        uri = await self.resolve_ropro_link(full_url)
                        if uri:
                            game_id = self.extract_game_id_from_uri(uri)
                            break
                
                if not uri:
                    self.is_processing = False
                    return {"success": False, "matched_category": None}
                
                if CONFIG_DATA.get("only_join_sols_links", True) and game_id and str(game_id) != "15532962292":
                    self.is_processing = False
                    return {"success": False, "matched_category": None}
                
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(executor, self.launch_game, uri)
                
                if CONFIG_DATA.get("minimize_other_windows", False):
                    await loop.run_in_executor(executor, self.minimize_other_windows)
                
                roblox_running, _ = await self.is_roblox_running()
                for _ in range(15):
                    if roblox_running:
                        break
                    await asyncio.sleep(0.3)
                    roblox_running, _ = await self.is_roblox_running()
                
                if not roblox_running:
                    logging.error("Roblox process did not start")
                    self.is_processing = False
                    return {"success": False, "matched_category": None}
                
                self.show_toast("Successful Snipe", 
                            f"Successfully sniped!\n\nCategory: {matched_category or 'Unknown'}\nKeyword: {detected_keyword or 'Unknown'}",
                            discord_server_id, discord_channel_id, discord_message_id)
                logging.info(f"Successfully sniped {matched_category}, keyword: {detected_keyword}")
                
                if CONFIG_DATA.get("auto_pause_sniper", True):
                    if matched_category:
                        category_key = matched_category.lower().replace(' ', '_')
                        pause_duration = int(CONFIG_DATA.get(f"pause_duration_{category_key}", 60))
                    else:
                        pause_duration = int(CONFIG_DATA.get("pause_duration", 120))
                    self.temporarily_pause_sniper(pause_duration)
                
                return {"success": True, "matched_category": matched_category}
                
            except Exception as e:
                logging.error(f"Error in process_server_link: {e}")
                return {"success": False, "matched_category": None}
            finally:
                self.is_processing = False

    def create_redirect_deeplink(self, redirect_place_id, game_instance_id):
        return f"roblox://experiences/start?placeId={redirect_place_id}&gameInstanceId={game_instance_id}"

    def minimize_other_windows(self):
        logging.info("Minimizing other windows")
        try:
            if platform.system() == 'Windows':
                def enum_handler(hwnd, lParam):
                    if hwnd != self.winId() and win32gui.IsWindowVisible(hwnd):
                        window_title = win32gui.GetWindowText(hwnd)
                        if "Roblox" not in window_title:
                            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                win32gui.EnumWindows(enum_handler, None)
            elif platform.system() == 'Darwin':
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                    set allApps to every application process whose visible is true and background only is false
                    repeat with appProcess in allApps
                        set appName to name of appProcess
                        if appName is not frontApp and appName is not "Finder" and appName is not "Sol Sniper" and appName is not "Roblox" then
                            try
                                tell application "System Events" to tell process appName
                                    set miniaturized of every window to true
                                end tell
                            on error
                            end try
                        end if
                    end repeat
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
        except Exception as e:
            logging.error(f"Error minimizing windows: {e}")

    def focus_roblox_window(self):
        logging.info("Focusing Roblox window")
        try:
            if platform.system() == 'Windows':
                def enum_handler(hwnd, lParam):
                    if 'Roblox' in win32gui.GetWindowText(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(hwnd)
                win32gui.EnumWindows(enum_handler, None)
            elif platform.system() == 'Darwin':
                script = '''
                tell application "System Events"
                    set robloxProcess to first application process whose name contains "Roblox"
                    if robloxProcess exists then
                        set frontmost of robloxProcess to true
                        try
                            tell robloxProcess
                                repeat with win in windows
                                    if miniaturized of win is true then
                                        set miniaturized of win to false
                                    end if
                                end repeat
                            end tell
                        end try
                    end if
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
        except Exception as e:
            logging.error(f"Error focusing Roblox window: {e}")

    def execute_leave_game(self):
        logging.info("Executing leave game sequence")
        try:
            if platform.system() == 'Windows':
                self.keyboard.press(pynput_keyboard.Key.esc)
                self.keyboard.release(pynput_keyboard.Key.esc)
                time.sleep(0.1)
                self.keyboard.press('l')
                self.keyboard.release('l')
                time.sleep(0.1)
                self.keyboard.press(pynput_keyboard.Key.enter)
                self.keyboard.release(pynput_keyboard.Key.enter)
            
            elif platform.system() == 'Darwin':  # macOS
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                    return frontApp
                end tell
                '''
                result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                front_app = result.stdout.strip()
                
                if "Roblox" in front_app:
                    self.keyboard.press(pynput_keyboard.Key.esc)
                    self.keyboard.release(pynput_keyboard.Key.esc)
                    time.sleep(0.1)
                    self.keyboard.press('l')
                    self.keyboard.release('l')
                    time.sleep(0.1)
                    self.keyboard.press(pynput_keyboard.Key.enter)
                    self.keyboard.release(pynput_keyboard.Key.enter)
            
        except Exception as e:
            logging.error(f"Error executing leave game sequence: {e}")
    
    def kill_roblox_process(self):
        logging.info("Killing Roblox process")
        try:
            if platform.system() == 'Windows':
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == 'RobloxPlayerBeta.exe' or proc.info['name'] == 'Windows10Universal.exe':
                        proc.kill()
            elif platform.system() == 'Darwin':
                subprocess.run(['pkill', '-f', 'RobloxPlayer'])
                subprocess.run(['pkill', '-f', 'Roblox'])
                subprocess.run(['killall', '-9', 'RobloxPlayer'], capture_output=True)
                subprocess.run(['killall', '-9', 'Roblox'], capture_output=True)
        except Exception as e:
            logging.error(f"Error killing Roblox process: {e}")
    
    def create_sidebar_btn(self, text, icon=None, svg=None, color="#4a7bff", url=None):
        btn = QPushButton()
        btn.setFixedHeight(45)
        layout = QHBoxLayout(btn)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        label = QLabel(text)
        label.setStyleSheet("color: white; font-weight: 500; font-size: 14px; background: transparent;")
        label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        r, g, b, a = self.hex_to_rgba(color)

        def rgb_to_hsl(r, g, b):
            r, g, b = r / 255.0, g / 255.0, b / 255.0
            mx = max(r, g, b)
            mn = min(r, g, b)
            l = (mx + mn) / 2
            if mx == mn:
                h = s = 0
            else:
                d = mx - mn
                s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
                if mx == r:
                    h = (g - b) / d + (6 if g < b else 0)
                elif mx == g:
                    h = (b - r) / d + 2
                else:
                    h = (r - g) / d + 4
                h /= 6
            return h, s, l

        h, s, l = rgb_to_hsl(r, g, b)
        h_deg = int(h * 360)
        s_pct = int(s * 100)
        l_pct = int(l * 100)

        hover_l = min(l + 0.04, 1.0)
        pressed_l = max(l - 0.04, 0.0)
        hover_l_pct = int(hover_l * 100)
        pressed_l_pct = int(pressed_l * 100)

        base_hsla = f"hsla({h_deg}, {s_pct}%, {l_pct}%, 1)"
        hover_hsla = f"hsla({h_deg}, {s_pct}%, {hover_l_pct}%, 1)"
        pressed_hsla = f"hsla({h_deg}, {s_pct}%, {pressed_l_pct}%, 1)"

        if svg:
            svg_widget = QSvgWidget()
            svg_widget.load(svg)
            svg_widget.setFixedSize(28, 28)
            svg_widget.setStyleSheet("background: transparent;")
            layout.addWidget(svg_widget)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {base_hsla};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                    font-size: 14px;
                    text-align: left;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    background-color: {hover_hsla};
                }}
                QPushButton:pressed {{
                    background-color: {pressed_hsla};
                }}
            """)
            if url:
                btn.clicked.connect(lambda: webbrowser.open(url))
        elif icon:
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(32, 32))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {base_hsla};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                    font-size: 14px;
                    text-align: center;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    background-color: {hover_hsla};
                }}
                QPushButton:pressed {{
                    background-color: {pressed_hsla};
                }}
            """)
            if url:
                btn.clicked.connect(lambda: webbrowser.open(url))
        elif not icon and not svg and color == "#4a7bff" and not url and CONFIG_DATA["gradient_theme"] == True:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                    font-size: 14px;
                    text-align: left;
                    padding: 8px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3a6bdf, stop:1 #7a3c9f);
                }
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {base_hsla};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                    font-size: 14px;
                    text-align: center;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    background-color: {hover_hsla};
                }}
                QPushButton:pressed {{
                    background-color: {pressed_hsla};
                }}
            """)
            if url:
                btn.clicked.connect(lambda: webbrowser.open(url))
        return btn

    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip('#')

        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])

        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = 1.0
        elif len(hex_color) == 8:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16) / 255.0
        else:
            raise ValueError("Invalid hexadecimal color string. Must be 6 or 8 digits.")

        return (r, g, b, a)
    
    def create_sniper_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(20)

        base_cat_frame = GradientFrame()
        base_cat_frame.setStyleSheet("border-radius: 12px;")
        base_cat_layout = QVBoxLayout(base_cat_frame)
        base_cat_layout.setContentsMargins(20, 20, 20, 20)

        base_cat_title = QLabel("Base Categories")
        base_cat_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
        base_cat_layout.addWidget(base_cat_title)

        def add_checkbox_row(label_text, checkbox, duration_input=None):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(3)
            row_layout.addWidget(checkbox)
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #e0e0e0; margin-left: 4px;")
            row_layout.addWidget(label)
            row_layout.addStretch()
            
            if duration_input:
                duration_label = QLabel("Pause:")
                duration_label.setStyleSheet("font-size: 14px; color: #e0e0e0; margin-right: 8px;")
                row_layout.addWidget(duration_label)
                
                duration_input.setFixedWidth(70)
                duration_input.setFixedHeight(30)
                duration_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #2d2d2d;
                        color: #e0e0e0;
                        border: 1px solid #444;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 12px;
                    }
                """)
                duration_input.setValidator(QIntValidator(1, 9999))
                row_layout.addWidget(duration_input)
                
                seconds_label = QLabel("sec")
                seconds_label.setStyleSheet("font-size: 12px; color: #888888; margin-left: 4px;")
                row_layout.addWidget(seconds_label)
            
            return row_widget

        self.glitch_cb = QCheckBox()
        self.glitch_cb.setChecked(CONFIG_DATA["glitchsniping"])
        self.glitch_duration = QLineEdit()
        self.glitch_duration.setText(str(CONFIG_DATA.get("pause_duration_glitched", 180)))
        base_cat_layout.addWidget(add_checkbox_row("Glitch Sniping", self.glitch_cb, self.glitch_duration))

        self.dream_cb = QCheckBox()
        self.dream_cb.setChecked(CONFIG_DATA["dreamsniping"])
        self.dream_duration = QLineEdit()
        self.dream_duration.setText(str(CONFIG_DATA.get("pause_duration_dreamspace", 180)))
        base_cat_layout.addWidget(add_checkbox_row("Dreamspace Sniping", self.dream_cb, self.dream_duration))

        self.cyber_cb = QCheckBox()
        self.cyber_cb.setChecked(CONFIG_DATA["cybersniping"])
        self.cyber_duration = QLineEdit()
        self.cyber_duration.setText(str(CONFIG_DATA.get("pause_duration_cyberspace", 720)))
        base_cat_layout.addWidget(add_checkbox_row("Cyberspace Sniping", self.cyber_cb, self.cyber_duration))

        self.singularity_cb = QCheckBox()
        self.singularity_cb.setChecked(CONFIG_DATA["singularitysniping"])
        self.singularity_duration = QLineEdit()
        self.singularity_duration.setText(str(CONFIG_DATA.get("pause_duration_singularity", 1200)))
        base_cat_layout.addWidget(add_checkbox_row("Singularity Sniping", self.singularity_cb, self.singularity_duration))

        self.jester_cb = QCheckBox()
        self.jester_cb.setChecked(CONFIG_DATA["jestersniping"])
        self.jester_duration = QLineEdit()
        self.jester_duration.setText(str(CONFIG_DATA.get("pause_duration_jester", 120)))
        base_cat_layout.addWidget(add_checkbox_row("Jester Sniping", self.jester_cb, self.jester_duration))

        self.void_cb = QCheckBox()
        self.void_cb.setChecked(CONFIG_DATA["voidcoinsniping"])
        self.void_duration = QLineEdit()
        self.void_duration.setText(str(CONFIG_DATA.get("pause_duration_void_coin", 120)))
        base_cat_layout.addWidget(add_checkbox_row("Void Coin Sniping", self.void_cb, self.void_duration))

        scroll_layout.addWidget(base_cat_frame)

        custom_categories = []
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, 'r') as f:
                    keywords_data = json.load(f)
                    custom_categories = keywords_data.get("custom_categories", [])
            except:
                pass

        self.custom_category_durations = {}

        if custom_categories:
            custom_cat_frame = GradientFrame()
            custom_cat_frame.setStyleSheet("border-radius: 12px;")
            custom_cat_frame.setObjectName("custom_cat_frame")
            custom_cat_layout = QVBoxLayout(custom_cat_frame)
            custom_cat_layout.setContentsMargins(20, 20, 20, 20)

            custom_cat_title = QLabel("Custom Categories")
            custom_cat_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
            custom_cat_layout.addWidget(custom_cat_title)

            custom_cat_label = QLabel("Loading...")
            custom_cat_label.setStyleSheet("font-size: 14px; color: #e0e0e0;")
            custom_cat_layout.addWidget(custom_cat_label)

            self.custom_category_checkboxes = {}

            scroll_layout.addWidget(custom_cat_frame)

        advanced_frame = GradientFrame()
        advanced_frame.setStyleSheet("border-radius: 12px;")
        advanced_layout = QVBoxLayout(advanced_frame)
        advanced_layout.setContentsMargins(20, 20, 20, 20)

        advanced_title = QLabel("Advanced Settings")
        advanced_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
        advanced_layout.addWidget(advanced_title)

        self.close_roblox_cb = QCheckBox()
        self.close_roblox_cb.setChecked(CONFIG_DATA["close_roblox_before_joining"])
        advanced_layout.addWidget(add_checkbox_row("Close Roblox Before Joining a Snipe", self.close_roblox_cb))

        self.leave_game_cb = QCheckBox()
        self.leave_game_cb.setChecked(CONFIG_DATA["leave_game_before_joining"])
        advanced_layout.addWidget(add_checkbox_row("Leave Game Before Joining a Snipe", self.leave_game_cb))

        leave_game_label = QLabel("This setting will automatically press Esc -> L -> Enter to leave the game the user is in.\nWill only execute if the user is tabbed into Roblox.")
        leave_game_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
        advanced_layout.addWidget(leave_game_label)

        self.minimize_other_windows_cb = QCheckBox()
        self.minimize_other_windows_cb.setChecked(CONFIG_DATA["minimize_other_windows"])
        advanced_layout.addWidget(add_checkbox_row("Minimize Other Windows on Snipe (Besides Roblox)", self.minimize_other_windows_cb))

        self.auto_pause_sniper_cb = QCheckBox()
        self.auto_pause_sniper_cb.setChecked(CONFIG_DATA["auto_pause_sniper"])
        advanced_layout.addWidget(add_checkbox_row("Auto Pause Sniper Upon Snipe", self.auto_pause_sniper_cb))

        pause_duration_label = QLabel("This setting will automatically pause the sniper for the configured length of the sniped category\nabove when you snipe.")
        pause_duration_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
        advanced_layout.addWidget(pause_duration_label)

        if CONFIG_DATA["advanced_mode"] == True:
            self.only_join_sols_links_cb = QCheckBox()
            self.only_join_sols_links_cb.setChecked(CONFIG_DATA["only_join_sols_links"])
            advanced_layout.addWidget(add_checkbox_row("Only Join Sol's RNG Servers When Sniping", self.only_join_sols_links_cb))

            only_join_sols_label = QLabel("This setting will make the sniper only join private servers that lead to Sol's RNG when sniping.\nTurning this off will allow you to snipe other Roblox games.")
            only_join_sols_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
            advanced_layout.addWidget(only_join_sols_label)

        self.ignore_messages_that_respond_cb = QCheckBox()
        self.ignore_messages_that_respond_cb.setChecked(CONFIG_DATA["ignore_messages_that_respond"])
        advanced_layout.addWidget(add_checkbox_row("Ignore Messages that are Responding to Other Messages", self.ignore_messages_that_respond_cb))

        scroll_layout.addWidget(advanced_frame)

        custom_links_frame = GradientFrame()
        custom_links_frame.setStyleSheet("border-radius: 12px;")
        custom_links_layout = QVBoxLayout(custom_links_frame)
        custom_links_layout.setContentsMargins(20, 20, 20, 20)

        custom_links_title = QLabel("Custom Link Sniping")
        custom_links_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
        custom_links_layout.addWidget(custom_links_title)

        self.snipe_ropro_links_cb = QCheckBox()
        self.snipe_ropro_links_cb.setChecked(CONFIG_DATA["snipe_ropro_links"])
        custom_links_layout.addWidget(add_checkbox_row("Snipe RoPro Links", self.snipe_ropro_links_cb))

        snipe_ropro_links_label = QLabel("This setting will make it so you will still join servers even if the user who sent the message\nsends a RoPro (ro.pro / ropro.io) link instead of a roblox.com link.")
        snipe_ropro_links_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
        custom_links_layout.addWidget(snipe_ropro_links_label)

        self.snipe_joinrbx_links_cb = QCheckBox()
        self.snipe_joinrbx_links_cb.setChecked(CONFIG_DATA["snipe_joinrbx_links"])
        custom_links_layout.addWidget(add_checkbox_row("Snipe JoinRBX Links", self.snipe_joinrbx_links_cb))

        snipe_joinrbx_links_label = QLabel("This setting will make it so you will still join servers even if the user who sent the message\nsends a JoinRBX (join-rbx.vexsys.site) link instead of a roblox.com link.")
        snipe_joinrbx_links_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
        custom_links_layout.addWidget(snipe_joinrbx_links_label)

        self.snipe_roseal_links_cb = QCheckBox()
        self.snipe_roseal_links_cb.setChecked(CONFIG_DATA["snipe_roseal_links"])
        custom_links_layout.addWidget(add_checkbox_row("Snipe RoSeal Links", self.snipe_roseal_links_cb))

        snipe_roseal_links_label = QLabel("This setting will make it so you will still join servers even if the user who sent the message\nsends a RoSeal (roseal.live) link instead of a roblox.com link.")
        snipe_roseal_links_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
        custom_links_layout.addWidget(snipe_roseal_links_label)

        self.snipe_fishstrap_links_cb = QCheckBox()
        self.snipe_fishstrap_links_cb.setChecked(CONFIG_DATA["snipe_fishstrap_links"])
        custom_links_layout.addWidget(add_checkbox_row("Snipe FishStrap links", self.snipe_fishstrap_links_cb))

        snipe_fishstrap_links_label = QLabel("This setting will make it so you will still join servers even if the user who sent the message\nsends a FishStrap (fishstrap.app) link instead of a roblox.com link.")
        snipe_fishstrap_links_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-top: 5px;")
        custom_links_layout.addWidget(snipe_fishstrap_links_label)

        scroll_layout.addWidget(custom_links_frame)

        if platform.system() == "Windows":
            advanced_protocol_frame = GradientFrame()
            advanced_protocol_frame.setStyleSheet("border-radius: 12px;")
            adv_layout = QVBoxLayout(advanced_protocol_frame)
            adv_layout.setContentsMargins(20, 20, 20, 20)

            override_protocol_label = QLabel("Protocol Override (Will only override roblox://)")
            override_protocol_label.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
            adv_layout.addWidget(override_protocol_label)

            version_selection_layout = QHBoxLayout()
            version_selection_layout.setSpacing(15)
            
            version_label = QLabel("Selected Version:")
            version_label.setStyleSheet("font-size: 16px; color: #e0e0e0;")
            version_selection_layout.addWidget(version_label)
            
            self.override_version_label = QLabel("No version selected")
            self.override_version_label.setStyleSheet("font-size: 14px; color: #888888; background-color: #2d2d2d; border: 1px solid #444; border-radius: 6px; padding: 8px 12px;")
            self.override_version_label.setMinimumHeight(50)
            self.override_version_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            version_selection_layout.addWidget(self.override_version_label)
            
            self.select_override_btn = QPushButton("Select Version")
            self.select_override_btn.setFixedSize(170, 40)
            if CONFIG_DATA["gradient_theme"] == True:
                self.select_override_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4a7bff, stop:1 #8a4caf);
                        color: white;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5a8bff, stop:1 #9a5cbf);
                    }
                    QPushButton:disabled {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a5baf, stop:1 #7a3c9f);
                    }
                """)
            else:
                self.select_override_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a7bff;
                        color: white;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #5a8bff;
                    }
                    QPushButton:disabled {
                        background-color: #3a5baf;
                    }
                """)
            self.select_override_btn.clicked.connect(self.select_override_version)
            version_selection_layout.addWidget(self.select_override_btn)
            
            adv_layout.addLayout(version_selection_layout)

            self.not_supported_note_label = QLabel("Note: The newest Microsoft Store version of Roblox (Name is \"Roblox - Windows\") is not supported.")
            self.not_supported_note_label.setStyleSheet("font-size: 12px; color: #888888; margin-top: 8px; margin-bottom: 0px;")
            self.not_supported_note_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            adv_layout.addWidget(self.not_supported_note_label)

            self.protocol_status_label = QLabel("No version selected for override")
            self.protocol_status_label.setStyleSheet("font-size: 13px; color: #ff5555; font-weight: 500; margin-top: 8px; margin-bottom: 12px;")
            self.protocol_status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            adv_layout.addWidget(self.protocol_status_label)

            protocol_buttons_layout = QHBoxLayout()
            protocol_buttons_layout.setSpacing(10)
            
            self.override_btn = QPushButton("Override Protocol")
            self.override_btn.setFixedHeight(40)
            if CONFIG_DATA["gradient_theme"] == True:
                self.override_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4a7bff, stop:1 #8a4caf);
                        color: white;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5a8bff, stop:1 #9a5cbf);
                    }
                    QPushButton:disabled {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a5baf, stop:1 #7a3c9f);
                    }
                """)
            else:
                self.override_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a7bff;
                        color: white;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #5a8bff;
                    }
                    QPushButton:disabled {
                        background-color: #3a5baf;
                    }
                """)
            self.override_btn.clicked.connect(self.override_roblox_protocol)
            protocol_buttons_layout.addWidget(self.override_btn, 1)
            
            self.restore_btn = QPushButton("Restore Protocol")
            self.restore_btn.setFixedHeight(40)
            if CONFIG_DATA["gradient_theme"] == True:
                self.restore_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4a7bff, stop:1 #8a4caf);
                        color: white;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5a8bff, stop:1 #9a5cbf);
                    }
                    QPushButton:disabled {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a5baf, stop:1 #7a3c9f);
                    }
                """)
            else:
                self.restore_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a7bff;
                        color: white;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #5a8bff;
                    }
                    QPushButton:disabled {
                        background-color: #3a5baf;
                    }
                """)
            self.restore_btn.clicked.connect(self.restore_roblox_protocol)
            protocol_buttons_layout.addWidget(self.restore_btn, 1)
            
            adv_layout.addLayout(protocol_buttons_layout)

            scroll_layout.addWidget(advanced_protocol_frame)

        credentials_frame = GradientFrame()
        credentials_frame.setStyleSheet("border-radius: 12px;")
        credentials_layout = QVBoxLayout(credentials_frame)
        credentials_layout.setContentsMargins(20, 20, 20, 20)

        credentials_title = QLabel("Credentials")
        credentials_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
        credentials_layout.addWidget(credentials_title)

        token_layout = QHBoxLayout()
        token_layout.setSpacing(15)

        token_star = ClickableLabel("★", "https://github.com/vexsyx/sniper-v3?tab=readme-ov-file#%EF%B8%8F-configuration:~:text=Credential%20Setup%20Guide")
        token_star.setStyleSheet("font-size: 16px; color: #e0e0e0;")
        token_star.setToolTip("The Discord Token is a required input. Click the star to learn how to get your Discord Token.")
        token_layout.addWidget(token_star)

        token_label = QLabel("Discord Token:")
        token_label.setStyleSheet("font-size: 16px; color: #e0e0e0;")
        token_layout.addWidget(token_label)

        token_input_widget = QWidget()
        token_input_layout = QHBoxLayout(token_input_widget)
        token_input_layout.setContentsMargins(0, 0, 0, 0)
        token_input_layout.setSpacing(0)

        self.token_input = QLineEdit()
        self.token_input.setText(CONFIG_DATA["token"])
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("Enter your Discord token")
        self.token_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                padding: 8px 12px;
                font-size: 14px;
                border-right: none;
            }
        """)
        self.token_input.setFixedHeight(50)
        token_input_layout.addWidget(self.token_input)

        self.token_eye_btn = QPushButton()
        self.token_eye_btn.setFixedSize(50, 50)
        self.token_eye_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.token_eye_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                border-left: none;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)

        self.token_eye_svg = QSvgWidget(self.token_eye_btn)
        self.token_eye_svg.load(QByteArray(EYE_CLOSED_SVG))
        self.token_eye_svg.setFixedSize(20, 20)
        self.token_eye_svg.move(15, 15)
        self.token_eye_svg.setStyleSheet("background: transparent;")

        self.token_eye_btn.clicked.connect(self.toggle_token_visibility)
        token_input_layout.addWidget(self.token_eye_btn)

        token_layout.addWidget(token_input_widget)
        credentials_layout.addLayout(token_layout)

        scroll_layout.addWidget(credentials_frame)

        status_frame = GradientFrame()
        status_frame.setStyleSheet("border-radius: 12px;")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(20, 20, 20, 20)

        status_title = QLabel("Sniper Status")
        status_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
        status_layout.addWidget(status_title)
        
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        status_layout.addWidget(self.status_label)
        
        self.start_btn = QPushButton("Start Sniping")
        self.start_btn.setFixedHeight(50)
        if CONFIG_DATA["gradient_theme"] == True:
            self.start_btn.setStyleSheet("""
                QPushButton {
                    font-weight: 600;
                    font-size: 16px;
                    padding: 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QPushButton:disabled {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3a5baf, stop:1 #7a3c9f);
                }
            """)
        else:
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 600;
                    font-size: 16px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
                QPushButton:disabled {
                    background-color: #3a5baf;
                }
            """)
        status_layout.addWidget(self.start_btn)

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setFixedHeight(45)
        if CONFIG_DATA["gradient_theme"] == True:
            self.save_btn.setStyleSheet("""
                QPushButton {
                    font-weight: 500;
                    font-size: 16px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8a4caf;
                    color: white;
                    font-weight: 500;
                    font-size: 16px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #9a5cbf;
                }
            """)
        self.save_btn.clicked.connect(self.save_settings_btn)
        status_layout.addWidget(self.save_btn)

        scroll_layout.addWidget(status_frame)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        return tab

    def toggle_token_visibility(self):
        if self.token_input.echoMode() == QLineEdit.EchoMode.Password:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.token_eye_svg.load(QByteArray(EYE_OPEN_SVG))
        else:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.token_eye_svg.load(QByteArray(EYE_CLOSED_SVG))
        self.token_input.setCursorPosition(0)

    def select_override_version(self):
        if platform.system() != 'Windows':
            QMessageBox.warning(self, "Unsupported Platform", "Protocol override is only available on Windows.")
            return
        
        dialog = RobloxVersionDialog(self, allow_custom=CONFIG_DATA["advanced_mode"])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_version = dialog.get_selected_version()
            if selected_version:
                self.selected_override_version = selected_version
                self.override_version_label.setText(selected_version["name"])
                self.update_protocol_status()

    def override_roblox_protocol(self):
        if not hasattr(self, 'selected_override_version') or not self.selected_override_version:
            QMessageBox.warning(self, "No Version Selected", "Please select a Roblox version first.")
            return
        
        success = override_roblox_protocol(
            self.selected_override_version["path"], 
            self.selected_override_version["type"],
            self.selected_override_version["version"]
        )
        
        if success:
            QMessageBox.information(self, "Success", "Roblox protocol overridden successfully!")
            self.update_protocol_status()
        else:
            QMessageBox.warning(self, "Error", "Failed to override Roblox protocol. Please try running as administrator.")

    def restore_roblox_protocol(self):
        success = restore_roblox_protocol()
        
        if success:
            QMessageBox.information(self, "Success", "Roblox protocol restored successfully!")
            self.update_protocol_status()
        else:
            QMessageBox.warning(self, "Error", "Failed to restore Roblox protocol. Please try running as administrator.")

    def update_protocol_status(self):
        if platform.system() != 'Windows':
            self.protocol_status_label.setText("Windows only feature")
            self.select_override_btn.setEnabled(False)
            self.override_btn.setEnabled(False)
            self.restore_btn.setEnabled(False)
            return
        
        is_overridden = is_roblox_protocol_overridden()
        has_selected_version = hasattr(self, 'selected_override_version') and self.selected_override_version is not None
        
        if is_overridden:
            target = get_roblox_protocol_target()
            if target and has_selected_version:
                current_path = self.selected_override_version["path"].lower().replace('"', '')
                target_path = target.lower().replace('"', '')
                if current_path in target_path:
                    self.protocol_status_label.setText("✓ Roblox protocol overridden and matches selected version")
                    self.protocol_status_label.setStyleSheet("font-size: 13px; color: #4CAF50; font-weight: 500; padding: 8px 0px;")
                    self.override_btn.setEnabled(False)
                else:
                    self.protocol_status_label.setText("⚠ Roblox protocol overridden but points to different version")
                    self.protocol_status_label.setStyleSheet("font-size: 13px; color: #FF9800; font-weight: 500; padding: 8px 0px;")
                    self.override_btn.setEnabled(True)
            else:
                self.protocol_status_label.setText("✓ Roblox protocol overridden")
                self.protocol_status_label.setStyleSheet("font-size: 13px; color: #4CAF50; font-weight: 500; padding: 8px 0px;")
                self.override_btn.setEnabled(has_selected_version)
            
            self.restore_btn.setEnabled(True)
        else:
            self.protocol_status_label.setText("✗ Roblox protocol not overridden")
            self.protocol_status_label.setStyleSheet("font-size: 13px; color: #ff5555; font-weight: 500; padding: 8px 0px;")
            self.override_btn.setEnabled(has_selected_version)
            self.restore_btn.setEnabled(False)
        
        self.select_override_btn.setEnabled(True)
    
    def save_settings_btn(self):
        self.save_settings()
        QMessageBox.information(self, "Success", "Settings saved successfully!")

    def create_accounts_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Account Management")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 10px;")
        frame_layout.addWidget(title)

        if platform.system() != "Windows":
            unsupported_label = QLabel("Account management features are only available on Windows.")
            unsupported_label.setStyleSheet("font-size: 14px; color: #ff5555; margin-bottom: 15px;")
            frame_layout.addWidget(unsupported_label)
            return tab
        
        desc = QLabel("Save and switch between different Roblox accounts. The sniper will patch your Roblox cookies to switch accounts. This feature does not violate the Roblox TOS and will not get you banned. This feature does not support multi-instance launching.")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #a0a0a0; margin-bottom: 20px;")
        frame_layout.addWidget(desc)
        
        self.pending_restart_label = QLabel("")
        self.pending_restart_label.setStyleSheet("font-size: 12px; color: #ff9800; background-color: rgba(255, 152, 0, 0.1); border-radius: 6px; padding: 8px; margin-bottom: 15px;")
        self.pending_restart_label.hide()
        frame_layout.addWidget(self.pending_restart_label)
        
        current_frame = QGroupBox("Current Roblox Account")
        current_frame.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        current_layout = QHBoxLayout(current_frame)
        current_layout.setContentsMargins(20, 15, 20, 15)
        current_layout.setSpacing(15)
        
        self.current_headshot_label = QLabel()
        self.current_headshot_label.setFixedSize(40, 40)
        self.current_headshot_label.setStyleSheet("background-color: #3a3a3a; border-radius: 20px;")
        current_layout.addWidget(self.current_headshot_label)
        
        self.current_account_label = QLabel("Loading...")
        self.current_account_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.current_account_label.setStyleSheet("font-size: 16px; color: #e0e0e0; background-color: rgba(45, 45, 45, 80); padding: 8px; border-radius: 6px;")
        current_layout.addWidget(self.current_account_label)
        
        self.current_account_status_label = QLabel("")
        self.current_account_status_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.current_account_status_label.setStyleSheet("font-size: 12px; color: #888888; background-color: rgba(45, 45, 45, 80); padding: 8px; border-radius: 6px;")
        current_layout.addWidget(self.current_account_status_label)
        
        self.detect_current_btn = QPushButton("Refresh")
        self.detect_current_btn.setFixedSize(100, 32)
        self.detect_current_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a7bff;
                color: white;
                border-radius: 6px;
                font-weight: 500;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5a8bff;
            }
        """)
        self.detect_current_btn.clicked.connect(self.refresh_current_account_display)
        current_layout.addWidget(self.detect_current_btn)
        
        frame_layout.addWidget(current_frame)
        
        accounts_group = QGroupBox("Saved Accounts")
        accounts_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        accounts_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        accounts_layout = QVBoxLayout(accounts_group)
        
        # Create scroll area for the table
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Create container widget for the table
        table_container = QWidget()
        table_container_layout = QVBoxLayout(table_container)
        table_container_layout.setContentsMargins(0, 0, 0, 0)
        table_container_layout.setSpacing(0)
        
        self.accounts_table = QTableWidget()
        self.accounts_table.setColumnCount(4)
        self.accounts_table.setHorizontalHeaderLabels(["Account", "User ID", "", ""])
        self.accounts_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.accounts_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.accounts_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.accounts_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.accounts_table.setColumnWidth(2, 100)
        self.accounts_table.setColumnWidth(3, 60)
        self.accounts_table.verticalHeader().setVisible(False)
        self.accounts_table.setShowGrid(False)
        self.accounts_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.accounts_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.accounts_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.accounts_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.accounts_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QHeaderView {
                background-color: #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
                border-right: none;
                color: white;
            }
            QTableWidget::item:selected {
                background-color: #4a7bff;
                color: white;
            }
        """)
        self.accounts_table.itemSelectionChanged.connect(self.on_account_selected)
        
        table_container_layout.addWidget(self.accounts_table)
        scroll_area.setWidget(table_container)
        accounts_layout.addWidget(scroll_area)
        
        table_btn_layout = QHBoxLayout()
        table_btn_layout.setSpacing(10)
        table_btn_layout.setContentsMargins(0, 10, 0, 0)
        
        self.add_account_btn = QPushButton("+ Save Current Account")
        self.add_account_btn.setFixedHeight(35)
        self.add_account_btn.setFixedWidth(240)
        if CONFIG_DATA["gradient_theme"]:
            self.add_account_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 13px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.add_account_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 13px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        self.add_account_btn.clicked.connect(self.add_current_account)
        table_btn_layout.addWidget(self.add_account_btn)
        
        table_btn_layout.addStretch()
        
        self.switch_account_btn = QPushButton("Switch to Selected Account")
        self.switch_account_btn.setFixedHeight(40)
        self.switch_account_btn.setFixedWidth(300)
        self.switch_account_btn.setEnabled(False)
        if CONFIG_DATA["gradient_theme"]:
            self.switch_account_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 600;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QPushButton:disabled {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3a5baf, stop:1 #7a3c9f);
                }
            """)
        else:
            self.switch_account_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 600;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
                QPushButton:disabled {
                    background-color: #3a5baf;
                }
            """)
        self.switch_account_btn.clicked.connect(self.switch_to_selected_account)
        table_btn_layout.addWidget(self.switch_account_btn)
        
        accounts_layout.addLayout(table_btn_layout)
        frame_layout.addWidget(accounts_group)
        
        layout.addWidget(frame)
        
        self.load_saved_accounts_table()
        self.refresh_current_account_display()
        
        return tab

    def load_saved_accounts_table(self):
        self.accounts_table.setRowCount(0)
        self.accounts_table.verticalHeader().setDefaultSectionSize(50)
        if ACCOUNTS_DIR.exists():
            account_list = []
            for account_dir in ACCOUNTS_DIR.iterdir():
                if account_dir.is_dir():
                    cookies_file = account_dir / "RobloxCookies.dat"
                    if cookies_file.exists():
                        data_file = account_dir / "data.json"
                        if data_file.exists():
                            with open(data_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                account_list.append({
                                    "user_id": account_dir.name,
                                    "username": data.get("username", "Unknown"),
                                    "display_name": data.get("display_name", ""),
                                    "headshot_path": str(account_dir / "headshot.png") if (account_dir / "headshot.png").exists() else "",
                                    "data": data
                                })
            
            if account_list:
                self.accounts_table.setRowCount(len(account_list))
                current_id = self.get_current_roblox_account_from_storage()
                for row, account in enumerate(account_list):
                    container_widget = QWidget()
                    container_layout = QHBoxLayout(container_widget)
                    container_layout.setContentsMargins(5, 5, 5, 5)
                    container_layout.setSpacing(10)
                    
                    if account.get("headshot_path") and os.path.exists(account["headshot_path"]):
                        pixmap = QPixmap(account["headshot_path"])
                        if not pixmap.isNull():
                            rounded = QPixmap(24, 24)
                            rounded.fill(Qt.GlobalColor.transparent)
                            painter = QPainter(rounded)
                            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                            path = QPainterPath()
                            path.addRoundedRect(0, 0, 24, 24, 12, 12)
                            painter.setClipPath(path)
                            scaled = pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                            painter.drawPixmap(0, 0, scaled)
                            painter.setPen(QPen(QColor(255, 255, 255, 128), 1))
                            painter.setBrush(Qt.BrushStyle.NoBrush)
                            painter.drawRoundedRect(0, 0, 24, 24, 12, 12)
                            painter.end()
                            
                            headshot_label = QLabel()
                            headshot_label.setPixmap(rounded)
                            headshot_label.setFixedSize(24, 24)
                            headshot_label.setStyleSheet("background-color: transparent;")
                            container_layout.addWidget(headshot_label)
                        else:
                            placeholder = QLabel()
                            placeholder.setFixedSize(24, 24)
                            placeholder.setStyleSheet("background-color: #3a3a3a; border-radius: 12px;")
                            container_layout.addWidget(placeholder)
                    else:
                        placeholder = QLabel()
                        placeholder.setFixedSize(24, 24)
                        placeholder.setStyleSheet("background-color: #3a3a3a; border-radius: 12px;")
                        container_layout.addWidget(placeholder)
                    
                    display_text = f"{account['display_name']} (@{account['username']})" if account['display_name'] else account['username']
                    name_label = QLabel(display_text)
                    name_label.setStyleSheet("font-size: 14px; color: #ffffff; background-color: transparent;")
                    container_layout.addWidget(name_label)
                    container_layout.addStretch()
                    
                    if account["user_id"] == current_id:
                        name_label.setStyleSheet("color: #ffffff; font-size: 14px; background-color: transparent;")
                    
                    container_widget.setAutoFillBackground(False)
                    self.accounts_table.setCellWidget(row, 0, container_widget)
                    
                    id_item = QTableWidgetItem(account["user_id"])
                    if account["user_id"] == current_id:
                        id_item.setForeground(QColor(255, 255, 255))
                    self.accounts_table.setItem(row, 1, id_item)
                    
                    profile_btn = QPushButton("Profile")
                    profile_btn.setFixedSize(90, 32)
                    profile_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #4a7bff;
                            color: white;
                            border-radius: 6px;
                            font-weight: 500;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #5a8bff;
                        }
                    """)
                    profile_btn.clicked.connect(lambda checked, uid=account["user_id"]: webbrowser.open(f"https://www.roblox.com/users/{uid}/profile"))
                    self.accounts_table.setCellWidget(row, 2, profile_btn)
                    
                    remove_btn = QPushButton()
                    remove_btn.setFixedSize(32, 32)
                    remove_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #ff5555;
                            border-radius: 6px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #ff8888;
                        }
                    """)
                    remove_svg = QSvgWidget(remove_btn)
                    remove_svg.load(QByteArray(b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                    </svg>"""))
                    remove_svg.setFixedSize(14, 14)
                    remove_svg.move(9, 9)
                    remove_btn.clicked.connect(lambda checked, r=row: self.remove_account_by_row(r))
                    self.accounts_table.setCellWidget(row, 3, remove_btn)
        
        self.accounts_table.clearSelection()
        self.on_account_selected()

    def remove_account_by_row(self, row):
        if row < 0:
            return
        
        id_item = self.accounts_table.item(row, 1)
        if not id_item:
            return
        
        user_id = id_item.text()
        current_id = self.get_current_roblox_account_from_storage()
        
        if user_id == current_id:
            QMessageBox.warning(self, "Cannot Remove", "Cannot remove the currently active Roblox account.")
            return
        
        confirm = QMessageBox.question(self, "Remove Account", f"Are you sure you want to remove account {user_id}?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            account_dir = ACCOUNTS_DIR / user_id
            if account_dir.exists():
                shutil.rmtree(account_dir)
            self.load_saved_accounts_table()
            logging.info(f"Removed account: {user_id}")

    def on_account_selected(self):
        selected = self.accounts_table.currentRow() >= 0
        if selected:
            id_item = self.accounts_table.item(self.accounts_table.currentRow(), 1)
            if id_item:
                user_id = id_item.text()
                current_id = self.get_current_roblox_account_from_storage()
                saved_accounts = self.get_saved_accounts_list()
                
                if user_id == current_id and user_id in saved_accounts:
                    self.switch_account_btn.setEnabled(False)
                    self.switch_account_btn.setText("Already Active")
                    self.add_account_btn.setText("+ Update Current Account")
                    self.add_account_btn.setFixedWidth(250)
                else:
                    self.switch_account_btn.setEnabled(True)
                    self.switch_account_btn.setText("Switch to Selected Account")
                    self.add_account_btn.setText("+ Save Current Account")
                    self.add_account_btn.setFixedWidth(240)
        else:
            self.switch_account_btn.setEnabled(False)
            self.switch_account_btn.setText("Switch to Selected Account")
            self.add_account_btn.setText("+ Save Current Account")
            self.add_account_btn.setFixedWidth(240)

    def switch_account_by_row(self, row):
        global restart_roblox_on_next_snipe
        if row < 0:
            return
        
        id_item = self.accounts_table.item(row, 1)
        if not id_item:
            return
        
        user_id = id_item.text()
        
        cookies_path = ACCOUNTS_DIR / user_id / "RobloxCookies.dat"
        if not cookies_path.exists():
            QMessageBox.warning(self, "Error", "Account cookies file not found.")
            return
        
        try:
            if ROBLOX_COOKIES_PATH.exists():
                shutil.copy2(str(cookies_path), str(ROBLOX_COOKIES_PATH))
            
            is_roblox_running = False
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                is_roblox_running = loop.run_until_complete(self.is_roblox_running())
            finally:
                loop.close()
            
            switched_account_data = None
            data_file = ACCOUNTS_DIR / user_id / "data.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    switched_account_data = json.load(f)
            
            if is_roblox_running:
                restart_roblox_on_next_snipe = True
                self.update_pending_restart_notice(True)
                
                if switched_account_data:
                    username = switched_account_data.get("username", "Unknown")
                    display_name = switched_account_data.get("display_name", username)
                    display_text = f"{display_name} (@{username})" if display_name != username else username
                    self.current_account_label.setText(display_text)
                    
                    local_headshot = ACCOUNTS_DIR / user_id / "headshot.png"
                    if local_headshot.exists():
                        try:
                            pixmap = QPixmap(str(local_headshot))
                            if not pixmap.isNull():
                                rounded = QPixmap(40, 40)
                                rounded.fill(Qt.GlobalColor.transparent)
                                painter = QPainter(rounded)
                                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                                path = QPainterPath()
                                path.addRoundedRect(0, 0, 40, 40, 20, 20)
                                painter.setClipPath(path)
                                scaled = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                                painter.drawPixmap(0, 0, scaled)
                                painter.setPen(QPen(QColor(255, 255, 255, 128), 1))
                                painter.setBrush(Qt.BrushStyle.NoBrush)
                                painter.drawRoundedRect(0, 0, 40, 40, 20, 20)
                                painter.end()
                                self.current_headshot_label.setPixmap(rounded)
                                self.current_headshot_label.setStyleSheet("background-color: transparent;")
                        except Exception as e:
                            logging.error(f"Failed to load switched account headshot: {e}")
                            self.current_headshot_label.setStyleSheet("background-color: #3a3a3a; border-radius: 20px;")
                    
                    self.current_account_status_label.setText("⚠️ Saved in sniper (pending restart)")
                    self.current_account_status_label.setStyleSheet("font-size: 12px; color: #ff9800; background-color: rgba(45, 45, 45, 80); padding: 8px; border-radius: 6px;")
                
                self.accounts_table.clearSelection()
                logging.info(f"Successfully switched to account {user_id} (but Roblox app is also running, so applies on next restart)")
                QMessageBox.information(self, "Account Switched", 
                                    f"Successfully switched to account {user_id}!\n\n"
                                    f"Roblox is currently running. The account will be applied on the next Roblox restart "
                                    f"(triggered by the next snipe).")
            else:
                logging.info(f"Successfully switched to account {user_id}")
                QMessageBox.information(self, "Account Switched", f"Successfully switched to account {user_id}!")
                self.refresh_current_account_display()
            
            self.load_saved_accounts_table()
                
        except Exception as e:
            logging.error(f"Failed to switch account: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to switch account: {str(e)}")

    def switch_to_selected_account(self):
        selected_row = self.accounts_table.currentRow()
        if selected_row >= 0:
            self.switch_account_by_row(selected_row)

    def add_current_account(self):
        user_id = self.get_current_roblox_account_from_storage()
        if not user_id:
            QMessageBox.warning(self, "No Account Detected", "Could not detect current Roblox account. Please make sure Roblox is running and you are logged in.")
            return
        
        updating = False
        account_dir = ACCOUNTS_DIR / user_id
        cookies_file = account_dir / "RobloxCookies.dat"
        if cookies_file.exists():
            updating = True
        
        try:
            user_data = {"username": "Unknown", "display_name": "Unknown", "headshot_url": ""}
            
            if ROBLOX_APPSTORAGE_PATH.exists():
                with open(ROBLOX_APPSTORAGE_PATH, 'r', encoding='utf-8') as f:
                    app_data = json.load(f)
                    user_data["username"] = app_data.get("Username", "Unknown")
                    user_data["display_name"] = app_data.get("DisplayName", user_data["username"])
            
            if ROBLOX_COOKIES_PATH.exists():
                account_dir.mkdir(parents=True, exist_ok=True)
                dest_cookies = account_dir / "RobloxCookies.dat"
                shutil.copy2(str(ROBLOX_COOKIES_PATH), str(dest_cookies))
            else:
                logging.error("RobloxCookies.dat not found")
                QMessageBox.warning(self, "Error", "RobloxCookies.dat not found. Please make sure Roblox is installed and you are logged in.")
                return
            
            try:
                response = requests.get(f"https://api-priv.vexsys.site/api/endpoints/roblox/user?id={user_id}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and user_id in data and data[user_id].get("success"):
                        user_info = data[user_id].get("user", {})
                        thumbnail_data = data[user_id].get("thumbnails", {})
                    elif data.get("success"):
                        user_info = data.get("user", {})
                        thumbnail_data = data.get("thumbnails", {})
                    else:
                        user_info = {}
                        thumbnail_data = {}
                    
                    if user_info:
                        if user_data["username"] == "Unknown":
                            user_data["username"] = user_info.get("name", "Unknown")
                        if user_data["display_name"] == "Unknown":
                            user_data["display_name"] = user_info.get("displayName", user_data["username"])
                        user_data["headshot_url"] = thumbnail_data.get("headshotUrl", "")
                        if not user_data["headshot_url"]:
                            user_data["headshot_url"] = thumbnail_data.get("imageUrl", "")
            except Exception as e:
                logging.error(f"API fetch failed: {e}")
            
            if user_data["headshot_url"]:
                try:
                    img_response = requests.get(user_data["headshot_url"], timeout=10)
                    if img_response.status_code == 200:
                        with open(account_dir / "headshot.png", "wb") as f:
                            f.write(img_response.content)
                        logging.info(f"Headshot saved to {account_dir / 'headshot.png'}")
                except Exception as e:
                    logging.error(f"Failed to download headshot: {e}")
            
            account_data = {
                "user_id": user_id,
                "username": user_data["username"],
                "display_name": user_data["display_name"],
                "headshot_url": user_data["headshot_url"]
            }
            
            data_file = account_dir / "data.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, indent=4)
            
            logging.info(f"{"Saved" if not updating else "Updated"} account: {user_id}")
            self.accounts_table.clearSelection()
            QTimer.singleShot(1000, self.load_saved_accounts_table)
            QTimer.singleShot(1000, self.refresh_current_account_display)
        except Exception as e:
            logging.error(f"Error saving account: {e}")
            QMessageBox.warning(self, "Error Saving Account", f"Failed to save account: {str(e)}")

    def refresh_current_account_display(self):
        self.current_account_label.setText("Loading...")
        self.current_account_status_label.setText("")
        try:
            user_id = self.get_current_roblox_account_from_storage()
            username = "Unknown"
            display_name = "Unknown"
            
            saved_accounts = self.get_saved_accounts_list()
            is_saved = user_id in saved_accounts
            
            if is_saved and user_id:
                data_file = ACCOUNTS_DIR / user_id / "data.json"
                if data_file.exists():
                    try:
                        with open(data_file, 'r', encoding='utf-8') as f:
                            account_data = json.load(f)
                            username = account_data.get("username", "Unknown")
                            display_name = account_data.get("display_name", username)
                    except Exception as e:
                        logging.error(f"Error reading saved account data: {e}")
            
            if username == "Unknown" and ROBLOX_APPSTORAGE_PATH.exists():
                try:
                    with open(ROBLOX_APPSTORAGE_PATH, 'r', encoding='utf-8') as f:
                        app_data = json.load(f)
                        username = app_data.get("Username", "Unknown")
                        display_name = app_data.get("DisplayName", username)
                except Exception as e:
                    logging.error(f"Error reading appStorage.json: {e}")
            
            if user_id:
                account_dir = ACCOUNTS_DIR / user_id
                local_headshot = account_dir / "headshot.png"
                local_data_file = account_dir / "data.json"
                
                try:
                    response = requests.get(f"https://api-priv.vexsys.site/api/endpoints/roblox/user?id={user_id}", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, dict) and user_id in data and data[user_id].get("success"):
                            user_info = data[user_id].get("user", {})
                            thumbnail_data = data[user_id].get("thumbnails", {})
                        elif data.get("success"):
                            user_info = data.get("user", {})
                            thumbnail_data = data.get("thumbnails", {})
                        else:
                            user_info = {}
                            thumbnail_data = {}
                        
                        if user_info:
                            if username == "Unknown":
                                username = user_info.get("name", "Unknown")
                            if display_name == "Unknown":
                                display_name = user_info.get("displayName", username)
                            headshot_url = thumbnail_data.get("headshotUrl", "")
                            if not headshot_url:
                                headshot_url = thumbnail_data.get("imageUrl", "")
                            
                            account_dir.mkdir(parents=True, exist_ok=True)
                            account_data = {
                                "user_id": user_id,
                                "username": username,
                                "display_name": display_name,
                                "headshot_url": headshot_url
                            }
                            with open(local_data_file, 'w', encoding='utf-8') as f:
                                json.dump(account_data, f, indent=4)
                            
                            if headshot_url and not local_headshot.exists():
                                try:
                                    img_response = requests.get(headshot_url, timeout=10)
                                    if img_response.status_code == 200:
                                        with open(local_headshot, "wb") as f:
                                            f.write(img_response.content)
                                        logging.info(f"Headshot saved to {local_headshot}")
                                except Exception as e:
                                    logging.error(f"Failed to download headshot: {e}")
                except Exception as e:
                    logging.error(f"API fetch failed: {e}")

                if local_headshot.exists():
                    try:
                        pixmap = QPixmap(str(local_headshot))
                        if not pixmap.isNull():
                            rounded = QPixmap(40, 40)
                            rounded.fill(Qt.GlobalColor.transparent)
                            painter = QPainter(rounded)
                            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                            path = QPainterPath()
                            path.addRoundedRect(0, 0, 40, 40, 20, 20)
                            painter.setClipPath(path)
                            scaled = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                            painter.drawPixmap(0, 0, scaled)
                            painter.setPen(QPen(QColor(255, 255, 255, 128), 1))
                            painter.setBrush(Qt.BrushStyle.NoBrush)
                            painter.drawRoundedRect(0, 0, 40, 40, 20, 20)
                            painter.end()
                            self.current_headshot_label.setPixmap(rounded)
                            self.current_headshot_label.setStyleSheet("background-color: transparent;")
                    except Exception as e:
                        logging.error(f"Failed to load local headshot: {e}")
                        self.current_headshot_label.setStyleSheet("background-color: #3a3a3a; border-radius: 20px;")
                else:
                    self.current_headshot_label.setStyleSheet("background-color: #3a3a3a; border-radius: 20px;")
                
                display_text = f"{display_name} (@{username})" if display_name != username else username
                
                status_text = "✓ Saved in sniper" if is_saved else "⚠️ Not saved in sniper"
                status_color = "#4CAF50" if is_saved else "#ff9800"
                
                self.current_account_label.setText(display_text)
                self.current_account_status_label.setText(status_text)
                self.current_account_status_label.setStyleSheet(f"font-size: 12px; color: {status_color}; background-color: rgba(45, 45, 45, 80); padding: 8px; border-radius: 6px;")
                self.load_saved_accounts_table()
            else:
                self.current_headshot_label.setStyleSheet("background-color: #3a3a3a; border-radius: 20px;")
                self.current_account_label.setText("Not detected")
                self.current_account_status_label.setText("⚠️ Roblox not running or not logged in")
                self.current_account_status_label.setStyleSheet("font-size: 12px; color: #ff9800; background-color: rgba(45, 45, 45, 80); padding: 8px; border-radius: 6px;")
                self.load_saved_accounts_table()
        except Exception as e:
            logging.error(f"Error refreshing account display: {e}")
            self.current_account_label.setText("Error loading")

    def get_current_roblox_account_from_storage(self):
        try:
            if ROBLOX_APPSTORAGE_PATH.exists():
                with open(ROBLOX_APPSTORAGE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return str(data.get("UserId", ""))
        except Exception as e:
            logging.error(f"Error reading current account: {e}")
        return None

    def get_saved_accounts_list(self):
        accounts = set()
        if ACCOUNTS_DIR.exists():
            for account_dir in ACCOUNTS_DIR.iterdir():
                cookie_dir = account_dir / "RobloxCookies.dat"
                if account_dir.is_dir() and cookie_dir.exists():
                    accounts.add(account_dir.name)
        return accounts

    def update_pending_restart_notice(self, show):
        global restart_roblox_on_next_snipe
        if show:
            self.pending_restart_label.setText('⚠️ Roblox will be restarted on the next snipe to apply account changes. <a href="#" style="color: #ff5555; text-decoration: underline; margin-left: 30px;">Click to Cancel</a>')
            self.pending_restart_label.show()
            self.pending_restart_label.setTextFormat(Qt.TextFormat.RichText)
            self.pending_restart_label.linkActivated.connect(self.cancel_pending_restart)
        else:
            self.pending_restart_label.hide()
            try:
                self.pending_restart_label.linkActivated.disconnect(self.cancel_pending_restart)
            except:
                pass

    def cancel_pending_restart(self, link):
        global restart_roblox_on_next_snipe
        restart_roblox_on_next_snipe = False
        self.update_pending_restart_notice(False)
        logging.info("Pending restart cancelled by user")

    def start_key_assignment(self, hotkey_number):
        global processing_hotkey_assignment
        processing_hotkey_assignment = True
        self.assigning_hotkey = hotkey_number
        
        listening_text = "Press key combination..."
        
        if hotkey_number == 1:
            self.hk1_display.setText(listening_text)
            self.hk1_display.setStyleSheet("""
                QLabel {
                    background-color: #4a7bff;
                    border: 1px solid #5a8bff;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: white;
                    min-width: 60px;
                    text-align: center;
                }
            """)
            self.hk1_assign_btn.setText("Listening...")
            self.hk1_assign_btn.setEnabled(False)
        elif hotkey_number == 2:
            self.hk2_display.setText(listening_text)
            self.hk2_display.setStyleSheet("""
                QLabel {
                    background-color: #4a7bff;
                    border: 1px solid #5a8bff;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: white;
                    min-width: 60px;
                    text-align: center;
                }
            """)
            self.hk2_assign_btn.setText("Listening...")
            self.hk2_assign_btn.setEnabled(False)
        elif hotkey_number == 3:
            self.hk3_display.setText(listening_text)
            self.hk3_display.setStyleSheet("""
                QLabel {
                    background-color: #4a7bff;
                    border: 1px solid #5a8bff;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: white;
                    min-width: 60px;
                    text-align: center;
                }
            """)
            self.hk3_assign_btn.setText("Listening...")
            self.hk3_assign_btn.setEnabled(False)
        elif hotkey_number == 4:
            self.hk4_display.setText(listening_text)
            self.hk4_display.setStyleSheet("""
                QLabel {
                    background-color: #4a7bff;
                    border: 1px solid #5a8bff;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: white;
                    min-width: 60px;
                    text-align: center;
                }
            """)
            self.hk4_assign_btn.setText("Listening...")
            self.hk4_assign_btn.setEnabled(False)
        elif hotkey_number == 5:
            self.hk5_display.setText(listening_text)
            self.hk5_display.setStyleSheet("""
                QLabel {
                    background-color: #4a7bff;
                    border: 1px solid #5a8bff;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: white;
                    min-width: 60px;
                    text-align: center;
                }
            """)
            self.hk5_assign_btn.setText("Listening...")
            self.hk5_assign_btn.setEnabled(False)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if (self.assigning_hotkey and 
            event.type() == QEvent.Type.KeyPress and 
            not event.isAutoRepeat()):
            
            key = event.key()
            modifiers = event.modifiers()
            key_name = self.qt_key_to_keyboard_format(key, modifiers)
            is_modifier_only = key in (Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Shift, Qt.Key.Key_Meta)
            
            if is_modifier_only:
                if self.assigning_hotkey == 1:
                    self.hk1_display.setText("Press combination... (modifier held)")
                elif self.assigning_hotkey == 2:
                    self.hk2_display.setText("Press combination... (modifier held)")
                elif self.assigning_hotkey == 3:
                    self.hk3_display.setText("Press combination... (modifier held)")
                elif self.assigning_hotkey == 4:
                    self.hk4_display.setText("Press combination... (modifier held)")
                elif self.assigning_hotkey == 5:
                    self.hk5_display.setText("Press combination... (modifier held)")
                
                return True
            
            modifier_parts = []
            if modifiers & Qt.KeyboardModifier.ControlModifier:
                modifier_parts.append("ctrl")
            if modifiers & Qt.KeyboardModifier.AltModifier:
                modifier_parts.append("alt")
            if modifiers & Qt.KeyboardModifier.ShiftModifier:
                modifier_parts.append("shift")
            if modifiers & Qt.KeyboardModifier.MetaModifier:
                modifier_parts.append("win")
            
            has_ctrl = 'ctrl' in MainWindow._pressed_keys
            has_alt = 'alt' in MainWindow._pressed_keys
            has_shift = 'shift' in MainWindow._pressed_keys
            has_win = 'win' in MainWindow._pressed_keys
            
            if 'ctrl' not in modifier_parts and has_ctrl:
                modifier_parts.append("ctrl")
            if 'alt' not in modifier_parts and has_alt:
                modifier_parts.append("alt")
            if 'shift' not in modifier_parts and has_shift:
                modifier_parts.append("shift")
            if 'win' not in modifier_parts and has_win:
                modifier_parts.append("win")
            
            if modifier_parts:
                modifier_parts.sort()  # sort for consistency (ctrl+shift+f, not shift+ctrl+f)
                final_key = "+".join(modifier_parts + [key_name])
            else:
                final_key = key_name
            
            if final_key:
                QTimer.singleShot(0, lambda: self.finish_key_assignment(final_key))
                return True
        
        return super().eventFilter(obj, event)

    def qt_key_to_keyboard_format(self, key, modifiers):
        key_map = {
            # function keys
            Qt.Key.Key_F1: "f1", Qt.Key.Key_F2: "f2", Qt.Key.Key_F3: "f3",
            Qt.Key.Key_F4: "f4", Qt.Key.Key_F5: "f5", Qt.Key.Key_F6: "f6",
            Qt.Key.Key_F7: "f7", Qt.Key.Key_F8: "f8", Qt.Key.Key_F9: "f9",
            Qt.Key.Key_F10: "f10", Qt.Key.Key_F11: "f11", Qt.Key.Key_F12: "f12",

            # whitespace/navigation
            Qt.Key.Key_Space: "space",
            Qt.Key.Key_Tab: "tab",
            Qt.Key.Key_Backspace: "backspace",
            Qt.Key.Key_Return: "enter",
            Qt.Key.Key_Enter: "enter",
            Qt.Key.Key_Escape: "esc",
            Qt.Key.Key_Delete: "delete",
            Qt.Key.Key_Insert: "insert",
            Qt.Key.Key_Home: "home",
            Qt.Key.Key_End: "end",
            Qt.Key.Key_PageUp: "page up",
            Qt.Key.Key_PageDown: "page down",
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right",

            # punctuation/unshifted
            Qt.Key.Key_Minus: "-",
            Qt.Key.Key_Equal: "=",
            Qt.Key.Key_BracketLeft: "[",
            Qt.Key.Key_BracketRight: "]",
            Qt.Key.Key_Backslash: "\\",
            Qt.Key.Key_Semicolon: ";",
            Qt.Key.Key_Apostrophe: "'",
            Qt.Key.Key_Comma: ",",
            Qt.Key.Key_Period: ".",
            Qt.Key.Key_Slash: "/",
            Qt.Key.Key_QuoteLeft: "`",

            # numpad keys
            Qt.Key.Key_0: "0", Qt.Key.Key_1: "1", Qt.Key.Key_2: "2",
            Qt.Key.Key_3: "3", Qt.Key.Key_4: "4", Qt.Key.Key_5: "5",
            Qt.Key.Key_6: "6", Qt.Key.Key_7: "7", Qt.Key.Key_8: "8",
            Qt.Key.Key_9: "9",
        }

        if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
            base = chr(key).lower()
        elif Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            base = chr(key)
        elif key in key_map:
            base = key_map[key]
        else:
            try:
                ch = chr(key)
                if 32 <= ord(ch) <= 126:
                    base = ch.lower()
                else:
                    return None
            except Exception:
                return None

        normalization = {
            "enter": "enter",
            "esc": "esc",
            "space": "space",
            "tab": "tab",
            "backspace": "backspace",
            "`": "`",
            "'": "'",
            "\\": "\\",
        }
        base = normalization.get(base, base)
        
        return str(base)
        
    def set_processing_hotkey_assignment(self, value):
        global processing_hotkey_assignment
        processing_hotkey_assignment = value

    def finish_key_assignment(self, key):
        global processing_hotkey_assignment
        
        if not self.assigning_hotkey:
            return

        hotkey_number = self.assigning_hotkey
        
        if key:
            if key == 'ctrl':
                key = 'ctrl'
            elif key == 'alt':
                key = 'alt'
            elif key == 'shift':
                key = 'shift'
            elif key == 'win' or key == 'meta':
                key = 'win'
            
            if hotkey_number == 1:
                CONFIG_DATA["open_roblox"] = key
                self.hk1_display.setText(str(key))
            elif hotkey_number == 2:
                CONFIG_DATA["stop_sniper"] = key
                self.hk2_display.setText(str(key))
            elif hotkey_number == 3:
                CONFIG_DATA["toggle_sniper"] = key
                self.hk3_display.setText(str(key))
            elif hotkey_number == 4:
                CONFIG_DATA["loading_asset_skipper"] = key
                self.hk4_display.setText(str(key))
            elif hotkey_number == 5:
                CONFIG_DATA["main_menu_skipper"] = key
                self.hk5_display.setText(str(key))
        else:
            if hotkey_number == 1:
                self.hk1_display.setText(str(CONFIG_DATA["open_roblox"]))
            elif hotkey_number == 2:
                self.hk2_display.setText(str(CONFIG_DATA["stop_sniper"]))
            elif hotkey_number == 3:
                self.hk3_display.setText(str(CONFIG_DATA["toggle_sniper"]))
            elif hotkey_number == 4:
                self.hk4_display.setText(str(CONFIG_DATA["loading_asset_skipper"]))
            elif hotkey_number == 5:
                self.hk5_display.setText(str(CONFIG_DATA["main_menu_skipper"]))

        self.hk1_assign_btn.setText("Assign")
        self.hk1_assign_btn.setEnabled(True)
        self.hk2_assign_btn.setText("Assign")
        self.hk2_assign_btn.setEnabled(True)
        self.hk3_assign_btn.setText("Assign")
        self.hk3_assign_btn.setEnabled(True)
        self.hk4_assign_btn.setText("Assign")
        self.hk4_assign_btn.setEnabled(True)
        self.hk5_assign_btn.setText("Assign")
        self.hk5_assign_btn.setEnabled(True)

        normal_style = """
            QLabel {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #e0e0e0;
                min-width: 60px;
                text-align: center;
            }
        """
        self.hk1_display.setStyleSheet(normal_style)
        self.hk2_display.setStyleSheet(normal_style)
        self.hk3_display.setStyleSheet(normal_style)
        self.hk4_display.setStyleSheet(normal_style)
        self.hk5_display.setStyleSheet(normal_style)
        
        self.assigning_hotkey = None
        self.removeEventFilter(self)
        
        if key:
            self.save_settings()
            logging.info(f"Hotkey {hotkey_number} assigned to: {key}")
        
        QTimer.singleShot(500, lambda: self.set_processing_hotkey_assignment(False))
    
    def create_keywords_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(20)

        header_frame = GradientFrame()
        header_frame.setStyleSheet("border-radius: 12px;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)

        header_title = QLabel(f"Keyword/Category{'/RegEx' if CONFIG_DATA['advanced_mode'] else ''} Management")
        header_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        export_btn = QPushButton("Export")
        export_btn.setFixedSize(100, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            export_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            export_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        export_btn.clicked.connect(self.export_keywords)
        header_layout.addWidget(export_btn)
        
        import_btn = QPushButton("Import")
        import_btn.setFixedSize(100, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            import_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            import_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        import_btn.clicked.connect(self.import_keywords)
        header_layout.addWidget(import_btn)
        
        scroll_layout.addWidget(header_frame)

        custom_cat_frame = GradientFrame()
        custom_cat_frame.setStyleSheet("border-radius: 12px;")
        custom_cat_layout = QVBoxLayout(custom_cat_frame)
        custom_cat_layout.setContentsMargins(20, 20, 20, 20)

        custom_cat_title_layout = QHBoxLayout()
        custom_cat_title = QLabel("Custom Categories")
        custom_cat_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        custom_cat_title_layout.addWidget(custom_cat_title)

        custom_cat_title_layout.addStretch()
        self.add_custom_cat_btn = QPushButton("+ Add Custom Category")
        self.add_custom_cat_btn.setFixedSize(266, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            self.add_custom_cat_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.add_custom_cat_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        self.add_custom_cat_btn.clicked.connect(self.show_add_custom_category_dialog)
        custom_cat_title_layout.addWidget(self.add_custom_cat_btn)
        custom_cat_layout.addLayout(custom_cat_title_layout)

        self.custom_cat_list = QListWidget()
        self.custom_cat_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                height: 120;
            }
            QListWidget::item {
                padding: 0px;
                border-bottom: 1px solid #3a3a3a;
                height: 120px;
            }
            QListWidget::item:selected {
                background-color: #4a7bff;
                color: white;
                border-radius: 8px;
            }
        """)
        self.custom_cat_list.setFixedHeight(120)
        custom_cat_layout.addWidget(self.custom_cat_list)

        scroll_layout.addWidget(custom_cat_frame)

        kw_frame = GradientFrame()
        kw_frame.setStyleSheet("border-radius: 12px;")
        kw_frame_layout = QVBoxLayout(kw_frame)
        kw_frame_layout.setContentsMargins(20, 20, 20, 20)

        title_layout = QHBoxLayout()
        title = QLabel("Keyword Management")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        title_layout.addWidget(title)

        title_layout.addStretch()
        self.plus_btn = QPushButton("+ Add Keyword")
        self.plus_btn.setFixedSize(180, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            self.plus_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.plus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        self.plus_btn.clicked.connect(self.show_add_keyword_dialog)
        title_layout.addWidget(self.plus_btn)
        kw_frame_layout.addLayout(title_layout)

        self.keyword_table = QTableWidget()
        self.keyword_table.setColumnCount(4)
        self.keyword_table.setHorizontalHeaderLabels(["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"])
        self.keyword_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.keyword_table.horizontalHeader().setStretchLastSection(False)
        self.keyword_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.keyword_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.keyword_table.verticalHeader().setVisible(False)
        self.keyword_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.keyword_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                height: 250;
            }
            QHeaderView {
                background-color: #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTableWidget::viewport {
                border-radius: 8px;
                gridline-color: transparent;
            }
        """)
        self.keyword_table.setFixedHeight(250)
        kw_frame_layout.addWidget(self.keyword_table)

        scroll_layout.addWidget(kw_frame)

        if CONFIG_DATA["advanced_mode"] == True:
            regex_frame = GradientFrame()
            regex_frame.setStyleSheet("border-radius: 12px;")
            regex_frame_layout = QVBoxLayout(regex_frame)
            regex_frame_layout.setContentsMargins(20, 20, 20, 20)

            regex_title_layout = QHBoxLayout()
            regex_title = QLabel("Custom RegEx Detections")
            regex_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
            regex_title_layout.addWidget(regex_title)

            regex_title_layout.addStretch()
            self.regex_plus_btn = QPushButton("+ Add RegEx")
            self.regex_plus_btn.setFixedSize(156, 30)
            if CONFIG_DATA["gradient_theme"] == True:
                self.regex_plus_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                        color: white;
                        border-radius: 6px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #5a8bff, stop:1 #9a5cbf);
                    }
                """)
            else:
                self.regex_plus_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a7bff;
                        color: white;
                        border-radius: 6px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #5a8bff;
                    }
                """)
            self.regex_plus_btn.clicked.connect(self.show_add_regex_dialog)
            regex_title_layout.addWidget(self.regex_plus_btn)
            regex_frame_layout.addLayout(regex_title_layout)

            self.regex_table = QTableWidget()
            self.regex_table.setColumnCount(4)
            self.regex_table.setHorizontalHeaderLabels(["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"])
            self.regex_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            self.regex_table.horizontalHeader().setStretchLastSection(False)
            self.regex_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
            self.regex_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.regex_table.verticalHeader().setVisible(False)
            self.regex_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

            self.regex_table.setStyleSheet("""
                QTableWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #444;
                    border-radius: 8px;
                    height: 120;
                }
                QHeaderView {
                    background-color: #3c3c3c;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QHeaderView::section {
                    background-color: #3c3c3c;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QTableWidget::viewport {
                    border-radius: 8px;
                    gridline-color: transparent;
                }
            """)
            self.regex_table.setFixedHeight(120)
            self.regex_table.setRowCount(1)
            regex_frame_layout.addWidget(self.regex_table)

            scroll_layout.addWidget(regex_frame)

        bl_frame = GradientFrame()
        bl_frame.setStyleSheet("border-radius: 12px;")
        bl_frame_layout = QVBoxLayout(bl_frame)
        bl_frame_layout.setContentsMargins(20, 20, 20, 20)

        bl_title_layout = QHBoxLayout()
        bl_title = QLabel("Keyword Blacklist")
        bl_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        bl_title_layout.addWidget(bl_title)

        bl_title_layout.addStretch()
        self.bl_plus_btn = QPushButton("+ Add Blacklist")
        self.bl_plus_btn.setFixedSize(180, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            self.bl_plus_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.bl_plus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff4a4a;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff5a5a;
                }
            """)
        self.bl_plus_btn.clicked.connect(self.show_add_blacklist_dialog)
        bl_title_layout.addWidget(self.bl_plus_btn)
        bl_frame_layout.addLayout(bl_title_layout)

        self.blacklist_table = QTableWidget()
        self.blacklist_table.setColumnCount(5)
        self.blacklist_table.setHorizontalHeaderLabels(["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"])
        self.blacklist_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.blacklist_table.horizontalHeader().setStretchLastSection(False)
        self.blacklist_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.blacklist_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.blacklist_table.verticalHeader().setVisible(False)
        self.blacklist_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.blacklist_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                height: 250;
            }
            QHeaderView {
                background-color: #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTableWidget::viewport {
                border-radius: 8px;
                gridline-color: transparent;
            }
        """)
        self.blacklist_table.setFixedHeight(250)
        bl_frame_layout.addWidget(self.blacklist_table)
        scroll_layout.addWidget(bl_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        return tab

    def show_add_keyword_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Keyword")
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        category_combo = QComboBox()
        
        data = self.get_current_keyword_data()
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        
        category_combo.addItems(base_categories + custom_categories)
        
        keyword_input = QLineEdit()
        
        form.addRow("Category:", category_combo)
        form.addRow("Keyword:", keyword_input)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            category_name = category_combo.currentText()
            keyword = keyword_input.text().strip()
            if keyword:
                if self.is_url_keyword(keyword):
                    QMessageBox.warning(
                        self,
                        "Invalid Keyword",
                        f"You cannot add keywords that are contained within the following URL patterns:\n"
                        f"• roblox.com\n"
                        f"• join-rbx.vexsys.site\n"
                        f"• ro.pro\n"
                        f"• ropro.io\n"
                        f"Because it will cause you to join random servers that you do not intend to join.\n\n"
                        f"Your keyword: '{keyword}'"
                    )
                    return
                
                all_categories = base_categories + custom_categories
                try:
                    category_index = all_categories.index(category_name)
                    self.add_keyword_to_table(category_index, keyword)
                    self.save_keywords_data()
                except ValueError:
                    self.add_custom_category(category_name)
                    all_categories = base_categories + data.get("custom_categories", []) + [category_name]
                    category_index = all_categories.index(category_name)
                    self.add_keyword_to_table(category_index, keyword)
                    self.save_keywords_data()

    def show_add_blacklist_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Blacklist Keyword")
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        category_combo = QComboBox()
        
        data = self.get_current_keyword_data()
        base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        
        category_combo.addItems(base_categories + custom_categories)
        
        keyword_input = QLineEdit()
        
        form.addRow("Category:", category_combo)
        form.addRow("Keyword:", keyword_input)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            category_name = category_combo.currentText()
            keyword = keyword_input.text().strip()
            if keyword:
                if self.is_url_keyword(keyword):
                    QMessageBox.warning(
                        self,
                        "Invalid Blacklist Keyword",
                        f"You cannot add blacklist keywords that are contained within the following URL patterns:\n"
                        f"• roblox.com\n"
                        f"• join-rbx.vexsys.site\n"
                        f"• ro.pro\n"
                        f"• ropro.io\n"
                        f"Because it will cause you to never be able to snipe those URLs again, regardless of keywords.\n\n"
                        f"Your keyword: '{keyword}'"
                    )
                    return
                
                all_categories = base_categories + custom_categories
                try:
                    category_index = all_categories.index(category_name)
                    self.add_blacklist_to_table(category_index, keyword)
                    self.save_keywords_data()
                except ValueError:
                    self.add_custom_category(category_name)
                    all_categories = base_categories + data.get("custom_categories", []) + [category_name]
                    category_index = all_categories.index(category_name)
                    self.add_blacklist_to_table(category_index, keyword)
                    self.save_keywords_data()

    def add_keyword_to_table(self, col, kw):
        if not kw:
            return
            
        data = self.get_current_keyword_data()
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        if col < len(all_categories):
            category = all_categories[col]
            
            if kw not in data["keywords"].get(category, []):
                if category not in data["keywords"]:
                    data["keywords"][category] = []
                data["keywords"][category].append(kw)
                
                self.rebuild_tables_from_data(data)

    def add_blacklist_to_table(self, col, kw):
        if not kw:
            return
            
        data = self.get_current_keyword_data()
        base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        if col < len(all_categories):
            category = all_categories[col]
            
            if kw not in data["blacklist"].get(category, []):
                if category not in data["blacklist"]:
                    data["blacklist"][category] = []
                data["blacklist"][category].append(kw)
                
                self.rebuild_tables_from_data(data)

    def show_add_custom_category_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Custom Category")
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        category_input = QLineEdit()
        category_input.setPlaceholderText("Enter category name")
        
        form.addRow("Category Name:", category_input)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            category = category_input.text().strip()
            if category:
                self.add_custom_category(category)

    def add_custom_category(self, category):
        if not category:
            return
        
        data = self.get_current_keyword_data()
        if category not in data.get("custom_categories", []):
            if "custom_categories" not in data:
                data["custom_categories"] = []
            data["custom_categories"].append(category)
            
            with open(KEYWORDS_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            
            self.rebuild_tables_from_data(data)
            self.update_custom_cat_list(data)
            self.refresh_custom_categories()
            
            setting_name = f"customcat_{category.replace(' ', '_')}"
            if setting_name not in CONFIG_DATA:
                CONFIG_DATA[setting_name] = False
            self.save_settings()

    def refresh_custom_categories(self):
        self.custom_category_durations.clear()
        
        if hasattr(self, 'custom_category_checkboxes'):
            for checkbox in self.custom_category_checkboxes.values():
                if checkbox and checkbox.parent():
                    parent_widget = checkbox.parent()
                    if parent_widget and parent_widget.layout():
                        parent_widget.layout().removeWidget(checkbox)
                    checkbox.deleteLater()
            self.custom_category_checkboxes.clear()
        
        custom_categories = []
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, 'r') as f:
                    keywords_data = json.load(f)
                    custom_categories = keywords_data.get("custom_categories", [])
            except:
                pass

        self.remove_custom_categories_frame()
        
        if not custom_categories:
            return

        custom_cat_frame = GradientFrame()
        custom_cat_frame.setObjectName("custom_cat_frame")
        custom_cat_frame.setStyleSheet("border-radius: 12px;")
        custom_cat_layout = QVBoxLayout(custom_cat_frame)
        custom_cat_layout.setContentsMargins(20, 20, 20, 20)

        custom_cat_title = QLabel("Custom Categories")
        custom_cat_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0; margin-bottom: 15px;")
        custom_cat_layout.addWidget(custom_cat_title)

        self.custom_category_checkboxes = {}
        
        for category in custom_categories:
            cb = QCheckBox()
            setting_name = f"customcat_{category.replace(' ', '_')}"
            cb.setChecked(CONFIG_DATA.get(setting_name, False))
            #cb.setText(category)
            cb.setStyleSheet("font-size: 16px; color: #e0e0e0;")
            cb.stateChanged.connect(self.save_settings)
            cb.stateChanged.connect(lambda state, cat=category: self.update_custom_category_setting(cat, state))
            self.custom_category_checkboxes[category] = cb
            
            duration_input = QLineEdit()
            duration_key = f"pause_duration_{category.lower().replace(' ', '_')}"
            duration_input.setText(str(CONFIG_DATA.get(duration_key, 60)))
            duration_input.setFixedWidth(70)
            duration_input.setFixedHeight(30)
            duration_input.setStyleSheet("""
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #444;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
            """)
            duration_input.setValidator(QIntValidator(1, 9999))
            duration_input.textChanged.connect(self.save_settings)
            self.custom_category_durations[category] = duration_input
            
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(3)
            row_layout.addWidget(cb)
            
            label = QLabel(category)
            label.setStyleSheet("font-size: 16px; color: #e0e0e0; margin-left: 4px;")
            row_layout.addWidget(label)
            row_layout.addStretch()
            
            duration_label = QLabel("Pause:")
            duration_label.setStyleSheet("font-size: 14px; color: #e0e0e0; margin-right: 8px;")
            row_layout.addWidget(duration_label)
            row_layout.addWidget(duration_input)
            
            seconds_label = QLabel("sec")
            seconds_label.setStyleSheet("font-size: 12px; color: #888888; margin-left: 4px;")
            row_layout.addWidget(seconds_label)
            
            custom_cat_layout.addWidget(row_widget)

        scroll_area = self.sniper_tab.findChild(QScrollArea)
        if scroll_area:
            scroll_content = scroll_area.widget()
            if scroll_content:
                base_cat_frame_index = -1
                for i in range(scroll_content.layout().count()):
                    item = scroll_content.layout().itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), GradientFrame):
                        frame = item.widget()
                        for j in range(frame.layout().count()):
                            frame_item = frame.layout().itemAt(j)
                            if (frame_item and frame_item.widget() and 
                                isinstance(frame_item.widget(), QLabel) and 
                                "Base Categories" in frame_item.widget().text()):
                                base_cat_frame_index = i
                                break
                        if base_cat_frame_index != -1:
                            break
                
                if base_cat_frame_index != -1:
                    scroll_content.layout().insertWidget(base_cat_frame_index + 1, custom_cat_frame)
                else:
                    scroll_content.layout().insertWidget(0, custom_cat_frame)

    def remove_custom_categories_frame(self):
        scroll_area = self.sniper_tab.findChild(QScrollArea)
        if scroll_area:
            scroll_content = scroll_area.widget()
            if scroll_content:
                for i in range(scroll_content.layout().count()):
                    item = scroll_content.layout().itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), GradientFrame):
                        frame = item.widget()
                        if frame.objectName() == "custom_cat_frame":
                            for j in range(frame.layout().count()):
                                frame_item = frame.layout().itemAt(j)
                                if (frame_item and frame_item.widget() and 
                                    isinstance(frame_item.widget(), QLabel) and 
                                    "Custom Categories" in frame_item.widget().text()):
                                    scroll_content.layout().removeWidget(frame)
                                    frame.deleteLater()
                                    return

    def create_custom_categories_frame(self):
        custom_cat_frame = GradientFrame()
        custom_cat_frame.setStyleSheet("border-radius: 12px;")
        custom_cat_layout = QVBoxLayout(custom_cat_frame)
        custom_cat_layout.setContentsMargins(20, 20, 20, 20)
        return custom_cat_frame

    def update_custom_category_setting(self, category, state):
        setting_name = f"customcat_{category.replace(' ', '_')}"
        CONFIG_DATA[setting_name] = (state == Qt.CheckState.Checked.value)
        self.save_settings()

    def update_custom_cat_list(self, data):
        self.custom_cat_list.clear()
        for category in data.get("custom_categories", []):
            item = QListWidgetItem()
            
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(10, 0, 10, 0)
            layout.setSpacing(5)
            
            label = QLabel(category)
            label.setWordWrap(True)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            layout.addWidget(label)
            
            remove_btn = QPushButton()
            remove_btn.setFixedSize(24, 24)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff8888;
                }
            """)
            remove_svg = QSvgWidget(remove_btn)
            remove_svg.load(QByteArray(b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
            </svg>"""))
            remove_svg.setFixedSize(12, 12)
            remove_svg.move(6, 6)
            remove_btn.clicked.connect(lambda checked, cat=category: self.remove_custom_category(cat))
            layout.addWidget(remove_btn, alignment=Qt.AlignmentFlag.AlignRight)
            
            item.setSizeHint(QSize(0, 36))
            self.custom_cat_list.addItem(item)
            self.custom_cat_list.setItemWidget(item, widget)

    def remove_custom_category(self, category):
        data = self.get_current_keyword_data()
        if category in data.get("custom_categories", []):
            data["custom_categories"].remove(category)
            
            if category in data.get("keywords", {}):
                del data["keywords"][category]
            if category in data.get("blacklist", {}):
                del data["blacklist"][category]
            if category in data.get("regex", {}):
                del data["regex"][category]
            
            with open(KEYWORDS_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            
            setting_name = f"customcat_{category.replace(' ', '_')}"
            if setting_name in CONFIG_DATA:
                del CONFIG_DATA[setting_name]
            
            if category in self.custom_category_durations:
                del self.custom_category_durations[category]
            
            self.save_settings()
            
            self.rebuild_tables_from_data(data)
            self.update_custom_cat_list(data)
            self.refresh_custom_categories()
            
            if not data.get("custom_categories", []):
                self.remove_custom_categories_frame()

    def show_add_regex_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Custom RegEx")
        dlg.setModal(True)
        dlg.resize(480, 200)
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        category_combo = QComboBox()
        data = self.get_current_keyword_data()
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        categories = base_categories + custom_categories
        
        available_categories = []
        for cat in categories:
            if cat not in data.get("regex", {}):
                available_categories.append(cat)
        
        if not available_categories:
            QMessageBox.information(self, "No Available Categories", "All categories already have RegEx patterns defined.")
            return
        
        category_combo.addItems(available_categories)
        
        pattern_input = QLineEdit()
        pattern_input.setPlaceholderText(r"e.g. d.{0,2}r.{0,2}e{1,3}.{0,2}a")
        
        ignore_case_cb = QCheckBox("Ignore Case")
        multiline_cb = QCheckBox("Multiline")
        
        form.addRow("Category:", category_combo)
        form.addRow("Pattern (PCRE):", pattern_input)
        form.addRow(ignore_case_cb, multiline_cb)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            pattern = pattern_input.text().strip()
            if not pattern:
                return
            
            try:
                re.compile(pattern)
            except re.error as e:
                QMessageBox.warning(self, "Invalid RegEx", f"The provided RegEx pattern is invalid:\n\n{str(e)}")
                return
            
            category = category_combo.currentText()
            flags = []
            if ignore_case_cb.isChecked():
                flags.append("i")
            if multiline_cb.isChecked():
                flags.append("m")
            
            self.add_regex_to_table(category, pattern, flags)

    def add_regex_to_table(self, category, pattern, flags):
        data = self.get_current_keyword_data()
        
        if "regex" not in data:
            data["regex"] = {}
        
        data["regex"][category] = {
            "pattern": pattern,
            "flags": flags
        }
        
        self.rebuild_tables_from_data(data)

    def add_regex_to_table_cell(self, category, pattern, flags):
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = self.get_current_keyword_data().get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        if category not in all_categories:
            return
        
        col = all_categories.index(category)
        
        widget = QWidget()
        widget.setProperty("pattern", pattern)
        widget.setProperty("flags", flags)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)
        
        display_pattern = pattern if len(pattern) <= 40 else pattern[:37] + "..."
        pattern_label = QLabel(display_pattern)
        pattern_label.setToolTip(pattern)
        pattern_label.setWordWrap(False)
        pattern_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(pattern_label)
        
        edit_btn = QPushButton()
        edit_btn.setFixedSize(24, 24)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a7bff;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a8bff;
            }
        """)

        svg = QSvgWidget(edit_btn)
        svg.load(QByteArray(EDIT_SVG))
        svg.setFixedSize(12, 12)
        svg.move(6, 6)
        edit_btn.clicked.connect(lambda: self.edit_regex(category))
        layout.addWidget(edit_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.regex_table.setCellWidget(0, col, widget)

    def edit_regex(self, category):
        data = self.get_current_keyword_data()
        regex_data = data.get("regex", {}).get(category, {})
        
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Edit RegEx for {category}")
        dlg.setModal(True)
        dlg.resize(480, 200)
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        pattern_input = QLineEdit()
        pattern_input.setText(regex_data.get("pattern", ""))
        pattern_input.setPlaceholderText(r"e.g. d.{0,2}r.{0,2}e{1,3}.{0,2}a")
        
        ignore_case_cb = QCheckBox("Ignore Case")
        multiline_cb = QCheckBox("Multiline")
        
        flags = regex_data.get("flags", [])
        ignore_case_cb.setChecked("i" in flags)
        multiline_cb.setChecked("m" in flags)
        
        form.addRow("Pattern (PCRE):", pattern_input)
        form.addRow(ignore_case_cb, multiline_cb)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            pattern = pattern_input.text().strip()
            if not pattern:
                return
            
            try:
                re.compile(pattern)
            except re.error as e:
                QMessageBox.warning(self, "Invalid RegEx", f"The provided RegEx pattern is invalid:\n\n{str(e)}")
                return
            
            flags = []
            if ignore_case_cb.isChecked():
                flags.append("i")
            if multiline_cb.isChecked():
                flags.append("m")
            
            self.add_regex_to_table(category, pattern, flags)

    def update_table_headers_for_custom_categories(self, data):
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        current_columns = self.keyword_table.columnCount()
        needed_columns = len(all_categories)
        
        if needed_columns > current_columns:
            for i in range(current_columns, needed_columns):
                self.keyword_table.insertColumn(i)
        elif needed_columns < current_columns:
            for i in range(current_columns - 1, needed_columns - 1, -1):
                self.keyword_table.removeColumn(i)
        
        for col, category in enumerate(all_categories):
            if col < self.keyword_table.columnCount():
                self.keyword_table.setHorizontalHeaderItem(col, QTableWidgetItem(category))
                self.keyword_table.resizeColumnToContents(col)
        
        self.keyword_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.keyword_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.keyword_table.horizontalHeader().setStretchLastSection(False)

        if CONFIG_DATA["advanced_mode"] and hasattr(self, 'regex_table'):
            current_regex_columns = self.regex_table.columnCount()
            needed_regex_columns = len(all_categories)
            
            if needed_regex_columns > current_regex_columns:
                for i in range(current_regex_columns, needed_regex_columns):
                    self.regex_table.insertColumn(i)
            elif needed_regex_columns < current_regex_columns:
                for i in range(current_regex_columns - 1, needed_regex_columns - 1, -1):
                    self.regex_table.removeColumn(i)
            
            for col, category in enumerate(all_categories):
                if col < self.regex_table.columnCount():
                    self.regex_table.setHorizontalHeaderItem(col, QTableWidgetItem(category))
                    self.regex_table.resizeColumnToContents(col)
            
            self.regex_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.regex_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            self.regex_table.horizontalHeader().setStretchLastSection(False)
        
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        bl_all_categories = bl_base_categories + custom_categories
        
        current_bl_columns = self.blacklist_table.columnCount()
        needed_bl_columns = len(bl_all_categories)
        
        if needed_bl_columns > current_bl_columns:
            for i in range(current_bl_columns, needed_bl_columns):
                self.blacklist_table.insertColumn(i)
        elif needed_bl_columns < current_bl_columns:
            for i in range(current_bl_columns - 1, needed_bl_columns - 1, -1):
                self.blacklist_table.removeColumn(i)
        
        for col, category in enumerate(bl_all_categories):
            if col < self.blacklist_table.columnCount():
                self.blacklist_table.setHorizontalHeaderItem(col, QTableWidgetItem(category))
                self.blacklist_table.resizeColumnToContents(col)
        
        self.blacklist_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.blacklist_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.blacklist_table.horizontalHeader().setStretchLastSection(False)

    def rebuild_tables_from_data(self, data):
        self.update_table_headers_for_custom_categories(data)
        
        self.keyword_table.setRowCount(0)
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        max_rows = 0
        for cat in all_categories:
            max_rows = max(max_rows, len(data["keywords"].get(cat, [])))
        
        if max_rows > 0:
            self.keyword_table.setRowCount(max_rows)
        
        while self.keyword_table.columnCount() < len(all_categories):
            self.keyword_table.insertColumn(self.keyword_table.columnCount())
        
        for col, cat in enumerate(all_categories):
            if col < self.keyword_table.columnCount():
                self.keyword_table.setHorizontalHeaderItem(col, QTableWidgetItem(cat))
            
            keywords = data["keywords"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.keyword_table.rowCount():
                    self.keyword_table.insertRow(row)
                self.add_keyword_to_table_cell(row, col, kw)
        
        self.blacklist_table.setRowCount(0)
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        bl_all_categories = bl_base_categories + custom_categories
        
        max_rows = 0
        for cat in bl_all_categories:
            max_rows = max(max_rows, len(data["blacklist"].get(cat, [])))
        
        if max_rows > 0:
            self.blacklist_table.setRowCount(max_rows)
        
        while self.blacklist_table.columnCount() < len(bl_all_categories):
            self.blacklist_table.insertColumn(self.blacklist_table.columnCount())
        
        for col, cat in enumerate(bl_all_categories):
            if col < self.blacklist_table.columnCount():
                self.blacklist_table.setHorizontalHeaderItem(col, QTableWidgetItem(cat))
            
            keywords = data["blacklist"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.blacklist_table.rowCount():
                    self.blacklist_table.insertRow(row)
                self.add_blacklist_to_table_cell(row, col, kw)
        
        if CONFIG_DATA["advanced_mode"] and hasattr(self, 'regex_table'):
            self.regex_table.setRowCount(0)
            self.regex_table.setRowCount(1)
            
            while self.regex_table.columnCount() < len(all_categories):
                self.regex_table.insertColumn(self.regex_table.columnCount())
            
            for col, cat in enumerate(all_categories):
                if col < self.regex_table.columnCount():
                    self.regex_table.setHorizontalHeaderItem(col, QTableWidgetItem(cat))
                
                regex_data = data.get("regex", {}).get(cat, {})
                if regex_data:
                    self.add_regex_to_table_cell(cat, regex_data.get("pattern", ""), regex_data.get("flags", []))
                else:
                    widget = self.regex_table.cellWidget(0, col)
                    if widget:
                        self.regex_table.removeCellWidget(0, col)
        
        if hasattr(self, 'custom_cat_list'):
            self.update_custom_cat_list(data)
        
        self.save_keywords_data()
        
        for col in range(self.keyword_table.columnCount()):
            self.keyword_table.resizeColumnToContents(col)

        if CONFIG_DATA["advanced_mode"] and hasattr(self, 'regex_table'):
            for col in range(self.regex_table.columnCount()):
                self.regex_table.resizeColumnToContents(col)

        for col in range(self.blacklist_table.columnCount()):
            self.blacklist_table.resizeColumnToContents(col)

    def remove_keyword_from_table(self, row, col):
        data = self.get_current_keyword_data()
        
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        if col < len(all_categories):
            category = all_categories[col]
            
            widget = self.keyword_table.cellWidget(row, col)
            if widget:
                label = widget.findChild(QLabel)
                if label:
                    keyword_to_remove = label.text().strip()
                    
                    if category in data["keywords"] and keyword_to_remove in data["keywords"][category]:
                        data["keywords"][category].remove(keyword_to_remove)
                        
                        with open(KEYWORDS_FILE, 'w') as f:
                            json.dump(data, f, indent=4)
                        
                        self.rebuild_tables_from_data(data)

    def remove_blacklist_from_table(self, row, col):
        data = self.get_current_keyword_data()
        
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        bl_all_categories = bl_base_categories + custom_categories
        
        if col < len(bl_all_categories):
            category = bl_all_categories[col]
            
            widget = self.blacklist_table.cellWidget(row, col)
            if widget:
                label = widget.findChild(QLabel)
                if label:
                    keyword_to_remove = label.text().strip()
                    
                    if category in data["blacklist"] and keyword_to_remove in data["blacklist"][category]:
                        data["blacklist"][category].remove(keyword_to_remove)
                        
                        with open(KEYWORDS_FILE, 'w') as f:
                            json.dump(data, f, indent=4)
                        
                        self.rebuild_tables_from_data(data)

    def rebuild_keyword_table(self):
        data = self.get_current_keyword_data()
        
        self.keyword_table.setRowCount(0)
        
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        max_rows = 0
        for cat in all_categories:
            max_rows = max(max_rows, len(data["keywords"].get(cat, [])))
        
        if max_rows > 0:
            self.keyword_table.setRowCount(max_rows)
        
        for col, cat in enumerate(all_categories):
            keywords = data["keywords"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.keyword_table.rowCount():
                    self.keyword_table.insertRow(row)
                self.add_keyword_to_table_cell(row, col, kw)
        
        self.save_keywords_data()

    def rebuild_blacklist_table(self):
        data = self.get_current_keyword_data()
        
        self.blacklist_table.setRowCount(0)
        
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        bl_all_categories = bl_base_categories + custom_categories
        
        max_rows = 0
        for cat in bl_all_categories:
            max_rows = max(max_rows, len(data["blacklist"].get(cat, [])))
        
        if max_rows > 0:
            self.blacklist_table.setRowCount(max_rows)
        
        for col, cat in enumerate(bl_all_categories):
            keywords = data["blacklist"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.blacklist_table.rowCount():
                    self.blacklist_table.insertRow(row)
                self.add_blacklist_to_table_cell(row, col, kw)
        
        self.save_keywords_data()

    def get_current_keyword_data(self):
        data = {"keywords": {}, "blacklist": {}, "regex": {}, "custom_categories": []}
        
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, 'r') as f:
                    data = json.load(f)
            except:
                pass
        
        if "keywords" not in data:
            data["keywords"] = {}
        if "blacklist" not in data:
            data["blacklist"] = {}
        if "regex" not in data:
            data["regex"] = {}
        if "custom_categories" not in data:
            data["custom_categories"] = []
        
        base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        for col in range(min(self.keyword_table.columnCount(), len(all_categories))):
            cat = all_categories[col]
            keywords = []
            for row in range(self.keyword_table.rowCount()):
                widget = self.keyword_table.cellWidget(row, col)
                if widget:
                    label = widget.findChild(QLabel)
                    if label and label.text().strip():
                        keywords.append(label.text().strip())
            if keywords or cat in base_categories:
                data["keywords"][cat] = keywords
        
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
        bl_all_categories = bl_base_categories + custom_categories
        
        for col in range(min(self.blacklist_table.columnCount(), len(bl_all_categories))):
            cat = bl_all_categories[col]
            keywords = []
            for row in range(self.blacklist_table.rowCount()):
                widget = self.blacklist_table.cellWidget(row, col)
                if widget:
                    label = widget.findChild(QLabel)
                    if label and label.text().strip():
                        keywords.append(label.text().strip())
            if keywords or cat in bl_base_categories:
                data["blacklist"][cat] = keywords
        
        if hasattr(self, 'regex_table') and CONFIG_DATA["advanced_mode"]:
            for col in range(min(self.regex_table.columnCount(), len(all_categories))):
                cat = all_categories[col]
                widget = self.regex_table.cellWidget(0, col)
                if widget:
                    pattern_label = widget.findChild(QLabel)
                    if pattern_label:
                        pattern = pattern_label.toolTip() if pattern_label.toolTip() else pattern_label.text()
                        if pattern:
                            flags = widget.property("flags")
                            if flags is None:
                                flags = []
                            data["regex"][cat] = {
                                "pattern": pattern,
                                "flags": flags
                            }
                elif cat in data["regex"]:
                    pass
        
        return data

    def add_keyword_to_table_cell(self, row, col, kw):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)
        
        display_text = kw if len(kw) <= 30 else kw[:27] + "..."
        label = QLabel(display_text)
        label.setToolTip(kw)
        label.setWordWrap(False)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(label)
        
        btn = QPushButton()
        btn.setFixedSize(24, 24)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff8888;
            }
        """)
        remove_svg = QSvgWidget(btn)
        remove_svg.load(QByteArray(b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
        </svg>"""))
        remove_svg.setFixedSize(12, 12)
        remove_svg.move(6, 6)
        btn.clicked.connect(lambda: self.remove_keyword_from_table(row, col))
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.keyword_table.setCellWidget(row, col, widget)

    def add_blacklist_to_table_cell(self, row, col, kw):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)
        
        display_text = kw if len(kw) <= 30 else kw[:27] + "..."
        label = QLabel(display_text)
        label.setToolTip(kw)
        label.setWordWrap(False)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(label)
        
        btn = QPushButton()
        btn.setFixedSize(24, 24)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff8888;
            }
        """)
        remove_svg = QSvgWidget(btn)
        remove_svg.load(QByteArray(b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
        </svg>"""))
        remove_svg.setFixedSize(12, 12)
        remove_svg.move(6, 6)
        btn.clicked.connect(lambda: self.remove_blacklist_from_table(row, col))
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.blacklist_table.setCellWidget(row, col, widget)

    def load_keywords_data(self):
        logging.info("Loading keywords data")
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logging.info(f"Keywords file loaded with {len(data.get('custom_categories', []))} custom categories")
                    
                    if "keywords" not in data:
                        data["keywords"] = {}
                    if "blacklist" not in data:
                        data["blacklist"] = {}
                    if "regex" not in data:
                        data["regex"] = {}
                    if "custom_categories" not in data:
                        data["custom_categories"] = []
                    
                    base_categories = ["Glitched", "Dreamspace", "Cyberspace", "Singularity", "Jester", "Void Coin"]
                    for cat in base_categories:
                        if cat not in data["keywords"]:
                            data["keywords"][cat] = []
                        if cat not in data["blacklist"]:
                            data["blacklist"][cat] = []
                    
                    if "Global" not in data["blacklist"]:
                        data["blacklist"]["Global"] = []
                    
                    if "regex" in data:
                        for category, regex_data in data["regex"].items():
                            logging.info(f"Loaded regex for {category}: {regex_data.get('pattern', '')}")
                    
                    if "Glitched" not in data["regex"]:
                        data["regex"]["Glitched"] = {
                            "pattern": r"\bg.{0,2}l.{0,2}(?:i.{0,2}t|t.{0,2}i).{0,2}c.{0,2}h[ed]*(?=\W|$)",
                            "flags": ["i"]
                        }
                    
                    if "Dreamspace" not in data["regex"]:
                        data["regex"]["Dreamspace"] = {
                            "pattern": r"d.{0,2}r.{0,2}e{1,3}.{0,2}a.{0,2}m.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)",
                            "flags": ["i"]
                        }

                    if "Cyberspace" not in data["regex"]:
                        data["regex"]["Cyberspace"] = {
                            "pattern": r"c.{0,2}y.{0,2}b{1,3}.{0,2}e.{0,2}r.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)",
                            "flags": ["i"]
                        }

                    if "Singularity" not in data["regex"]:
                        data["regex"]["Singularity"] = {
                            "pattern": r"s.{0,2}i.{0,2}n.{0,2}g.{0,2}u.{0,2}l.{0,2}a.{0,2}r.{0,2}i.{0,2}t.{0,2}y(?:\s*biome)?(?=\W|$)",
                            "flags": ["i"]
                        }

                    if "Jester" not in data["regex"]:
                        data["regex"]["Jester"] = {
                            "pattern": r"j.{0,2}e.{0,2}s.{0,2}t.{0,2}e.{0,2}r(?=\W|$)",
                            "flags": ["i"]
                        }

                    if "Void Coin" not in data["regex"]:
                        data["regex"]["Void Coin"] = {
                            "pattern": r"v.{0,2}o.{0,2}i.{0,2}d.{0,2}c.{0,2}o.{0,2}i.{0,2}n(?=\W|$)",
                            "flags": ["i"]
                        }

                    self.rebuild_tables_from_data(data)
                    self.refresh_custom_categories()
                    
            except Exception as e:
                logging.error(f"Error loading keywords: {e}")
                with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        custom_categories = data.get("custom_categories", [])
                    except:
                        custom_categories = []
                
                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                    default_data = {
                        "keywords": {
                            "Glitched": ["glitch", "glig", "404", "4o4"],
                            "Dreamspace": ["dream"],
                            "Cyberspace": ["cyber"],
                            "Singularity": ["singul"],
                            "Jester": ["jest", "obi"],
                            "Void Coin": ["void", "viod"]
                        },
                        "blacklist": {
                            "Global": ["bait", "fake", "aura", "chill", "stigma", "sol", "zero", "day", "dimensional"],
                            "Glitched": [],
                            "Dreamspace": [],
                            "Cyberspace": [],
                            "Singularity": [],
                            "Jester": [],
                            "Void Coin": []
                        },
                        "regex": {
                            "Glitched": {
                                "pattern": r"\bg.{0,2}l.{0,2}(?:i.{0,2}t|t.{0,2}i).{0,2}c.{0,2}h[ed]*(?=\W|$)",
                                "flags": ["i"]
                            },
                            "Dreamspace": {
                                "pattern": r"d.{0,2}r.{0,2}e{1,3}.{0,2}a.{0,2}m.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)",
                                "flags": ["i"]
                            },
                            "Cyberspace": {
                                "pattern": r"c.{0,2}y.{0,2}b{1,3}.{0,2}e.{0,2}r.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)",
                                "flags": ["i"]
                            },
                            "Singularity": {
                                "pattern": r"s.{0,2}i.{0,2}n.{0,2}g.{0,2}u.{0,2}l.{0,2}a.{0,2}r.{0,2}i.{0,2}t.{0,2}y(?:\s*biome)?(?=\W|$)",
                                "flags": ["i"]
                            },
                            "Jester": {
                                "pattern": r"j.{0,2}e.{0,2}s.{0,2}t.{0,2}e.{0,2}r(?=\W|$)",
                                "flags": ["i"]
                            },
                            "Void Coin": {
                                "pattern": r"v.{0,2}o.{0,2}i.{0,2}d.{0,2}c.{0,2}o.{0,2}i.{0,2}n(?=\W|$)",
                                "flags": ["i"]
                            }
                        },
                        "custom_categories": custom_categories
                    }
                    json.dump(default_data, f)
                self.rebuild_tables_from_data(default_data)
                self.refresh_custom_categories()
        else:
            default_data = {
                "keywords": {
                    "Glitched": ["glitch", "glig", "404", "4o4"],
                    "Dreamspace": ["dream"],
                    "Cyberspace": ["cyber"],
                    "Singularity": ["singul"],
                    "Jester": ["jest", "obi"],
                    "Void Coin": ["void", "viod"]
                },
                "blacklist": {
                    "Global": ["bait", "fake", "aura", "chill", "stigma", "sol", "zero", "day", "dimensional"],
                    "Glitched": [],
                    "Dreamspace": [],
                    "Cyberspace": [],
                    "Singularity": [],
                    "Jester": [],
                    "Void Coin": []
                },
                "regex": {
                    "Glitched": {
                        "pattern": r"\bg.{0,2}l.{0,2}(?:i.{0,2}t|t.{0,2}i).{0,2}c.{0,2}h[ed]*(?=\W|$)",
                        "flags": ["i"]
                    },
                    "Dreamspace": {
                        "pattern": r"d.{0,2}r.{0,2}e{1,3}.{0,2}a.{0,2}m.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)",
                        "flags": ["i"]
                    },
                    "Cyberspace": {
                        "pattern": r"c.{0,2}y.{0,2}b{1,3}.{0,2}e.{0,2}r.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)",
                        "flags": ["i"]
                    },
                    "Singularity": {
                        "pattern": r"s.{0,2}i.{0,2}n.{0,2}g.{0,2}u.{0,2}l.{0,2}a.{0,2}r.{0,2}i.{0,2}t.{0,2}y(?:\s*biome)?(?=\W|$)",
                        "flags": ["i"]
                    },
                    "Jester": {
                        "pattern": r"j.{0,2}e.{0,2}s.{0,2}t.{0,2}e.{0,2}r(?=\W|$)",
                        "flags": ["i"]
                    },
                    "Void Coin": {
                        "pattern": r"v.{0,2}o.{0,2}i.{0,2}d.{0,2}c.{0,2}o.{0,2}i.{0,2}n(?=\W|$)",
                        "flags": ["i"]
                    }
                },
                "custom_categories": []
            }
            with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(default_data, f)
                logging.info("Created default keywords file")
            self.rebuild_tables_from_data(default_data)

    def save_keywords_data(self):
        logging.info("Saving keywords data")
        data = self.get_current_keyword_data()
        
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            logging.info(f"Keywords data saved: {data}")
            self.keyword_matcher.reload()

    def export_keywords(self):
        data = self.get_current_keyword_data()
        dialog = KeywordExportDialog(self, data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selection = dialog.get_selected_data()
            
            export_data = {
                "keywords": {},
                "blacklist": {},
                "regex": {},
                "custom_categories": selection.get("custom_categories", [])
            }
            
            for category, keywords in selection.get("keywords", {}).items():
                if keywords:
                    export_data["keywords"][category] = keywords
            
            for category, blacklist in selection.get("blacklist", {}).items():
                if blacklist:
                    export_data["blacklist"][category] = blacklist
            
            for category, regex_data in selection.get("regex", {}).items():
                if regex_data:
                    export_data["regex"][category] = regex_data
            
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Keywords", "", "JSON Files (*.json)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=4)
                QMessageBox.information(self, "Success", "Keywords exported successfully!")
                logging.info(f"Keywords exported to {file_path}")

    def import_keywords(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Keywords", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    import_data = json.load(f)
                
                current_data = self.get_current_keyword_data()
                
                for category in import_data.get("custom_categories", []):
                    if category not in current_data.get("custom_categories", []):
                        current_data.get("custom_categories", []).append(category)
                
                for category, keywords in import_data.get("keywords", {}).items():
                    if category not in current_data.get("keywords", {}):
                        current_data["keywords"][category] = []
                    
                    existing_keywords = set(kw.lower() for kw in current_data["keywords"][category])
                    for kw in keywords:
                        if kw.lower() not in existing_keywords:
                            current_data["keywords"][category].append(kw)
                
                for category, regex_data in import_data.get("regex", {}).items():
                    if category not in current_data.get("regex", {}):
                        current_data["regex"][category] = regex_data
                
                for category, blacklist in import_data.get("blacklist", {}).items():
                    if category not in current_data.get("blacklist", {}):
                        current_data["blacklist"][category] = []
                    
                    existing_blacklist = set(bw.lower() for bw in current_data["blacklist"][category])
                    for bw in blacklist:
                        if bw.lower() not in existing_blacklist:
                            current_data["blacklist"][category].append(bw)
                
                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                    json.dump(current_data, f, indent=4)
                
                self.load_keywords_data()
                QMessageBox.information(self, "Success", "Keywords imported successfully!")
                logging.info(f"Keywords imported from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import keywords: {str(e)}")
                logging.error(f"Failed to import keywords: {str(e)}")

    def export_servers(self):
        with open(SERVERS_FILE, "r") as f:
            servers_data = json.load(f)
        
        dialog = ServerExportDialog(self, servers_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selection = dialog.get_selected_servers()
            
            export_data = []
            for server in servers_data:
                server_id = server.get("id")
                if server_id in selection:
                    export_server = server.copy()
                    selected_channels = selection[server_id]
                    if selected_channels:
                        export_server['channels'] = [ch for ch in server.get('channels', []) if ch.get('id') in selected_channels]
                    else:
                        export_server['channels'] = []
                    export_data.append(export_server)
            
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Servers", "", "JSON Files (*.json)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=4)
                QMessageBox.information(self, "Success", "Servers exported successfully!")
                logging.info(f"Servers exported to {file_path}")

    def import_servers(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Servers", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    import_data = json.load(f)
                
                with open(SERVERS_FILE, "r", encoding="utf-8") as f:
                    current_data = json.load(f)
                
                if not isinstance(import_data, list):
                    import_data = import_data.get("servers", [])
                if not isinstance(current_data, list):
                    current_data = current_data.get("servers", [])
                
                existing_server_ids = set(s.get("id") for s in current_data)
                
                for import_server in import_data:
                    server_id = import_server.get("id")
                    
                    if server_id in existing_server_ids:
                        for current_server in current_data:
                            if current_server.get("id") == server_id:
                                current_channels = set(ch.get("id") for ch in current_server.get("channels", []))
                                for import_channel in import_server.get("channels", []):
                                    if import_channel.get("id") not in current_channels:
                                        if "channels" not in current_server:
                                            current_server["channels"] = []
                                        current_server["channels"].append(import_channel)
                                break
                    else:
                        current_data.append(import_server)
                
                with open(SERVERS_FILE, "w", encoding="utf-8") as f:
                    json.dump(current_data, f, indent=4)
                
                self.load_servers()
                QMessageBox.information(self, "Success", "Servers imported successfully!")
                logging.info(f"Servers imported from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import servers: {str(e)}")
                logging.error(f"Failed to import servers: {str(e)}")


    def create_servers_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        
        title_layout = QHBoxLayout()
        title = QLabel("Server Management")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        export_srv_btn = QPushButton("Export")
        export_srv_btn.setFixedSize(100, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            export_srv_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            export_srv_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        export_srv_btn.clicked.connect(self.export_servers)
        title_layout.addWidget(export_srv_btn)
        
        import_srv_btn = QPushButton("Import")
        import_srv_btn.setFixedSize(100, 30)
        if CONFIG_DATA["gradient_theme"] == True:
            import_srv_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            import_srv_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        import_srv_btn.clicked.connect(self.import_servers)
        title_layout.addWidget(import_srv_btn)
        frame_layout.addLayout(title_layout)
        
        self.server_tree = QTreeWidget()
        self.server_tree.setHeaderLabels(["Enabled", "Server Name", "Server ID", "Channels"])
        self.server_tree.setColumnWidth(0, 100)
        self.server_tree.setColumnWidth(1, 200)
        self.server_tree.setColumnWidth(2, 150)
        self.server_tree.setColumnWidth(3, 350)
        self.server_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.server_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.server_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.server_tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.server_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                height: 500px;
                outline: none;
            }
            QHeaderView {
                background-color: #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;       
            }
            QTreeWidget::item {
                height: 50px;
                border-bottom: 1px solid #3a3a3a;
                color: #ffffff;
            }
            QTreeWidget::item:selected {
                background-color: #4a7bff;
                color: #ffffff;
            }
            QTreeWidget::item:hover:!selected {
                background-color: #3a3a3a;
            }
        """)
        self.server_tree.setMinimumHeight(500)
        frame_layout.addWidget(self.server_tree)
        
        btn_layout = QHBoxLayout()
        self.add_btn_server = QPushButton("Add Server")
        if CONFIG_DATA["gradient_theme"] == True:
            self.add_btn_server.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.add_btn_server.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        self.add_btn_server.clicked.connect(self.show_add_server_dialog)
        btn_layout.addWidget(self.add_btn_server)
        btn_layout.addStretch()
        frame_layout.addLayout(btn_layout)
        frame_layout.addStretch()
        
        layout.addWidget(frame)
        layout.addStretch()

        self.load_servers()
        return tab

    def show_add_server_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Server")
        dlg.setFixedSize(400, 200)
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        self.server_name_input = QLineEdit()
        self.server_id_input = QLineEdit()
        
        self.server_name_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #2d2d2d; color: white;")
        self.server_id_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #2d2d2d; color: white;")
        
        form.addRow("Server Name:", self.server_name_input)
        form.addRow("Server ID:", self.server_id_input)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.add_server(
            self.server_name_input.text().strip(),
            self.server_id_input.text().strip()
        ))
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        dlg.exec()

    def handle_add_server(self, name, server_id):
        name = name.strip()
        server_id = server_id.strip()
        if name and server_id:
            self.add_server(name, server_id)

    def add_server(self, name, server_id):
        if not name or not server_id:
            return
            
        server_data = {
            "name": name,
            "id": server_id,
            "channels": [],
            "enabled": True
        }
        
        if not SERVERS_FILE.exists():
            os.makedirs(SERVERS_FILE.parent, exist_ok=True)
            servers = [server_data]
        else:
            with open(SERVERS_FILE, "r", encoding="utf-8") as f:
                servers = json.load(f)
                servers.append(server_data)
        
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4)
        
        self.load_servers()

    def remove_server(self, server_id):
        if not SERVERS_FILE.exists():
            return

        if server_id == "1186570213077041233":
            msg = QMessageBox(self)
            msg.setWindowTitle("Remove Maincord Server")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("You are about to remove the maincord server.")
            msg.setInformativeText(
                "maincord is the default server that everyone should be sniping in.\n\n"
                "Removing this server will prevent you from sniping any private servers\n"
                "posted in maincord's channels.\n\n"
                "Are you sure you want to remove this server (not recommended)?"
            )
            
            remove_btn = msg.addButton("Remove Anyway", QMessageBox.ButtonRole.AcceptRole)
            cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            msg.setDefaultButton(cancel_btn)
            
            msg.exec()
            
            if msg.clickedButton() != remove_btn:
                return
        
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            servers = json.load(f)
        
        servers = [s for s in servers if s["id"] != server_id]
        
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4)
        
        self.load_servers()

    def edit_server_item(self, item, column):
        if column == 2:
            server_id = item.text(1)
            self.edit_server_channels(server_id)

    def edit_server_channels(self, server_id):
        if not SERVERS_FILE.exists():
            os.makedirs(SERVERS_FILE.parent, exist_ok=True)
            
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            servers = json.load(f)
            
        server = next((s for s in servers if s["id"] == server_id), None)
        if not server:
            return
            
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Edit Channels - {server['name']}")
        dlg.resize(600, 400)
        layout = QVBoxLayout(dlg)
        
        self.channels_table = QTableWidget()
        self.channels_table.setColumnCount(3)
        self.channels_table.setHorizontalHeaderLabels(["Channel Name", "Channel ID", ""])
        self.channels_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.channels_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.channels_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.channels_table.setColumnWidth(2, 40)
        self.channels_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QHeaderView {
                background-color: #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTableWidget::item {
                padding: 0px;
                border-bottom: 1px solid #3a3a3a;
            }
            QTableWidget::item:selected {
                background-color: #4a7bff;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4a7bff;
                border-radius: 6px;
                padding: 4px;
                selection-background-color: #4a7bff;
            }
            QTableWidget::viewport {
                border-radius: 8px;
                gridline-color: transparent;
            }
        """)
        self.channels_table.verticalHeader().setVisible(False)
        self.channels_table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.SelectedClicked)

        for channel in server["channels"]:
            self.add_channel_to_table(channel["name"], channel["id"])

        add_btn = QPushButton("Add Channel")
        if CONFIG_DATA["gradient_theme"] == True:
            add_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
        add_btn.clicked.connect(lambda: self.add_channel_dialog(server_id))
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_channels(server_id))
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        
        layout.addWidget(self.channels_table)
        layout.addWidget(add_btn)
        layout.addWidget(buttons)
        
        dlg.exec()

    def add_channel_dialog(self, server_id):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Channel")
        dlg.setFixedSize(400, 150)
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        channel_name = QLineEdit()
        channel_id = QLineEdit()
        
        channel_name.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #2d2d2d; color: white;")
        channel_id.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #2d2d2d; color: white;")
        
        form.addRow("Channel Name:", channel_name)
        form.addRow("Channel ID:", channel_id)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name = channel_name.text().strip()
            cid = channel_id.text().strip()
            
            if name and cid:
                if cid == "1282554696032194593" and server_id == "1186570213077041233":
                    notice_shown = self.show_dismissible_notice(
                        "Others Channel Warning",
                        "The channel you're trying to add (ID: 1282554696032194593) is the others channel.\n\n"
                        "NOT RECOMMENDED TO SNIPE IN THIS CHANNEL\n\n"
                        "Only handout servers are posted in this channel. Sniping here may cause:\n"
                        "• A ton of false detections\n"
                        "• Wasted snipes on \"LF\" servers\n"
                        "• Unnecessary pauses and cooldowns\n\n"
                        "Are you sure you want to add this channel?",
                        "handout_channel_warning"
                    )
                    if not notice_shown:
                        return
                
                if cid in SNIPERMEOW_CHANNELS and server_id == SOL_SNIPER_SERVER_ID:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Warning: SniperMeow Channel")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText("It is not recommended that you snipe the channels where snipermeow sends messages.")
                    msg.setInformativeText(
                        "Those messages it sends are sniped directly from maincord.\n"
                        "You will 100% never join any server if you attempt to snipe these channels.\n"
                        "Please snipe maincord directly instead.\n\n"
                        "Are you sure you would like to continue and snipe these channels anyways?"
                    )
                    continue_btn = msg.addButton("Continue Anyway", QMessageBox.ButtonRole.AcceptRole)
                    cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
                    msg.setDefaultButton(cancel_btn)
                    
                    msg.exec()
                    clicked_button = msg.clickedButton()
                    if clicked_button == continue_btn:
                        self.add_channel_to_table(name, cid)
                    return
                
                if cid in GLOBALMEOW_CHANNELS and not CONFIG_DATA.get("snipe_joinrbx_links", False) and server_id == SOL_SNIPER_SERVER_ID:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Notice: JoinRBX Required")
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText("Sniping globalmeow messages requires that you enable the Snipe JoinRBX Links feature.")
                    msg.setInformativeText(
                        "Would you like to enable the \"Snipe JoinRBX Links\" feature now?\n\n"
                        "This feature allows the sniper to properly handle and join JoinRBX links."
                    )
                    enable_btn = msg.addButton("Enable and Add Channel", QMessageBox.ButtonRole.AcceptRole)
                    cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
                    msg.setDefaultButton(enable_btn)
                    
                    msg.exec()
                    clicked_button = msg.clickedButton()
                    if clicked_button == enable_btn:
                        CONFIG_DATA["snipe_joinrbx_links"] = True
                        self.snipe_joinrbx_links_cb.setChecked(True)
                        self.save_settings()
                        self.add_channel_to_table(name, cid)
                    return
                
                self.add_channel_to_table(name, cid)

    def add_channel_to_table(self, name, cid):
        row = self.channels_table.rowCount()
        self.channels_table.insertRow(row)
        
        name_item = QTableWidgetItem(name)
        name_item.setForeground(QColor("#ffffff"))
        name_item.setFlags(name_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.channels_table.setItem(row, 0, name_item)
        
        id_item = QTableWidgetItem(cid)
        id_item.setForeground(QColor("#ffffff"))
        id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.channels_table.setItem(row, 1, id_item)
        
        remove_btn = QPushButton()
        remove_btn.setFixedSize(24, 24)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff8888;
            }
        """)
        remove_svg = QSvgWidget(remove_btn)
        remove_svg.load(QByteArray(b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
        </svg>"""))
        remove_svg.setFixedSize(12, 12)
        remove_svg.move(6, 6)
        remove_btn_layout = QHBoxLayout(remove_btn)
        remove_btn_layout.setContentsMargins(0, 0, 0, 0)
        remove_btn.clicked.connect(lambda: self.remove_channel_from_table(row))
        self.channels_table.setCellWidget(row, 2, remove_btn)

    def remove_channel_from_table(self, row):
        self.channels_table.removeRow(row)

    def save_channels(self, server_id):
        if not SERVERS_FILE.exists():
            os.makedirs(SERVERS_FILE.parent, exist_ok=True)
            
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            servers = json.load(f)
            
        server = next((s for s in servers if s["id"] == server_id), None)
        if not server:
            return
            
        server["channels"] = []
        for row in range(self.channels_table.rowCount()):
            name_item = self.channels_table.item(row, 0)
            id_item = self.channels_table.item(row, 1)
            
            if name_item and id_item:
                name = name_item.text().strip()
                cid = id_item.text().strip()
                if name and cid:
                    server["channels"].append({
                        "name": name,
                        "id": cid
                    })
        
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4)
        
        self.load_servers()

    def load_servers(self):
        logging.info("Loading servers data")
        if not SERVERS_FILE.exists():
            os.makedirs(SERVERS_FILE.parent, exist_ok=True)
            with open(SERVERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.default_servers, f)
            logging.info("Created empty servers file")
            return
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            servers = json.load(f)
            logging.info(f"Servers loaded: {servers}")
            
        self.server_tree.clear()
        for server in servers:
            item = QTreeWidgetItem(self.server_tree)
            
            enabled_checkbox = QCheckBox()
            enabled_checkbox.setChecked(server.get("enabled", True))
            enabled_checkbox.stateChanged.connect(lambda state, sid=server["id"]: self.toggle_server_enabled(sid, state))
            
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.addWidget(enabled_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
            
            self.server_tree.setItemWidget(item, 0, checkbox_widget)
            
            item.setText(1, server["name"])
            item.setText(2, server["id"])
            item.setForeground(1, QBrush(QColor("#ffffff")))
            item.setForeground(2, QBrush(QColor("#ffffff")))
            
            channels_widget = QWidget()
            channels_layout = QHBoxLayout(channels_widget)
            channels_layout.setContentsMargins(0, 0, 10, 0)
            channels_layout.setSpacing(10)

            label_container = QWidget()
            label_layout = QVBoxLayout(label_container)
            label_layout.setContentsMargins(0, 0, 0, 0)
            label_layout.setSpacing(0)

            channels_label = QLabel()
            channels_label.setText(", ".join([f"{ch['name']}" for ch in server["channels"]]) or "No channels")
            channels_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            channels_label.setStyleSheet("color: #ffffff; padding: 5px;")
            channels_label.setWordWrap(True)
            label_layout.addWidget(channels_label)

            channels_layout.addWidget(label_container, stretch=1)

            edit_btn = QPushButton()
            edit_btn.setFixedSize(32, 32)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
            """)
            svg = QSvgWidget()
            svg.load(EDIT_SVG)
            svg.setFixedSize(16, 16)
            btn_layout = QHBoxLayout(edit_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.addWidget(svg, alignment=Qt.AlignmentFlag.AlignCenter)
            edit_btn.clicked.connect(lambda checked=False, sid=server["id"]: self.edit_server_channels(sid))
            channels_layout.addWidget(edit_btn, alignment=Qt.AlignmentFlag.AlignRight)
            
            remove_btn = QPushButton()
            remove_btn.setFixedSize(32, 32)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff8888;
                }
            """)
            remove_svg = QSvgWidget()
            remove_svg.load(QByteArray(b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
            </svg>"""))
            remove_svg.setFixedSize(16, 16)
            remove_btn_layout = QHBoxLayout(remove_btn)
            remove_btn_layout.setContentsMargins(0, 0, 0, 0)
            remove_btn_layout.addWidget(remove_svg, alignment=Qt.AlignmentFlag.AlignCenter)
            remove_btn.clicked.connect(lambda checked=False, sid=server["id"]: self.remove_server(sid))
            channels_layout.addWidget(remove_btn, alignment=Qt.AlignmentFlag.AlignRight)

            self.server_tree.setItemWidget(item, 3, channels_widget)
            self.server_tree.addTopLevelItem(item)

    def toggle_server_enabled(self, server_id, state):
        if not SERVERS_FILE.exists():
            return
            
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            servers = json.load(f)
        
        for server in servers:
            if server["id"] == server_id:
                server["enabled"] = (state == Qt.CheckState.Checked.value)
                break
        
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4)
        
        logging.info(f"Server {server_id} enabled state changed to {state == Qt.CheckState.Checked.value}")

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Miscellaneous Settings")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        frame_layout.addWidget(title)
        
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(30)

        def add_checkbox_row(label_text, checkbox):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(3)
            row_layout.addWidget(checkbox)
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #e0e0e0; margin-left: 4px;")
            row_layout.addWidget(label)
            row_layout.addStretch()
            form_layout.addRow(row_widget)
        
        self.stillbackground_cb = QCheckBox()
        self.stillbackground_cb.setChecked(CONFIG_DATA["stillbackground"])
        add_checkbox_row("Still Background (Performance Increase for the UI)", self.stillbackground_cb)

        self.semi_transparent_background_cb = QCheckBox()
        self.semi_transparent_background_cb.setChecked(CONFIG_DATA["semi_transparent_background"])
        add_checkbox_row("Semi-Transparent UI Background", self.semi_transparent_background_cb)

        self.notify_cb = QCheckBox()
        self.notify_cb.setChecked(CONFIG_DATA["toast_notifications"])
        add_checkbox_row("Toast Notifications", self.notify_cb)

        self.use_discord_app_in_notifs_cb = QCheckBox()
        self.use_discord_app_in_notifs_cb.setChecked(CONFIG_DATA["use_discord_app"])
        add_checkbox_row("Use Discord App in Successful Snipe Toasts \"Jump To Message\" Button", self.use_discord_app_in_notifs_cb)

        self.gradient_theme_cb = QCheckBox()
        self.gradient_theme_cb.setChecked(CONFIG_DATA["gradient_theme"])
        add_checkbox_row("Gradient Theme", self.gradient_theme_cb)

        self.advanced_mode_cb = QCheckBox()
        self.advanced_mode_cb.setChecked(CONFIG_DATA["advanced_mode"])
        add_checkbox_row("Advanced Mode", self.advanced_mode_cb)

        self.advanced_mode_note = QLabel("Enabling Advanced Mode will unlock additional settings and features intended for users who know what they're doing.\nPlease refrain from enabling this unless you understand the implications.")
        self.advanced_mode_note.setWordWrap(True)
        self.advanced_mode_note.setStyleSheet("font-size: 12px; color: #bbbbbb;")
        form_layout.addRow(self.advanced_mode_note)

        self.hide_from_board_cb = QCheckBox()
        self.hide_from_board_cb.setChecked(CONFIG_DATA.get("hide_from_board", False))
        add_checkbox_row("Show Me as Anonymous on Active Snipers Board", self.hide_from_board_cb)

        frame_layout.addLayout(form_layout)

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setFixedHeight(45)
        if CONFIG_DATA["gradient_theme"] == True:
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 16px;
                    border-radius: 8px;
                }
                    QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8a4caf;
                    color: white;
                    font-weight: 500;
                    font-size: 16px;
                    border-radius: 8px;
                }
                    QPushButton:hover {
                    background-color: #9a5cbf;
                }
            """)
        self.save_btn.clicked.connect(self.save_settings_btn)
        frame_layout.addWidget(self.save_btn)

        scroll_layout.addWidget(frame)

        tap_frame = GradientFrame()
        tap_frame.setStyleSheet("border-radius: 12px;")
        tap_frame_layout = QVBoxLayout(tap_frame)
        tap_frame_layout.setContentsMargins(20, 20, 20, 20)
        
        tap_title = QLabel("1-Tap Hotkeys")
        tap_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        tap_frame_layout.addWidget(tap_title)
        
        tap_desc = QLabel("Executes the attached action once when the hotkey is pressed.")
        tap_desc.setWordWrap(True)
        tap_desc.setStyleSheet("font-size: 13px; color: #d0d0d0; margin-bottom: 12px;")
        tap_frame_layout.addWidget(tap_desc)

        def create_hotkey_row(label_text, checkbox, key_label, key_value, duration_input=None):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(15)
            
            row_layout.addWidget(checkbox)
            
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #e0e0e0;")
            row_layout.addWidget(label)
            
            if duration_input:
                duration_layout = QHBoxLayout()
                duration_layout.setSpacing(5)
                duration_label = QLabel("Duration (in seconds):")
                duration_label.setStyleSheet("font-size: 12px; color: #e0e0e0; margin-left: 10px;")
                duration_layout.addWidget(duration_label)
                duration_layout.addWidget(duration_input)
                row_layout.addLayout(duration_layout)
            
            row_layout.addStretch()
            
            key_display = QLabel(key_value)
            key_display.setStyleSheet("""
                QLabel {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: #e0e0e0;
                    min-width: 60px;
                    text-align: center;
                }
            """)
            row_layout.addWidget(key_display)
            
            assign_btn = QPushButton("Assign")
            assign_btn.setFixedSize(120, 35)
            assign_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
                QPushButton:pressed {
                    background-color: #3a6bdf;
                }
                QPushButton:disabled {
                    background-color: #3a5baf;
                }
            """)
            row_layout.addWidget(assign_btn)
            
            return row_widget, key_display, assign_btn

        self.hk1_cb = QCheckBox()
        self.hk1_cb.setChecked(CONFIG_DATA["open_roblox_toggle"])
        hk1_row, self.hk1_display, self.hk1_assign_btn = create_hotkey_row(
            "Join Random Server", self.hk1_cb, "Key:", CONFIG_DATA["open_roblox"]
        )
        tap_frame_layout.addWidget(hk1_row)

        self.pause_duration_input = QLineEdit()
        self.pause_duration_input.setText(str(CONFIG_DATA["pause_duration"]))
        self.pause_duration_input.setFixedSize(70, 30)
        self.pause_duration_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }
        """)
        self.pause_duration_input.setValidator(QIntValidator(1, 3600))

        self.hk2_cb = QCheckBox()
        self.hk2_cb.setChecked(CONFIG_DATA["stop_sniper_toggle"])
        hk2_row, self.hk2_display, self.hk2_assign_btn = create_hotkey_row(
            "Pause Sniper", self.hk2_cb, "Key:", CONFIG_DATA["stop_sniper"], self.pause_duration_input
        )
        tap_frame_layout.addWidget(hk2_row)

        self.hk3_cb = QCheckBox()
        self.hk3_cb.setChecked(CONFIG_DATA["toggle_sniper_toggle"])
        hk3_row, self.hk3_display, self.hk3_assign_btn = create_hotkey_row(
            "Toggle Sniper (Will Resume Sniping if Paused)", self.hk3_cb, "Key:", CONFIG_DATA["toggle_sniper"]
        )
        tap_frame_layout.addWidget(hk3_row)

        scroll_layout.addWidget(tap_frame)

        hold_frame = GradientFrame()
        hold_frame.setStyleSheet("border-radius: 12px;")
        hold_frame_layout = QVBoxLayout(hold_frame)
        hold_frame_layout.setContentsMargins(20, 20, 20, 20)
        
        hold_title = QLabel("Hold Hotkeys")
        hold_title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        hold_frame_layout.addWidget(hold_title)
        
        hold_desc = QLabel("Executes the attached action continuously while the hotkey is held down.\nThese keys are required to be held down to execute their function properly.")
        hold_desc.setWordWrap(True)
        hold_desc.setStyleSheet("font-size: 13px; color: #d0d0d0; margin-bottom: 12px;")
        hold_frame_layout.addWidget(hold_desc)

        self.hk4_cb = QCheckBox()
        self.hk4_cb.setChecked(CONFIG_DATA["loading_asset_skipper_toggle"])
        hk4_row, self.hk4_display, self.hk4_assign_btn = create_hotkey_row(
            "Loading Asset Skipper", self.hk4_cb, "Key:", CONFIG_DATA["loading_asset_skipper"]
        )
        hold_frame_layout.addWidget(hk4_row)

        self.hk5_cb = QCheckBox()
        self.hk5_cb.setChecked(CONFIG_DATA["main_menu_skipper_toggle"])
        hk5_row, self.hk5_display, self.hk5_assign_btn = create_hotkey_row(
            "Play Button Skipper", self.hk5_cb, "Key:", CONFIG_DATA["main_menu_skipper"]
        )
        hold_frame_layout.addWidget(hk5_row)

        scroll_layout.addWidget(hold_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        self.assigning_hotkey = None
        self.hk1_assign_btn.clicked.connect(lambda: self.start_key_assignment(1))
        self.hk2_assign_btn.clicked.connect(lambda: self.start_key_assignment(2))
        self.hk3_assign_btn.clicked.connect(lambda: self.start_key_assignment(3))
        self.hk4_assign_btn.clicked.connect(lambda: self.start_key_assignment(4))
        self.hk5_assign_btn.clicked.connect(lambda: self.start_key_assignment(5))

        return tab

    def on_advanced_mode_changed(self):
        if self.advanced_mode_cb.isChecked():
            msg = QMessageBox(self)
            msg.setWindowTitle("Enable Advanced Mode?")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Advanced Mode Confirmation")
            msg.setInformativeText(
                "Advanced Mode unlocks experimental features and settings that are intended for experienced users only.\n\n"
                "Features include:\n"
                "• Ability to Snipe Non-Sol's RNG Roblox Games\n"
                "• Custom RegEx Keyword Detections\n\n"
                "Are you sure you want to enable Advanced Mode?\nEnabling Advanced Mode requires an application restart to take effect."
            )
            
            enable_btn = msg.addButton("Enable Advanced Mode", QMessageBox.ButtonRole.AcceptRole)
            cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            
            msg.setDefaultButton(cancel_btn)
            msg.exec()
            
            if msg.clickedButton() == cancel_btn:
                self.advanced_mode_cb.setChecked(False)
            else:
                self.advanced_mode_cb.setChecked(True)
        else:
            self.advanced_mode_cb.setChecked(False)
        
        self.save_settings()

    def create_logs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame.setMinimumHeight(600)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setSpacing(15)

        title = QLabel("Logs")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        title.setContentsMargins(0, 0, 0, 10)
        frame_layout.addWidget(title)

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(20)
        filter_layout.setContentsMargins(0, 0, 0, 15)

        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("font-size: 14px; color: #e0e0e0; font-weight: 500;")
        filter_layout.addWidget(filter_label)

        self.info_checkbox = QCheckBox("INFO")
        self.info_checkbox.setChecked(True)
        self.info_checkbox.setStyleSheet("color: #4a9eff; font-size: 13px;")
        self.info_checkbox.stateChanged.connect(self.update_log_filter)
        filter_layout.addWidget(self.info_checkbox)

        self.warning_checkbox = QCheckBox("WARNING")
        self.warning_checkbox.setChecked(True)
        self.warning_checkbox.setStyleSheet("color: #ffb84a; font-size: 13px;")
        self.warning_checkbox.stateChanged.connect(self.update_log_filter)
        filter_layout.addWidget(self.warning_checkbox)

        self.error_checkbox = QCheckBox("ERROR")
        self.error_checkbox.setChecked(True)
        self.error_checkbox.setStyleSheet("color: #ff6b6b; font-size: 13px;")
        self.error_checkbox.stateChanged.connect(self.update_log_filter)
        filter_layout.addWidget(self.error_checkbox)

        filter_layout.addStretch()

        clear_btn = QPushButton("Clear Logs")
        clear_btn.setFixedHeight(32)
        clear_btn.setFixedWidth(110)
        if CONFIG_DATA["gradient_theme"]:
            clear_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                    border-radius: 6px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3a6bef, stop:1 #7a3c9f);
                }
            """)
        else:
            clear_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                    border-radius: 6px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
                QPushButton:pressed {
                    background-color: #3a6bef;
                }
            """)
        clear_btn.clicked.connect(self.clear_logs)
        filter_layout.addWidget(clear_btn)

        export_btn = QPushButton("Export Logs")
        export_btn.setFixedHeight(32)
        export_btn.setFixedWidth(120)
        if CONFIG_DATA["gradient_theme"]:
            export_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                    border-radius: 6px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3a6bef, stop:1 #7a3c9f);
                }
            """)
        else:
            export_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                    border-radius: 6px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
                QPushButton:pressed {
                    background-color: #3a6bef;
                }
            """)
        export_btn.clicked.connect(self.export_logs)
        filter_layout.addWidget(export_btn)

        open_dir_btn = QPushButton("Open Logs")
        open_dir_btn.setFixedHeight(32)
        open_dir_btn.setFixedWidth(110)
        if CONFIG_DATA["gradient_theme"]:
            open_dir_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                    border-radius: 6px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3a6bef, stop:1 #7a3c9f);
                }
            """)
        else:
            open_dir_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a7bff;
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                    border-radius: 6px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #5a8bff;
                }
                QPushButton:pressed {
                    background-color: #3a6bef;
                }
            """)
        open_dir_btn.clicked.connect(self.open_logs_directory)
        filter_layout.addWidget(open_dir_btn)

        frame_layout.addLayout(filter_layout)

        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(3)
        self.logs_table.setHorizontalHeaderLabels(["Time", "Level", "Message"])
        self.logs_table.setColumnWidth(0, 90)
        self.logs_table.setColumnWidth(1, 80)
        self.logs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.logs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.logs_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.logs_table.verticalHeader().setVisible(False)
        self.logs_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.logs_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.logs_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.logs_table.setAlternatingRowColors(True)
        self.logs_table.setShowGrid(False)

        if CONFIG_DATA["gradient_theme"]:
            scrollbar_handle = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a7bff, stop:1 #8a4caf);"
            scrollbar_hover = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5a8bff, stop:1 #9a5cbf);"
        else:
            scrollbar_handle = "background-color: #4a7bff;"
            scrollbar_hover = "background-color: #5a8bff;"
        
        table_stylesheet = f"""
            QTableWidget {{
                background-color: #2a2a2a;
                alternate-background-color: #252525;
                gridline-color: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
            }}
            QTableWidget::item:selected {{
                background-color: #4a7bff;
                color: white;
            }}
            QHeaderView {{
                background-color: #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: #3c3c3c;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 8px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 8px;
            }}
            QScrollBar:vertical {{
                background-color: #2a2a2a;
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                {scrollbar_handle}
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                {scrollbar_hover}
            }}
            QScrollBar::add-line:vertical {{
                border: none;
                background: none;
            }}
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QScrollBar:horizontal {{
                background-color: #2a2a2a;
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                {scrollbar_handle}
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                {scrollbar_hover}
            }}
            QScrollBar::add-line:horizontal {{
                border: none;
                background: none;
            }}
            QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
            }}
        """
        self.logs_table.setStyleSheet(table_stylesheet)

        frame_layout.addWidget(self.logs_table)

        layout.addWidget(frame)
        layout.addStretch()

        log_emitter.log_signal.connect(self.add_log_entry)
        if not log_emitter.isRunning():
            log_emitter.start()

        self.log_entries = []

        return tab

    def add_log_entry(self, timestamp, level, message):
        self.log_entries.append({
            'timestamp': timestamp,
            'level': level,
            'message': message
        })

        self.update_log_filter()

    def update_log_filter(self):
        show_info = self.info_checkbox.isChecked()
        show_warning = self.warning_checkbox.isChecked()
        show_error = self.error_checkbox.isChecked()

        scroll_value = self.logs_table.verticalScrollBar().value()
        self.logs_table.setRowCount(0)

        for entry in self.log_entries:
            level = entry['level']
            
            if (level == 'INFO' and not show_info) or \
               (level == 'WARNING' and not show_warning) or \
               (level == 'ERROR' and not show_error):
                continue

            row = self.logs_table.rowCount()
            self.logs_table.insertRow(row)

            time_item = QTableWidgetItem(entry['timestamp'])
            time_item.setForeground(QColor("#888888"))
            time_item.setFont(QFont("Consolas", 11))
            self.logs_table.setItem(row, 0, time_item)

            level_item = QTableWidgetItem(level)
            level_item.setFont(QFont("Consolas", 11))
            if level == 'INFO':
                level_item.setForeground(QColor("#4a9eff"))
            elif level == 'WARNING':
                level_item.setForeground(QColor("#ffb84a"))
            elif level == 'ERROR':
                level_item.setForeground(QColor("#ff6b6b"))
            self.logs_table.setItem(row, 1, level_item)

            message_item = QTableWidgetItem(entry['message'])
            message_item.setFont(QFont("Consolas", 11))
            message_item.setForeground(QColor("#e0e0e0"))
            message_item.setToolTip(entry['message'])
            self.logs_table.setItem(row, 2, message_item)

        self.logs_table.verticalScrollBar().setValue(scroll_value)

    def clear_logs(self):
        self.log_entries.clear()
        self.logs_table.setRowCount(0)

    def export_logs(self):
        try:
            current_log_file = LOGS_DIR / log_filename
            if not current_log_file.exists():
                QMessageBox.warning(self, "Export Logs", "No log file found to export.")
                return
            
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Logs",
                str(current_log_file),
                f"Log Files (*.log);;All Files (*)"
            )
            
            if save_path:
                shutil.copy2(str(current_log_file), save_path)
                QMessageBox.information(self, "Export Logs", f"Logs exported successfully to:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export logs:\n{str(e)}")

    def open_logs_directory(self):
        try:
            logs_path = str(LOGS_DIR)
            
            if platform.system() == "Windows":
                os.startfile(logs_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", logs_path])
            else:
                logging.error(f"Unsupported OS: {platform.system()}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open logs directory:\n{str(e)}")

    def create_credits_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(24)

        def create_svg_icon(svg_bytes, url, username, platform):
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            svg_widget = QSvgWidget()
            svg_widget.load(svg_bytes)
            svg_widget.setFixedSize(40, 40)
            svg_widget.setCursor(Qt.CursorShape.PointingHandCursor)
            def open_url(event):
                webbrowser.open(url)
            svg_widget.mousePressEvent = open_url

            overlay_layout = QHBoxLayout()
            overlay_layout.setContentsMargins(0, 0, 0, 0)
            overlay_layout.addWidget(svg_widget)
            
            container_layout.addLayout(overlay_layout)
            
            platform_name = platform.capitalize()
            if platform == "discord_srv":
                platform_name = "Discord"
            icon = ""
            if platform != "website" and platform != "discord_srv":
                icon = "@"
            container.setToolTip(f"🔗 {icon}{username} - {platform_name}")
            
            return container

        def create_rounded_pixmap(path, size, radius=12):
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                return QPixmap()
            
            rounded = QPixmap(size, size)
            rounded.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            
            path = QPainterPath()
            path.addRoundedRect(0, 0, size, size, radius, radius)
            painter.setClipPath(path)
            
            scaled = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled)
            painter.end()
            
            return rounded

        def create_profile_card(img_path, name, quote, icons):
            frame = GradientFrame()
            frame.setFixedHeight(220)
            frame.setStyleSheet("border-radius: 16px;")
            layout = QHBoxLayout(frame)
            layout.setContentsMargins(24, 16, 24, 16)
            layout.setSpacing(24)
            layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            img_label = QLabel()
            rounded_pixmap = create_rounded_pixmap(img_path, 180, 16)
            img_label.setPixmap(rounded_pixmap)
            img_label.setFixedSize(180, 180)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.setStyleSheet("background-color: transparent;")

            info_frame = QFrame()
            info_frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(30,30,30,180);
                    border-radius: 12px;
                }
                QLabel {
                    background-color: transparent;
                }
            """)
            info_layout = QVBoxLayout(info_frame)
            info_layout.setContentsMargins(18, 12, 18, 12)
            info_layout.setSpacing(10)

            name_label = QLabel(name)
            name_label.setStyleSheet("""
                QLabel {
                    font-size: 28px; 
                    font-weight: 700; 
                    color: #fff;
                }
            """)
            quote_label = QLabel(f"\"{quote}\"")
            quote_label.setWordWrap(True)
            quote_label.setStyleSheet("""
                QLabel {
                    font-size: 16px; 
                    color: #bdbdbd; 
                    font-style: italic; 
                    margin-bottom: 8px;
                    margin-left: -8px;
                }
            """)

            icons_layout = QHBoxLayout()
            icons_layout.setSpacing(12)
            for icon_widget in icons:
                icons_layout.addWidget(icon_widget)
            icons_layout.addStretch()

            info_layout.addWidget(name_label)
            info_layout.addWidget(quote_label)
            info_layout.addLayout(icons_layout)
            info_layout.addStretch()

            layout.addWidget(img_label)
            layout.addWidget(info_frame)
            return frame

        vex_icons = [
            create_svg_icon(DISCORD_SVG, "https://discord.com/users/1018875765565177976", "vex.sys", "discord"),
            create_svg_icon(ROBLOX_SVG, "https://www.roblox.com/users/682980257/profile", "vex_coder", "roblox"),
            create_svg_icon(GITHUB_SVG, "https://github.com/vexsyx", "vexsyx", "github"),
            create_svg_icon(WEBSITE_SVG, "https://vexsys.site", "vexsys.site", "website"),
        ]
        vex_card = create_profile_card(
            SETTINGS_DIR / "vex.png", "vex", "i program from time to time", vex_icons
        )
        scroll_layout.addWidget(vex_card)

        solsniper_icons = [
            create_svg_icon(DISCORD_SVG, "https://discord.gg/solsniper", "Join the Community Server", "discord_srv"),
            create_svg_icon(WEBSITE_SVG, "https://solsniper.vexsys.site", "Sol Sniper Dashboard", "website"),
        ]
        solsniper_card = create_profile_card(
            SETTINGS_DIR / "solsniper.png", "Sol's Sniper", "An easier way to join rare servers.", solsniper_icons
        )
        scroll_layout.addWidget(solsniper_card)

        donate_btn = QPushButton("Donate to Sol's Sniper/vex")
        donate_btn.setFixedHeight(60)
        if CONFIG_DATA["gradient_theme"] == True:
            donate_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a7bff, stop:1 #8a4caf);
                    color: white;
                    font-size: 20px;
                    font-weight: 600;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
            """)
        else:
            donate_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8a4caf;
                    color: white;
                    font-size: 20px;
                    font-weight: 600;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #9a5cbf;
                }
            """)
        donate_btn.clicked.connect(lambda: webbrowser.open("https://www.roblox.com/games/86163153952489/Sols-Sniper-Donation-Game#!/store"))
        scroll_layout.addWidget(donate_btn)

        yeswe_icons = [
            create_svg_icon(DISCORD_SVG, "https://discord.com/users/463575384961581066", "yeswe", "discord"),
            create_svg_icon(ROBLOX_SVG, "https://www.roblox.com/users/551612000/profile", "or472", "roblox"),
            create_svg_icon(GITHUB_SVG, "https://github.com/the2727", "the2727", "github"),
        ]
        yeswe_card = create_profile_card(
            SETTINGS_DIR / "yeswe.png", "yeswe", "  - No Quote Provided -  ", yeswe_icons
        )
        scroll_layout.addWidget(yeswe_card)

        scroll_layout.addStretch()
        scroll.setWidget(content)
        scroll.setStyleSheet("border-radius: 12px;")
        layout.addWidget(scroll)
        return tab
    
    def get_stylesheet(self):
        if CONFIG_DATA["gradient_theme"] == True:
            return """
                QMainWindow {
                    background-color: #1e1e1e;
                    border-radius: 12px;
                }
                QWidget {
                    background-color: transparent;
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QTabWidget::pane {
                    border: none;
                }
                QCheckBox {
                    spacing: 10px;
                    color: #e0e0e0;
                    font-size: 16px;
                }
                QCheckBox::indicator {
                    width: 24px;
                    height: 24px;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #3a3a3a;
                    border: 2px solid #555;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                    border: 2px solid #5a8bff;
                    border-radius: 4px;
                }
                QCheckBox:disabled {
                    color: #b0b0b0;
                }
                QCheckBox::indicator:disabled {
                    background-color: #2a2a2a;
                    border: 2px solid #404040;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked:disabled {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #3a5baf, stop:1 #6a3c8f);
                    border: 2px solid #4a4a6a;
                    border-radius: 4px;
                }
                QLineEdit, QComboBox {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 8px;
                    padding: 10px;
                    color: #e0e0e0;
                    font-size: 14px;
                    height: 40px;
                }
                QLineEdit:disabled, QComboBox:disabled {
                    background-color: #252525;
                    color: #b0b0b0;
                    border: 1px solid #383838;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox:disabled {
                    color: #b0b0b0;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 8px;
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QListWidget:disabled {
                    background-color: #252525;
                    color: #b0b0b0;
                    border: 1px solid #383838;
                }
                QListWidget::item {
                    padding: 12px;
                    border-bottom: 1px solid #3a3a3a;
                }
                QListWidget::item:selected {
                    background-color: #4a7bff;
                    color: white;
                }
                QListWidget::item:disabled {
                    color: #b0b0b0;
                    background-color: transparent;
                }
                QListWidget::item:selected:disabled {
                    background-color: #3a5baf;
                    color: #d0d0d0;
                }
                QLabel {
                    color: #e0e0e0;
                    background-color: transparent;
                }
                QLabel:disabled {
                    color: #b0b0b0;
                }
                QScrollBar:vertical {
                    background: transparent;
                    width: 12px;
                    margin: 2px 0 2px 0;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                    min-height: 24px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QScrollBar::handle:vertical:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3a5baf, stop:1 #7a3c9f);
                }
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {
                    height: 0;
                    background: none;
                }
                QScrollBar:horizontal {
                    background: transparent;
                    height: 12px;
                    margin: 0 2px 0 2px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4a7bff, stop:1 #8a4caf);
                    min-width: 24px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a8bff, stop:1 #9a5cbf);
                }
                QScrollBar::handle:horizontal:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3a5baf, stop:1 #7a3c9f);
                }
                QScrollBar::add-line:horizontal,
                QScrollBar::sub-line:horizontal {
                    width: 0;
                    background: none;
                }
            """
        else:
            return """
                QMainWindow {
                    background-color: #1e1e1e;
                    border-radius: 12px;
                }
                QWidget {
                    background-color: transparent;
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QTabWidget::pane {
                    border: none;
                }
                QCheckBox {
                    spacing: 10px;
                    color: #e0e0e0;
                    font-size: 16px;
                }
                QCheckBox::indicator {
                    width: 24px;
                    height: 24px;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #3a3a3a;
                    border: 2px solid #555;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background-color: #4a7bff;
                    border: 2px solid #5a8bff;
                    border-radius: 4px;
                }
                QCheckBox:disabled {
                    color: #b0b0b0;
                }
                QCheckBox::indicator:disabled {
                    background-color: #2a2a2a;
                    border: 2px solid #404040;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked:disabled {
                    background-color: #3a5baf;
                    border: 2px solid #4a4a6a;
                    border-radius: 4px;
                }
                QLineEdit, QComboBox {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 8px;
                    padding: 10px;
                    color: #e0e0e0;
                    font-size: 14px;
                    height: 40px;
                }
                QLineEdit:disabled, QComboBox:disabled {
                    background-color: #252525;
                    color: #b0b0b0;
                    border: 1px solid #383838;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox:disabled {
                    color: #b0b0b0;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 8px;
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QListWidget:disabled {
                    background-color: #252525;
                    color: #b0b0b0;
                    border: 1px solid #383838;
                }
                QListWidget::item {
                    padding: 12px;
                    border-bottom: 1px solid #3a3a3a;
                }
                QListWidget::item:selected {
                    background-color: #4a7bff;
                    color: white;
                }
                QListWidget::item:disabled {
                    color: #b0b0b0;
                    background-color: transparent;
                }
                QListWidget::item:selected:disabled {
                    background-color: #3a5baf;
                    color: #d0d0d0;
                }
                QLabel {
                    color: #e0e0e0;
                    background-color: transparent;
                }
                QLabel:disabled {
                    color: #b0b0b0;
                }
                QScrollBar:vertical {
                    background: transparent;
                    width: 12px;
                    margin: 2px 0 2px 0;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: #4a7bff;
                    min-height: 24px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #5a8bff;
                }
                QScrollBar::handle:vertical:pressed {
                    background: #3a5baf;
                }
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {
                    height: 0;
                    background: none;
                }
                QScrollBar:horizontal {
                    background: transparent;
                    height: 12px;
                    margin: 0 2px 0 2px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal {
                    background: #4a7bff;
                    min-width: 24px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: #5a8bff;
                }
                QScrollBar::handle:horizontal:pressed {
                    background: #3a5baf;
                }
                QScrollBar::add-line:horizontal,
                QScrollBar::sub-line:horizontal {
                    width: 0;
                    background: none;
                }
            """
    
    def setup_connections(self):
        self.sniper_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(0))
        self.accounts_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        self.keywords_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        self.servers_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(3))
        self.settings_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(4))
        self.logs_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(5))
        self.credits_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(6))

        self.start_btn.clicked.connect(self.toggle_sniping)

        self.token_input.textChanged.connect(self.save_settings)
        self.glitch_cb.stateChanged.connect(self.save_settings)
        self.dream_cb.stateChanged.connect(self.save_settings)
        self.cyber_cb.stateChanged.connect(self.save_settings)
        self.singularity_cb.stateChanged.connect(self.save_settings)
        self.jester_cb.stateChanged.connect(self.save_settings)
        self.void_cb.stateChanged.connect(self.save_settings)
        
        self.glitch_duration.textChanged.connect(self.save_settings)
        self.dream_duration.textChanged.connect(self.save_settings)
        self.cyber_duration.textChanged.connect(self.save_settings)
        self.singularity_duration.textChanged.connect(self.save_settings)
        self.jester_duration.textChanged.connect(self.save_settings)
        self.void_duration.textChanged.connect(self.save_settings)
        
        self.notify_cb.stateChanged.connect(self.save_settings)
        self.use_discord_app_in_notifs_cb.stateChanged.connect(self.save_settings)
        self.close_roblox_cb.stateChanged.connect(lambda: self.toggle_leave_settings("close_roblox"))
        self.leave_game_cb.stateChanged.connect(lambda: self.toggle_leave_settings("leave_game"))
        self.minimize_other_windows_cb.stateChanged.connect(self.save_settings)
        self.auto_pause_sniper_cb.stateChanged.connect(self.save_settings)
        self.pause_duration_input.textChanged.connect(self.save_settings)
        self.hk1_cb.stateChanged.connect(self.save_settings)
        self.hk2_cb.stateChanged.connect(self.save_settings)
        self.hk3_cb.stateChanged.connect(self.save_settings)
        self.stillbackground_cb.stateChanged.connect(self.save_settings)
        self.semi_transparent_background_cb.stateChanged.connect(self.save_settings)
        self.gradient_theme_cb.stateChanged.connect(self.save_settings)
        self.advanced_mode_cb.stateChanged.connect(self.on_advanced_mode_changed)
        self.hide_from_board_cb.stateChanged.connect(self._schedule_websocket_hide_setting_update)
        self.snipe_ropro_links_cb.stateChanged.connect(self.save_settings)
        self.snipe_joinrbx_links_cb.stateChanged.connect(self.save_settings)
        self.snipe_roseal_links_cb.stateChanged.connect(self.save_settings)
        self.snipe_fishstrap_links_cb.stateChanged.connect(self.save_settings)
        self.ignore_messages_that_respond_cb.stateChanged.connect(self.save_settings)

        if CONFIG_DATA.get("advanced_mode", False) == True:
            self.only_join_sols_links_cb.stateChanged.connect(self.save_settings)

    def toggle_leave_settings(self, toggle_pressed):
        if not toggle_pressed:
            return
        if toggle_pressed == "close_roblox":
            if self.close_roblox_cb.isChecked():
                self.leave_game_cb.setChecked(False)
                self.leave_game_cb.setEnabled(False)
            else:
                self.leave_game_cb.setEnabled(True)
        elif toggle_pressed == "leave_game":
            if self.leave_game_cb.isChecked():
                self.close_roblox_cb.setChecked(False)
                self.close_roblox_cb.setEnabled(False)
            else:
                self.close_roblox_cb.setEnabled(True)
        self.save_settings()
    
    def load_settings(self):
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        keywords = data
                    else:
                        keywords = data.get("keywords", [])
                    
                    self.keyword_list.clear()
                    for kw in keywords:
                        self.keyword_list.addItem(kw['name'])
            except:
                pass
        else:
            os.makedirs(KEYWORDS_FILE.parent, exist_ok=True)
            with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.default_keywords, f)
        
        if SERVERS_FILE.exists():
            try:
                with open(SERVERS_FILE, "r", encoding="utf-8") as f:
                    servers = json.load(f)
                    self.server_list.clear()
                    for server in servers:
                        self.server_list.addItem(server['name'])
            except:
                pass
        else:
            os.makedirs(SERVERS_FILE.parent, exist_ok=True)
            with open(SERVERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.default_servers, f)
        
        load_settings()
        
        if CONFIG_DATA["override_protocol_enabled"] and CONFIG_DATA["override_protocol_path"]:
            self.selected_override_version = {
                "name": f"Custom: {Path(CONFIG_DATA['override_protocol_path']).name}",
                "path": CONFIG_DATA["override_protocol_path"],
                "type": CONFIG_DATA["override_protocol_type"],
                "version": CONFIG_DATA["override_protocol_version"]
            }
            self.override_version_label.setText(self.selected_override_version["name"])
        
        if hasattr(self, 'override_protocol_container'):
            self.override_protocol_container.setVisible(CONFIG_DATA["advanced_mode"])
        
        self.update_protocol_status()
    
    def add_keyword_list(self):
        dialog = KeywordDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_settings()
    
    def remove_keyword_list(self):
        if self.keyword_list.currentRow() >= 0:
            row = self.keyword_list.currentRow()
            self.keyword_list.takeItem(row)
            
            if KEYWORDS_FILE.exists():
                try:
                    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            keywords = data
                            if 0 <= row < len(keywords):
                                del keywords[row]
                                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                                    json.dump(keywords, f, indent=4)
                        else:
                            keywords = data.get("keywords", [])
                            custom_categories = data.get("custom_categories", [])
                            if 0 <= row < len(keywords):
                                del keywords[row]
                                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                                    json.dump({"keywords": keywords, "custom_categories": custom_categories}, f, indent=4)
                except:
                    pass
            else:
                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                    json.dump(self.default_keywords, f)

    def save_settings(self):
        CONFIG_DATA["token"] = self.token_input.text()
        CONFIG_DATA["glitchsniping"] = self.glitch_cb.isChecked()
        CONFIG_DATA["dreamsniping"] = self.dream_cb.isChecked()
        CONFIG_DATA["cybersniping"] = self.cyber_cb.isChecked()
        CONFIG_DATA["singularitysniping"] = self.singularity_cb.isChecked()
        CONFIG_DATA["jestersniping"] = self.jester_cb.isChecked()
        CONFIG_DATA["voidcoinsniping"] = self.void_cb.isChecked()
        CONFIG_DATA["toast_notifications"] = self.notify_cb.isChecked()
        CONFIG_DATA["use_discord_app"] = self.use_discord_app_in_notifs_cb.isChecked()
        CONFIG_DATA["advanced_mode"] = self.advanced_mode_cb.isChecked()
        CONFIG_DATA["close_roblox_before_joining"] = self.close_roblox_cb.isChecked()
        CONFIG_DATA["leave_game_before_joining"] = self.leave_game_cb.isChecked()
        CONFIG_DATA["minimize_other_windows"] = self.minimize_other_windows_cb.isChecked()
        CONFIG_DATA["auto_pause_sniper"] = self.auto_pause_sniper_cb.isChecked()
        CONFIG_DATA["open_roblox_toggle"] = self.hk1_cb.isChecked()
        CONFIG_DATA["stop_sniper_toggle"] = self.hk2_cb.isChecked()
        CONFIG_DATA["toggle_sniper_toggle"] = self.hk3_cb.isChecked()
        CONFIG_DATA["loading_asset_skipper_toggle"] = self.hk4_cb.isChecked()
        CONFIG_DATA["main_menu_skipper_toggle"] = self.hk5_cb.isChecked()
        CONFIG_DATA["pause_duration"] = self.pause_duration_input.text()
        CONFIG_DATA["stillbackground"] = self.stillbackground_cb.isChecked()
        CONFIG_DATA["semi_transparent_background"] = self.semi_transparent_background_cb.isChecked()
        CONFIG_DATA["gradient_theme"] = self.gradient_theme_cb.isChecked()
        CONFIG_DATA["snipe_ropro_links"] = self.snipe_ropro_links_cb.isChecked()
        CONFIG_DATA["snipe_joinrbx_links"] = self.snipe_joinrbx_links_cb.isChecked()
        CONFIG_DATA["snipe_roseal_links"] = self.snipe_roseal_links_cb.isChecked()
        CONFIG_DATA["snipe_fishstrap_links"] = self.snipe_fishstrap_links_cb.isChecked()
        CONFIG_DATA["ignore_messages_that_respond"] = self.ignore_messages_that_respond_cb.isChecked()
        CONFIG_DATA["pause_duration_glitched"] = self.glitch_duration.text()
        CONFIG_DATA["pause_duration_dreamspace"] = self.dream_duration.text()
        CONFIG_DATA["pause_duration_cyberspace"] = self.cyber_duration.text()
        CONFIG_DATA["pause_duration_singularity"] = self.singularity_duration.text()
        CONFIG_DATA["pause_duration_jester"] = self.jester_duration.text()
        CONFIG_DATA["pause_duration_void_coin"] = self.void_duration.text()
        CONFIG_DATA["hide_from_board"] = self.hide_from_board_cb.isChecked()
        
        if "dismissed_notices" not in CONFIG_DATA:
            CONFIG_DATA["dismissed_notices"] = {
                "handout_channel_warning": False,
                "handout_channel_warning_launch": False,
                "missing_maincord_warning": False,
                "locked_pre_release_warning": False
            }

        if hasattr(self, 'custom_category_durations'):
            for category, duration_input in list(self.custom_category_durations.items()):
                try:
                    if duration_input and not duration_input.isHidden():
                        duration_key = f"pause_duration_{category.lower().replace(' ', '_')}"
                        CONFIG_DATA[duration_key] = duration_input.text()
                except (RuntimeError, AttributeError):
                    if category in self.custom_category_durations:
                        del self.custom_category_durations[category]
        
        if hasattr(self, 'selected_override_version'):
            CONFIG_DATA["override_protocol_enabled"] = True
            CONFIG_DATA["override_protocol_path"] = self.selected_override_version["path"]
            CONFIG_DATA["override_protocol_type"] = self.selected_override_version["type"]
            CONFIG_DATA["override_protocol_version"] = self.selected_override_version["version"]

        data = self.get_current_keyword_data()
        custom_categories = data.get("custom_categories", [])
        
        for key in list(CONFIG_DATA.keys()):
            if key.startswith("customcat_"):
                category_name = key.replace("customcat_", "").replace("_", " ")
                if category_name not in custom_categories:
                    custom_categories.append(category_name)
        
        for category in custom_categories:
            checkbox = self.custom_category_checkboxes.get(category)
            if checkbox:
                setting_name = f"customcat_{category.replace(' ', '_')}"
                CONFIG_DATA[setting_name] = checkbox.isChecked()
            else:
                setting_name = f"customcat_{category.replace(' ', '_')}"
                if setting_name not in CONFIG_DATA:
                    CONFIG_DATA[setting_name] = False

        if CONFIG_DATA["advanced_mode"] == True and hasattr(self, 'only_join_sols_links_cb'):
            CONFIG_DATA["only_join_sols_links"] = self.only_join_sols_links_cb.isChecked()

        save_settings()
        logging.info("Settings saved successfully")

    def handle_session_kicked(self, reason):
        logging.info("Session terminated due to dashboard kick")
        
        global CONFIG_DATA
        CONFIG_DATA["token"] = ""
        save_settings()
        
        if sniper_active:
            self.stop_sniping(toast=True)
        
        if hasattr(self, 'token_input'):
            self.token_input.setText("")
        
        self.show_toast("Session Terminated", f"Your session has been terminated.\nReason: {reason}")
        QMessageBox.warning(
            self,
            "Session Terminated",
            f"Your session has been terminated from the dashboard.\n\nReason: {reason}"
        )
    
    def _schedule_websocket_pause_update(self, paused):
        if not hasattr(self, 'websocket_manager') or not self.websocket_manager:
            return
        try:
            result = self.websocket_manager.update_pause_status(paused)
            if asyncio.iscoroutine(result):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None

                if loop is not None:
                    loop.create_task(result)
                elif hasattr(self.websocket_manager, 'loop') and getattr(self.websocket_manager, 'loop') and self.websocket_manager.loop.is_running():
                    asyncio.run_coroutine_threadsafe(result, self.websocket_manager.loop)
                else:
                    asyncio.run(result)
        except Exception as e:
            logging.error(f"Error scheduling websocket pause status update: {e}")

    def _schedule_websocket_hide_setting_update(self):
        self.save_settings()
        if not hasattr(self, 'websocket_manager') or not self.websocket_manager:
            return
        try:
            result = self.websocket_manager.update_hide_setting(CONFIG_DATA["hide_from_board"])
            if asyncio.iscoroutine(result):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None

                if loop is not None:
                    loop.create_task(result)
                elif hasattr(self.websocket_manager, 'loop') and getattr(self.websocket_manager, 'loop') and self.websocket_manager.loop.is_running():
                    asyncio.run_coroutine_threadsafe(result, self.websocket_manager.loop)
                else:
                    asyncio.run(result)
        except Exception as e:
            logging.error(f"Error scheduling websocket hidden setting update: {e}")

    def check_pause_status(self):
        global sniper_paused, pause_end_time
        
        if sniper_paused and pause_end_time:
            if datetime.now() >= pause_end_time:
                self.unpause_sniper()

    def temporarily_pause_sniper(self, duration_seconds):
        global sniper_paused, pause_end_time
        try:
            duration_int = int(duration_seconds)
            pause_end_time = datetime.now() + timedelta(seconds=duration_int)
            sniper_paused = True
            
            logging.info(f"Sniper paused for {duration_int} seconds")
            
            self._schedule_websocket_pause_update(sniper_paused)
            
            self.status_label.setText(f"Status: Paused ({duration_int}s)")
            self.status_label.setStyleSheet("font-size: 14px; color: #FF9800;")
            self.start_btn.setText("Resume Sniping")
            
        except Exception as e:
            logging.error(f"Error in temporarily_pause_sniper: {e}")
            logging.error(f"Duration value received: {duration_seconds}, type: {type(duration_seconds)}")

    def unpause_sniper(self):
        global sniper_paused, pause_end_time
        if sniper_paused == False:
            logging.info("Sniper already running, skipping unpause")
            return
        
        sniper_paused = False
        pause_end_time = None
        
        if sniper_active:
            self.status_label.setText("Status: Running")
            self.status_label.setStyleSheet("font-size: 14px; color: #55ff55;")
            self.start_btn.setText("Stop Sniping")
            self.show_toast("Sniper Resumed", "Sniping has been resumed.")
            logging.info("Sniper Unpaused")
            self._schedule_websocket_pause_update(sniper_paused)
        else:
            self.status_label.setText("Status: Stopped")
            self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")

    def toggle_sniping(self):
        global sniper_active, sniper_paused
        if sniper_paused:
            self.unpause_sniper()
        elif sniper_active:
            self.stop_sniping(toast=True)
        else:
            self.start_sniping()

    def start_sniping(self):
        self.save_settings()
        self.load_settings()
        global sniper_active
        
        if not CONFIG_DATA["token"]:
            QMessageBox.warning(self, "Missing Token", "Please enter your Discord token!\n\nIf you have entered a Discord token, please attempt to start the sniper again.\nIf the issue persists, create a support thread in the Discord server. (NOT A TICKET!!)")
            return

        try:
            if hasattr(self, 'websocket_manager') and self.websocket_manager:
                self.websocket_manager.auth_failed = False
                self.websocket_manager.blacklisted = False
                if hasattr(self.websocket_manager, 'reset_auth_state'):
                    self.websocket_manager.reset_auth_state()
            
            self._showing_auth_error = False
            
            if hasattr(self, 'discord_client') and self.discord_client:
                self.stop_sniping(toast=False, wait_for_close=True)

            self.discord_client = DiscordClient(self)
            
            self.discord_thread = threading.Thread(
                target=self.run_discord_in_thread,
                daemon=True
            )
            self.discord_thread.start()

            self.status_label.setText("Status: Initializing")
            self.status_label.setStyleSheet("font-size: 14px; color: #F57736;")
            self.start_btn.setText("Stop Sniping")
            self.start_btn.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start sniper: {str(e)}")
            logging.error(f"Error starting sniper: {e}")
            self.start_btn.setEnabled(True)

    def stop_sniping(self, toast=False, wait_for_close=False):
        global sniper_active, sniper_paused
        sniper_paused = False

        if hasattr(self, 'websocket_manager') and self.websocket_manager:
            try:
                self.websocket_manager.running = False
                self.websocket_manager.stop()
                
                if wait_for_close:
                    time.sleep(0.2)
                
                self.websocket_manager = None
                logging.info("WebSocket manager stopped")
            except Exception as e:
                logging.error(f"Error stopping WebSocket manager: {e}")

        if hasattr(self, 'discord_client') and self.discord_client:
            try:
                if hasattr(self.discord_client, 'is_running'):
                    self.discord_client.is_running = False
                
                if wait_for_close and hasattr(self.discord_client, 'loop') and self.discord_client.loop:
                    try:
                        for task in asyncio.all_tasks(self.discord_client.loop):
                            task.cancel()
                    except:
                        pass
                    
                    future = asyncio.run_coroutine_threadsafe(self.discord_client.close(), self.discord_client.loop)
                    try:
                        future.result(timeout=2.0)
                    except:
                        pass
            except RuntimeError:
                pass
            except Exception as e:
                logging.error(f"Error stopping Discord client: {e}")
            finally:
                self.discord_client = None
        else:
            logging.info("No Discord client instance found to stop")

        sniper_active = False
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(True)
        logging.info("Sniper Stopped")
        
        if toast:
            self.show_toast("Sniper Stopped", "Sniping has been stopped.")

    @pyqtSlot(str)
    def _on_blacklisted(self, reason):
        QTimer.singleShot(0, lambda: self._show_blacklisted_dialog(reason))

    def _show_blacklisted_dialog(self, reason):
        msg = QMessageBox(self)
        msg.setWindowTitle("Sniper Stopped - Blacklisted")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(reason)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.stop_sniping(toast=False)

        global sniper_active, sniper_paused
        sniper_active = False
        sniper_paused = False

        self.status_label.setText("Status: Blacklisted")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(False)
        self.start_btn.setToolTip("You are blacklisted and cannot start the sniper")

        if hasattr(self, 'websocket_manager') and self.websocket_manager:
            try:
                self.websocket_manager.stop()
                self.websocket_manager = None
            except Exception as e:
                logging.error(f"Error stopping WebSocket manager on blacklist: {e}")

        msg.exec()

    def _format_blacklist_message(self, reason, expires_at):
        if not expires_at:
            return f"Your account has been blacklisted from using Sol Sniper.\n\nReason: {reason if reason else 'Unspecified'}\n\nYou may appeal by making a ticket in the Discord Server, found by clicking the Discord button in the bottom left."
        
        current_ts = time.time()
        remaining_seconds = expires_at - current_ts
        if remaining_seconds <= 0:
            expiry_text = "already expired"
            absolute_date = ""
        else:
            # round up to nearest minute
            remaining_minutes = int((remaining_seconds + 59) // 60)
            if remaining_minutes < 60:
                expiry_text = f"{remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
            elif remaining_minutes < 1440:  # less than 24 hours
                hours = (remaining_minutes + 59) // 60
                expiry_text = f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                days = (remaining_minutes + 1439) // 1440
                expiry_text = f"{days} day{'s' if days != 1 else ''}"
            
            unban_date = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S")
            absolute_date = f" (on {unban_date})"
        
        return (f"Your account has been blacklisted from using Sol Sniper.\n\n"
                f"Reason: {reason if reason else 'Unspecified'}\n"
                f"You will be unblacklisted in {expiry_text}{absolute_date}.\n\n"
                f"You may appeal by making a ticket in the Discord Server, found by clicking the Discord button in the bottom left.")

    def show_blacklisted_dialog(self, reason):
        self.blacklisted_signal.emit(reason)

    @pyqtSlot(str)
    def _on_kicked(self, reason):
        QTimer.singleShot(0, lambda: self._show_kicked_dialog(reason))

    def _show_kicked_dialog(self, reason):
        msg = QMessageBox(self)
        msg.setWindowTitle("Session Kicked")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(f"Your Sol Sniper session has been kicked offline.\n\nReason: {reason}")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        if sniper_active:
            self.stop_sniping(toast=False)

    def show_kicked_dialog(self, reason):
        self.kicked_signal.emit(reason)

    def show_auth_error_dialog(self, message):
        QTimer.singleShot(0, lambda: self._show_auth_error_message_box(message))

    def handle_server_maintenance(self, message):
        QTimer.singleShot(0, lambda: self._show_maintenance_dialog(message))

    def _show_maintenance_dialog(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Maintenance Mode")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(f"The server is under maintenance.\n\nReason: {message}\n\nThe sniper will stop.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        global sniper_active, sniper_paused
        sniper_active = False
        sniper_paused = False
        self.status_label.setText("Status: Stopped (Maintenance)")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(True)
        if hasattr(self, 'discord_client') and self.discord_client:
            try:
                if hasattr(self.discord_client, 'loop') and self.discord_client.loop and self.discord_client.loop.is_running():
                    asyncio.run_coroutine_threadsafe(self.discord_client.close(), self.discord_client.loop)
            except:
                pass
            self.discord_client = None
        if hasattr(self, 'websocket_manager'):
            self.websocket_manager = None
    
    def handle_version_blocked(self, message, required_version, download_url):
        QTimer.singleShot(0, lambda: self._show_version_blocked_dialog(message, required_version, download_url))

    def _show_version_blocked_dialog(self, message, required_version, download_url):
        msg = QMessageBox(self)
        msg.setWindowTitle("Version Blocked")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(f"Reason: {message}\n\nRequired version: {required_version}\n\nPlease update to continue.")
        if download_url:
            update_btn = msg.addButton("Download Update", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        msg.exec()
        if download_url and msg.clickedButton() == update_btn:
            webbrowser.open(download_url)

        global sniper_active, sniper_paused
        sniper_active = False
        sniper_paused = False
        self.status_label.setText("Status: Stopped (Version Blocked)")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(True)
        if hasattr(self, 'discord_client') and self.discord_client:
            try:
                if hasattr(self.discord_client, 'loop') and self.discord_client.loop and self.discord_client.loop.is_running():
                    asyncio.run_coroutine_threadsafe(self.discord_client.close(), self.discord_client.loop)
            except:
                pass
            self.discord_client = None
        if hasattr(self, 'websocket_manager'):
            self.websocket_manager = None

    def handle_auth_error(self, message):
        QTimer.singleShot(0, lambda: self._show_auth_error_dialog(message))

    def _show_auth_error_dialog(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Authentication Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(f"Authentication failed: {message}\n\nThe sniper will stop.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        global sniper_active, sniper_paused
        sniper_active = False
        sniper_paused = False
        self.status_label.setText("Status: Stopped (Auth Error)")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(True)
        if hasattr(self, 'discord_client') and self.discord_client:
            try:
                if hasattr(self.discord_client, 'loop') and self.discord_client.loop and self.discord_client.loop.is_running():
                    asyncio.run_coroutine_threadsafe(self.discord_client.close(), self.discord_client.loop)
            except:
                pass
            self.discord_client = None
        if hasattr(self, 'websocket_manager'):
            self.websocket_manager = None

    @pyqtSlot(str)
    def _on_auth_error(self, message):
        global sniper_active, sniper_paused
        
        if hasattr(self, '_showing_auth_error') and self._showing_auth_error:
            return
        
        self._showing_auth_error = True

        self.status_label.setText("Status: Stopped (Auth Failed)")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(True)

        if hasattr(self, 'discord_client') and self.discord_client:
            try:
                if hasattr(self.discord_client, 'loop') and self.discord_client.loop and self.discord_client.loop.is_running():
                    future = asyncio.run_coroutine_threadsafe(self.discord_client.close(), self.discord_client.loop)
                    try:
                        future.result(timeout=2.0)
                    except:
                        pass
            except RuntimeError:
                pass
            except Exception as e:
                logging.error(f"Error closing Discord client: {e}")
            finally:
                self.discord_client = None
        
        sniper_active = False
        sniper_paused = False
        
        QTimer.singleShot(0, lambda: self._show_auth_error_message_box(message))
        QTimer.singleShot(3000, lambda: setattr(self, '_showing_auth_error', False))

    def _show_auth_error_message_box(self, message):
        dialog = InputNoticeDialog(
            parent=self,
            title="Authentication Required",
            message=(
                "There was an error authenticating your sniper session.\n\n"
                "To automatically authenticate, press the 'Connect Sniper' button on the dashboard. "
                "If you have already done so, the authentication will happen automatically and this dialog will close.\n\n"
                "If automatic authentication does not work, you can paste your WebSocket token from the dashboard below.\n\n"
                "1. Click 'Go to Dashboard' below\n"
                "2. Sign in with your Discord account\n"
                "3. Click 'Connect Sniper' and then 'Copy Token'\n"
                "4. Paste the token below\n\n"
                "Error: " + message
            ),
            placeholder="Paste your token here...",
            accept_text="Submit",
            cancel_text="Cancel",
            show_dashboard_btn=True
        )
        self.auth_error_dialog = dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            token = dialog.get_value()
            if token:
                CONFIG_DATA["ws_token"] = token
                self.save_settings()
                if hasattr(self, 'websocket_manager') and self.websocket_manager:
                    self.websocket_manager.set_auth_token(token)
                self.show_notice("Token Saved", "WebSocket token saved. Click 'Start Sniping' to reconnect.", QMessageBox.Icon.Information)
                if hasattr(self, 'discord_client') and self.discord_client:
                    try:
                        if hasattr(self.discord_client, 'loop') and self.discord_client.loop and self.discord_client.loop.is_running():
                            future = asyncio.run_coroutine_threadsafe(self.discord_client.close(), self.discord_client.loop)
                            try:
                                future.result(timeout=2.0)
                            except:
                                pass
                    except:
                        pass
                    finally:
                        self.discord_client = None
                global sniper_active, sniper_paused
                sniper_active = False
                sniper_paused = False
        self.auth_error_dialog = None
        self._showing_auth_error = False

    def close_auth_error_dialog_if_open(self):
        if hasattr(self, 'auth_error_dialog') and self.auth_error_dialog is not None:
            try:
                self.auth_error_dialog.accept()
                self.auth_error_dialog = None
            except:
                pass

    def run_discord_in_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def start_discord_then_websocket():
            try:
                await self.discord_client.start(CONFIG_DATA["token"])
            except Exception as e:
                logging.error(f"Discord client error: {e}")
                if "Improper token has been passed" in str(e):
                    QTimer.singleShot(0, self.show_token_error)
                else:
                    QTimer.singleShot(0, self.update_status_error)
                QTimer.singleShot(0, self.stop_sniping)
        
        try:
            loop.run_until_complete(start_discord_then_websocket())
        except Exception as e:
            logging.error(f"Unexpected error in discord thread: {e}")
        finally:
            loop.close()

    def _discord_loop_exception_handler(self, loop, context):
        exception = context.get('exception')
        if exception:
            logging.error(f"Discord loop exception: {exception}")
            if "Authentication failed" in str(exception):
                QTimer.singleShot(0, lambda: self.show_auth_error_dialog(str(exception)))

    def show_token_error(self):
        QMessageBox.warning(
            self, 
            "Invalid Discord Token", 
            "Your Discord token is invalid.\nPlease follow the steps on the GitHub README to obtain a valid Discord Token."
        )

    def update_status_error(self):
        self.status_label.setText("Status: Error - Check Token")
        self.start_btn.setText("Start Sniping")
        self.start_btn.setEnabled(True)
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")

    async def run_discord_client(self):
        try:
            await self.discord_client.start(CONFIG_DATA["token"])
        except Exception as e:
            logging.error(f"Discord client error: {e}")
            if "Improper token has been passed" in str(e):
                QTimer.singleShot(0, lambda: QMessageBox.warning(
                    self, "Invalid Discord Token", 
                    "Your Discord token is invalid.\nPlease follow the steps on the GitHub README to obtain a valid Discord Token."
                ))
            elif "list index out of range" in str(e):
                QTimer.singleShot(0, lambda: QMessageBox.warning(
                    self, "Unexpected Error", 
                    "An unexpected error has occured. Please attempt to restart the sniper.\nIf the issue persists, create a support thread in the Discord server. (NOT A TICKET!!)"
                ))
            self.status_label.setText("Status: Error - Check Token")
            self.start_btn.setText("Start Sniping")
            self.start_btn.setEnabled(True)
            self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")

    def resizeEvent(self, event):
        if hasattr(self, 'bg_widget'):
            self.bg_widget.setGeometry(0, 0, self.width(), self.height())
        logging.info(f"Window resized to {self.width()}x{self.height()}")
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 12, 12)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        super().resizeEvent(event)

    def show_toast(self, title, message, guildid = None, channelid = None, messageid = None):
        if not CONFIG_DATA["toast_notifications"]:
            return
        
        if hasattr(self, '_current_toast_thread') and self._current_toast_thread:
            try:
                self._toast_cancel_flag = True
            except:
                pass
        
        def show_toast_thread():
            try:
                self._toast_cancel_flag = False
                
                if platform.system() == "Windows":
                    icon_path = str(SETTINGS_DIR / "snipercat.png")
                    beta_version_text = f" [BETA {BETA_VERSION}]" if IS_BETA_VERSION else ""
                    pre_release_text = f" [PRE-RELEASE {PRE_RELEASE_VERSION}]" if IS_PRE_RELEASE else ""
                    final_text = f"Sol Sniper V{CURRENT_VERSION.strip('.0')}{beta_version_text}{pre_release_text}"
                    
                    if getattr(self, '_toast_cancel_flag', False):
                        return
                    
                    result_queue = Queue()
                    
                    def toast_worker():
                        try:
                            if getattr(self, '_toast_cancel_flag', False):
                                return
                            toast(
                                title,
                                message,
                                icon=icon_path,
                                duration="short",
                                app_id=final_text,
                                button={'activationType': 'protocol', 'arguments': f'{'discord://' if CONFIG_DATA.get("use_discord_app") else "https://discord.com"}/channels/{guildid}/{channelid}/{messageid}', 'content': 'Jump to Message'} if guildid != None and channelid != None and messageid != None else None
                            )
                            result_queue.put(True)
                        except Exception as e:
                            result_queue.put(e)
                    
                    toast_thread = threading.Thread(target=toast_worker, daemon=True)
                    toast_thread.start()
                    toast_thread.join(timeout=5.0)
                    
                elif platform.system() == "Darwin":
                    if getattr(self, '_toast_cancel_flag', False):
                        return
                        
                    try:
                        script = f'''
                        display notification "{message}" with title "{title}" sound name "default"
                        '''
                        subprocess.run(['osascript', '-e', script], check=True)
                    except subprocess.CalledProcessError:
                        logging.info(f"Toast: {title} - {message}")
                else:
                    if getattr(self, '_toast_cancel_flag', False):
                        return
                        
                    logging.info(f"Toast: {title} - {message}")
                    
            except Exception as e:
                logging.error(f"Failed to show toast: {e}")
            finally:
                if hasattr(self, '_current_toast_thread'):
                    self._current_toast_thread = None
        
        self._current_toast_thread = threading.Thread(target=show_toast_thread, daemon=True)
        self._current_toast_thread.start()

    def show_dismissible_notice(self, title, message, notice_key):
        dismissed_notices = CONFIG_DATA.get("dismissed_notices", {})
        if dismissed_notices.get(notice_key, False):
            return True
        
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        
        dont_show_checkbox = QCheckBox("Don't show this again")
        msg.setCheckBox(dont_show_checkbox)
        
        proceed_btn = msg.addButton("Proceed", QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msg.setDefaultButton(cancel_btn)
        
        msg.exec()
        
        if dont_show_checkbox.isChecked():
            if "dismissed_notices" not in CONFIG_DATA:
                CONFIG_DATA["dismissed_notices"] = {}
            CONFIG_DATA["dismissed_notices"][notice_key] = True
            self.save_settings()
        
        return msg.clickedButton() == proceed_btn

    def show_notice(self, title, message, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(message)
        
        ok_btn = msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
        msg.setDefaultButton(ok_btn)
        
        msg.exec()
        
        return msg.clickedButton() == ok_btn

    def is_url_keyword(self, keyword):
        url_patterns = [
            "roblox.com",
            "join-rbx.vexsys.site",
            "ro.pro",
            "ropro.io"
        ]
        
        keyword_lower = keyword.lower()
        for pattern in url_patterns:
            if keyword_lower in pattern:
                return True
        return False


class DiscordClient(discord.Client):
    def __init__(self, main_window):
        super().__init__(
            chunk_guilds_at_startup=False,
            member_cache_flags=discord.MemberCacheFlags.none(),
            fetch_offline_members=False
        )
        self.main_window = main_window
        self.monitored_channels = self.load_monitored_channels()
        self.monitored_servers = self.load_monitored_servers()
        self.ready = False
        self.auth_failed = False

    def load_monitored_channels(self):
        channels = set()
        try:
            if SERVERS_FILE.exists():
                with open(SERVERS_FILE, 'r') as f:
                    servers = json.load(f)
                for server in servers:
                    if server.get('enabled', True):
                        for channel in server.get('channels', []):
                            channels.add(channel['id'])
        except Exception as e:
            logging.error(f"Error loading monitored channels: {e}")
        return channels

    def load_monitored_servers(self):
        servers = set()
        try:
            if SERVERS_FILE.exists():
                with open(SERVERS_FILE, 'r') as f:
                    server_data = json.load(f)
                for server in server_data:
                    if server.get('enabled', True):
                        servers.add(server['id'])
        except Exception as e:
            logging.error(f"Error loading monitored servers: {e}")
        return servers

    def reload_monitors(self):
        self.monitored_channels = self.load_monitored_channels()
        self.monitored_servers = self.load_monitored_servers()

    async def on_ready(self):
        if self.auth_failed:
            logging.warning("Not completing Discord ready due to WebSocket auth failure")
            return
        
        logging.info(f'Logged in as {self.user}')
        
        blacklisted, reason, expires_at = await self.main_window.init_websocket()
        message = self.main_window._format_blacklist_message(reason, expires_at)
        
        if blacklisted:
            self.main_window.show_blacklisted_dialog(message)
            await self.close()
            return
        
        if hasattr(self.main_window, 'websocket_manager') and self.main_window.websocket_manager:
            if self.main_window.websocket_manager.blacklisted:
                self.main_window.show_blacklisted_dialog(message)
                await self.close()
                return
            elif self.main_window.websocket_manager.auth_failed:
                self.main_window.show_auth_error_dialog("Invalid authentication token")
                await self.close()
                return
            
            await self.main_window.websocket_manager._send_user_connected()
        
        global sniper_active
        sniper_active = True
        self.main_window.status_label.setText("Status: Running")
        self.main_window.status_label.setStyleSheet("font-size: 14px; color: #55ff55;")
        self.main_window.start_btn.setEnabled(True)
        self.main_window.show_toast("Sniper Started", "Successfully connected to Discord and started sniper.")
        self.main_window.keyword_matcher = KeywordMatcher(KEYWORDS_FILE)
        self.main_window.keyword_matcher.update_categories(CONFIG_DATA)
        logging.info("Sniper Started")

    async def on_connect(self):
        logging.info("Connected to Gateway, waiting for ready...")

    async def on_error(self, event_method, *args, **kwargs):
        logging.error(f"Discord client error in {event_method}: args={args}, kwargs={kwargs}", exc_info=True)
        
        # dont let on_message handler errors crash the client
        if event_method == 'on_message':
            if args and len(args) > 0:
                message = args[0]
                logging.error(f"Failed to process message from {message.author if hasattr(message, 'author') else 'unknown'}")

    async def on_message(self, message):
        if not sniper_active or sniper_paused or self.main_window.is_processing:
            return
        
        try:
            channel_id = str(message.channel.id) if str(message.channel.id) else None
            guild_id = str(message.guild.id) if str(message.guild.id) else None
            
            if channel_id not in self.monitored_channels or guild_id not in self.monitored_servers:
                return
            
            content_lower = message.content.lower()
            if not any(url_indicator in content_lower for url_indicator in ['roblox', 'ro.pro', 'ropro', 'join-rbx', 'https', 'http']):
                if not message.embeds:
                    return
            
            embeds_data = []
            if message.embeds:
                for embed in message.embeds:
                    embed_dict = embed.to_dict()
                    embeds_data.append(embed_dict)
                
                if not embeds_data and not message.content:
                    return
            
            if CONFIG_DATA.get("ignore_messages_that_respond", False) and message.reference:
                logging.warning(f"Message {message.id} is replying, skipping")
                return
            
            asyncio.create_task(self.main_window.process_server_link(
                message.content if message.content else "", 
                embeds=embeds_data if message.author.bot else None, 
                discord_user_id=self.user.id, 
                discord_channel_id=message.channel.id, 
                discord_server_id=message.guild.id, 
                discord_message_id=message.id, 
                avatar_url=self.user.display_avatar.url,
                message=message
            ))
        except Exception as e:
            logging.error(f"Error in on_message handler: {e}", exc_info=True)


def get_embedded_user_data():
    try:
        exe_path = sys.executable
        with open(exe_path, 'rb') as f:
            data = f.read()
        
        marker_start = b"SLSNPRDAT_START<<<"
        marker_end = b">>>SLSNPRDAT_END"
        
        start = data.find(marker_start)
        if start != -1:
            start += len(marker_start)
            end = data.find(marker_end, start)
            if end != -1:
                encoded_data = data[start:end].decode()
                decoded = base64.b64decode(encoded_data).decode('utf-8')
                return json.loads(decoded)
    except:
        pass
    return {}

class WebsocketManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.websocket = None
        self.running = False
        self.reconnect_delay = 5
        self.max_reconnect_delay = 60
        self.current_reconnect_delay = 5
        self.ping_interval = 30
        self.last_pong_time = 0
        self.server_url = "wss://solsniper.vexsys.site/ws"
        self.loop = None
        self.thread = None
        self.ping_task = None
        self._original_process_server_link = None
        self.current_user = None
        self.reconnect_attempts = 0
        self.hide_from_board = False
        self.blacklisted = False
        self.blacklist_reason = None
        self.auth_failed = False
        self.auth_event = None
        self.auth_result = (False, None)
        self.main_window.load_settings()

    def get_user_info_for_websocket(self):
        embedded = get_embedded_user_data()
        return {
            "user_id": embedded.get("user_id"),
            "username": embedded.get("username"),
            "download_time": embedded.get("download_time"),
            "download_id": embedded.get("download_id")
        }

    async def start(self):
        if self.running:
            return False, None, 0
        self.running = True
        self.current_reconnect_delay = 5
        self.reconnect_attempts = 0
        self.auth_failed = False
        self.blacklisted = False
        self._patch_process_server_link()
        
        if hasattr(self, 'auth_token') and self.auth_token:
            pass
        else:
            self.auth_token = CONFIG_DATA.get("token", "")
        
        self.auth_event = asyncio.Event()
        self.auth_result = (False, None, 0)
        
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        try:
            await asyncio.wait_for(self.auth_event.wait(), timeout=20.0)
        except asyncio.TimeoutError:
            logging.error("WebSocket auth timeout")
            self.running = False
            return False, None, 0
        
        return self.auth_result

    def stop(self):
        self.running = False
        self._unpatch_process_server_link()
        if self.websocket and self.loop:
            try:
                asyncio.run_coroutine_threadsafe(self._close(), self.loop)
            except:
                pass
        if self.ping_task and self.loop:
            try:
                self.ping_task.cancel()
            except:
                pass

    def _patch_process_server_link(self):
        if hasattr(self.main_window, 'process_server_link'):
            self._original_process_server_link = self.main_window.process_server_link
            
            async def patched_process_server_link(content, embeds=None, discord_user_id=None, discord_channel_id=None, discord_server_id=None, discord_message_id=None, avatar_url=None, message=None):
                result = await self._original_process_server_link(content, embeds, discord_user_id, discord_channel_id, discord_server_id, discord_message_id, avatar_url, message)
                
                matched_category = None
                success = False
                if result and isinstance(result, dict):
                    success = result.get('success', False)
                    matched_category = result.get('matched_category')
                
                if success and self.websocket is not None and not (hasattr(self.websocket, 'closed') and self.websocket.closed):
                    try:
                        username = "Unknown"
                        discriminator = "0"
                        if self.main_window.discord_client and self.main_window.discord_client.user:
                            username = self.main_window.discord_client.user.name
                            discriminator = self.main_window.discord_client.user.discriminator
                        
                        server_name = None
                        server_icon = None
                        channel_name = None
                        if discord_server_id and hasattr(self.main_window.discord_client, 'get_guild'):
                            guild = self.main_window.discord_client.get_guild(int(discord_server_id))
                            if guild:
                                server_name = guild.name
                                server_icon = guild.icon.key if guild.icon else None
                            if discord_channel_id:
                                channel = guild.get_channel(int(discord_channel_id)) if guild else None
                                if channel:
                                    channel_name = channel.name
                        
                        snipe_data = {
                            "type": "snipe_event",
                            "data": {
                                "user_id": str(discord_user_id) if discord_user_id else None,
                                "username": username,
                                "discriminator": discriminator,
                                "channel_id": str(discord_channel_id) if discord_channel_id else None,
                                "channel_name": channel_name,
                                "server_id": str(discord_server_id) if discord_server_id else None,
                                "server_name": server_name,
                                "server_icon": server_icon,
                                "message_id": str(discord_message_id) if discord_message_id else None,
                                "content_preview": content[:500] if content else "",
                                "full_content": content if content else "",
                                "timestamp": datetime.now().isoformat(),
                                "avatar_url": str(avatar_url) if avatar_url else None,
                                "category": matched_category
                            }
                        }
                        await self.websocket.send(json.dumps(snipe_data))
                    except Exception as e:
                        logging.error(f"Failed to send snipe event: {e}")
                
                return result
            
            self.main_window.process_server_link = patched_process_server_link

    def _unpatch_process_server_link(self):
        if self._original_process_server_link is not None:
            self.main_window.process_server_link = self._original_process_server_link
            self._original_process_server_link = None

    async def _close(self):
        if self.websocket:
            try:
                await self._send_user_disconnected()
                await self.websocket.close()
            except:
                pass

    def is_healthy(self):
        if not self.running:
            return False
        if self.websocket is None:
            return False
        try:
            if hasattr(self.websocket, 'closed') and self.websocket.closed:
                return False
            return True
        except:
            return False

    def _run_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_and_run())

    async def _send_user_connected(self):
        user = self.main_window.discord_client.user if self.main_window.discord_client else None
        if not user:
            logging.warning("Discord client not ready, user_connected will be sent later")
            asyncio.create_task(self._retry_send_user_connected())
            return False, None

        self.current_user = user

        try:
            avatar_url = None
            if getattr(user, "avatar", None) is not None:
                avatar_url = str(user.avatar)

            servers_data = []
            if hasattr(self.main_window, 'discord_client') and hasattr(self.main_window.discord_client, 'monitored_servers'):
                for server_id in self.main_window.discord_client.monitored_servers:
                    guild = self.main_window.discord_client.get_guild(int(server_id))
                    if guild:
                        servers_data.append({
                            "id": str(guild.id),
                            "name": guild.name,
                            "icon": guild.icon.key if guild.icon else None
                        })

            message = {
                "type": "user_connected",
                "data": {
                    "id": str(user.id),
                    "username": user.name,
                    "discriminator": user.discriminator,
                    "avatar_url": avatar_url,
                    "connected_at": datetime.now().isoformat(),
                    "version": self.main_window.RAW_VERSION_STR,
                    "servers": servers_data,
                    "hide_from_board": self.main_window.hide_from_board_cb.isChecked() if hasattr(self.main_window, 'hide_from_board_cb') else False,
                    "paused": False,
                    "total_snipes": 0,
                    "embedded_info": self.get_user_info_for_websocket()
                }
            }
            await self.websocket.send(json.dumps(message))
            logging.info(f"Successfully sent user_connected for {user.name}")
            return False, None
        except Exception as e:
            logging.error(f"Failed to send user_connected: {e}")
            return False, None

    async def _retry_send_user_connected(self):
        await asyncio.sleep(2)
        if self.websocket and not self.websocket.closed and self.main_window.discord_client and self.main_window.discord_client.user:
            await self._send_user_connected()

    async def _connect_and_run(self):
        while self.running:
            try:
                self.websocket = await websockets.connect(self.server_url)
                self.current_reconnect_delay = 5
                self.reconnect_attempts = 0

                auth_message = {
                    "type": "auth",
                    "token": self.get_auth_token()
                }
                await self.websocket.send(json.dumps(auth_message))

                auth_received = False
                auth_error = None
                blacklisted_reason = None

                while not auth_received and self.running:
                    try:
                        response = await asyncio.wait_for(self.websocket.recv(), timeout=10.0)
                        response_data = json.loads(response)
                        msg_type = response_data.get("type")

                        if msg_type == "auth_success":
                            self.auth_failed = False
                            self.auth_result = (False, None)
                            self.auth_event.set()
                            auth_received = True

                            if self.main_window.discord_client and self.main_window.discord_client.user:
                                self.current_user = self.main_window.discord_client.user
                                await self._send_user_connected()
                                logging.info("Sent user_connected after auth_success")
                        elif msg_type == "auth_error":
                            error_message = response_data.get('message', 'Authentication failed')
                            auth_error = error_message
                            auth_received = True
                        elif msg_type == "maintenance":
                            maintenance_message = response_data.get('message', 'System is under maintenance')
                            self.main_window.maintenance_signal.emit(maintenance_message)
                            self.running = False
                            self.auth_result = (False, None)
                            self.auth_event.set()
                            await self.websocket.close()
                            return
                        elif msg_type == "version_blocked":
                            message_text = response_data.get('message', 'Version not supported')
                            required_version = response_data.get('required_version', '')
                            download_url = response_data.get('download_url', '')
                            self.main_window.version_blocked_signal.emit(message_text, required_version, download_url)
                            self.running = False
                            self.auth_result = (False, None)
                            self.auth_event.set()
                            await self.websocket.close()
                            return
                        elif msg_type == "error":
                            error_message = response_data.get('message', 'An error occurred')
                            self.main_window.error_signal.emit(error_message)
                            self.running = False
                            self.auth_result = (False, None)
                            self.auth_event.set()
                            await self.websocket.close()
                            return
                        elif msg_type == "blacklisted":
                            reason = response_data.get("reason", "No reason provided")
                            expires_at = response_data.get("expires_at")
                            if expires_at:
                                try:
                                    expires_at = int(float(expires_at))
                                except (ValueError, TypeError):
                                    expires_at = None
                            else:
                                expires_at = None
                            self.auth_result = (True, reason, expires_at)
                            self.auth_event.set()
                            await self.websocket.close()
                            self.running = False
                            return
                        elif msg_type == "require_auth":
                            continue
                        else:
                            continue
                    except asyncio.TimeoutError:
                        auth_error = "Timeout waiting for authentication response"
                        auth_received = True
                    except Exception as e:
                        auth_error = str(e)
                        auth_received = True

                if auth_error:
                    logging.error(f"Authentication failed: {auth_error}")
                    self.running = False
                    self.auth_failed = True
                    self.auth_result = (False, None)
                    self.auth_event.set()
                    if hasattr(self, 'main_window') and self.main_window:
                        self.main_window.auth_error_signal.emit(auth_error)
                    await self.websocket.close()
                    return

                if blacklisted_reason:
                    self.blacklisted = True
                    self.blacklist_reason = blacklisted_reason
                    self.auth_result = (True, blacklisted_reason)
                    self.auth_event.set()
                    await self.websocket.close()
                    self.running = False
                    return

                self.ping_task = asyncio.create_task(self._heartbeat())
                await self._receive_messages()
            
            except websockets.exceptions.ConnectionClosed as e:
                logging.warning(f"WebSocket connection closed: {e.code} - {e.reason}")
                if self.running:
                    logging.info(f"Reconnecting in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    break

            except Exception as e:
                if self.running:
                    logging.error(f"WebSocket connection error: {e}")
                    self.reconnect_attempts += 1
                    delay = min(self.current_reconnect_delay * (2 ** self.reconnect_attempts), self.max_reconnect_delay)
                    await asyncio.sleep(delay)
                else:
                    break

    async def _send_user_disconnected(self):
        try:
            if self.current_user:
                message = {
                    "type": "user_disconnected",
                    "data": {
                        "id": str(self.current_user.id),
                        "username": self.current_user.name,
                        "discriminator": self.current_user.discriminator
                    }
                }
                await self.websocket.send(json.dumps(message))
        except Exception as e:
            logging.error(f"Failed to send user_disconnected: {e}")

    async def _heartbeat(self):
        while self.running and self.websocket and not (hasattr(self.websocket, 'closed') and self.websocket.closed):
            try:
                await self.websocket.send(json.dumps({
                    "type": "ping",
                    "timestamp": time.time()
                }))
                await asyncio.sleep(self.ping_interval)
            except Exception as e:
                logging.error(f"Heartbeat error: {e}")
                break

    async def _receive_messages(self):
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    logging.debug(f"Received message: {data}")
                    if data.get("type") == "pong":
                        logging.debug("Received pong message")
                    elif data.get("type") == "blacklisted":
                        reason = data.get("reason", "No reason provided")
                        expires_at = data.get("expires_at")
                        if expires_at:
                            try:
                                expires_at = int(float(expires_at))
                            except (ValueError, TypeError):
                                expires_at = None
                        else:
                            expires_at = None
                        logging.warning(f"BLACKLISTED: {reason}, expires {expires_at}")
                        message = self.main_window._format_blacklist_message(reason, expires_at)
                        self.main_window.blacklisted_signal.emit(message)
                        self.auth_result = (True, reason, expires_at)
                        if self.auth_event:
                            self.auth_event.set()
                        await self.websocket.close()
                        self.running = False
                        return
                    elif data.get("type") == "kicked":
                        reason = data.get("reason", "No reason provided")
                        logging.warning(f"Kicked from server: {reason}")
                        self.main_window.kicked_signal.emit(reason)
                        self.main_window.stop_sniping(toast=False)
                        self.running = False
                        await self.websocket.close()
                        break
                    elif data.get("type") == "auth_error":
                        message_text = data.get("message", "Authentication error")
                        logging.error(f"Authentication error: {message_text}")
                        self.auth_failed = True
                        self.auth_result = (False, message_text, None)
                        if self.auth_event:
                            self.auth_event.set()
                        self.main_window.auth_error_signal.emit(message_text)
                        self.running = False
                        await self.websocket.close()
                        break
                    elif data.get("type") == "auth_success":
                        self.auth_failed = False
                        self.auth_result = (False, None, None)
                        if self.auth_event:
                            self.auth_event.set()
                    elif data.get("type") == "maintenance":
                        message_text = data.get("message", "System is under maintenance")
                        logging.info(f"Maintenance mode activated: {message_text}")
                        self.main_window.maintenance_signal.emit(message_text)
                        self.running = False
                        await self.websocket.close()
                        break
                    elif data.get("type") == "version_blocked":
                        message_text = data.get("message", "Your version is no longer supported")
                        required_version = data.get("required_version", "")
                        download_url = data.get("download_url", "")
                        logging.error(f"Version blocked: {message_text}")
                        self.main_window.version_blocked_signal.emit(message_text, required_version, download_url)
                        self.running = False
                        await self.websocket.close()
                        break
                    elif data.get("type") == "error":
                        error_message = data.get("message", "An error occurred")
                        logging.error(f"Error occurred: {error_message}")
                        self.main_window.error_signal.emit(error_message)
                        self.running = False
                        self.auth_result = (False, error_message, None)
                        if self.auth_event:
                            self.auth_event.set()
                        await self.websocket.close()
                        return
                except json.JSONDecodeError:
                    logging.error("Error decoding JSON message")
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
        except websockets.exceptions.ConnectionClosed as e:
            logging.warning(f"WebSocket connection closed: {e}")
        except Exception as e:
            logging.error(f"Receive error: {e}")
        finally:
            if self.running and self.websocket:
                await self._send_user_disconnected()

    async def update_hide_setting(self, hide):
        try:
            self.hide_from_board = hide
            if self.websocket and not (hasattr(self.websocket, 'closed') and self.websocket.closed) and self.current_user:
                message = {
                    "type": "update_hide_setting",
                    "data": {
                        "user_id": str(self.current_user.id),
                        "hide": hide
                    }
                }
                await self.websocket.send(json.dumps(message))
        except Exception as e:
            logging.error(f"Failed to send hide setting update: {e}")

    async def update_pause_status(self, paused):
        try:
            if self.websocket and not (hasattr(self.websocket, 'closed') and self.websocket.closed) and self.current_user:
                message = {
                    "type": "update_pause_status",
                    "data": {
                        "user_id": str(self.current_user.id),
                        "paused": paused
                    }
                }
                await self.websocket.send(json.dumps(message))
        except Exception as e:
            logging.error(f"Failed to update pause status: {e}")

    def set_auth_token(self, token):
        self.auth_token = token

    def get_auth_token(self):
        if hasattr(self, 'auth_token') and self.auth_token:
            return self.auth_token
        if hasattr(self, 'main_window'):
            return self.main_window.getWSToken()
        return ""

    def handle_auth_url(self, url):
        logging.info(f"Handling auth URL: {url}")
        parsed = urlparse(url)
        if parsed.scheme == "solsniper" and parsed.path == "/auth":
            params = parse_qs(parsed.query)
            token = params.get("token", [None])[0]
            if token:
                self.set_auth_token(token)
                return True
        return False

    def reset_auth_state(self):
        self.auth_failed = False
        self.blacklisted = False
        self.blacklist_reason = None
        self.reconnect_attempts = 0
        self.current_reconnect_delay = 5

    def set_server_url(self, url):
        self.server_url = url


if __name__ == "__main__":
    register_protocol()

    if len(sys.argv) > 1:
        if send_to_existing_instance(sys.argv[1:]):
            sys.exit(0)

    app = QApplication(sys.argv)
    setup_logging()
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(resource_path("snipercat.png")))
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 123, 255))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)
    
    font_path = str(SETTINGS_DIR / "font.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                app.setFont(QFont(font_families[0], 10))

    load_settings()
    
    global gradient_theme_persist
    gradient_theme_persist = CONFIG_DATA.get("gradient_theme", True)

    local_server = QLocalServer()
    if not local_server.listen(APP_NAME):
        if send_to_existing_instance(sys.argv[1:]):
            sys.exit(0)
        else:
            QLocalServer.removeServer(APP_NAME)
            local_server.listen(APP_NAME)

    def handle_new_connection():
        socket = local_server.nextPendingConnection()
        if socket and socket.waitForReadyRead(500):
            data = socket.readAll().data().decode("utf-8")
            try:
                msg = json.loads(data)
                argv = msg.get("argv", [])
                if argv and argv[0].startswith("solsniper://"):
                    url = argv[0]
                    logging.info(f"Handling protocol URL: {url}")
                    CONFIG_DATA["ws_token"] = url.split("token=")[-1]
                    if hasattr(window, 'websocket_manager') and window.websocket_manager:
                        window.websocket_manager.handle_auth_url(url)
                    save_settings()
                    window.close_auth_error_dialog_if_open()
                    window.show_notice("Sniper Connected", "Successfully authenticated sniper with dashboard. You can now close this notice.", QMessageBox.Icon.Information)
            except Exception as e:
                logging.error(f"Error processing incoming protocol message: {e}")
            socket.disconnectFromServer()
            socket.deleteLater()

    local_server.newConnection.connect(handle_new_connection)

    window = MainWindow()
    window.local_server = local_server
    window.hide()
    
    download_assets(window)
    
    font_path = str(SETTINGS_DIR / "font.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                app.setFont(QFont(font_families[0], 10))

    app.processEvents()
    window.show()

    if len(sys.argv) > 1 and sys.argv[1].startswith("solsniper://"):
        logging.info(f"Handling protocol URL: {sys.argv[1]}")
        CONFIG_DATA["ws_token"] = sys.argv[1].split("token=")[-1]
        window.save_settings()
        if hasattr(window, 'websocket_manager'):
            window.websocket_manager.handle_auth_url(sys.argv[1])
        window.show_notice("Sniper Connected", "Successfully authenticated sniper with dashboard. You can now close this notice.", QMessageBox.Icon.Information)

    sys.exit(app.exec())