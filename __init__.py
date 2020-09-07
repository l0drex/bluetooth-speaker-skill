from mycroft import MycroftSkill, intent_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
import subprocess
from bluetooth import Bluetooth
from status import Status


class BluetoothSpeaker(CommonPlaySkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.bluetooth_status = Status.INACTIVE

    def initialize(self):
        # use a2dp profile
        subprocess.run(['bluealsa-aplay', '--profile-a2dp'])
        
        # get current bluetooth status
        self.bluetooth_status = Bluetooth().get_status()

    def CPS_match_query_phrase(self, phrase):
        """
        This method responds wether the skill can play the input phrase.

        The method is invoked by the PlayBackControlSkill.

        Returns: tuple (matched phrase(str),
                        match level(CPSMatchLevel),
                        optional data(dict))
                    or None if no match was found.
        """
        for device in self.bluetooth_controller.get_connected_devices():
            if device['name'] in phrase:
                return (device['name'], CPSMatchLevel.EXACT, {'device': device['uuid']})

        if 'from my bluetooth device' in phrase:
            return ('from my bluetooth device', CPSMatchLevel.EXACT)
        elif 'bluetooth' in phrase:
            return ('bluetooth', CPSMatchLevel.GENERIC)
        else:
            return None

    def CPS_start(self, phrase, data):
        """
        Starts playback.

        Called by the playback control skill to start playback if the
        skill is selected (has the best match level)
        """
        if self.bluetooth_status is Status.CONNECTED:
            # get the uuid
            uuid = data['device']
            if uuid is None:
                uuid = '00:00:00:00:00:00'

            # route the audio from bluetooth device to audio output
            # TODO not sure if the '&' is needed
            subprocess.run(['bluealsa-aplay', uuid, '&'])
        else:
            self.speak_dialog('bluetooth.no_devices')

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

        # set status to connected
        self.bluetooth_status = Status.CONNECTED

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
