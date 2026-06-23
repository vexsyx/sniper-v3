> [!NOTE]  
> This repository is actively maintained. Beta 7 is the latest release.

<div align="center">

<div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px;">
  <img src="https://raw.githubusercontent.com/vexsyx/sniper-v3/main/assets/snipercat.png" width="80" height="80" style="border-radius: 12px;">
  <div>
    <h1 style="margin: 0; font-size: 2.5em;">Sol Sniper V3</h1>
    <p style="margin: 5px 0 0 0; font-size: 1.2em; opacity: 0.8;">The Most Advanced Roblox Server Sniper for Sol's RNG</p>
  </div>
</div>

<div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin: 20px 0;">
  <a href="https://github.com/vexsyx/sniper-v3/releases">
    <img src="https://img.shields.io/github/v/release/vexsyx/sniper-v3?style=for-the-badge&logo=github&label=Latest%20Release&logoColor=white" alt="Latest Release">
  </a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/vexsyx/sniper-v3?style=for-the-badge&logo=nextdns&label=License&logoColor=white" alt="License"></a>
  <a href="https://python.org/downloads"><img src="https://img.shields.io/badge/Python-3.8+-ffd043?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows | macOS-2d2d2d?style=for-the-badge&logo=files&logoColor=white" alt="Platform"></a>
</div>

</div>

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [⚡ Features](#-features)
- [📥 Installation](#-installation)
- [🏗️ Standalone Executable](#️-standalone-executable)
- [🎮 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [⌨️ Hotkeys](#️-hotkeys)
- [🔧 Troubleshooting](#-troubleshooting)
- [🔨 Building from Source](#-building-from-source)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👥 Credits](#-credits)
- [💬 Support](#-support)

## 🌟 Overview

Sol Sniper V3 is a powerful, modern Sol's RNG based app specifically designed to snipe private servers. With its sleek interface and advanced detection, it automatically finds and joins private servers based on your customized keyword patterns, giving you the edge in sniping rare biomes and merchants.

---

## ⚡ Features

### 🎯 Detection
- Real-time Discord message monitoring
- Smart keyword system with RegEx support
- Multi-category support (Glitched, Dreamspace, Cyberspace, Singularity, Jester, Void Coin & custom)
- Per-category pause durations

### 🎨 Interface
- Modern gradient-themed UI
- Fully customizable hotkeys
- Toast notifications
- Performance modes

### 🔧 Advanced
- Account management (Windows only)
- Server & channel management
- Blacklist system
- Protocol override with version checking
- Import/Export for keywords and servers
- Custom link sniping (RoPro, JoinRBX, RoSeal, FishStrap)

---

## 📥 Installation

### 🎯 Quick Start (Recommended)

1. **Download** and **Run** the EXE from the [latest release](https://github.com/vexsyx/sniper-v3/releases/latest)
2. **Configure** the settings to your liking
3. **Start** the sniper

### 🐍 Python Version (🍎 MacOS)

```bash
git clone https://github.com/vexsyx/sniper-v3.git
cd sniper-v3
pip install -r requirements.txt
python main.py
```

---

## 🏗️ Standalone Executable

### 📦 One-Click Solution

**Benefits:**
- ✅ No Python installation required
- ✅ Single executable file
- ✅ Portable & sharable

**Download:** Grab the latest EXE from our [Releases](https://github.com/vexsyx/sniper-v3/releases)

---

## ⚙️ Configuration

### 🔧 Initial Setup

1. Enter your Discord token (Sniper tab)
2. Configure servers and channels (Servers tab)
3. Set up keywords and blacklists (Keywords tab)
4. Click "Start Sniping" (Sniper tab)

<details>
<summary><strong>🔐 Discord Token Extraction</strong></summary>

1. Visit [Discord Web Client](https://discord.com/app)
2. Log in and open Developer Tools (F12)
3. In Console tab, paste:

```javascript
window.webpackChunkdiscord_app.push([
	[Symbol()],
	{},
	req => {
		if (!req.c) return;
		for (let m of Object.values(req.c)) {
			try {
				if (!m.exports || m.exports === window) continue;
				if (m.exports?.getToken) return copy(m.exports.getToken());
				for (let ex in m.exports) {
					if (m.exports?.[ex]?.getToken && m.exports[ex][Symbol.toStringTag] !== 'IntlMessagesProxy') return copy(m.exports[ex].getToken());
				}
			} catch {}
		}
	},
]);

window.webpackChunkdiscord_app.pop();
console.log('%cSuccess!', 'font-size: 50px');
console.log(`%cYour token has been copied to your clipboard!`, 'font-size: 16px');
```

</details>

---

## ⌨️ Hotkeys

| Hotkey | Default | Action |
|--------|---------|--------|
| Join Random Server | `-` | Launches random Sol's RNG server |
| Pause Sniper | `[` | Temporary pause (configurable duration) |
| Toggle Sniper | `F4` | Enable/disable sniper |
| Loading Asset Skipper | `F5` | Skips loading assets (hold) |
| Main Menu Skipper | `F6` | Skips main menu (hold) |

**Customization:** Navigate to Miscellaneous tab → Click "Assign" → Press desired key combination → Save.

---

## 🎮 Usage

1. Launch and configure credentials
2. Set up servers, keywords, and blacklist
3. Click "Start Sniping"
4. App auto-detects server links in channels/servers you have set up and have access to and launches Roblox
5. Desktop notifications alert you to successful snipes

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **App won't start** | Check Python 3.8+ or re-download EXE |
| **No detections** | Verify token and server configuration, as well as checking if you have access to that channel |
| **Roblox not launching** | Ensure Roblox is installed and protocol is set correctly, we recommend you use the [Web Version](https://roblox.com/download) of Roblox as it works better |
| **Performance issues** | Enable "Still Background" in the Miscellaneous tab |

**Getting Help:**
- Check [Issues](https://github.com/vexsyx/sniper-v3/issues)
- Join [Discord Community](https://discord.gg/solsniper)

---

## 🔨 Building from Source

### 🤖 Automated Build (Windows)

```bash
cd builder
./build.bat
```

### 🛠️ Manual Build (Requires Python)

```bash
pip install pyinstaller
cd builder
pyinstaller sniper.spec
```

**Output:** Executable in `dist` folder

---

## 🤝 Contributing

### How You Can Help

- **Report issues** with detailed steps
- **Suggest features** with use cases
- **Submit PRs** following our guidelines

**Development Setup:**
```bash
git clone https://github.com/vexsyx/sniper-v3.git
cd sniper-v3
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under **GNU General Public License v3.0 (GPLv3)**.

**Your Rights:**
- Use for any purpose
- Study and modify
- Redistribute copies
- Improve and release enhancements

**Your Responsibilities:**
- Credit original authors
- Same license for derivatives
- Disclose source when distributing

Full license: [LICENSE](LICENSE)

---

## 👥 Credits

| Member | Role | Contact |
|--------|------|---------|
| **vex** | Lead Developer & Maintainer | [GitHub](https://github.com/vexsyx) \| [Discord](https://discord.com/users/1018875765565177976) |
| **yeswe** | Core Contributor | [GitHub](https://github.com/the2727) \| [Discord](https://discord.com/users/463575384961581066) |

**Support Development:** [Donate to Sol's Sniper](https://www.roblox.com/games/86163153952489/Sols-Sniper-Donation-Game#!/store)

---

## 💬 Support

- **Documentation:** This README
- **Community:** [Discord Server](https://discord.gg/solsniper)
- **Issues:** [GitHub Issues](https://github.com/vexsyx/sniper-v3/issues)

---

<div align="center">

## 🚀 Ready to Snipe?

[![Download EXE](https://img.shields.io/badge/Download_EXE-2d2d2d?style=for-the-badge&logo=googleanalytics&logoColor=white)](https://github.com/vexsyx/sniper-v3/releases/latest)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-2d2d2d?style=for-the-badge&logo=github)](https://github.com/vexsyx/sniper-v3)
[![Discord](https://img.shields.io/discord/1271189425459826699?style=for-the-badge&logo=discord&label=Discord&labelColor=5865F2)](https://discord.gg/solsniper)

**Made with ❤️ by the Sol Sniper Team**

*Please use responsibly and respect Discord's Terms of Service and Biome Hunt Servers' rules.*

</div>