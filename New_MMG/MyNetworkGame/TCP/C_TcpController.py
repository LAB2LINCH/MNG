import socket
import time

from TCP.C_Pack import DataStruct
from Data.C_RoomData import *
from State import C_collision
data_struct = DataStruct

SELECT_LOBBY = 0
SELECT_ROOM_DATA = 1
SELECT_JOIN = 2
SELECT_CREATE = 3
SELECT_EXIT = 4

IS_STARTED = 3
IS_FULL = 2
CAN_JOIN = 1

class TcpContoller:
    def get_addr(self):
        addr_file = open('ADDR.txt','r')
        addr=addr_file.readlines()
        return (addr[0][0:len(addr[0])-1], int(addr[1]))

    client_socket=socket

    def tcp_client_init(self):
        addr=self.get_addr()
        ip = addr[0]
        port = addr[1]
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        return self.client_socket

    def loof(self):
        while 1:
            while 1:
                data = "Hello world"
                self.client_socket.sendall(C_collision.DATA_PACK_ENEMY)
                print("send data = ", data)
                self.recv_is_game_over()

    def recv_is_game_over(self):
        # recv is_game_over
        packed_is_game_over = self.client_socket.recv(1)
        is_game_over = data_struct.unpack_is_game_over(packed_is_game_over)
        print('i\'m recv ', is_game_over)
        time.sleep(1)


    def exit(client_socket):
        client_socket.close()
        print("SOCKET closed... END")


    #Lobby selection 0 = LOBBY_DATA, selection 1 = ROOM_DATA, selection 2 = JOIN, selection 3 = CREATE
    def send_exit_server(client_socket):
        selection = SELECT_EXIT
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)

        packed_data = client_socket.recv(data_struct.boolean_size)
        exit_ack = data_struct.unpack_boolean(packed_data)
        return exit_ack

    def send_create_room(client_socket, player_number, room_name, full_player, player_name):
        selection = SELECT_CREATE
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)
        room_data = RoomData().room_data
        room_data['host_number'] = player_number
        room_data['room_name'] = room_name
        room_data['full_player'] = full_player
        room_data['player_name1'] = player_name
        create_room = data_struct.pack_room_data(room_data)
        client_socket.send(create_room)
        packed_can_make_room = client_socket.recv(data_struct.integer_size)
        return data_struct.unpack_integer(packed_can_make_room)

    def recv_lobby_data(client_socket):
        selection = SELECT_LOBBY
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)
        packed_room_count = client_socket.recv(data_struct.integer_size)
        room_count = data_struct.unpack_integer(packed_room_count)

        rooms_data = []

        for i in range(room_count):
            packed_room_data = client_socket.recv(data_struct.room_data_size)
            room_data = data_struct.unpack_room_data(packed_room_data)
            rooms_data.append(room_data)

        for room in rooms_data:
            print(room["room_name"])

        return rooms_data

    def send_join_room(client_socket, room_number, player_name):
        selection = SELECT_JOIN
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)
        join_request_data = {
            'room_number': room_number,
            'player_name': player_name
        }
        join_room = data_struct.pack_join_request_data(join_request_data)
        client_socket.send(join_room)

        packed_room_data = client_socket.recv(data_struct.room_data_size)
        room_data = data_struct.unpack_room_data(packed_room_data)

        if room_data['is_started'] == True: #3 = 시작 1 = 참가가능, 2 = 풀방
           return IS_STARTED
        elif (room_data['full_player'] == 4 and room_data['player_name4'] == 'default_name') or\
            (room_data['full_player'] == 3 and room_data['player_name3'] == 'default_name') or\
            (room_data['full_player'] == 2 and room_data['player_name2'] == 'default_name'):
            return CAN_JOIN
        else:
            return IS_FULL

    #Wait Room
    def send_in_room_data(client_socket, character_select, is_ready, is_exit, emotion):
        in_room_data = {
            'character_select': character_select,
            'is_ready': is_ready,
            'is_exit': is_exit,
            'emotion': emotion
        }
        packed_in_room_data = data_struct.pack_in_room_data(in_room_data)
        client_socket.send(packed_in_room_data)

    def receive_in_room_data(client_socket):
        packed_data = client_socket.recv(data_struct.in_room_data_server_size)
        in_room_data = data_struct.unpack_in_room_data_server(packed_data)
        return in_room_data

    def recv_exit_ack(client_socket):
        packed_data = client_socket.recv(data_struct.boolean_size)
        exit_ack = data_struct.unpack_boolean(packed_data)
        return exit_ack
