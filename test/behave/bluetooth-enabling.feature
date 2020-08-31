Feature: bluetooth-enabling
    Scenario: Bluetooth is turned off
        Given an english speaking user
            When the user says "enable bluetooth"
            Then "bluetooth-speaker" should reply with dialog from "bluetooth.activate"
    Scenario: Bluetooth is turned on
        Given an english speaking user
            When the user says "enable bluetooth"
            Then the reply should be exactly "Bluetooth is already activated"
