# Gesture-Controlled Car Racing Game

🚗 **Control any game using hand gestures with AI/ML!**

## 📌 Overview
The **Gesture-Controlled Car Racing Game** is an AI/ML-powered project that eliminates hardware dependencies by allowing users to control games with hand gestures. While originally designed for racing games, its adaptable gesture-to-key mapping system makes it compatible with any game that supports keyboard inputs, offering an innovative and accessible gaming experience.

## ✨ Features
- 🎮 **Gesture-Based Controls** – Move, jump, accelerate, or perform any in-game action using real-time hand tracking.
- 🧠 **Deep Learning Integration** – Uses a **CNN-based model in TensorFlow** to classify hand gestures accurately.
- 🎥 **Webcam-Based Input** – No additional hardware required.
- ⚡ **Real-Time Processing** – Fast and responsive gesture recognition.
- 💻 **Cross-Platform Compatibility** – Works on different devices and OS.
- ☁️ **Cloud-Synced Gesture Mapping** – Users can save and reuse their custom gesture settings across multiple devices.
- 🔧 **Customizable Gesture-to-Key Mapping** – Modify which gesture triggers which keybind for personalized control.
- 🕹️ **Supports All Games** – Works with any game that accepts keyboard inputs, including FPS, RPGs, and platformers.

## 🛠️ Tech Stack
- **Programming Language:** Python
- **Libraries & Frameworks:**
  - OpenCV – for real-time video processing
  - MediaPipe – for hand tracking
  - **TensorFlow/Keras – for deep learning (CNN) gesture classification**
  - PyAutoGUI – for simulating keyboard inputs
  - Flask – for backend API handling
  - MongoDB – for storing user-specific gesture mappings
- **Game Engine Compatibility:** Any game that supports keyboard inputs

## 🌍 Cloud-Based Gesture Mapping
- **MongoDB Integration:**
  - Stores user profiles along with their personalized gesture mappings.
  - Enables users to retrieve their saved gesture settings on any device.
  - Allows users to update, modify, or reset their gesture mappings anytime.

## 🚀 Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Mehnaz2004/Gestured-Controlled-Car-Racing-Game.git
   cd Gestured-Controlled-Car-Racing-Game
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up MongoDB**
   - Ensure you have a MongoDB instance running.
   - Configure your MongoDB URI in the `.env` file.

4. **Run the Flask app**
   ```bash
   python app.py
   ```

## 🎥 How It Works
1. **Start the game** – Launch any game that uses keyboard controls.
2. **Run the script** – The script captures real-time webcam input.
3. **Perform gestures** – Move your hand in predefined gestures to control the game.
4. **Deep Learning Model Interprets Gestures** – Uses a CNN-based model to classify hand gestures.
5. **AI Converts Gestures into Keyboard Inputs** – Sends corresponding key presses to the game.
6. **Game reacts accordingly** – The game responds as if real keyboard inputs were given.
7. **Save Gesture Mappings** – Customize and store gesture-to-keybind settings in MongoDB.
8. **Load on Any Device** – Access saved settings on different devices for a seamless experience.

## 🏗️ Future Enhancements
- 🎮 Enhanced support for different game genres
- 📱 Mobile device compatibility
- 🎨 Improved UI/UX for gesture mapping panel
- 🔄 Auto-calibration for different lighting conditions
- 🎙️ Voice commands integration for additional controls

## 🤝 Contribution
We welcome contributions! Feel free to fork the repo, create a branch, and submit a pull request.

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---

🚀 **Take your gaming experience to the next level with gestures!** 🖐️🎮
