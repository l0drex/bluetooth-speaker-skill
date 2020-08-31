import subprocess
from status import Status


class Bluetooth:
    def __init__(self):
        self.status = self.get_status()
    
    def get_status(self):
        """
        Returns the current status of the default bluetooth controller
        (inactive, Powered, Discoverable, Pairable)
        """
        info = self.get_controller_information()

        if info['Powered'] == 'no':
            return Status.INACTIVE
        elif info['Discoverable'] == 'no':
            return Status.POWERED
        elif info['Pairable'] == 'no':
            return Status.DISCOVERABLE
        else:
            return Status.PAIRING
    
    def get_controller_information(self):
        info_string = subprocess.run(['bluetoothctl', 'show'], capture_output=True, text=True).stdout
        info_string.split('\n')
        info = {}
        key = info_string[0]
        for s in info_string:
            if s[0] == ' ':
                info[key].append(s)
            else:
                key = s

        return info
