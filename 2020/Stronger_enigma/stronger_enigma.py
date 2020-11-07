import string
import random
import sys
import time
import socket
import itertools


#SERVER = ('18.156.68.123', 80)
SERVER = ('127.0.0.1', 8080)
RECV_SIZE = 8192
conn = None


def create_configuration():
    number_of_rotors = random.randrange(3, 6)
    rotates_amounts = [3, 5, 7, 11, 17, 19, 23]
    
    result = []
    for _ in range(number_of_rotors):
        rotor = "".join(random.sample(string.ascii_uppercase, 26))
        rotates_amount = random.choice(rotates_amounts)
        result.append([rotor, rotates_amount])
    print("ENIGMA:", result)
    return result


def enumerate_configurations():
    number_of_rotors = 3
    rotates_amounts = [3, 5, 7, 11, 17, 19, 23]
    
    rotor = itertools.product(
                ["".join(l) for l in itertools.permutations(string.ascii_uppercase, 26)],
                rotates_amounts)

    for result in itertools.combinations_with_replacement(rotor,number_of_rotors):
        yield result


class StrongerEnigma:

    class Rotor:
        def __init__(self, configuration, rotate_amount):
            self.data = configuration
            self.rotate_amount = rotate_amount

        def rotate(self):
            self.data = self.data[self.rotate_amount:] + self.data[:self.rotate_amount]

        def encrypt(self, char):
            char_idx = string.ascii_uppercase.index(char)
            encrypted = self.data[char_idx]
            self.rotate()
            return encrypted

        def decrypt(self, char):
            char_idx = self.data.index(char)
            decrypted = string.ascii_uppercase[char_idx]
            self.rotate()
            return decrypted

        def __str__(self):
            return self.data

    def __init__(self, cfg = None):
        if cfg is None:
            todays_configuration = create_configuration()
        else:
            todays_configuration = cfg

        self.rotors = []
        for d in todays_configuration:
            self.rotors.append(StrongerEnigma.Rotor(d[0], d[1]))

    def __encrypt_char(self, char):
        encrypted = char
        if char in string.ascii_uppercase:
            for r in self.rotors:
                encrypted = r.encrypt(encrypted)
        return encrypted

    def __decrypt_char(self, char):
        decrypted = char
        if char in string.ascii_uppercase:
            for r in reversed(self.rotors):
                decrypted = r.decrypt(decrypted)
        return decrypted

    def encrypt(self, message):
        encrypted_message = ""
        for char in message:
            encrypted_message += self.__encrypt_char(char)
        return encrypted_message

    def decrypt(self, message):
        decrypted_message = ""
        for char in message:
            decrypted_message += self.__decrypt_char(char)
        return decrypted_message

    def __str__(self):
        s = "===============================\n" + string.ascii_uppercase + "\n"
        for r in self.rotors:
            s += str(r) + "\n"
        s += "\n==============================="
        return s


def send_interface(machine):
    to_send = """
HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE
    """
    message = machine.encrypt(to_send)
    send(message)
    return message


def process_message(server_machine, message):
    decrypted = server_machine.decrypt(message)
    print(decrypted, message)

    if decrypted == "GET-SECRET-DATA":
        flag = open("flag.txt", "rt").read()
        encrypted = server_machine.encrypt(flag)
        send(encrypted)
    elif decrypted == "SEND-SECRET-DATA":
        encrypted = receive()
        decrypted = server_machine.decrypt(encrypted)
        open("secrets.txt", "a+").write(decrypted)
    elif decrypted == "GOODBYE":
        send("See you next time")
        exit()
    else:
        send("I don't understand you")


def send(message):
    global conn

    print("SENDING |", message, "|")
    conn.send(message.encode('utf-8'))


def receive():
    global conn

    return [s.strip() for s in conn.recv(RECV_SIZE).decode('utf-8').splitlines()]


def doEngima():
    global machine

    starting_session_seconds = time.time()
    send("Insecure channel. Encrypting with today's configuration..")
    #machine = StrongerEnigma()

    while True:
        send_interface(machine)
        client_message = receive()
        process_message(machine, client_message[0])


def server():
    global conn
    global machine
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(SERVER)
                s.listen(1)
                machine = StrongerEnigma()
                print("LISTENING")
                conn, _ = s.accept()
                with conn:
                    doEngima()
        except KeyboardInterrupt:
            return
        except:
            pass


def bombe(txt, encrypted):
    print(txt, encrypted)
    cfg = input('ENIGMA CONFIG:')
    config = eval(cfg.strip())
    m = StrongerEnigma(config)
    return m


def client():
    global conn

    machine = None
    conn = socket.create_connection(SERVER)
    cleartext = """

HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE

"""

    cleartext_lines = [s.strip() for s in cleartext.splitlines()]
    received_lines = []
    encrypted_lines = []
    while len(received_lines) < len(cleartext_lines):
        received_lines.extend(receive())

    expected = [c for c in cleartext if c in string.ascii_uppercase]
    encrypted = []
    for line in received_lines:
        if len(line) > 0 and len([c for c in line if c.islower()]) == 0:
            encrypted.extend([c for c in line if c in string.ascii_uppercase])
            encrypted_lines.append(line)
        else:
            print(line)

    if machine is None:
        machine = bombe(expected, encrypted)
    for line in encrypted_lines:
        print(machine.decrypt(line))

    send(machine.encrypt("GET-SECRET-DATA"))
    #send(data[4])
    print(receive())


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        server()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        machine = StrongerEnigma()
        #print(str(machine))
        print(machine.encrypt(sys.argv[2]))
        #print(str(machine))
    else:
        client()


if __name__ == '__main__':
    main()
