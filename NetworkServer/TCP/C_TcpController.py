import socket
import threading
import time

from GameSys.C_GameSysMain import *
from Data.C_BulletData import *
from Data.C_EnemyData import *
from Data.C_PlayerData import *
from Data.C_RoomData import *
from Data.C_StructSet import *
from TCP.C_Pack import *

data_struct = Pack
game_sys_main = GameSysMain()

class TcpController:
    PORT = 19000
    IP = ''
    MAX_BIND = 5

    def tcp_server_init(self):
        TcpController.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TcpController.server_socket.bind((self.IP, self.PORT))
        TcpController.server_socket.listen(self.MAX_BIND)
        print('TCPServer Waiting for client on port %d'% self.PORT)
        print("=" * 50)
        print("[Thread version] 서버 초기화 완료")

    '''
    클라이언트의 접속을 accept()합니다.
    accept()되면 process_client쓰레드에 client소켓을 전달해주고 client소켓을 삭제합니다.
    '''
    def accept_loof(self):
        print("[정보] 접속 대기중...")
        print("=" * 50)
        while 1:
            client_socket, address = TcpController.server_socket.accept()
            print("I got a connection from ", address)
            t1 = threading.Thread(target=TcpController.process_client, args=(client_socket,))
            t1.start()

    '''
    클라이언트와 통신하는 스레드입니다.
    로직을 이안에 쓰는것은 지양합니다.
    함수를 호출하여 수정을 최소화 하세요.
    '''
    def process_client(client_socket):
        while 1:
            #테스트용으로 넣음 완성본에는 지울것임을 감안하시오.
            time.sleep(1)
            # todo :recv_player_data
            # todo :recv_bullet_data
            # todo :충돌체크하시오
            # todo :if isdameged
            TcpController.send_is_game_over(client_socket)
            # todo :gamelogic damaged
            # todo :send_player_data
            # todo :send_enemy_data
            # todo :send_bullet_data
            # todo :리더보드

    #Lobby
    def send_room_data(socket):
        packed_request_data = socket.recv(1)
        unpack_join_request_data = data_struct.unpack_join_request_data(packed_request_data)
        #방 정보를 모두 불러들이면 구현할필요 없음 (임시)
        for i in range(game_sys_main.exist_room_count()):
            if game_sys_main.rooms_data[i]['room_number'] == unpack_join_request_data['room_number']:
                packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
                socket.send(packed_room_data)
                if (game_sys_main.rooms_data[i]['full_player'] == 4 and
                            game_sys_main.rooms_data[i]['player_name4'] == 'default_name') or\
                    (game_sys_main.rooms_data[i]['full_player'] == 3 and
                             game_sys_main.rooms_data[i]['player_name3'] == 'default_name') or\
                    (game_sys_main.rooms_data[i]['full_player'] == 2 and
                             game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                    for i in range(2, 5):
                        if(game_sys_main.rooms_data[i]['full_player'] == 2):
                            game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data[1]
                            #언팩시 딕셔너리 형태 유지되는지 확인필요
                        if(game_sys_main.rooms_data[i]['full_player'] == 3):
                            if(game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                                game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data[1]
                            else:
                                game_sys_main.rooms_data[i]['player_name3'] = unpack_join_request_data[1]
                        if(game_sys_main.rooms_data[i]['full_player'] == 4):
                            if(game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                                game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data[1]
                            elif(game_sys_main.rooms_data[i]['player_name3'] == 'default_name'):
                                game_sys_main.rooms_data[i]['player_name3'] = unpack_join_request_data[1]
                            else:
                                game_sys_main.rooms_data[i]['player_name4'] = unpack_join_request_data[1]
                break

    def send_lobby_data(socket):
        room_count = game_sys_main.exist_room_count()
        packed_room_count = data_struct.pack_count_data(room_count)
        socket.send(packed_room_count)
        for i in range(room_count):
            packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
            socket.send(packed_room_data)

    def recv_create_room(socket):
        packed_create_room_data = socket.recv(1)
        create_room_data = data_struct.unpack_room_data(packed_create_room_data)
        if game_sys_main.exist_room_count() <= game_sys_main.MAXROOMCOUNT:
            game_sys_main.rooms_data[game_sys_main.exist_room_count()] = create_room_data



    def send_is_game_over(socket):
         # 게임결과를 보냅니다
         packed_is_game_over = data_struct.pack_is_game_over(game_sys_main.is_game_over)
         socket.send(packed_is_game_over)

    def exit(self):
        TcpController.server_socket.close()
        print("SOCKET closed... END")