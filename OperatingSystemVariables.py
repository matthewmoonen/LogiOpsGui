import os

class EnvironmentInfo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvironmentInfo, cls).__new__(cls)
            cls._instance.desktop_environment = cls._detect_desktop_environment()
            cls._instance.display_server = cls._detect_display_server()
        return cls._instance

    @staticmethod
    def _detect_desktop_environment():
        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")    
        if not desktop_env:
            if "GNOME_DESKTOP_SESSION_ID" in os.environ:
                return "GNOME"
            elif "KDE_FULL_SESSION" in os.environ:
                return "KDE"
            return "Unknown"
        return desktop_env

    @staticmethod
    def _detect_display_server():
        if os.environ.get("WAYLAND_DISPLAY"):
            return "Wayland"
        elif os.environ.get("DISPLAY"):
            return "X11"
        return "Unknown"

