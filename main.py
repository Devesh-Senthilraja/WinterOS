from pathlib import Path
import ctypes
import ctypes.util
import os
import sys

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def _load_vlc() -> None:
    library = ctypes.util.find_library("vlc")
    if library is None:
        raise RuntimeError("libvlc not found. Install 'vlc libvlc-dev' via apt.")

    ctypes.CDLL(library)

    plugins_dir = Path("/usr/lib/x86_64-linux-gnu/vlc/plugins")
    os.environ.setdefault("VLC_PLUGIN_PATH", str(plugins_dir))


_load_vlc()

from PyQt5.QtWidgets import QApplication

from core.window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())


    
