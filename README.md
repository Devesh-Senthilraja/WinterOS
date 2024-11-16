# Proxima - Lightweight UI Interface

## 📋 Project Description
**Proxima** is an experimental Python-based lightweight user interface (UI) that mimics some core functionalities of an operating system across multiple platforms. Leveraging the power of **PyQt5** and several other third-party libraries, this project draws widgets on the screen that resemble a minimalistic OS interface, providing utilities like a web browser, video player, calculator, and more. The goal of Proxima is to explore and demonstrate how Python can be used to create a modular and efficient UI interface with essential system functionalities.

## ✨ Features
- **Custom Window Management**: Frameless, full-screen mode with a smooth and responsive interface.
- **Standalone Functional Modules**:
  - **Web Browser**: Browse the internet using an integrated web engine.
  - **Video Player**: Stream videos using the VLC media player library.
  - **Calculator**: Perform mathematical calculations.
  - **Image Processing**: Capture and process images using OpenCV.
  - **Language Translation**: Translate text using Google Translate's API.
  - **Geolocation Services**: Display maps and coordinates using Folium.
- **Optimized Resource Management**: Includes a custom window instantiator and instance manager to keep the interface lightweight and responsive.
- **Self-contained Dependencies**: All required packages are kept within the project directory for easier management.

## 🛠️ Prerequisites and Installation
### Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8+**
- **pip** (Python package installer)

### Installation
To set up the environment and install all required packages, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/proxima.git
    cd proxima
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Running the Program
After installing the necessary packages, you can run the program using:

```bash
python Program.py
```

The application will launch in full-screen mode, providing you with a custom UI that includes the various modules.

## 🖥️ Usage
- **Web Browser**: Navigate to the browser module to access websites.
- **Calculator**: Use the calculator module for mathematical operations.
- **Video Player**: Open and stream video files using the video player module.
- **Image Processing**: Capture images using your webcam and apply filters or transformations.
- **Language Translation**: Translate text between different languages.
- **Geolocation Services**: View maps and find locations using the geolocation module.

### Customization
All the modules are organized into separate classes within the script. You can modify or extend functionalities by editing the relevant classes in the `Program.py` file.

## 🗃️ Project Structure
```
proxima/
├── Program.py
├── Icons/                # Images, icons, and other assets used in the UI
└── requirements.txt      # List of dependencies
└── ...
```

## 📦 Dependencies
The following Python packages are used in this project:

- `PyQt5`: For creating the graphical user interface.
- `opencv-python` (`cv2`): For capturing and processing images.
- `vlc`: For video streaming and playback.
- `googletrans`: For translating text between languages.
- `folium`: For rendering maps and geolocation services.
- `requests`: For handling API requests.
- `textblob`: For natural language processing.
- `subprocess`: For executing system-level commands.

To install these dependencies, simply run:
```bash
pip install -r requirements.txt
```

## 📝 License
This project is licensed under the MIT License - feel free to use, modify, and distribute it as you like.
