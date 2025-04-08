# 🕹️ Hand Gesture Controlled Smash Karts 🎮 (OpenCV + MediaPipe)

Control the Smash Karts game using **hand gestures** instead of a keyboard!  
This project uses **OpenCV** and **MediaPipe** for real-time hand tracking and maps specific gestures to in-game controls (like accelerate, turn, brake, fire, etc.).

---

## ✨ Features

- 🖐️ Real-time hand gesture recognition (MediaPipe)
- 🎯 Accurate gesture mapping for game actions
- 🕹️ Control movement: accelerate, brake, turn left/right
- 💥 Fire weapon or boost using specific gestures
- 👊 One-hand only control (Right hand)
- 👓 On-screen gesture indicator (emoji or icon)

---

## 🤖 Recognized Gestures

| Gesture        | Action         | Key Press |
|----------------|----------------|-----------|
| Open Palm      | Accelerate     | Up Arrow  |
| Fist           | Brake          | Down Arrow|
| Point Right    | Turn Right     | Right Arrow|
| Point Left     | Turn Left      | Left Arrow|
| Two Fingers Up | Fire Weapon    | Spacebar  |
---

## 🧰 Tech Stack

- **OpenCV** - for webcam input and image processing
- **MediaPipe Hands** - for real-time hand landmark detection
- **Python** - core programming
- **`keyboard` or `pyautogui`** - for simulating key presses
- **Emoji/Image Overlay** - displays the current gesture on-screen

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/gesture-smashkarts.git
cd gesture-smashkarts
