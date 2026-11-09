# 🌐 Hacking Simulator

> A cyberpunk hacking simulator that runs entirely in your terminal — built with [Rich](https://github.com/Textualize/rich).

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-rich-informational)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

---

## 📖 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Commands](#-commands)
- [How to Play](#-how-to-play)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## 🎯 About

**Hacking Simulator** drops you into the "Neon Grid" as a low-level runner. You scan for vulnerable nodes, hack them for credits, upgrade your deck, and try to stay one step ahead of Netwatch. But every action raises your **Trace Level** — hit 100% and you're done.

It's a small, self-contained terminal game meant to be run with `python main.py`.

---

## ✨ Features

- 🖥️ **Full-screen terminal UI** powered by Rich (panels, tables, layout)
- 🎮 **Command-driven gameplay**: `scan`, `hack`, `upgrade`, `heal`, `flee`, `clear`, `help`, `exit`
- 📊 **Live status panel**: credits, health, trace level, inventory
- 🧠 **Randomized hacking outcomes** with risk/reward mechanics
- 💾 **Zero setup beyond `rich`** – no external services, no data files
- 🎨 **Color-coded feedback** (health, trace, logs) for at-a-glance state

---

## 🧰 Requirements

- **Python 3.8+**
- **[rich](https://pypi.org/project/rich/)** (only external dependency)

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/euroschein/<your-repo>.git
cd <your-repo>

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install the dependency
pip install rich
```

> 💡 Alternatively: `pip install -r requirements.txt` if you add a `requirements.txt` (see [Project Structure](#-project-structure)).

---

## ⚡ Quick Start

```bash
python main.py
```

You'll be prompted for a **hacker handle**, then dropped into the main screen:

```
🌐 HACKING SIMULATOR 🌐
Location: Neon District (Slums) | Target: Netwatch Mainframe

root@neon »
```

Type `help` to see the command list. That's it.

### 🖼️ Preview

<!-- Add a screenshot or GIF here -->
<!-- ![Gameplay](assets/screenshot.png) -->

---

## 🎮 Commands

| Command | Effect | Trace | Cost |
|---------|--------|-------|------|
| `scan` | Search for a vulnerable node (needed before `hack`) | +10% | – |
| `hack` | Breach the current target node | +25% | – |
| `upgrade` | Buy an ICE Breaker (+30% hack success rate) | – | 100 ₡ |
| `heal` | Buy a Med-Stim (+50 HP, max 100) | – | 150 ₡ |
| `flee` | Disconnect and wipe tracks | −30% | – |
| `clear` | Clear the terminal | – | – |
| `help` / `?` | Show the command list | – | – |
| `exit` | Quit the game | – | – |

**Lose conditions:** Trace reaches **100%** (Netwatch catches you) or Health hits **0** (ICE fries your deck).

---

## 🕹️ How to Play

The core loop is simple:

1. **`scan`** — look for an unsecured node. If you find one, `Node IP` lands in your inventory.
2. **`hack`** — breach it. Success → credits. Failure → −20 HP and the node is gone.
3. **`upgrade`** once you have 100 ₡ to raise your success rate.
4. **`heal`** when HP is low (costs 150 ₡).
5. **`flee`** when your Trace is getting dangerous — it shaves 30% off.

Every `scan` and `hack` raises your **Trace Level**, so balance greed against survival. Manage your credits, keep your HP above zero, and don't let Netwatch pin you down.

---

## 📁 Project Structure

```
<your-repo>/
├── main.py            # The entire game (UI + logic)
├── requirements.txt   # Optional: just "rich"
└── README.md
```

> 💡 If you add a `requirements.txt`, generate it with:
> ```bash
> pip freeze | grep -i rich > requirements.txt
> ```
> or simply create it with the single line:
> ```
> rich
> ```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
