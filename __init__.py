from mycroft import MycroftSkill, intent_file_handler


class BluetoothSpeaker(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('speaker.bluetooth.intent')
    def handle_speaker_bluetooth(self, message):
        self.speak_dialog('speaker.bluetooth')


def create_skill():
    return BluetoothSpeaker()

