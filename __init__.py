from mycroft import MycroftSkill, intent_handler
import subprocess
from bluetooth import Bluetooth
from status import Status


class BluetoothSpeaker(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.bluetooth_status = Status.INACTIVE

    def initialize(self):
        # use a2dp profile
        subprocess.run(['bluealsa-aplay', '--profile-a2dp'])

        # route the audio from bluetooth device to audio output
        # TODO not sure if the '&' is needed
        # TODO actually, this should only be run if a device is connected i think
        subprocess.run(['bluealsa-aplay', '00:00:00:00:00:00', '&'])
        
        # get current bluetooth status
        self.bluetooth_status = Bluetooth().get_status()

    @intent_handler('bluetooth.activate.intent')
    def handle_bluetooth_activate(self, message):
        if self.bluetooth_status is 'active':
            pass
        else:
            # activate bluetooth
            success = subprocess.run(['bluetoothctl', 'power', 'on'])

            # log the result
            if success.returncode == 0:
                self.log.info('Bluetooth enabled successfully')
                self.speak_dialog('bluetooth.activated')
            else:
                self.log.warn('Bluetooth could not be activated')
                self.log.err(success.stderr)

    @intent_handler('bluetooth.pairing.intent')
    def handle_bluetooth_pairing(self, message):
        self.speak_dialog('bluetooth.pairing')

        # activate pairing mode

        # make device visible
        subprocess.run(['bluetoothctl', 'default-agent'])
        subprocess.run(['bluetoothctl', 'discoverable', 'on'])
        subprocess.run(['bluetoothctl', 'pairable', 'on'])        

    def handle_bluetooth_request(self):
        self.speak_dialog('bluetooth.pairing.request')

        # TODO handle pairing requests from new devices
        
        # receive request
        
        # confirm request
        
        # authorize services
        
        # trust the new device (opt)

    def stop(self):
        # disable audio playback
        # TODO experimental
        # killall bluealsa-aplay
        
        # make device invisible
        subprocess.run(['bluetoothctl', 'discoverable', 'off'])

        # deactivate bluetooth (opt)
        if self.settings.get('deactivate_bluetooth', False):
            subprocess.run(['bluetoothctl', 'power', 'off'])


def create_skill():
    return BluetoothSpeaker()
