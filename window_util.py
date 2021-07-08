import win32gui
import win32process

def _get_hwnd_by_pid(self, pid):
    """Gets handle of the window that belongs to a process.

    Args:
      pid: process id.
    Returns:
      Window handle.
    """

    def callback(hwnd, hwnds):
      if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
          hwnds.append(hwnd)
      return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None