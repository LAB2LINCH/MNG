from Data.C_RoomData import RoomData
from  Data.C_PlayerData import PlayerData

from Data.C_WaittingRoomData import WaittingRoomData


class GameSysMain:


    def __init__(self):
        self.is_game_over = False

        self.players_data = []
        self.waitting_room_data = WaittingRoomData().waitting_room_data
        #self.rooms_data= [RoomData() for RoomData() in range(1,5)]

        self.rooms_data= [RoomData() for i in range(5)]
        self.maxroomcount = 4
        self.player_count = 0
        self.players_data = []
        self.is_start=False
        self.ready_state = 0b0000


    def init_game_sys(self):
        self.is_game_over = False

    def exist_room_count(self):
        count = 0
        for room in self.rooms_data:
            if room.is_room_exist():
                count += 1
        return count

    def join_player(self,player_data):
        self.players_data.append(player_data)
        (self.waitting_room_data)['player_count']+=1
        print('플레이어',(self.waitting_room_data)['player_count'],'가 접속했습니다.')
