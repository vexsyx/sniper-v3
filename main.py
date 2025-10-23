import sys
import os
import json
import configparser
import re
import time
import random
import requests
from requests import RequestException
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
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QStandardPaths, QRect, QPoint, QUrl, QEvent, QRectF, QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QFontDatabase, QPainter, QBrush, QPen, QLinearGradient, QPainterPath, QColor, QRegion, QTransform, QIntValidator
from PyQt6.QtSvgWidgets import QSvgWidget
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
if platform.system() == "Darwin":
    KEYBIND_SUPPORT = False
else:
    KEYBIND_SUPPORT = True
    import keyboard
if platform.system() == "Windows":
    from win11toast import toast
else:
    from desktop_notifier import DesktopNotifier
from queue import Queue

APP_NAME = "sol-sniper"
BASE_DIR = Path(os.getcwd())
SETTINGS_DIR = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)) / APP_NAME
SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

KEYWORDS_FILE = SETTINGS_DIR / "keywords.json"
SERVERS_FILE = SETTINGS_DIR / "servers.json"
CONFIG_FILE = SETTINGS_DIR / "sniper_config.ini"
DATA_FILE = SETTINGS_DIR / "currentKeyword.json"
LOGS_DIR = SETTINGS_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

ASSETS = {
    "snipercat.png": "https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/assets/snipercat.png",
    "yeswe.png": "https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/assets/yeswe.png",
    "pajamas.png": "https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/assets/pajamas.png",
    "font.ttf": "https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/assets/font.ttf",
    "vex.png": "https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/assets/vex.png"
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
EDIT_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#fff" class="bi bi-pencil-square" viewBox="0 0 16 16">
  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
</svg>"""

OYSTERDETECTOR_API_URL = "http://127.0.0.1:5005/OysterDetector"
MAXSTELLAR_API_URL = "http://127.0.0.1:5006/maxstellar"

PRIVATE_SERVER_PATTERN = re.compile(r'https://www\.roblox\.com/games/(\d+)/.+\?privateServerLinkCode=([\w-]+)')
SHARE_CODE_PATTERN = re.compile(r'https://www\.roblox\.com/share\?code=([a-f0-9]+)&type=Server')
DEEPLINK_PATTERN = re.compile(r'https://www\.roblox\.com/games/start\?placeId=(\d+)(?:&launchData=([^&]+))?')
URL_PATTERN = re.compile(r'(?P<url>https?://[^\s]+)')
GLITCHED_PATTERN = re.compile(
    r"\bg.{0,2}l.{0,2}(?:i.{0,2}t|t.{0,2}i).{0,2}c.{0,2}h[ed]*(?=\W|$)", 
    re.IGNORECASE
)
DREAM_PATTERN = re.compile(
    r"d.{0,2}r.{0,2}e{1,3}.{0,2}a.{0,2}m.{0,4}(?:space|scape|spce|scpae|s.?p.?a.?c.?e)(?=\W|$)", 
    re.IGNORECASE
)

IS_BETA_VERSION = True
CURRENT_VERSION = "3.0.0"
BETA_VERSION = 5
IS_PRE_RELEASE = False


config = configparser.ConfigParser()
url_pattern = re.compile(r'https?://[^\s]+')
game_pattern = r"https:\/\/www\.roblox\.com\/games\/(\d+)\/[^?]+\?privateServerLinkCode=(\d+)"
share_pattern = r"https:\/\/www\.roblox\.com\/share\?code=([a-f0-9]+)&type=([A-Za-z]+)"
timer_running = False
sniper_active = False
sniper_paused = False
pause_end_time = None

open_roblox_toggle = True
stop_sniper_toggle = True
toggle_sniper_toggle = True
open_roblox_key = '-'
stop_sniper_key = '['
toggle_sniper_key = "F4"
pause_duration = 120
glitchsniping = False
dreamsniping = False
jestersniping = False
voidcoinsniping = False
toast_notifications = True
advanced_mode = False
close_roblox_before_joining = False
leave_if_wrong_biome = True
minimize_other_windows = False
launch_protocol = "roblox://"
token = ""
roblox_cookie = ""
blockedUsers = []
stillbackground = False
gradient_theme = False
semi_transparent_background = False
processing_hotkey_assignment = False

executor = ThreadPoolExecutor(max_workers=4)
config_lock = Lock()

log_filename = datetime.now().strftime("%m-%d-%Y %H-%M-%S.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(LOGS_DIR / log_filename), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def download_assets():
    class AssetDownloadDialog(QDialog):
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

        def apply_rounded_corners(self):
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), 20, 20)
            region = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(region)
            
        def setup_ui(self):
            if stillbackground:
                self.bg_widget = StarryBackgroundStill(self)
            else:
                self.bg_widget = StarryBackground(self)
            self.bg_widget.setGeometry(0, 0, self.width(), int(self.height() * 1.25))
            
            layout = QVBoxLayout(self)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)
            
            title_bar = ModernTitleBar(self)
            title_bar.title.setText("Checking & Downloading Assets")
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
            if gradient_theme:
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
            
        def update_progress(self, asset_name, status, completed):
            self.progress_bar.setValue(completed)
            
            for i in range(2, 0, -1):
                self.history_labels[i].setText(self.history_labels[i-1].text())
                self.history_labels[i].setStyleSheet(f"font-size: {12 - i * 2}px; color: #888888;")
            
            status_color = "#e0e0e0" if status in ("Downloaded", "Updated", "Done") else "#888888"
            display_text = f"{asset_name} ({status})"
            self.history_labels[0].setText(display_text)
            self.history_labels[0].setStyleSheet(f"font-size: 12px; color: {status_color};")
            
            QApplication.processEvents()
            
        def show_error_message(self, failed_assets):
            error_dialog = QDialog(self)
            error_dialog.setWindowTitle("Failed Assets")
            error_dialog.setFixedSize(500, 438)
            error_dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            error_dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            
            if stillbackground:
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
            if gradient_theme:
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
                            self.update_progress(filename, status, completed)
                            completed += 1
                            continue
                        response.raise_for_status()
                        remote_bytes = response.content
                        with open(asset_path, "rb") as f:
                            local_bytes = f.read()
                            if local_bytes == remote_bytes:
                                status = "Done"
                                logging.info(f"Asset '{filename}' is up to date.")
                                self.update_progress(filename, status, completed)
                                completed += 1
                                continue
                        status = "Updated"
                        with open(asset_path, "wb") as f:
                            f.write(remote_bytes)
                        logging.info(f"Asset '{filename}' updated.")
                        self.update_progress(filename, status, completed)
                        completed += 1
                    else:
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        status = "Downloaded"
                        with open(asset_path, "wb") as f:
                            f.write(response.content)
                        logging.info(f"Asset '{filename}' downloaded.")
                        self.update_progress(filename, status, completed)
                        completed += 1
                except Exception as e:
                    status = "Failed"
                    self.failed_assets.append((filename, str(e)))
                    logging.error(f"Asset '{filename}' failed to download/update: {e}")
                    self.update_progress(filename, status, completed)
                    completed += 1
                    
            if self.failed_assets:
                self.show_error_message(self.failed_assets)
    
    download_dialog = AssetDownloadDialog()
    
    def download_task():
        completed = 0
        for filename, url in ASSETS.items():
            if download_dialog.download_canceled:
                logging.info("Asset download canceled by user")
                break
                
            asset_path = SETTINGS_DIR / filename
            status = ""
            try:
                if asset_path.exists():
                    response = requests.get(url, timeout=10)
                    if response.status_code in (403, 429):
                        status = "Rate-Limited"
                        download_dialog.failed_assets.append((filename, f"Rate-limited ({response.status_code})"))
                        logging.warning(f"Asset '{filename}' rate-limited with status {response.status_code}")
                        download_dialog.update_progress(filename, status, completed)
                        completed += 1
                        continue
                    response.raise_for_status()
                    remote_bytes = response.content
                    with open(asset_path, "rb") as f:
                        local_bytes = f.read()
                        if local_bytes == remote_bytes:
                            status = "Done"
                            logging.info(f"Asset '{filename}' is up to date.")
                            download_dialog.update_progress(filename, status, completed)
                            completed += 1
                            continue
                    status = "Updated"
                    with open(asset_path, "wb") as f:
                        f.write(remote_bytes)
                    logging.info(f"Asset '{filename}' updated.")
                    download_dialog.update_progress(filename, status, completed)
                    completed += 1
                else:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    status = "Downloaded"
                    with open(asset_path, "wb") as f:
                        f.write(response.content)
                    logging.info(f"Asset '{filename}' downloaded.")
                    download_dialog.update_progress(filename, status, completed)
                    completed += 1
            except Exception as e:
                status = "Failed"
                download_dialog.failed_assets.append((filename, str(e)))
                logging.error(f"Asset '{filename}' failed to download/update: {e}")
                download_dialog.update_progress(filename, status, completed)
                completed += 1
                
        if download_dialog.failed_assets and not download_dialog.download_canceled:
            QTimer.singleShot(100, lambda: download_dialog.show_error_message(download_dialog.failed_assets))
        
        if not download_dialog.download_canceled:
            QTimer.singleShot(500, download_dialog.close)
    
    download_thread = threading.Thread(target=download_task, daemon=True)
    download_thread.start()
    
    download_dialog.exec()
    
    if download_dialog.download_canceled:
        logging.info("Asset download was canceled, continuing with available assets")

def load_settings():
    global token, roblox_cookie, open_roblox_toggle, stop_sniper_toggle, toggle_sniper_toggle, open_roblox_key, stop_sniper_key, toggle_sniper_key
    global glitchsniping, dreamsniping, jestersniping, voidcoinsniping, leave_if_wrong_biome, close_roblox_before_joining, minimize_other_windows, launch_protocol, pause_duration
    global stillbackground, toast_notifications, semi_transparent_background
    global gradient_theme, advanced_mode

    try:
        if CONFIG_FILE.exists():
            config.read(CONFIG_FILE)
            token = config['sniping'].get('token', '')
            roblox_cookie = config['sniping'].get('roblox_cookie', '')
            glitchsniping = config['sniping'].get('glitchsniping', "False") == "True"
            dreamsniping = config['sniping'].get('dreamsniping', "False") == "True"
            jestersniping = config['sniping'].get('jestersniping', "False") == "True"
            voidcoinsniping = config['sniping'].get('voidcoinsniping', "False") == "True"
            close_roblox_before_joining = config['sniping'].get('close_roblox_before_joining', "False") == "True"
            leave_if_wrong_biome = config['sniping'].get('leave_if_wrong_biome', "True") == "True"
            minimize_other_windows = config['sniping'].get('minimize_other_windows', "False") == "True"
            launch_protocol = config['sniping'].get('launch_protocol', 'roblox://')
            pause_duration = int(config['sniping'].get('pause_duration', 120))
            open_roblox_toggle = config['Hotkeys'].get('open_roblox_toggle', "True") == "True"
            open_roblox_key = config["Hotkeys"].get('open_roblox', '-')
            stop_sniper_toggle = config['Hotkeys'].get('stop_sniper_toggle', "True") == "True"
            stop_sniper_key = config["Hotkeys"].get('stop_sniper', '[')
            toggle_sniper_toggle = config['Hotkeys'].get('toggle_sniper_toggle', "True") == "True"
            toggle_sniper_key = config["Hotkeys"].get('toggle_sniper', 'F4')
            toast_notifications = config['Settings'].get('toast_notifications', "True") == "True"
            stillbackground = config['Settings'].get('stillbackground', "False") == "True"
            semi_transparent_background = config['Settings'].get('semi_transparent_background', "False") == "True"
            gradient_theme = config['Settings'].get('gradient_theme', "False") == "True"
            advanced_mode = config['Settings'].get('advanced_mode', "False") == "True"
            
            if KEYWORDS_FILE.exists():
                with open(KEYWORDS_FILE, 'r') as f:
                    keywords_data = json.load(f)
                    custom_categories = keywords_data.get("custom_categories", [])
                    for category in custom_categories:
                        category_key = category.replace(" ", "_")
                        setting_name = f"customcat_{category_key}"
                        globals()[setting_name] = config['sniping'].get(setting_name, "False") == "True"
        else:
            config['sniping'] = {
                'glitchsniping': 'False',
                'dreamsniping': 'False',
                'jestersniping': 'False',
                'voidCoinsniping': 'False',
                'leave_if_wrong_biome': 'True',
                'minimize_other_windows': 'False',
                'launch_protocol': 'roblox://',
                'close_roblox_before_joining': 'False',
                'token': '',
                'roblox_cookie': '',
                'pause_duration': 120
            }
            config['Hotkeys'] = {
                'open_roblox': '-',
                'open_roblox_toggle': 'True',
                'stop_sniper': '[',
                'stop_sniper_toggle': 'True',
                'toggle_sniper': 'F4',
                'toggle_sniper_toggle': 'True'
            }
            config['Settings'] = {
                'toast_notifications': 'True',
                'stillbackground': 'False',
                'semi_transparent_background': 'False',
                'gradient_theme': 'False',
                'advanced_mode': 'False'
            }
            config['Beta'] = {}
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
    except KeyError:
        # if category doesnt exist, create it, if it does, skip it
        if 'sniping' not in config:
            config['sniping'] = {
                'glitchsniping': 'False',
                'dreamsniping': 'False',
                'jestersniping': 'False',
                'voidCoinsniping': 'False',
                'leave_if_wrong_biome': 'True',
                'minimize_other_windows': 'False',
                'launch_protocol': 'roblox://',
                'close_roblox_before_joining': 'False',
                'token': '',
                'roblox_cookie': '',
                'pause_duration': 120
            }
        if 'Hotkeys' not in config:
            config['Hotkeys'] = {
                'open_roblox': '-',
                'open_roblox_toggle': 'True',
                'stop_sniper': '[',
                'stop_sniper_toggle': 'True',
                'toggle_sniper': 'F4',
                'toggle_sniper_toggle': 'True'
            }
        if 'Settings' not in config:
            config['Settings'] = {
                'toast_notifications': 'True',
                'stillbackground': 'False',
                'semi_transparent_background': 'False',
                'gradient_theme': 'False',
                'advanced_mode': 'False'
            }
        if 'Beta' not in config:
            config['Beta'] = {}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)


def save_settings():
    config['sniping'] = {
        'glitchsniping': str(glitchsniping),
        'dreamsniping': str(dreamsniping),
        'jestersniping': str(jestersniping),
        'voidCoinsniping': str(voidcoinsniping),
        'leave_if_wrong_biome': str(leave_if_wrong_biome),
        'minimize_other_windows': str(minimize_other_windows),
        'launch_protocol': str(launch_protocol),
        'close_roblox_before_joining': str(close_roblox_before_joining),
        'token': str(token),
        'roblox_cookie': str(roblox_cookie),
        'pause_duration': int(pause_duration)
    }
    
    if KEYWORDS_FILE.exists():
        with open(KEYWORDS_FILE, 'r') as f:
            keywords_data = json.load(f)
            custom_categories = keywords_data.get("custom_categories", [])
            for category in custom_categories:
                category_key = category.replace(" ", "_")
                setting_name = f"customcat_{category_key}"
                config['sniping'][setting_name] = str(globals().get(setting_name, False))
    
    config['Hotkeys'] = {
        'open_roblox': open_roblox_key,
        'open_roblox_toggle': str(open_roblox_toggle),
        'stop_sniper': stop_sniper_key,
        'stop_sniper_toggle': str(stop_sniper_toggle),
        'toggle_sniper': toggle_sniper_key,
        'toggle_sniper_toggle': str(toggle_sniper_toggle)
    }
    config['Settings'] = {
        'toast_notifications': str(toast_notifications),
        'stillbackground': str(stillbackground),
        'semi_transparent_background': str(semi_transparent_background),
        'gradient_theme': str(gradient_theme),
        'advanced_mode': str(advanced_mode)
    }
    config['Beta'] = {}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

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
        for name in ("yeswe", "pajamas", "vex"):
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
        alpha = int(0.7 * 255) if semi_transparent_background == True else 255
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
        painter.fillRect(self.rect(), QColor(0, 0, 0, 255))
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
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        logo = QLabel()
        logo_pixmap = QPixmap(str(SETTINGS_DIR / "snipercat.png"))
        rounded = QPixmap(24, 24)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 24, 24, 6, 6)
        painter.setClipPath(path)
        scaled = logo_pixmap.scaled(24, 24, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        logo.setPixmap(rounded)
        logo.setStyleSheet("background-color: transparent;")
        logo.setCursor(Qt.CursorShape.ArrowCursor)
        if KEYBIND_SUPPORT:
            logo.mousePressEvent = lambda event: self.parent.open_snake_game()
        layout.addWidget(logo)

        beta_version_text = f" [BETA {BETA_VERSION}]" if IS_BETA_VERSION else ""
        pre_release_text = " [PRE-RELEASE]" if IS_PRE_RELEASE else ""
        self.title = QLabel(f"Sol Sniper V{CURRENT_VERSION.strip('.0')}{beta_version_text}{pre_release_text}")
        self.title.setStyleSheet("font-size: 14px; font-weight: 600; color: #e0e0e0; background-color: transparent;")
        layout.addWidget(self.title)
        
        layout.addStretch()
        
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
        layout.addWidget(self.min_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        
        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)
        self.setStyleSheet("background-color: #1a1a1a;")

class KeywordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyword Selection")
        self.setWindowIcon(QIcon(str(SETTINGS_DIR / "snipercat.png")))
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
                    keywords = json.load(f)
                    for kw in keywords:
                        item = QTreeWidgetItem(self.tree)
                        item.setText(0, kw['name'])
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            except:
                pass
        else:
            with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

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
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            keywords.append({
                "name": item.text(0),
                "ids": []
            })
        
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(keywords, f, indent=4)
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("Initializing MainWindow")
        beta_version_text = f" [BETA {BETA_VERSION}]" if IS_BETA_VERSION else ""
        pre_release_text = " [PRE-RELEASE]" if IS_PRE_RELEASE else ""
        self.setWindowTitle(f"Sol Sniper V{CURRENT_VERSION.strip('.0')}{beta_version_text}{pre_release_text}")
        self.setWindowIcon(QIcon(str(SETTINGS_DIR / "snipercat.png")))
        self.resize(1200, 800)
        self.setFixedSize(1200, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._current_toast_thread = None
        self._toast_cancel_flag = False

        if platform.system() == 'Darwin':
            self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
            font = self.font()
            font.setPointSize(font.pointSize() + 1)
            self.setFont(font)

        self.default_keywords = {
            "keywords": {
                "Glitched": [
                    "glitch",
                    "glig",
                    "404",
                    "4o4"
                ],
                "Dreamspace": [
                    "dream",
                    "scape",
                    "space"
                ],
                "Jester": [
                    "jest",
                    "obl",
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
                        "name": "others",
                        "id": "1282554696032194593"
                    },
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
        load_settings()
        global gradient_theme_persist
        gradient_theme_persist = gradient_theme
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("""
            QWidget {
                border-radius: 12px;
            }
        """)
        
        if stillbackground == False:
            self.bg_widget = StarryBackground(self.central_widget)
        elif stillbackground == True:
            self.bg_widget = StarryBackgroundStill(self.central_widget)
        self.bg_widget.setGeometry(0, 0, self.width(), self.height())

        self.drag_start_position = None
        self.initial_window_pos = None
        self.central_widget.setMouseTracking(True)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = ModernTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
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
        self.hotkeys_btn = self.create_sidebar_btn("Hotkeys")
        self.keywords_btn = self.create_sidebar_btn("Keywords")
        self.servers_btn = self.create_sidebar_btn("Servers")
        self.settings_btn = self.create_sidebar_btn("Miscellaneous")
        if IS_BETA_VERSION:
            self.beta_btn = self.create_sidebar_btn("Beta Features")
        self.credits_btn = self.create_sidebar_btn("Credits")
        self.discord_btn = self.create_sidebar_btn("Discord", svg=DISCORD_SVG, color="#5865F2", url="https://discord.gg/RPcPUp47YD")
        self.github_btn = self.create_sidebar_btn("GitHub", svg=GITHUB_SVG, color="#333", url="https://github.com/vexthecoder/sniper-v3")

        sidebar_layout.addWidget(self.sniper_btn)
        sidebar_layout.addWidget(self.hotkeys_btn)
        sidebar_layout.addWidget(self.keywords_btn)
        sidebar_layout.addWidget(self.servers_btn)
        sidebar_layout.addWidget(self.settings_btn)
        if IS_BETA_VERSION:
            sidebar_layout.addWidget(self.beta_btn)
        sidebar_layout.addWidget(self.credits_btn)
        sidebar_layout.addStretch()
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
        self.hotkeys_tab = self.create_hotkeys_tab()
        self.keywords_tab = self.create_keywords_tab()
        self.servers_tab = self.create_servers_tab()
        self.settings_tab = self.create_settings_tab()
        self.beta_tab = self.create_beta_tab()
        self.credits_tab = self.create_credits_tab()
        
        self.tab_widget.addTab(self.sniper_tab, "Sniper")
        self.tab_widget.addTab(self.hotkeys_tab, "Hotkeys")
        self.tab_widget.addTab(self.keywords_tab, "Keywords")
        self.tab_widget.addTab(self.servers_tab, "Servers")
        self.tab_widget.addTab(self.settings_tab, "Miscellaneous")
        if IS_BETA_VERSION:
            self.tab_widget.addTab(self.beta_tab, "Beta Features")
        self.tab_widget.addTab(self.credits_tab, "Credits")

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.tab_widget)
        main_layout.addLayout(content_layout)
        
        self.setup_connections()
        self.setStyleSheet(self.get_stylesheet())
        self.load_keywords_data()

        self.is_processing = False
        self.hotkey_monitor_running = False
        self.csrf_token = None
        if not hasattr(self, 'hotkey_thread') or not self.hotkey_thread:
            self.hotkey_monitor_running = True
            self.hotkey_thread = threading.Thread(
                target=self.start_hotkey_monitor,
                daemon=True
            )
            self.hotkey_thread.start()
        logging.info("MainWindow initialized")

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

            if hasattr(self, 'bg_widget') and stillbackground == False:
                self.bg_widget.update_star_positions()
                
            event.accept()

    def moveEvent(self, event):
        super().moveEvent(event)
        if hasattr(self, 'bg_widget') and stillbackground == False:
            self.bg_widget.update_star_positions()

    def closeEvent(self, event):
        self.on_close()
        event.accept()

    def on_close(self):
        logging.info("Application closing - performing cleanup")
        
        if sniper_active:
            logging.info("Stopping sniper before closing")
            self.stop_sniping(toast=False)
        
        logging.info("Saving settings before closing")
        self.save_settings()
        
        if hasattr(self, 'hotkey_thread') and self.hotkey_thread:
            self.hotkey_monitor_running = False
            self.hotkey_thread = None
        
        logging.info("Cleanup completed")

    def handle_hotkeys(self):
        if KEYBIND_SUPPORT == False:
            return
        if processing_hotkey_assignment:
            return
        if open_roblox_toggle and keyboard.is_pressed(open_roblox_key):
            logging.info(f"Hotkey pressed: open_roblox_key={open_roblox_key}")
            self.launch_game(f"{launch_protocol}placeID=15532962292")
            time.sleep(0.5)

        if stop_sniper_toggle and keyboard.is_pressed(stop_sniper_key) and not sniper_paused:
            logging.info(f"Hotkey pressed: stop_sniper_key={stop_sniper_key}")
            self.temporarily_pause_sniper(pause_duration)
            time.sleep(0.5)

        if toggle_sniper_toggle and keyboard.is_pressed(toggle_sniper_key):
            logging.info(f"Hotkey pressed: toggle_sniper_key={toggle_sniper_key}")
            self.toggle_sniping()
            time.sleep(0.5)

    def start_hotkey_monitor(self):
        logging.info("Starting hotkey monitor thread")
        self.hotkey_monitor_running = True
        while self.hotkey_monitor_running:
            try:
                self.handle_hotkeys()
                time.sleep(0.1)
            except Exception as e:
                logging.error(f"Hotkey monitor error: {e}")

    def launch_game(self, uri):
        logging.info(f"Launching game with URI: {uri}")
        try:
            if platform.system() == 'Darwin':
                if close_roblox_before_joining:
                    self.kill_roblox_process()
                subprocess.Popen(['open', uri])
                logging.info(f"Launched Roblox with URI: {uri}")
            elif platform.system() == 'Windows':
                if close_roblox_before_joining:
                    self.kill_roblox_process()
                os.startfile(uri)
            else:
                logging.warning(f"Unsupported OS: {platform.system()}")
        except Exception as e:
            logging.error(f"Error launching game: {e}")

    async def is_roblox_running(self):
        logging.info("Checking if Roblox is running")
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if platform.system() == 'Windows':
                    if 'RobloxPlayer' in proc.info['name']:
                        logging.info(f"Roblox process found: {proc.info}")
                        return True, proc
                elif platform.system() == 'Darwin':
                    process_name = proc.info['name'].lower()
                    if 'roblox' in process_name:
                        logging.info(f"Roblox process found: {proc.info}")
                        return True, proc
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logging.warning(f"Process access error: {e}")
                continue
            await asyncio.sleep(0)
        logging.info("Roblox process not found")
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

    async def is_game_loaded(self, process):
        logging.info("Checking if game is loaded")
        
        roblox_version, _ = await self.get_roblox_version()
        if not roblox_version:
            logging.warning("Cannot determine Roblox version")
            return False
        
        log_dir = await self.get_log_directory(roblox_version)
        if not log_dir:
            logging.warning("Log directory not available")
            return False
        
        for attempt in range(30):
            latest_file, latest_time = await self.find_latest_log_file(log_dir)
            if not latest_file:
                await asyncio.sleep(2)
                continue
            
            try:
                with open(latest_file, 'r', encoding='utf-8', errors='ignore') as f:
                    logs = f.readlines()
                    
                for line in reversed(logs[-100:]):
                    if 'BloxstrapRPC' in line and 'SetRichPresence' in line and 'Sol\'s RNG' in line:
                        logging.info("Game loaded detected via rich presence log")
                        return True
                        
            except Exception as e:
                logging.error(f"Error reading log file on attempt {attempt}: {e}")
            
            await asyncio.sleep(2)
        
        logging.warning("Game load detection timeout")
        return False

    async def verify_biome_match(self, expected_category, detected_keyword):
        if not leave_if_wrong_biome or expected_category not in ["GLITCHED", "DREAMSPACE"]:
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
                            logging.debug("RichPresence line found but no biome info yet")
            except Exception as e:
                logging.error(f"Error reading log file on attempt {attempt + 1}: {e}")

            await asyncio.sleep(2)

        logging.warning("Biome detection timeout after 30 attempts")
        return None

    async def resolve_share_code(self, share_code):
        if roblox_cookie:
            csrf_token = await self.get_csrf_token()
            if not csrf_token:
                logging.error("Failed to get CSRF token for share code resolution")
                return await self.fallback_to_private_api(share_code)

            url = 'https://apis.roblox.com/sharelinks/v1/resolve-link'
            headers = {
                'Content-Type': 'application/json;charset=utf-8',
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://www.roblox.com',
                'Referer': 'https://www.roblox.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Cookie': f'.ROBLOSECURITY={roblox_cookie}',
                'x-csrf-token': csrf_token
            }

            data = {
                "linkId": share_code,
                "linkType": "Server"
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=data, headers=headers) as response:
                        if response.status == 200:
                            result = await response.json()
                            ps_data = result.get('privateServerInviteData', {})
                            return ps_data.get('placeId'), ps_data.get('privateServerLinkCode')
                        elif response.status == 403:
                            logging.warning("CSRF token expired, refreshing...")
                            self.csrf_token = None
                            return await self.resolve_share_code(share_code)
                        elif response.status == 401:
                            logging.error("Authentication failed - cookie is invalid or expired")
                            return await self.fallback_to_private_api(share_code)
                        else:
                            logging.error(f"Roblox API failed to resolve share code: {response.status}")
                            return await self.fallback_to_private_api(share_code)
            except Exception as e:
                logging.error(f"Error resolving share code with Roblox API: {e}")
                return await self.fallback_to_private_api(share_code)
        else:
            return await self.fallback_to_private_api(share_code)

    async def fallback_to_private_api(self, share_code):
        logging.info("Using private API for share code resolution")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'https://api-priv.nerdgpt.online/api/endpoints/roblox/resolve-link?linkId={share_code}') as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('placeId'), result.get('privateServerLinkCode')
                    else:
                        logging.error(f"Private API failed to resolve share code: {response.status}")
                        return None, None
        except Exception as e:
            logging.error(f"Error resolving share code with private API: {e}")
            return None, None

    async def get_csrf_token(self):
        if hasattr(self, 'csrf_token') and self.csrf_token:
            return self.csrf_token

        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.roblox.com',
            'Referer': 'https://www.roblox.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': f'.ROBLOSECURITY={roblox_cookie}'
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://auth.roblox.com/v2/logout', headers=headers) as response:
                    csrf_token = response.headers.get('x-csrf-token')
                    if csrf_token:
                        self.csrf_token = csrf_token
                        return csrf_token
                    else:
                        logging.error("Failed to get CSRF token from logout endpoint")
                        return None
        except Exception as e:
            logging.error(f"Error getting CSRF token: {e}")
            return None

    async def process_server_link(self, content, embeds=None):
        if self.is_processing:
            return

        self.is_processing = True
        game_id, private_code = None, None
        matched_category = None
        detected_keyword = None
        
        try:
            if embeds and isinstance(embeds, list):
                for embed in embeds:
                    if isinstance(embed, dict):
                        for key in ("title", "description"):
                            if key in embed and embed[key]:
                                content += f" {embed[key]}"
                        if "fields" in embed and isinstance(embed["fields"], list):
                            for field in embed["fields"]:
                                if "value" in field and field["value"]:
                                    content += f" {field['value']}"
            
            url_match = URL_PATTERN.search(content)
            if not url_match:
                self.is_processing = False
                return

            clean_content = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', content)
            clean_content = re.sub(r'[\u2000-\uFFFF]', '', clean_content)
            clean_content = clean_content.lower()
            logging.info(f"Processing content: {clean_content}")

            with open(KEYWORDS_FILE, 'r') as f:
                keywords_data = json.load(f)

            blacklisted = False
            for category in ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"] + keywords_data.get("custom_categories", []):
                if any(kw.lower() in clean_content for kw in keywords_data.get("blacklist", {}).get(category, [])):
                    blacklisted = True
                    break
            
            if blacklisted:
                self.is_processing = False
                return

            allowed = False
            categories_to_check = []
            
            if glitchsniping:
                categories_to_check.append("Glitched")
            if dreamsniping:
                categories_to_check.append("Dreamspace")
            if jestersniping:
                categories_to_check.append("Jester")
            if voidcoinsniping:
                categories_to_check.append("Void Coin")
            
            custom_categories = keywords_data.get("custom_categories", [])
            for custom_cat in custom_categories:
                custom_cat_stripped = custom_cat.replace(" ", "_")
                if globals().get(f"customcat_{custom_cat_stripped}", False):
                    categories_to_check.append(custom_cat)
            
            for category in categories_to_check:
                if allowed:
                    break
                   
                for kw in keywords_data.get("keywords", {}).get(category, []):
                    if kw.lower() in clean_content:
                        allowed = True
                        matched_category = category.upper()
                        logging.info(f"Matched keyword: {kw} in category {category}")
                        detected_keyword = kw
                        break
                
                if not allowed and category in keywords_data.get("regex", {}):
                    regex_data = keywords_data["regex"][category]
                    pattern = regex_data["pattern"]
                    flags = 0
                    if "i" in regex_data.get("flags", []):
                        flags |= re.IGNORECASE
                    if "m" in regex_data.get("flags", []):
                        flags |= re.MULTILINE
                    
                    try:
                        regex_pattern = re.compile(pattern, flags)
                        regex_match = regex_pattern.search(clean_content)
                        if regex_match:
                            allowed = True
                            matched_category = category.upper()
                            logging.info(f"Matched regex: {regex_match.group(0)} in category {category}")
                            detected_keyword = regex_match.group(0)
                            break
                    except re.error as e:
                        logging.error(f"Invalid regex pattern for category {category}: {e}")

            if not allowed:
                self.is_processing = False
                return
            
            if allowed and detected_keyword:
                toast_thread = threading.Thread(
                    target=lambda: self.show_toast("Keyword Matched", f"Matched: {detected_keyword}\nCategory: {matched_category}"),
                    daemon=True
                )
                toast_thread.start()
            
            if game_id and str(game_id) != "15532962292":
                logging.info(f"Invalid game ID detected: {game_id}.")
                self.is_processing = False
                return

            if url_match:
                url = url_match.group('url')
                if match := PRIVATE_SERVER_PATTERN.search(url):
                    game_id, private_code = match.groups()
                    uri = f"{launch_protocol}placeId={game_id}&linkCode={private_code}"
                    if str(game_id) != "15532962292" and game_id != None:
                        logging.info(f"Place ID mismatch: {game_id}")
                        self.is_processing = False
                        return
                    await asyncio.get_event_loop().run_in_executor(executor, self.launch_game, uri)
                    logging.info(f"Launching private server with game ID: {game_id} and code: {private_code}")
                elif match := SHARE_CODE_PATTERN.search(url):
                    share_code = match.group(1)
                    uri = f"{launch_protocol}navigation/share_links?code={share_code}&type=Server"
                    resolved_game_id, resolved_private_code = await self.resolve_share_code(share_code)
                    if resolved_game_id:
                        game_id = resolved_game_id
                    if str(game_id) != "15532962292" and game_id != None:
                        logging.info(f"Place ID mismatch: {game_id}")
                        self.is_processing = False
                        return
                    await asyncio.get_event_loop().run_in_executor(executor, self.launch_game, uri)
                    logging.info(f"Launching private server with game ID: {game_id} and code: {share_code}")
                elif match := DEEPLINK_PATTERN.search(url):
                    place_id, launch_data = match.groups()
                    uri = f"{launch_protocol}placeId={place_id}"
                    if launch_data:
                        uri += f"&launchData={launch_data}"
                    if str(game_id) != "15532962292" and game_id != None:
                        logging.info(f"Place ID mismatch: {game_id}")
                        self.is_processing = False
                        return
                    await asyncio.get_event_loop().run_in_executor(executor, self.launch_game, uri)
                    logging.info(f"Launching private server with game ID: {place_id} and launch data: {launch_data}")

            if matched_category in ["GLITCHED", "DREAMSPACE"]:
                self.stop_running_external_detectors()

            if minimize_other_windows == True:
                self.minimize_other_windows()
        
            roblox_running, roblox_process = await self.is_roblox_running()
            iterator = 0
            while not roblox_running and iterator < 50:
                iterator += 1
                await asyncio.sleep(.5)
                roblox_running, roblox_process = await self.is_roblox_running()
        
            if iterator >= 50:
                self.is_processing = False
                return

            toast_msg = (
                f"Successfully sniped!\n\nBiome: {matched_category}\nKeyword: {detected_keyword or 'Unknown'}"
                if matched_category in ["GLITCHED", "DREAMSPACE"]
                else f"Successfully sniped!\n\nCategory: {matched_category or 'Unknown'}\nKeyword: {detected_keyword or 'Unknown'}"
            )
            threading.Thread(
                target=lambda: self.show_toast("Successful Snipe", toast_msg),
                daemon=True
            ).start()

            if matched_category in ["GLITCHED", "DREAMSPACE"]:
                biome_match = await self.verify_biome_match(matched_category, detected_keyword)
                if not biome_match:
                    self.is_processing = False
                    return

        except Exception as e:
            logging.error(f"Error in process_server_link: {e}")
        finally:
            self.is_processing = False

    def minimize_other_windows(self):
        logging.info("Minimizing other windows")
        try:
            if platform.system() == 'Windows':
                import win32gui
                import win32con
                def enum_handler(hwnd, lParam):
                    if hwnd != self.winId() and win32gui.IsWindowVisible(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                win32gui.EnumWindows(enum_handler, None)
            elif platform.system() == 'Darwin':
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                    set allApps to every application process whose visible is true and background only is false
                    repeat with appProcess in allApps
                        set appName to name of appProcess
                        if appName is not frontApp and appName is not "Finder" and appName is not "Sol Sniper" then
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
                import win32gui
                import win32con
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

    def stop_running_external_detectors(self):
        self.toggle_oysterdetector_if_running()
        self.toggle_maxstellar_if_running()
    
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
        elif not icon and not svg and color == "#4a7bff" and not url and gradient_theme == True:
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
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Sniper Configuration")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        frame_layout.addWidget(title)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

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
            return row_widget

        base_categories_label = QLabel("Base Categories")
        base_categories_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #e0e0e0; margin-top: 10px; margin-bottom: 5px;")
        form_layout.addWidget(base_categories_label)

        self.glitch_cb = QCheckBox()
        self.glitch_cb.setChecked(glitchsniping)
        form_layout.addWidget(add_checkbox_row("Glitch Sniping", self.glitch_cb))

        self.dream_cb = QCheckBox()
        self.dream_cb.setChecked(dreamsniping)
        form_layout.addWidget(add_checkbox_row("Dreamspace Sniping", self.dream_cb))

        self.jester_cb = QCheckBox()
        self.jester_cb.setChecked(jestersniping)
        form_layout.addWidget(add_checkbox_row("Jester Sniping", self.jester_cb))

        self.void_cb = QCheckBox()
        self.void_cb.setChecked(voidcoinsniping)
        form_layout.addWidget(add_checkbox_row("Void Coin Sniping", self.void_cb))

        custom_categories = []
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, 'r') as f:
                    keywords_data = json.load(f)
                    custom_categories = keywords_data.get("custom_categories", [])
            except:
                pass

        self.custom_category_checkboxes = {}
        for category in custom_categories:
            cb = QCheckBox()
            setting_name = f"customcat_{category.replace(' ', '_')}"
            cb.setChecked(globals().get(setting_name, False))
            cb.setText(category)
            cb.setStyleSheet("font-size: 16px; color: #e0e0e0;")
            cb.stateChanged.connect(self.save_settings)
            self.custom_category_checkboxes[category] = cb
            form_layout.addWidget(cb)

        advanced_settings_label = QLabel("Advanced Settings")
        advanced_settings_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #e0e0e0; margin-top: 20px; margin-bottom: 5px;")
        form_layout.addWidget(advanced_settings_label)

        self.close_roblox_cb = QCheckBox()
        self.close_roblox_cb.setChecked(close_roblox_before_joining)
        form_layout.addWidget(add_checkbox_row("Close Roblox Before Joining a Snipe", self.close_roblox_cb))

        self.leave_biome_cb = QCheckBox()
        self.leave_biome_cb.setChecked(leave_if_wrong_biome)
        form_layout.addWidget(add_checkbox_row("Close Roblox if not Glitched/Dreamspace", self.leave_biome_cb))

        self.minimize_other_windows_cb = QCheckBox()
        self.minimize_other_windows_cb.setChecked(minimize_other_windows)
        form_layout.addWidget(add_checkbox_row("Minimize Other Windows on Snipe", self.minimize_other_windows_cb))
        
        frame_layout.addLayout(form_layout)

        protocol_label = QLabel("Launch Protocol")
        protocol_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #e0e0e0; margin-top: 20px; margin-bottom: 5px;")
        frame_layout.addWidget(protocol_label)

        protocol_layout = QHBoxLayout()
        protocol_layout.setSpacing(15)
        protocol_sublabel = QLabel("Protocol:")
        protocol_sublabel.setStyleSheet("font-size: 16px; color: #e0e0e0;")
        protocol_layout.addWidget(protocol_sublabel)
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems([
            "roblox://",
            "roblox-player://",
            "roblox-uwp-migration://"
        ])
        self.protocol_combo.setCurrentText(launch_protocol)
        protocol_layout.addWidget(self.protocol_combo)
        frame_layout.addLayout(protocol_layout)

        credentials_label = QLabel("Credentials")
        credentials_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #e0e0e0; margin-top: 20px; margin-bottom: 5px;")
        frame_layout.addWidget(credentials_label)

        token_layout = QHBoxLayout()
        token_layout.setSpacing(15)
        token_label = QLabel("Discord Token:")
        token_label.setStyleSheet("font-size: 16px; color: #e0e0e0;")
        token_layout.addWidget(token_label)
        self.token_input = QLineEdit()
        self.token_input.setText(token)
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("Enter your Discord token")
        token_layout.addWidget(self.token_input)
        frame_layout.addLayout(token_layout)

        cookie_layout = QHBoxLayout()
        cookie_layout.setSpacing(15)
        cookie_label = QLabel("Roblox Cookie:")
        cookie_label.setStyleSheet("font-size: 16px; color: #e0e0e0;")
        cookie_layout.addWidget(cookie_label)
        self.cookie_input = QLineEdit()
        self.cookie_input.setText(roblox_cookie)
        self.cookie_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.cookie_input.setPlaceholderText("Enter your Roblox .ROBLOSECURITY cookie")
        cookie_layout.addWidget(self.cookie_input)
        frame_layout.addLayout(cookie_layout)
        
        status_label = QLabel("Sniper Status")
        status_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #e0e0e0; margin-top: 20px; margin-bottom: 5px;")
        frame_layout.addWidget(status_label)
        
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        frame_layout.addWidget(self.status_label)
        
        self.start_btn = QPushButton("Start Sniping")
        self.start_btn.setFixedHeight(50)
        if gradient_theme == True:
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
        frame_layout.addWidget(self.start_btn)
        frame_layout.addStretch()

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setFixedHeight(45)
        if gradient_theme == True:
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
        frame_layout.addWidget(self.save_btn)
        
        layout.addWidget(frame)
        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        return scroll
    
    def save_settings_btn(self):
        self.save_settings()
        QMessageBox.information(self, "Success", "Settings saved successfully!")
    
    def create_hotkeys_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Hotkey Configuration")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        if KEYBIND_SUPPORT == False:
            warning_label = QLabel(" (Hotkey support is not available on this OS.)")
            warning_label.setStyleSheet("font-size: 14px; color: #ff5555;")
            title_layout = QHBoxLayout()
            title_layout.addWidget(title)
            title_layout.addWidget(warning_label)
            frame_layout.addLayout(title_layout)
        else:
            frame_layout.addWidget(title)

        hotkeys_layout = QVBoxLayout()
        hotkeys_layout.setSpacing(15)

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
                duration_label = QLabel("Duration (s):")
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
        self.hk1_cb.setChecked(open_roblox_toggle)
        hk1_row, self.hk1_display, self.hk1_assign_btn = create_hotkey_row(
            "Join Random Server", self.hk1_cb, "Key:", open_roblox_key
        )
        hotkeys_layout.addWidget(hk1_row)

        self.pause_duration_input = QLineEdit()
        self.pause_duration_input.setText(str(pause_duration))
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
        self.hk2_cb.setChecked(stop_sniper_toggle)
        hk2_row, self.hk2_display, self.hk2_assign_btn = create_hotkey_row(
            "Pause Sniper", self.hk2_cb, "Key:", stop_sniper_key, self.pause_duration_input
        )
        hotkeys_layout.addWidget(hk2_row)

        self.hk3_cb = QCheckBox()
        self.hk3_cb.setChecked(toggle_sniper_toggle)
        hk3_row, self.hk3_display, self.hk3_assign_btn = create_hotkey_row(
            "Toggle Sniper", self.hk3_cb, "Key:", toggle_sniper_key
        )
        hotkeys_layout.addWidget(hk3_row)

        if KEYBIND_SUPPORT == False:
            self.hk1_cb.setEnabled(False)
            self.hk1_assign_btn.setEnabled(False)
            self.hk2_cb.setEnabled(False)
            self.hk2_assign_btn.setEnabled(False)
            self.pause_duration_input.setEnabled(False)
            self.hk3_cb.setEnabled(False)
            self.hk3_assign_btn.setEnabled(False)

        frame_layout.addLayout(hotkeys_layout)

        self.assigning_hotkey = None
        self.hk1_assign_btn.clicked.connect(lambda: self.start_key_assignment(1))
        self.hk2_assign_btn.clicked.connect(lambda: self.start_key_assignment(2))
        self.hk3_assign_btn.clicked.connect(lambda: self.start_key_assignment(3))

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setFixedHeight(45)
        if gradient_theme == True:
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
        
        layout.addWidget(frame)
        layout.addStretch()
        return tab

    def start_key_assignment(self, hotkey_number):
        if not KEYBIND_SUPPORT:
            return

        global processing_hotkey_assignment
        processing_hotkey_assignment = True
        self.assigning_hotkey = hotkey_number
        
        if hotkey_number == 1:
            self.hk1_display.setText("Press any key...")
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
            self.hk2_display.setText("Press any key...")
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
            self.hk3_display.setText("Press any key...")
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
        
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if (self.assigning_hotkey and 
            event.type() == QEvent.Type.KeyPress and 
            not event.isAutoRepeat()):
            
            key = event.key()
            modifiers = event.modifiers()
            
            key_name = self.qt_key_to_keyboard_format(key, modifiers)
            
            if key_name:
                QTimer.singleShot(0, lambda: self.finish_key_assignment(key_name))
                return True
        
        return super().eventFilter(obj, event)

    def qt_key_to_keyboard_format(self, key, modifiers):
        key_map = {
            Qt.Key.Key_F1: "f1", Qt.Key.Key_F2: "f2", Qt.Key.Key_F3: "f3",
            Qt.Key.Key_F4: "f4", Qt.Key.Key_F5: "f5", Qt.Key.Key_F6: "f6",
            Qt.Key.Key_F7: "f7", Qt.Key.Key_F8: "f8", Qt.Key.Key_F9: "f9",
            Qt.Key.Key_F10: "f10", Qt.Key.Key_F11: "f11", Qt.Key.Key_F12: "f12",
            Qt.Key.Key_Space: "space", Qt.Key.Key_Tab: "tab",
            Qt.Key.Key_Backspace: "backspace", Qt.Key.Key_Return: "enter",
            Qt.Key.Key_Enter: "enter", Qt.Key.Key_Escape: "esc",
            Qt.Key.Key_Delete: "delete", Qt.Key.Key_Insert: "insert",
            Qt.Key.Key_Home: "home", Qt.Key.Key_End: "end",
            Qt.Key.Key_PageUp: "page up", Qt.Key.Key_PageDown: "page down",
            Qt.Key.Key_Up: "up", Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left", Qt.Key.Key_Right: "right",
        }
        
        if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
            key_name = chr(key).lower()
        elif Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            key_name = chr(key)
        elif key in key_map:
            key_name = key_map[key]
        else:
            return None
        
        modifier_parts = []
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            modifier_parts.append("ctrl")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            modifier_parts.append("alt")
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            modifier_parts.append("shift")
        if modifiers & Qt.KeyboardModifier.MetaModifier:
            modifier_parts.append("windows")
        
        if modifier_parts:
            return "+".join(modifier_parts + [key_name])
        else:
            return key_name
        
    def set_processing_hotkey_assignment(self, value):
        global processing_hotkey_assignment
        processing_hotkey_assignment = value

    def finish_key_assignment(self, key):
        global processing_hotkey_assignment
        
        if not self.assigning_hotkey:
            return

        hotkey_number = self.assigning_hotkey
        
        global open_roblox_key, stop_sniper_key, toggle_sniper_key
        
        if key:
            if hotkey_number == 1:
                open_roblox_key = key
                self.hk1_display.setText(str(key))
            elif hotkey_number == 2:
                stop_sniper_key = key
                self.hk2_display.setText(str(key))
            elif hotkey_number == 3:
                toggle_sniper_key = key
                self.hk3_display.setText(str(key))
        else:
            if hotkey_number == 1:
                self.hk1_display.setText(str(open_roblox_key))
            elif hotkey_number == 2:
                self.hk2_display.setText(str(stop_sniper_key))
            elif hotkey_number == 3:
                self.hk3_display.setText(str(toggle_sniper_key))
        
        self.hk1_assign_btn.setText("Assign")
        self.hk1_assign_btn.setEnabled(True)
        self.hk2_assign_btn.setText("Assign")
        self.hk2_assign_btn.setEnabled(True)
        self.hk3_assign_btn.setText("Assign")
        self.hk3_assign_btn.setEnabled(True)
        
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
        
        self.assigning_hotkey = None
        self.removeEventFilter(self)
        
        if key:
            self.save_settings()
            logging.info(f"Hotkey {hotkey_number} assigned to: {key}")
        
        time.sleep(1)
        self.set_processing_hotkey_assignment(False)
    
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
        if gradient_theme == True:
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
        if gradient_theme == True:
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
        self.keyword_table.setHorizontalHeaderLabels(["Glitched", "Dreamspace", "Jester", "Void Coin"])
        self.keyword_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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

        if advanced_mode == True:
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
            if gradient_theme == True:
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
            self.regex_table.setHorizontalHeaderLabels(["Glitched", "Dreamspace", "Jester", "Void Coin"])
            self.regex_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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
        if gradient_theme == True:
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
        self.blacklist_table.setHorizontalHeaderLabels(["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"])
        self.blacklist_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
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
        base_categories = ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"]
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
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
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
        base_categories = ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"]
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
            
            self.rebuild_tables_from_data(data)
            self.update_custom_cat_list(data)
            self.refresh_custom_categories()

    def refresh_custom_categories(self):
        if hasattr(self, 'custom_category_checkboxes'):
            for checkbox in self.custom_category_checkboxes.values():
                if checkbox.parent():
                    checkbox.parent().layout().removeWidget(checkbox)
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
        
        sniper_widget = self.sniper_tab.widget()
        form_layout = None
        for i in range(sniper_widget.layout().count()):
            item = sniper_widget.layout().itemAt(i)
            if isinstance(item.widget(), GradientFrame):
                frame = item.widget()
                for j in range(frame.layout().count()):
                    frame_item = frame.layout().itemAt(j)
                    if isinstance(frame_item, QVBoxLayout):
                        form_layout = frame_item
                        break
                if form_layout:
                    break

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
            return row_widget
        
        if form_layout and custom_categories:
            for i in range(form_layout.count()):
                item = form_layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), QLabel) and item.widget().text() == "Custom Categories":
                    form_layout.removeItem(item)
                    item.widget().deleteLater()
                    break
            
            custom_categories_label = QLabel("Custom Categories")
            custom_categories_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #e0e0e0; margin-top: 20px; margin-bottom: 5px;")
            form_layout.insertWidget(5, custom_categories_label)

            for i, category in enumerate(custom_categories):
                checkbox = QCheckBox()
                checkbox.setChecked(globals().get(f"customcat_{category.replace(' ', '_')}", False))
                checkbox.stateChanged.connect(lambda state, cat=category: self.update_custom_category_setting(cat, state))
                self.custom_category_checkboxes[category] = checkbox
                row_widget = add_checkbox_row(category, checkbox)
                form_layout.insertWidget(6 + i, row_widget)

    def update_custom_category_setting(self, category, state):
        setting_name = f"customcat_{category.replace(' ', '_')}"
        globals()[setting_name] = (state == Qt.CheckState.Checked.value)
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
            
            remove_btn = QPushButton("-")
            remove_btn.setFixedSize(20, 20)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background: #ff5555;
                    color: white;
                    border-radius: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #ff8888;
                }
            """)
            remove_btn.clicked.connect(lambda: self.remove_custom_category(category))
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
            
            self.rebuild_tables_from_data(data)
            self.update_custom_cat_list(data)
            self.refresh_custom_categories()

    def show_add_regex_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Custom RegEx")
        dlg.setModal(True)
        dlg.resize(480, 200)
        layout = QVBoxLayout(dlg)
        
        form = QFormLayout()
        category_combo = QComboBox()
        data = self.get_current_keyword_data()
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
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
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
        custom_categories = self.get_current_keyword_data().get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        if category not in all_categories:
            return
        
        col = all_categories.index(category)
        
        widget = QWidget()
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
        edit_btn.setFixedSize(20, 20)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a7bff;
                border-radius: 10px; /* perfect circle */
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #5a8bff;
            }
        """)

        svg = QSvgWidget(edit_btn)
        svg.load(QByteArray(EDIT_SVG))
        svg.setFixedSize(10, 10)
        svg.move((20 - 10) // 2, (20 - 10) // 2)

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
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
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
            self.keyword_table.setHorizontalHeaderItem(col, QTableWidgetItem(category))

        if advanced_mode and hasattr(self, 'regex_table'):
            current_regex_columns = self.regex_table.columnCount()
            needed_regex_columns = len(all_categories)
            
            if needed_regex_columns > current_regex_columns:
                for i in range(current_regex_columns, needed_regex_columns):
                    self.regex_table.insertColumn(i)
            elif needed_regex_columns < current_regex_columns:
                for i in range(current_regex_columns - 1, needed_regex_columns - 1, -1):
                    self.regex_table.removeColumn(i)
            
            for col, category in enumerate(all_categories):
                self.regex_table.setHorizontalHeaderItem(col, QTableWidgetItem(category))
        
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"]
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
            self.blacklist_table.setHorizontalHeaderItem(col, QTableWidgetItem(category))

    def rebuild_tables_from_data(self, data):
        self.update_table_headers_for_custom_categories(data)
        self.keyword_table.setRowCount(0)
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
        custom_categories = data.get("custom_categories", [])
        all_categories = base_categories + custom_categories
        
        max_rows = max(len(data["keywords"].get(cat, [])) for cat in all_categories)
        if max_rows > 0:
            self.keyword_table.setRowCount(max_rows)
        
        for col, cat in enumerate(all_categories):
            if col >= self.keyword_table.columnCount():
                self.keyword_table.insertColumn(col)
                self.keyword_table.setHorizontalHeaderItem(col, QTableWidgetItem(cat))
            
            keywords = data["keywords"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.keyword_table.rowCount():
                    self.keyword_table.insertRow(row)
                self.add_keyword_to_table_cell(row, col, kw)
        
        self.blacklist_table.setRowCount(0)
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"]
        bl_all_categories = bl_base_categories + custom_categories
        
        max_rows = max(len(data["blacklist"].get(cat, [])) for cat in bl_all_categories)
        if max_rows > 0:
            self.blacklist_table.setRowCount(max_rows)
        
        for col, cat in enumerate(bl_all_categories):
            if col >= self.blacklist_table.columnCount():
                self.blacklist_table.insertColumn(col)
                self.blacklist_table.setHorizontalHeaderItem(col, QTableWidgetItem(cat))
            
            keywords = data["blacklist"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.blacklist_table.rowCount():
                    self.blacklist_table.insertRow(row)
                self.add_blacklist_to_table_cell(row, col, kw)
        
        if advanced_mode and hasattr(self, 'regex_table'):
            self.regex_table.setRowCount(0)
            self.regex_table.setRowCount(1)
            
            if len(all_categories) != self.regex_table.columnCount():
                self.regex_table.setColumnCount(len(all_categories))
                self.regex_table.setHorizontalHeaderLabels(all_categories)
            
            for col, cat in enumerate(all_categories):
                regex_data = data.get("regex", {}).get(cat, {})
                if regex_data:
                    self.add_regex_to_table_cell(cat, regex_data.get("pattern", ""), regex_data.get("flags", []))
                else:
                    self.regex_table.setCellWidget(0, col, None)
        
        if hasattr(self, 'custom_cat_list'):
            self.update_custom_cat_list(data)
        
        self.save_keywords_data()

    def remove_keyword_from_table(self, row, col):
        widget = self.keyword_table.cellWidget(row, col)
        if widget:
            self.keyword_table.removeCellWidget(row, col)
        
        self.rebuild_keyword_table()

    def remove_blacklist_from_table(self, row, col):
        widget = self.blacklist_table.cellWidget(row, col)
        if widget:
            self.blacklist_table.removeCellWidget(row, col)
        
        self.rebuild_blacklist_table()

    def rebuild_keyword_table(self):
        data = self.get_current_keyword_data()
        
        self.keyword_table.setRowCount(0)
        
        categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
        
        max_rows = max(len(data["keywords"].get(cat, [])) for cat in categories)
        
        if max_rows > 0:
            self.keyword_table.setRowCount(max_rows)
        
        for col, cat in enumerate(categories):
            keywords = data["keywords"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.keyword_table.rowCount():
                    self.keyword_table.insertRow(row)
                self.add_keyword_to_table_cell(row, col, kw)
        
        self.save_keywords_data()

    def rebuild_blacklist_table(self):
        data = self.get_current_keyword_data()
        
        self.blacklist_table.setRowCount(0)
        
        categories = ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"]
        
        max_rows = max(len(data["blacklist"].get(cat, [])) for cat in categories)
        
        if max_rows > 0:
            self.blacklist_table.setRowCount(max_rows)
        
        for col, cat in enumerate(categories):
            keywords = data["blacklist"].get(cat, [])
            for row, kw in enumerate(keywords):
                if row >= self.blacklist_table.rowCount():
                    self.blacklist_table.insertRow(row)
                self.add_blacklist_to_table_cell(row, col, kw)
        
        self.save_keywords_data()

    def get_current_keyword_data(self):
        data = {"keywords": {}, "blacklist": {}, "regex": {}, "custom_categories": []}
        
        base_categories = ["Glitched", "Dreamspace", "Jester", "Void Coin"]
        custom_categories = []
        
        if hasattr(self, 'custom_cat_list'):
            for i in range(self.custom_cat_list.count()):
                item = self.custom_cat_list.item(i)
                if item:
                    widget = self.custom_cat_list.itemWidget(item)
                    if widget:
                        label = widget.findChild(QLabel)
                        if label and label.text().strip():
                            custom_categories.append(label.text().strip())
        
        all_categories = base_categories + custom_categories
        
        for col in range(self.keyword_table.columnCount()):
            if col < len(all_categories):
                cat = all_categories[col]
                keywords = []
                for row in range(self.keyword_table.rowCount()):
                    widget = self.keyword_table.cellWidget(row, col)
                    if widget:
                        label = widget.findChild(QLabel)
                        if label and label.text().strip():
                            keywords.append(label.text().strip())
                data["keywords"][cat] = keywords
        
        bl_base_categories = ["Global", "Glitched", "Dreamspace", "Jester", "Void Coin"]
        bl_all_categories = bl_base_categories + custom_categories
        
        for col in range(self.blacklist_table.columnCount()):
            if col < len(bl_all_categories):
                cat = bl_all_categories[col]
                keywords = []
                for row in range(self.blacklist_table.rowCount()):
                    widget = self.blacklist_table.cellWidget(row, col)
                    if widget:
                        label = widget.findChild(QLabel)
                        if label and label.text().strip():
                            keywords.append(label.text().strip())
                data["blacklist"][cat] = keywords
        
        if advanced_mode and hasattr(self, 'regex_table'):
            for col in range(self.regex_table.columnCount()):
                if col < len(all_categories):
                    cat = all_categories[col]
                    widget = self.regex_table.cellWidget(0, col)
                    if widget:
                        pattern_label = widget.findChild(QLabel)
                        if pattern_label and pattern_label.text().strip():
                            data["regex"][cat] = {
                                "pattern": pattern_label.toolTip(),
                                "flags": []
                            }
        
        data["custom_categories"] = custom_categories
        
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
        
        btn = QPushButton("-")
        btn.setFixedSize(20, 20)
        btn.setStyleSheet("""
            QPushButton {
                background: #ff5555;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ff8888;
            }
        """)
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
        
        btn = QPushButton("-")
        btn.setFixedSize(20, 20)
        btn.setStyleSheet("""
            QPushButton {
                background: #ff5555;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ff8888;
            }
        """)
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
                    
                    if "regex" in data:
                        for category, regex_data in data["regex"].items():
                            logging.info(f"Loaded regex for {category}: {regex_data.get('pattern', '')}")
                    
                    if "regex" not in data:
                        data["regex"] = {}
                    
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
                    
                    self.rebuild_tables_from_data(data)
                    self.refresh_custom_categories()
                    
            except Exception as e:
                logging.error(f"Error loading keywords: {e}")
                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                    default_data = {
                        "keywords": {
                            "Glitched": ["glitch", "glig", "404", "4o4"],
                            "Dreamspace": ["dream", "scape", "space"],
                            "Jester": ["jest", "obl", "obi"],
                            "Void Coin": ["void", "viod"]
                        },
                        "blacklist": {
                            "Global": ["bait", "fake", "aura", "chill", "stigma", "sol", "zero", "day", "dimensional"],
                            "Glitched": [],
                            "Dreamspace": [],
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
                            }
                        },
                        "custom_categories": []
                    }
                    json.dump(default_data, f)
                self.rebuild_tables_from_data(default_data)
                self.refresh_custom_categories()
        else:
            default_data = {
                "keywords": {
                    "Glitched": ["glitch", "glig", "404", "4o4"],
                    "Dreamspace": ["dream", "scape", "space"],
                    "Jester": ["jest", "obl", "obi"],
                    "Void Coin": ["void", "viod"]
                },
                "blacklist": {
                    "Global": ["bait", "fake", "aura", "chill", "stigma", "sol", "zero", "day", "dimensional"],
                    "Glitched": [],
                    "Dreamspace": [],
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

    def create_servers_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Server Management")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        frame_layout.addWidget(title)
        
        self.server_tree = QTreeWidget()
        self.server_tree.setHeaderLabels(["Server Name", "Server ID", "Channels"])
        self.server_tree.setColumnWidth(0, 200)
        self.server_tree.setColumnWidth(1, 150)
        self.server_tree.setColumnWidth(2, 450)
        self.server_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.server_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.server_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
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
        if gradient_theme == True:
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
        self.remove_btn_server = QPushButton("Remove Server")
        if gradient_theme == True:
            self.remove_btn_server.setStyleSheet("""
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
            self.remove_btn_server.setStyleSheet("""
                QPushButton {
                    background-color: #ff4a4a;
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #ff5a5a;
                }
            """)
        btn_layout.addWidget(self.add_btn_server)
        btn_layout.addWidget(self.remove_btn_server)
        btn_layout.addStretch()
        frame_layout.addLayout(btn_layout)
        frame_layout.addStretch()
        
        layout.addWidget(frame)
        layout.addStretch()
        
        self.add_btn_server.clicked.connect(self.show_add_server_dialog)
        self.remove_btn_server.clicked.connect(self.remove_server)
        self.load_servers()
        return tab

    def remove_server(self):
        item = self.server_tree.currentItem()
        if not item:
            return
            
        server_id = item.text(1)
        
        if not SERVERS_FILE.exists():
            return
            
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            servers = json.load(f)
        
        servers = [s for s in servers if s["id"] != server_id]
        
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4)
        
        self.load_servers()

    def show_add_server_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Server")
        dlg.setFixedSize(400, 150)
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
            "channels": []
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
        dlg.resize(500, 400)
        layout = QVBoxLayout(dlg)
        
        self.channels_table = QTableWidget()
        self.channels_table.setColumnCount(2)
        self.channels_table.setHorizontalHeaderLabels(["Channel Name", "Channel ID"])
        self.channels_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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
            row = self.channels_table.rowCount()
            self.channels_table.insertRow(row)
            name_item = QTableWidgetItem(channel["name"])
            id_item = QTableWidgetItem(channel["id"])
            name_item.setForeground(QColor("#ffffff"))
            id_item.setForeground(QColor("#ffffff"))
            name_item.setFlags(name_item.flags() | Qt.ItemFlag.ItemIsEditable)
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.channels_table.setItem(row, 0, name_item)
            self.channels_table.setItem(row, 1, id_item)

        add_btn = QPushButton("Add Channel")
        if gradient_theme == True:
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
                self.add_channel_to_table(name, cid)

    def add_channel_to_table(self, name, cid):
        row = self.channels_table.rowCount()
        self.channels_table.insertRow(row)
        
        name_item = QTableWidgetItem(name)
        id_item = QTableWidgetItem(cid)
        name_item.setForeground(QColor("#ffffff"))
        id_item.setForeground(QColor("#ffffff"))
        
        self.channels_table.setItem(row, 0, name_item)
        self.channels_table.setItem(row, 1, id_item)

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
            name = self.channels_table.item(row, 0).text()
            cid = self.channels_table.item(row, 1).text()
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
            item.setText(0, server["name"])
            item.setText(1, server["id"])
            item.setForeground(0, QBrush(QColor("#ffffff")))
            item.setForeground(1, QBrush(QColor("#ffffff")))
            
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
                    border-radius: 16px;
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

            self.server_tree.setItemWidget(item, 2, channels_widget)
            self.server_tree.addTopLevelItem(item)

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

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
        self.stillbackground_cb.setChecked(stillbackground)
        add_checkbox_row("Still Background (Performance Increase for the UI)", self.stillbackground_cb)

        self.semi_transparent_background_cb = QCheckBox()
        self.semi_transparent_background_cb.setChecked(semi_transparent_background)
        add_checkbox_row("Semi-Transparent UI Background", self.semi_transparent_background_cb)

        self.notify_cb = QCheckBox()
        self.notify_cb.setChecked(toast_notifications)
        add_checkbox_row("Toast Notifications", self.notify_cb)

        self.gradient_theme_cb = QCheckBox()
        self.gradient_theme_cb.setChecked(gradient_theme)
        add_checkbox_row("Gradient Theme", self.gradient_theme_cb)

        self.advanced_mode_note = QLabel("Enabling Advanced Mode will unlock additional settings and features intended for users who know what they're doing.\nPlease refrain from enabling this unless you understand the implications.")
        self.advanced_mode_note.setWordWrap(True)
        self.advanced_mode_note.setStyleSheet("font-size: 12px; color: #bbbbbb;")
        form_layout.addRow(self.advanced_mode_note)
        self.advanced_mode_cb = QCheckBox()
        self.advanced_mode_cb.setChecked(advanced_mode)
        self.advanced_mode_cb.stateChanged.connect(self.on_advanced_mode_changed)
        add_checkbox_row("Advanced Mode", self.advanced_mode_cb)

        frame_layout.addLayout(form_layout)

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setFixedHeight(45)
        if gradient_theme == True:
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
        
        layout.addWidget(frame)
        layout.addStretch()
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
                "• Custom RegEx Keyword Detections\n\n"
                "Are you sure you want to enable Advanced Mode?"
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
            container.setToolTip(f"🔗 @{username} - {platform_name}")
            
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

        yeswe_icons = [
            create_svg_icon(DISCORD_SVG, "https://discord.com/users/463575384961581066", "yeswe", "discord"),
            create_svg_icon(ROBLOX_SVG, "https://www.roblox.com/users/551612000/profile", "or472", "roblox"),
            create_svg_icon(GITHUB_SVG, "https://github.com/the2727", "the2727", "github"),
        ]
        yeswe_card = create_profile_card(
            SETTINGS_DIR / "yeswe.png", "yeswe", "  - No Quote Provided -  ", yeswe_icons
        )
        scroll_layout.addWidget(yeswe_card)

        pajamas_icons = [
            create_svg_icon(DISCORD_SVG, "https://discord.com/users/773604524573196298", "hxz0", "discord"),
            create_svg_icon(ROBLOX_SVG, "https://www.roblox.com/users/981817164/profile", "Detecel", "roblox"),
        ]
        pajamas_card = create_profile_card(
            SETTINGS_DIR / "pajamas.png", "PJ", "uhhm ok", pajamas_icons
        )
        scroll_layout.addWidget(pajamas_card)

        vex_icons = [
            create_svg_icon(DISCORD_SVG, "https://discord.com/users/1018875765565177976", "vex.rng", "discord"),
            create_svg_icon(ROBLOX_SVG, "https://www.roblox.com/users/682980257/profile", "vex_coder", "roblox"),
            create_svg_icon(GITHUB_SVG, "https://github.com/vexthecoder", "vexthecoder", "github"),
        ]
        vex_card = create_profile_card(
            SETTINGS_DIR / "vex.png", "vex", "yo: gurt", vex_icons
        )
        scroll_layout.addWidget(vex_card)

        donate_btn = QPushButton("Donate to yeswe/PJ")
        donate_btn.setFixedHeight(60)
        if gradient_theme == True:
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
        donate_btn.clicked.connect(lambda: webbrowser.open("https://www.roblox.com/games/121743595575824/donate#!/store"))
        scroll_layout.addWidget(donate_btn)

        donate_btn2 = QPushButton("Donate to vex")
        donate_btn2.setFixedHeight(60)
        if gradient_theme == True:
            donate_btn2.setStyleSheet("""
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
            donate_btn2.setStyleSheet("""
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
        donate_btn2.clicked.connect(lambda: webbrowser.open("https://www.roblox.com/games/17060128444/Aura-Game-Yes#!/store"))
        scroll_layout.addWidget(donate_btn2)

        scroll_layout.addStretch()
        scroll.setWidget(content)
        scroll.setStyleSheet("border-radius: 12px;")
        layout.addWidget(scroll)
        return tab

    def create_beta_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        frame = GradientFrame()
        frame.setStyleSheet("border-radius: 12px;")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Beta Features")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #e0e0e0;")
        title.setContentsMargins(0,0,0,20)
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

        no_beta_features_label = QLabel("There are currently no Beta Features available for testing.")
        no_beta_features_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #fff;
            }
        """)
        form_layout.addRow(no_beta_features_label)

        frame_layout.addLayout(form_layout)

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setFixedHeight(45)
        if gradient_theme == True:
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
        #frame_layout.addWidget(self.save_btn)
        
        layout.addWidget(frame)
        layout.addStretch()
        return tab
    
    def get_stylesheet(self):
        if gradient_theme == True:
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
        self.hotkeys_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        self.keywords_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        self.servers_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(3))
        self.settings_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(4))
        self.beta_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(5))
        self.credits_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(6))

        self.start_btn.clicked.connect(self.toggle_sniping)

        self.token_input.textChanged.connect(self.save_settings)
        self.cookie_input.textChanged.connect(self.save_settings)
        self.glitch_cb.stateChanged.connect(self.save_settings)
        self.dream_cb.stateChanged.connect(self.save_settings)
        self.jester_cb.stateChanged.connect(self.save_settings)
        self.void_cb.stateChanged.connect(self.save_settings)
        self.notify_cb.stateChanged.connect(self.save_settings)
        self.leave_biome_cb.stateChanged.connect(self.save_settings)
        self.close_roblox_cb.stateChanged.connect(self.save_settings)
        self.minimize_other_windows_cb.stateChanged.connect(self.save_settings)
        self.hk1_cb.stateChanged.connect(self.save_settings)
        self.hk2_cb.stateChanged.connect(self.save_settings)
        self.hk3_cb.stateChanged.connect(self.save_settings)
        self.stillbackground_cb.stateChanged.connect(self.save_settings)
        self.semi_transparent_background_cb.stateChanged.connect(self.save_settings)
        self.gradient_theme_cb.stateChanged.connect(self.save_settings)
        self.protocol_combo.currentTextChanged.connect(self.save_settings)
    
    def load_settings(self):
        if KEYWORDS_FILE.exists():
            try:
                with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                    keywords = json.load(f)
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
                        keywords = json.load(f)
                        if 0 <= row < len(keywords):
                            del keywords[row]
                            with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                                json.dump(keywords, f, indent=4)
                except:
                    pass
            else:
                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                    json.dump(self.default_keywords, f)

    def save_settings(self):
        global token, roblox_cookie, glitchsniping, dreamsniping, jestersniping, voidcoinsniping, toast_notifications, leave_if_wrong_biome, close_roblox_before_joining, minimize_other_windows, launch_protocol, advanced_mode
        global open_roblox_toggle, stop_sniper_toggle, toggle_sniper_toggle, open_roblox_key, stop_sniper_key, toggle_sniper_key, pause_duration
        global stillbackground, semi_transparent_background
        global gradient_theme
        
        token = self.token_input.text()
        roblox_cookie = self.cookie_input.text()
        glitchsniping = self.glitch_cb.isChecked()
        dreamsniping = self.dream_cb.isChecked()
        jestersniping = self.jester_cb.isChecked()
        voidcoinsniping = self.void_cb.isChecked()
        toast_notifications = self.notify_cb.isChecked()
        advanced_mode = self.advanced_mode_cb.isChecked()
        close_roblox_before_joining = self.close_roblox_cb.isChecked()
        leave_if_wrong_biome = self.leave_biome_cb.isChecked()
        minimize_other_windows = self.minimize_other_windows_cb.isChecked()
        launch_protocol = self.protocol_combo.currentText()
        open_roblox_toggle = self.hk1_cb.isChecked()
        stop_sniper_toggle = self.hk2_cb.isChecked()
        toggle_sniper_toggle = self.hk3_cb.isChecked()
        pause_duration = self.pause_duration_input.text()
        stillbackground = self.stillbackground_cb.isChecked()
        semi_transparent_background = self.semi_transparent_background_cb.isChecked()
        gradient_theme = self.gradient_theme_cb.isChecked()

        data = self.get_current_keyword_data()
        custom_categories = data.get("custom_categories", [])
        for category in custom_categories:
            checkbox = self.custom_category_checkboxes.get(category)
            if checkbox:
                globals()[f"customcat_{category}"] = checkbox.isChecked()

        save_settings()
        logging.info("Settings saved successfully")
    
    def temporarily_pause_sniper(self, duration=None):
        global sniper_paused, pause_end_time
        if sniper_active and not sniper_paused:
            if duration is None:
                duration = pause_duration
            
            sniper_paused = True
            pause_end_time = time.time() + duration
            
            self.status_label.setText(f"Status: Paused ({duration}s)")
            self.status_label.setStyleSheet("font-size: 14px; color: #ffff55;")
            self.start_btn.setText("Resume Sniping")
            
            logging.info(f"Sniper paused for {duration} seconds")
            self.show_toast("Sniper Paused", f"Sniping paused for {duration} seconds.")
            
            threading.Timer(duration, self.unpause_sniper).start()

    def unpause_sniper(self):
        global sniper_paused
        sniper_paused = False
        if sniper_active:
            self.status_label.setText("Status: Running")
            self.status_label.setStyleSheet("font-size: 14px; color: #55ff55;")
            self.start_btn.setText("Stop Sniping")
            self.show_toast("Sniper Resumed", "Sniping has been resumed.")
            logging.info("Sniper Unpaused")
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
        global sniper_active, token
        
        if not token:
            QMessageBox.warning(self, "Missing Token", "Please enter your Discord token!\n\nIf you have entered a Discord token, please attempt to start the sniper again.\nIf the issue persists, create a support thread in the Discord server. (NOT A TICKET!!)")
            return

        try:
            if hasattr(self, 'discord_client') and self.discord_client:
                self.stop_sniping(toast=False)

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
            logging.info("Sniper Initializing")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start sniper: {str(e)}")
            logging.error(f"Error starting sniper: {e}")

    def run_discord_in_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.discord_client.start(token))
        except Exception as e:
            logging.error(f"Discord client error: {e}")
            if "Improper token has been passed" in str(e):
                QTimer.singleShot(0, self.show_token_error)
            QTimer.singleShot(0, self.update_status_error)
        finally:
            if not loop.is_closed():
                loop.close()

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
            await self.discord_client.start(token)
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

    def stop_sniping(self, toast=False):
        global sniper_active, sniper_paused
        sniper_paused = False

        if hasattr(self, 'discord_client') and self.discord_client:
            try:
                if hasattr(self.discord_client, 'is_running'):
                    self.discord_client.is_running = False
                
                if hasattr(self, 'discord_loop') and self.discord_loop:
                    future = asyncio.run_coroutine_threadsafe(
                        self.discord_client.close(), 
                        self.discord_loop
                    )
                    future.result(timeout=5.0)
                    
            except Exception as e:
                logging.error(f"Error stopping Discord client: {e}")
                try:
                    if hasattr(self.discord_client, 'loop'):
                        self.discord_client.loop.call_soon_threadsafe(self.discord_client.loop.stop)
                except:
                    pass
        else:
            logging.info("No Discord client instance found to stop")

        sniper_active = False
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px; color: #ff5555;")
        self.start_btn.setText("Start Sniping")
        logging.info("Sniper Stopped")
        
        if toast:
            self.show_toast("Sniper Stopped", "Sniping has been stopped.")

    def resizeEvent(self, event):
        if hasattr(self, 'bg_widget'):
            self.bg_widget.setGeometry(0, 0, self.width(), self.height())
        logging.info(f"Window resized to {self.width()}x{self.height()}")
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 12, 12)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        super().resizeEvent(event)

    def get_oysterdetector_status(self):
        try:
            response = requests.get(
                f"{OYSTERDETECTOR_API_URL}/status",
                timeout=2
            )
            if response.status_code == 200:
                return response.json().get("running", False)
            return False
        except RequestException as e:
            logging.info(f"Oyster Detector not responding: {e}")
            return False
        except Exception as e:
            logging.error(f"Error checking detector status: {e}")
            return False
    
    def toggle_oysterdetector_if_running(self):
        if self.get_oysterdetector_status():
            try:
                response = requests.post(
                    f"{OYSTERDETECTOR_API_URL}/toggle",
                    json={"only_if": "running"},
                    timeout=2
                )
                if response.status_code == 200:
                    return response.json().get("success", False)
            except RequestException as e:
                logging.error(f"Error toggling detector: {e}")
        return False
    
    def get_maxstellar_status(self):
        try:
            response = requests.get(
                f"{MAXSTELLAR_API_URL}/status",
                timeout=2
            )
            if response.status_code == 200:
                return response.json().get("running", False)
            return False
        except RequestException as e:
            logging.info(f"Maxstellar not responding: {e}")
            return False
        except Exception as e:
            logging.error(f"Error checking detector status: {e}")
            return False

    def toggle_maxstellar_if_running(self):
        if self.get_maxstellar_status():
            try:
                response = requests.post(
                    f"{MAXSTELLAR_API_URL}/pause",
                    json={"only_if": "running"},
                    timeout=2
                )
                if response.status_code == 200:
                    return response.json().get("success", False)
            except RequestException as e:
                logging.error(f"Error toggling Max Stellar: {e}")
        return False

    def show_toast(self, title, message):
        if not toast_notifications:
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
                    pre_release_text = " [PRE-RELEASE]" if IS_PRE_RELEASE else ""
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
                                app_id=final_text
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
                        import subprocess
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

class DiscordClient(discord.Client):
    def __init__(self, main_window):
        super().__init__(
            chunk_guilds_at_startup=False, 
            member_cache_flags=discord.MemberCacheFlags.none()
        )
        self.main_window = main_window
        self.monitored_channels = self.load_monitored_channels()

    def load_monitored_channels(self):
        channels = set()
        try:
            if SERVERS_FILE.exists():
                with open(SERVERS_FILE, 'r') as f:
                    servers = json.load(f)
                for server in servers:
                    for channel in server.get('channels', []):
                        channels.add(channel['id'])
        except Exception as e:
            logging.error(f"Error loading monitored channels: {e}")
        return channels

    def reload_monitored_channels(self):
        self.monitored_channels = self.load_monitored_channels()

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        global sniper_active
        sniper_active = True
        self.main_window.status_label.setText("Status: Running")
        self.main_window.status_label.setStyleSheet("font-size: 14px; color: #55ff55;")
        self.main_window.start_btn.setEnabled(True)
        self.main_window.show_toast("Sniper Started", "Successfully connected to Discord and started sniper.")
        logging.info("Sniper Started")

    async def on_message(self, message):
        if not sniper_active or sniper_paused or self.main_window.is_processing:
            return

        self.reload_monitored_channels()

        if str(message.channel.id) not in self.monitored_channels:
            return

        if not message.content and not message.embeds:
            return

        embeds_data = []
        for embed in message.embeds:
            embed_dict = embed.to_dict()
            embeds_data.append(embed_dict)

        asyncio.create_task(self.main_window.process_server_link(message.content if message.content else "", embeds=embeds_data if message.author.bot else None))


if __name__ == "__main__":
    load_settings()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
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
    
    window = MainWindow()
    download_assets()
    window.show()
    
    sys.exit(app.exec())