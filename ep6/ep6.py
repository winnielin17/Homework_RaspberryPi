import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
import requests

TARGET_URL = 'localhost'

continue_reading = True

def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Hold a tag near the reader")
print("Press Ctrl-C to stop")

# check the UID
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        # uid_decimal = uid[0] * 256 * 256 * 256 + uid[1] * 256 * 256 + uid[2] * 256 + uid[3]
        print("UID length:", len(uid))
        uid_len = len(uid) - 1
        uid_decimal = 0
        for x in range(0, uid_len):
            uid_decimal = uid_decimal + uid[x] * 256 ** (uid_len - 1 - x)
        print("Card read UID decimal: " + str(uid_decimal))
        print("Card read UID hexadecimal: 0x{:X}".format(uid_decimal))

        # Check UID
        print("Check uid[4] = uid[0] XOR uid[1] XOR uid[2] XOR uid[3]")
        if uid[4] == uid[0] ^ uid[1] ^ uid[2] ^ uid[3]:
            print("0x{:X} = 0x{:X} XOR 0x{:X} XOR 0x{:X} XOR 0x{:X}".format(
                uid[4], uid[0], uid[1], uid[2], uid[3]))

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check OK
        if status == MIFAREReader.MI_OK:
            # Variable for the data to write
            name = "Pei-Ying Lin    "
            data = []
            # Fill the data with name
            for i in range(0, 16):
                data.append(ord(name[i]))

            print("Sector 8 will now be filled with data in code")
            # Write the data
            MIFAREReader.MFRC522_Write(8, data)

            print("It now looks like this:")
            rdData = MIFAREReader.MFRC522_Read(8)
            print("No. 8")
            print("Card read Data 0-3: " + str(rdData[0]) + "," + str(rdData[1]) + ","
                  + str(rdData[2]) + "," + str(rdData[3]))
            print("Card read Data 4-7: " + str(rdData[4]) + "," + str(rdData[5]) + ","
                  + str(rdData[6]) + "," + str(rdData[7]))
            print("Card read Data 8-11: " + str(rdData[8]) + "," + str(rdData[9]) + ","
                  + str(rdData[10]) + "," + str(rdData[11]))
            print("Card read Data 12-15: " + str(rdData[12]) + "," + str(rdData[13]) + ","
                  + str(rdData[14]) + "," + str(rdData[15]))

            nameData = "".join(chr(i) for i in rdData)
            print("Card read Data: " + nameData)

            r = requests.get('http://{0}/LogRecord_GET.php?NAME={1}&ID={2}'.format(
                TARGET_URL, nameData, uid_decimal))
            print("Server Return Code:", r.status_code)
            print(r.text)
            MIFAREReader.MFRC522_StopCrypto1()

            print("Hold a tag near the reader")
            print("Press Ctrl-C to stop")
        else:
            print("Authentication error")
