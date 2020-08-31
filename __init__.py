from mycroft import MycroftSkill, intent_handler
import subprocess


class BluetoothSpeaker(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        # use a2dp profile
        subprocess.run(['bluealsa-aplay', '--profile-a2dp'])

        # route the audio from bluetooth device to audio output
        # TODO not sure if the '&' is needed
        # TODO actually, this should only be run if a device is connected i think
        subprocess.run(['bluealsa-aplay', '00:00:00:00:00:00', '&'])

    @intent_handler('bluetooth.activate.intent')
    def handle_bluetooth_activate(self, message):
        self.speak_dialog('bluetooth.activated')

        # activate bluetooth
        success = subprocess.run(['bluetoothctl', 'power', 'on'])

        # log the result
        if success.returncode == 0:
            self.log.info('Bluetooth enabled successfully')
        else:
            self.log.warn('Bluetooth could not be activated')
            self.log.err(success.stderr)

    @intent_handler('bluetooth.pairing.intent')
    def handle_bluetooth_pairing(self, message):
        self.speak_dialog('bluetooth.pairing')

        # activate pairing mode
        subprocess.run(['bluetoothctl', 'default-agent'])

        # make device visible
        subprocess.run(['bluetoothctl', 'discoverable', 'on'])

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
