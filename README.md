> [!WARNING]  
> This Repo is **NOT** finished.<br>
> The source code is still closed source until **Beta 5** is released, so the build script will not work.

<div align="center">

<div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px;">
  <img src="https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/assets/snipercat.png" width="80" height="80" style="border-radius: 12px;">
  <div>
    <h1 style="margin: 0; font-size: 2.5em;">Sol Sniper V3</h1>
    <p style="margin: 5px 0 0 0; font-size: 1.2em; opacity: 0.8;">The Most Advanced Discord Server Sniper for Sol's RNG</p>
  </div>
</div>

<div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin: 20px 0;">
  <a href="https://github.com/vexthecoder/sniper-v3/releases">
    <img src="https://img.shields.io/badge/Version-3.0.0_BETA_5-4a7bff?style=for-the-badge&logo=github" alt="Latest Release">
  </a>
  <!-- 
  change to this once you make a release :D
  https://img.shields.io/github/v/release/vexthecoder/sniper-v3?style=for-the-badge&logo=github&label=Latest%20Release&logoColor=white 
  -->
  <a href="LICENSE"><img src="https://img.shields.io/github/license/vexthecoder/sniper-v3?style=for-the-badge&logo=nextdns&label=License&logoColor=white" alt="License"></a>
  <a href="https://python.org/downloads"><img src="https://img.shields.io/badge/Python-3.8+-ffd043?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows | macOS-2d2d2d?style=for-the-badge&logo=files&logoColor=white" alt="Platform"></a>
  <a href="https://raw.githubusercontent.com/vexthecoder/sniper-v3/main/Sol Sniper V3.exe"><img src="https://img.shields.io/badge/Standalone_EXE-Download-00c853?style=for-the-badge&logo=googleanalytics&logoColor=white" alt="Standalone EXE"></a>
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

Sol Sniper V3 is a powerful, modern Sol's RNG based app specifically designed to snipe private servers. With its sleek interface and advanced detection algorithms, it automatically finds and joins private servers based on your customized keyword patterns, giving you the edge in sniping rare biomes and merchants.

---

## ⚡ Features

### 🎯 Intelligent Detection
| Feature | Description |
|---------|-------------|
| **Real-time Monitoring** | Just like a normal Discord client, it checks all incoming messages |
| **Smart Keyword System** | Advanced pattern matching with RegEx support |
| **Multi-Category Support** | Glitched, Dreamspace, Jester, Void Coin & custom categories |
| **Biome Verification** | Auto-closes Roblox if the sniped Glitched/Dreamspace was fake/bait |

### 🎨 Modern Experience
| Feature | Description |
|---------|-------------|
| **Beautiful GUI** | Gradient themes with modern-ish design |
| **Customizable Hotkeys** | Fully configurable keyboard shortcuts |
| **Desktop Notifications** | Toast alerts for successful snipes (if enabled) |
| **Performance Modes** | Adjustable UI settings for optimal performances (requires app restart on change) |

### 🔧 Advanced Controls
| Feature | Description |
|---------|-------------|
| **Server Management** | Multiple Discord servers & channels |
| **Blacklist System** | Filter out bait and fake servers |
| **Cross-Platform** | Windows & macOS support |
| **Standalone EXE** | No installation required |

---

## 📥 Installation

### 🎯 Quick Start (Recommended)

**For most users, download the pre-built executable:**

1. **Download** the latest release from the [latest release](https://github.com/vexthecoder/sniper-v3/releases/latest)
2. **Run** `Sol Sniper V3.exe` - No installation needed!
3. **Configure** your settings and start sniping

### 🐍 Python Version

#### Prerequisites
- Python 3.8 or higher
- PIP in your system PATH
- Roblox installed
- Discord account

#### Setup Steps

```bash
# Clone the repository
git clone https://github.com/vexthecoder/sniper-v3.git
cd sniper-v3

# Install dependencies
pip install -r requirements.txt

# Launch the application
python main.py
```

#### Required Packages
```txt
requests
PyQt6
psutil
discord.py-self
aiohttp
keyboard
win11toast (Windows)
desktop-notifier (macOS)
```

---

## 🏗️ Standalone Executable

### 📦 One-Click Solution

Our standalone Windows executable provides the ultimate convenience:

**🎁 Benefits:**
- ✅ No Python installation required
- ✅ Single executable file
- ✅ Portable and easy to share

**⬇️ Download:**
- Grab the latest `Sol Sniper V3.exe` from our [Releases](https://github.com/vexthecoder/sniper-v3/releases)

**🚀 Usage:**
1. Download `Sol Sniper V3.exe`
2. Double-click to launch
3. Configure and start sniping!

---

## ⚙️ Configuration

### 🔧 Initial Setup Guide

#### 1. Credentials Setup
- Navigate to the **Sniper** tab
- Enter your Discord token and Roblox cookie
- Enable desired sniper categories

#### 2. Server Configuration
- Add Discord servers to monitor
- Configure specific channels for each server
- Test connectivity and permissions

#### 3. Keyword Optimization
- Customize detection keywords per category
- Set up blacklists to avoid false positives
- Configure advanced regex patterns

<details>
<summary><strong>🔐 Credential Setup Guide</strong></summary>

### ⚠️ Security Notice

**Handle these credentials with extreme care:**
- 🔒 Never share tokens with anyone
- 🚫 Tokens provide full account access
- ✅ Use exclusively for this application

### Discord Token Extraction

1. Visit the [Discord Web Client](https://discord.com/app)
2. Log into your account
3. Open Developer Tools (F12)
4. Enable mobile mode (📱 icon)
5. Switch to Console tab
6. Paste and execute:

```javascript
// Discord Token Extractor
const iframe = document.createElement('iframe');
document.body.appendChild(iframe);

try {
    const token = iframe.contentWindow.localStorage.token;
    
    if (token) {
        let tokenValue;
        try {
            tokenValue = JSON.parse(token);
        } catch (e) {
            tokenValue = token;
        }
        
        const copyToClipboard = async (text) => {
            try {
                await navigator.clipboard.writeText(text);
                return true;
            } catch (err) {
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                const success = document.execCommand('copy');
                document.body.removeChild(textArea);
                return success;
            }
        };
        
        copyToClipboard(tokenValue).then(success => {
            if (success) {
                console.log('✅ Token copied to clipboard: %c%s', 'font-size:16px; color: green;', tokenValue);
                console.log('📋 Token has been automatically copied to your clipboard!');
            } else {
                console.log('✅ Token: %c%s', 'font-size:16px; color: green;', tokenValue);
                console.log('❌ Could not copy to clipboard. Manually copy the token above.');
            }
        });
        
    } else {
        console.log('❌ No token found in localStorage');
        console.log('%c📱 Mobile Mode Required:', 'font-size:16px; color: orange; font-weight: bold;');
        console.log('1. Press F12 to open Developer Tools');
        console.log('2. Click the 📱 mobile device icon');
        console.log('3. Refresh the page');
        console.log('4. Run this script again');
    }
} catch (e) {
    console.log('❌ Error:', e.message);
    console.log('%c📱 Enable mobile mode and try again!', 'font-size:14px; color: orange;');
} finally {
    iframe.remove();
}
```

### Roblox Cookie Guide

For Roblox `.ROBLOSECURITY` cookie extraction, follow our video tutorial:

[🎥 Roblox Cookie Tutorial](https://youtu.be/sz07F5inaFg?t=16)

### 🛠️ Troubleshooting
- **Token not found?** Ensure mobile mode is enabled
- **Copy failed?** Manually copy from console output
- **Errors?** Verify you're logged into Discord and using the [Web Client](https://discord.com/app)

</details>

---

## ⌨️ Hotkeys

### ⚡ Quick Actions

| Hotkey | Default | Action |
|--------|---------|--------|
| Join Random Server | `-` | Launches random Sol's RNG server |
| Pause Sniper | `[` | Temporary stop (configurable duration) |
| Toggle Sniper | `F4` | Enable/disable sniper entirely |

### 🎛️ Customization
1. Navigate to **Hotkeys** tab
2. Click **"Assign"** for any hotkey
3. Press your desired key combination
4. Save settings

---

## 🎮 Usage

### 🚀 Getting Started

#### 1. Launch & Configure
- Open the application
- Set up credentials in **Sniper** tab
- Configure servers, keywords, and blacklist
- Click **"Start Sniping"**

#### 2. Monitor & React
- Application auto-detects relevant server links
- Desktop notifications alert you to detections (if enabled)
- Roblox launches automatically with correct server

#### 3. Advanced Operations
- Create custom categories for specific events
- Use regex patterns for complex detection

---

## 🔧 Troubleshooting

### 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| **App won't start** | Check Python 3.8+ (Python version) or re-download EXE |
| **No detections** | Verify token validity and config |
| **Roblox not launching** | Ensure Roblox is installed and updated and that you have specified the correct Launch Protocol |
| **Performance issues** | Enable "Still Background" in settings |

### 📞 Getting Help

1. **Check** [Issues](https://github.com/vexthecoder/sniper-v3/issues) page
2. **Review** troubleshooting guide above
3. **Join** our [Discord Community](https://discord.gg/RPcPUp47YD)
4. **Create** detailed issue reports

---

## 🔨 Building from Source

### 🤖 Automated Build (Windows)

We provide an automated build script for convenience:

```bash
cd builder
./build.bat
```

**The script automatically:**
- ✅ Checks Python installation
- ✅ Installs PyInstaller if needed
- ✅ Builds using `sniper.spec`
- ✅ Outputs `Sol Sniper V3.exe`

### 🛠️ Manual Build

**Requirements:**
- Python 3.8+
- PyInstaller
- All dependencies

**Build commands:**
```bash
# Install PyInstaller
pip install pyinstaller

# Build using spec file
cd builder
pyinstaller sniper.spec
```

**Output:** Executable in `dist` folder

### ⚙️ Build Configuration

The `sniper.spec` includes:
- One-file bundle setup
- Icon and version info
- Hidden imports for dependencies
- File size optimizations

---

## 🤝 Contributing

### 🌟 How You Can Help

We love community contributions! Here's how to get involved:

#### 🐛 Reporting Issues
- Use issue templates
- Provide detailed reproduction steps
- Include system info and logs

#### 💡 Feature Requests
- Check existing issues first <br>(Both on the Repo and Discord)
- Explain use case and benefits
- Consider implementation complexity

#### 💻 Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request

#### 🏗️ Development Setup
```bash
# Clone repository
git clone https://github.com/vexthecoder/sniper-v3.git
cd sniper-v3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under **GNU General Public License v3.0 (GPLv3)**.

### 📜 License Summary

| Permission | Condition |
|------------|-----------|
| ✅ Commercial use | ✅ Same license |
| ✅ Distribution | ✅ Disclose source |
| ✅ Modification | ✅ State changes |
| ✅ Patent use | ✅ Copyright notice |

### 🆓 Your Rights
- Use software for any purpose
- Study and adapt the code
- Redistribute copies
- Improve and release enhancements

### 📝 Your Responsibilities
- **Credit** original authors
- **Same License** for derivatives
- **Disclose Source** when distributing
- **Keep Free** no additional restrictions

**Full license:** [LICENSE](LICENSE)

---

## 👥 Credits

### 🧑‍💻 Core Team

| Member | Role | Contact |
|--------|------|---------|
| **vex** | Lead Developer & Maintainer | [GitHub](https://github.com/vexthecoder) \| [Discord](https://discord.com/users/1018875765565177976) |
| **yeswe** | Core Contributor | [GitHub](https://github.com/the2727) \| [Discord](https://discord.com/users/463575384961581066) |
| **PJ** | Core Contributor | [Discord](https://discord.com/users/773604524573196298) |

### 🙏 Special Thanks
- Our amazing beta testers
- The Sol's RNG community

### 💝 Support Developers
Consider supporting our developers:

- [🎁 Donate to vex](https://www.roblox.com/games/17060128444/Aura-Game-Yes#!/store)
- [🎁 Donate to yeswe/PJ](https://www.roblox.com/games/121743595575824/donate#!/store)

---

## 💬 Support

### 📚 Resources
- **Documentation**: This README & project wiki
- **Community**: [Discord Server](https://discord.gg/RPcPUp47YD)
- **Issues**: [GitHub Issues](https://github.com/vexthecoder/sniper-v3/issues)
- **Contact**: Via Discord profiles

---

<div align="center">

## 🚀 Ready to Snipe?

**Get started now with our standalone executable or Python version!**

[![Download EXE](https://img.shields.io/badge/Download_EXE-2d2d2d?style=for-the-badge&logo=googleanalytics&logoColor=white)](https://github.com/vexthecoder/sniper-v3)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-2d2d2d?style=for-the-badge&logo=github)](https://github.com/vexthecoder/sniper-v3)
[![Discord](https://img.shields.io/badge/Discord-Join_Server-5865F2?style=for-the-badge&logo=discord)](https://discord.gg/RPcPUp47YD)

**Made with ❤️ by the Sol Sniper Team**

*Please use responsibly and respect Discord's Terms of Service*

</div>