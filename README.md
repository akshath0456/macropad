# macropad
# 🎛️ Raspberry Pi Pico Macro Pad

A customizable macro pad built using the **Raspberry Pi Pico and CircuitPython**, featuring a rotary encoder, a display screen, and a 4×4 matrix keypad.

The goal of this project is to create a programmable hardware controller that can interact with a computer and control different software applications. It can be configured to launch applications, trigger keyboard shortcuts, navigate menus, control media playback, and automate repetitive tasks.

## ✨ Features

- **Raspberry Pi Pico:** Main microcontroller running CircuitPython.
- **Rotary Encoder:** Navigate menus, scroll through options, and adjust values.
- **Display Screen:** Show menus, selected actions, active profiles, and device status.
- **4×4 Matrix Keypad:** 16 programmable keys for macros and shortcuts.
- **USB HID Support:** Send keyboard shortcuts and keystrokes to a connected computer.
- **Custom Macros:** Assign actions to individual keys.
- **Menu System:** Use the rotary encoder and display to navigate available functions.
- **Expandable Software:** Add new macros, profiles, and features as needed.
  <img width="553" height="606" alt="Screenshot From 2026-10-11 23-43-42" src="https://github.com/user-attachments/assets/1702ab42-3ba5-4e0c-82d3-e671c94e7eb9" />


## 🧰 Hardware Requirements

| Component | Purpose |
|---|---|
| Raspberry Pi Pico | Main controller |
| Rotary encoder | Menu navigation and value adjustment |
| Display (such as SSD1306 OLED) | User interface |
| 4×4 matrix keypad | 16 programmable buttons |
| Breadboard or custom PCB | Circuit assembly |
| Jumper wires | Electrical connections |
| USB cable | Power and USB communication |

## 💻 Software Requirements

- **CircuitPython** — firmware for the Raspberry Pi Pico.
- **Adafruit HID Library** — USB keyboard and consumer-control functionality.
- **Adafruit Display Libraries** — for the selected screen.
- **Matrix keypad and rotary encoder drivers** — for reading hardware inputs.
- **Mu Editor, Thonny, or another compatible editor** — for developing and uploading code.

The exact libraries depend on the display and encoder modules used.

## ⚙️ How It Works

1. CircuitPython runs on the Raspberry Pi Pico.
2. The firmware reads the 4×4 keypad and rotary encoder.
3. The display updates to show the selected menu, action, or profile.
4. When a key or encoder action is triggered, the Pico sends the configured USB HID input or processes the corresponding command.
5. The computer receives the input and performs the associated action.

### Example Macro Assignments

| Input | Example Function |
|---|---|
| Key 1 | Open a browser using a configured shortcut or host application |
| Key 2 | Open a code editor |
| Key 3 | Copy selected text |
| Key 4 | Paste copied text |
| Key 5 | Save the current document |
| Key 6 | Switch between applications |
| Encoder rotation | Navigate the menu or adjust volume |
| Encoder press | Select an item |
| Display | Show the current menu and active profile |

These assignments are customizable. Opening applications directly may require an operating-system shortcut or a companion program on the computer.

## 📂 Project Structure

```text
macro-pad/
├── code.py              # Main CircuitPython program
├── settings.toml        # Optional configuration
└── lib/
    ├── adafruit_hid/    # USB HID library
    └── display_drivers/ # Required display libraries, if applicable
```

The `lib` folder should contain the libraries required by your specific hardware. CircuitPython automatically executes `code.py` when the device starts.

## 🔌 USB Communication

The macro pad can use USB HID to behave like a keyboard, sending shortcuts such as:

- `Ctrl + C` — Copy
- `Ctrl + V` — Paste
- `Ctrl + S` — Save
- `Alt + Tab` — Switch applications

For more advanced automation, such as launching arbitrary applications, running scripts, or controlling software through APIs, a companion program on the host computer can receive commands over USB serial and execute the configured actions.

## 🛠️ Development Roadmap

- [ ] Set up CircuitPython on the Raspberry Pi Pico.
- [ ] Connect and test the rotary encoder.
- [ ] Scan the 4×4 matrix keypad.
- [ ] Initialize the display.
- [ ] Implement a menu navigation system.
- [ ] Add USB HID keyboard shortcuts.
- [ ] Create configurable macro profiles.
- [ ] Add persistent settings and custom actions.
- [ ] Develop optional host-side automation software.

## 📜 License

This project can be released under the MIT License or another open-source license of your choice.

---

**A small hardware controller for a fully customizable software workflow.**
