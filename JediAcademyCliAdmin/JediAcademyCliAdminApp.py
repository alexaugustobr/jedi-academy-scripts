#!/usr/bin/python2.7 
import socket
import time
import JediAcademyCliAdminConfig as cfg
import JediAcademyCliAdminMapList as map_cfg

version = "3.0"

class Server:

    def __init__(self, id=0, name="", host="", port=0, rcon_password="", cheats=False):
        self.rcon_password = rcon_password
        self.host = host
        self.port = port
        self.name = name
        self.id = id
        self.cheats = cheats

    def send_data(self, data):
        data = ("\xff\xff\xff\xffrcon %s" % (data))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data + "\n", (self.host, self.port))
        received_data = sock.recv(1024)
        if "ShutdownGame:" in received_data:
            print("\nServer Response: Map is loading!")
        else:
            print("\nServer Response: {}".format(received_data[9:-1]))

    def send_rcon_command(self, cmd, parameter):
        data = ("%s %s %s" % (self.rcon_password, cmd, parameter))
        self.send_data(data)

    def load_map(self, mapname):
        self.send_rcon_command("map", mapname)

    def load_map_with_cheats(self, mapname):
        self.send_rcon_command("devmap", mapname)

    def enable_cheats(self, mapname):
        self.send_rcon_command("devmap", mapname)

    def disable_cheats(self, mapname):
        self.send_rcon_command("map", mapname)

    def load_map_change_mode(self, mapname, mbmode):
        print "The server will reload the map twice"
        self.send_rcon_command("mbmode", mbmode)
        print "Changing the map and disabling cheats in 20 seconds"
        time.sleep(20)
        self.send_rcon_command("map", mapname)

    def load_map_change_mode_with_cheats(self, mapname, mbmode):
        print "The server will reload the map twice"
        self.send_rcon_command("mbmode", mbmode)
        print "Changing the map and enabling cheats in 20 seconds"
        time.sleep(20)
        self.send_rcon_command("devmap", mapname)

    def send_message(self, msg):
        self.send_rcon_command("svsay", msg)


class Option:
    cmd = ""
    name = ""
    id = 0

    def __init__(self, cmd, name, id):
        self.cmd = cmd
        self.name = name
        self.id = id

class App:

    servers = []
    options = []
    config_file_path = ""

    def __init__(self, servers):
        print "\nJKA CLI Admin"
        print "\nMade by the Farmers Sons Family \nVersion: " + version
        self.servers = servers

    def start(self):
        self.load_menu_options()
        while True:
            self.show_menu()

    def show_modes_list(self):
        print "Select the mode"
        print "\n\t0 - Open Mode \t1 - Semi-Authentic Mode\n\t2 - Full-Authentic Mode \n\t3 - Duel mode"

    def read_mode_number(self):
        return raw_input("\nInsert the mode number:\n")

    def read_map_option(self):
        self.show_map_list()
        number = raw_input("\nInsert the map number:\n")

        if number < 0 or len(map_cfg.maps_list) <= int(number):
            raise RuntimeError("Map number {} not found".format(number))

        map_name = map_cfg.maps_list[int(number)]

        return map_name

    def read_map_and_mode_option(self):
        return self.read_map_option(), self.read_mode_number()

    def read_message(self):
        return raw_input("\nInsert the message:\n")

    def send_option_to_server(self, option, server):
        if option.cmd == "loadMapWithCheats":
            map_name = self.read_map_option()
            server.load_map_with_cheats(map_name)

        if option.cmd == "loadMap":
            map_name = self.read_map_option()
            server.load_map(map_name)

        if option.cmd == "changeModeWCheats":
            map_name, mbmode = self.read_map_and_mode_option()
            server.load_map_change_mode_with_cheats(map_name, mbmode)

        if option.cmd == "changeMode":
            map_name, mbmode = self.read_map_and_mode_option()
            server.load_map_change_mode(map_name, mbmode)

        if option.cmd == "sendMessage":
            msg = self.read_message()
            server.send_message(msg)

    def load_menu_options(self):
        changeMap = Option("loadMap", "Change the map with no cheats", 1)
        changeMapWCheats = Option("loadMapWithCheats", "Change the map with cheats", 2)
        changeMode = Option("changeMode", "Change the map and mode with no cheats", 3)
        changeModeWCheats = Option("changeModeWCheats", "Change the map and mode with cheats", 4)
        sendMessage = Option("sendMessage", "Send a message for the players", 5)

        self.options.append(changeMap)
        self.options.append(changeMapWCheats)
        self.options.append(changeMode)
        self.options.append(changeModeWCheats)
        self.options.append(sendMessage)
        
    def find_option_by_id(self, id):
        for option in self.options:
            if id == option.id:
                return option
        return None

    def find_server_by_id(self, id):
        for server in self.servers:
            if id == server.id:
                return server
        return None

    def show_server_list(self):
        for i in range(0, len(self.servers)):
            print "\t%d - %s" % (i + 1, self.servers[i].name)

    def show_options_list(self):
        print "\nOptions list:"
        for option in self.options:
            print "\t%d - %s" % (option.id, option.name)

    def read_input_option(self):
        return int(raw_input("\nType a option number from the list:\n"))

    def show_map_list(self):
        i=0
        for map in map_cfg.maps_list:
            print "{} - {}".format(i, map)
            i+=1

    def show_menu(self):
        self.show_options_list()
        optionNumber = self.read_input_option()
        option = self.find_option_by_id(optionNumber)
        if option != None:
            print "\nSelect a server:"
            self.show_server_list()
            serverNumber = int(raw_input("\nType the server number from the list:\n"))
            server = self.find_server_by_id(serverNumber)
            if server != None:
                self.send_option_to_server(option, server)
            else:
                "Invalid server"
        else:
            print "Invalid option"

if __name__ == "__main__":

    servers = []
    i = 1
    for server_cfg in cfg.servers:
        servers.append(
            Server(
                id=i,
                name=server_cfg["name"],
                host=server_cfg["host"],
                port=int(server_cfg["port"]),
                rcon_password=server_cfg["rcon_password"]
            )
        )
    i+=1

    app = App(
        servers
    )
    app.start()