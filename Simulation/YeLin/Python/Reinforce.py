import socket
from threading import Thread
import threading
import time
import random
import gym
from gym import spaces
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.callbacks import ModelIntervalCheckpoint, FileLogger

from face_module import faceDetect
##### Face Module #####
import cv2
##### Face Module #####
HOST = '192.168.0.26'
PORT = 8585

recv_packet = []
mode = []
lock = threading.Lock()
condition_recv = threading.Condition()
condition_send = threading.Condition()

Actions = 20  # action 가짓수
Spaces = [5, 5, 5, 2, 2, 6, 5, 5, 2, 8]  # state종류와 각 종류별 가짓수
pre_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Hungry_Para = 0
Tired_Para = 0
Touch_Sensor = 0
Force_Sensor = 0
Lift_Sensor = 0
Oled_State = 0
Fin_State = 0
Tail_State = 0
Face_Detect = 0
Reward = 0
STT_Mode = 0

step_cnt = 0

class ComebotEnv(gym.Env):  # gym.Env 상속

    def __init__(self, cv_send, cv_recv, mode=None):
        self.action_space = spaces.Discrete(Actions)  # action 갯수만큼 불연속적인 값들로 이루어진 action_space 생성
        self.observation_space = spaces.MultiDiscrete(Spaces)  # 각 state별 상태갯수만큼 불연속적인 값들로 이루어진 observation_space 생성
        self.cv_send = cv_send
        self.cv_recv = cv_recv
        self.Hungry_Para = 0
        self.Tired_Para = 0
        self.Touch_Sensor = 0
        self.Force_Sensor = 0
        self.Lift_Sensor = 0
        self.Oled_State = 0
        self.Fin_State = 0
        self.Tail_State = 0
        self.Face_Detect = 0
        self.Reward = 0
        self.STT_Mode = 0

        if mode is None:
            self.mode = []
        else:
            self.mode = mode
        self.mode = mode

    def reset(self):
        # 새로운 episode가 시작됨에 따라 환경 초기화하는 부분
        print('----reset----')
        self.done = False
        self.cnt = 0
        self.reward = 0
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 초기 observation(=state)반환

    def step(self, action):
        global recv_packet
        global pre_state
        global step_cnt
        # action을 수행하고 변화된 state, reward, episode 종료여부 등을 반환하는 부분
        print('\n\n----step----')

        self.mode.clear()
        self.mode.append(action)
        print("mode: ", self.mode)
        self.cv_send.acquire()
        self.cv_send.notifyAll()
        self.cv_send.release()

        self.cv_recv.acquire()
        self.cv_recv.wait()
        self.cv_recv.release()

        if recv_packet[0] == "ID:":
            pass
        else:
            print("packet: ", recv_packet)
            self.Hungry_Para = int(int(recv_packet[1]) / 25)
            self.Tired_Para = int(int(recv_packet[2]) / 25)
            self.Touch_Sensor = int(recv_packet[3][2])
            self.Force_Sensor = int(recv_packet[4][2])
            self.Lift_Sensor = int(recv_packet[5][2])
            self.Oled_State = int(recv_packet[6][2])
            self.Fin_State = int(recv_packet[7][2])
            self.Tail_State = int(recv_packet[8][2])
            self.Face_Detect = 0
            #self.Face_Detect = int(faceDetect())
            #self.Face_Detect = int(recv_packet[10])
            self.Reward = int(recv_packet[11])
            self.STT_Mode = int(recv_packet[12])
            print("Face: ",self.Face_Detect)

        obs = [self.Hungry_Para, self.Tired_Para,
               self.Touch_Sensor, self.Force_Sensor,
               self.Lift_Sensor, self.Oled_State,
               self.Fin_State, self.Tail_State,
               self.Face_Detect, self.STT_Mode]


        if pre_state[2] == 1:
            print('Head Touch!!!')
            if (pre_state[0] > 2 and pre_state[1] > 2):
                if action == 18 :
                    reward = 30
                elif (action > 6 and action < 18):
                    reward = -10
                else:
                    reward = -5
            elif (pre_state[0] == 2 and pre_state[1] == 2):
                if action == 6 :
                    reward = 30
                elif (action > 6 and action < 18):
                    reward = -10
                else:
                    reward = -5
            elif (pre_state[0] == 1 and pre_state[1] == 1):
                if action == 7 :
                    reward = 30
                elif (action < 7 or action > 17):
                    reward = -10
                else:
                    reward = -5
            else:
                if action == 12:
                    reward = 30
                elif (action < 7 or action > 17):
                    reward = -10
                else:
                    reward = -5
        elif pre_state[2] == 2:
            print('Fin Touch!!!')
            if (pre_state[0] > 2 and pre_state[1] > 2):
                if action == 1 :
                    reward = 30
                elif (action > 6 and action < 18):
                    reward = -10
                else:
                    reward = -5
            elif (pre_state[0] == 2 and pre_state[1] == 2):
                if action == 3 :
                    reward = 30
                elif (action > 6 and action < 18):
                    reward = -10
                else:
                    reward = -5
            elif (pre_state[0] == 1 and pre_state[1] == 1):
                if action == 16 :
                    reward = 30
                elif (action < 7 or action > 17):
                    reward = -10
                else:
                    reward = -5
            else:
                if action == 9 :
                    reward = 30
                elif (action < 7 or action > 17):
                    reward = -10
                else:
                    reward = -5
        elif pre_state[2] == 3:
            print('Tail Touch!!!')
            if (pre_state[0] > 2 and pre_state[1] > 2):
                if action == 2:
                    reward = 30
                elif ((action > 3 and action < 11) or action > 17):
                    reward = -10
                else:
                    reward = -5
            elif (pre_state[0] == 2 and pre_state[1] == 2):
                if action == 15 :
                    reward = 30
                elif ((action > 3 and action < 11) or action > 17):
                    reward = -10
                else:
                    reward = -5
            elif (pre_state[0] == 1 and pre_state[1] == 1):
                if action == 17 :
                    reward = 30
                elif (action < 7 or action > 17):
                    reward = -10
                else:
                    reward = -5
            else:
                if action == 14:
                    reward = 30
                elif (action < 7 or action > 17):
                    reward = -10
                else:
                    reward = -5
        else:
            print('Not Touch!!!')
            if (pre_state[4] == 1):
                print('Lift!!!')
                if (pre_state[0] > 2 and pre_state[1] > 2):
                    if action == 4:
                        reward = 30
                    elif (action > 10 and action < 18):
                        reward = -10
                    else:
                        reward = -5
                elif (pre_state[0] == 2 and pre_state[1] == 2):
                    if action == 0:
                        reward = 30
                    elif (action > 10 and action < 18):
                        reward = -10
                    else:
                        reward = -5
                elif (pre_state[0] == 1 and pre_state[1] == 1):
                    if action == 8:
                        reward = 30
                    elif ((action > 3 and action < 7) or (action > 14 and action < 18)):
                        reward = -10
                    else:
                        reward = -5
                else:
                    if action == 11:
                        reward = 30
                    elif ((action > 3 and action < 7) or (action > 14 and action < 18)):
                        reward = -10
                    else:
                        reward = -5
            elif (pre_state[3] == 1):
                print('Force!!!')
                if (pre_state[0] > 2 and pre_state[1] > 2):
                    if action == 19:
                        reward = 30
                    elif (action > 10 and action < 18):
                        reward = -10
                    else:
                        reward = -5
                elif (pre_state[0] == 2 and pre_state[1] == 2):
                    if action == 7:
                        reward = 30
                    elif (action > 10 and action < 18):
                        reward = -10
                    else:
                        reward = -5
                elif (pre_state[0] == 1 and pre_state[1] == 1):
                    if action == 16:
                        reward = 30
                    elif ((action > 3 and action < 7) or (action > 14 and action < 18)):
                        reward = -10
                    else:
                        reward = -5
                else:
                    if action == 11:
                        reward = 30
                    elif ((action > 3 and action < 7) or (action > 14 and action < 18)):
                        reward = -10
                    else:
                        reward = -5
            elif(pre_state[9] == 1):
                print('text1')
                if action == 18:
                    reward = 30
                else:
                    reward = -10
            elif (pre_state[9] == 2):
                print('text2')
                if action == 19:
                    reward = 30
                else:
                    reward = -10
            elif (pre_state[9] == 3):
                print('text3')
                if action == 9:
                    reward = 30
                else:
                    reward = -10
            elif (pre_state[9] == 4):
                print('text4')
                if action == 7:
                    reward = 30
                else:
                    reward = -10
            elif (pre_state[9] == 5):
                print('text5')
                if action == 5:
                    reward = 30
                else:
                    reward = -10
            elif (pre_state[9] == 6):
                print('text6')
                if action == 2:
                    reward = 30
                else:
                    reward = -10
            elif (pre_state[9] == 7):
                print('text7')
                if action == 13:
                    reward = 30
                else:
                    reward = -10
            else:
                if (pre_state[0] > 2 and pre_state[1] > 2):
                    if ((action > 3 and action < 7) or action > 17):
                        reward = 10
                    else:
                        reward = -10
                elif (pre_state[0] == 2 and pre_state[1] == 2):
                    if action < 4:
                        reward = 10
                    else:
                        reward = -10
                elif (pre_state[0] == 1 and pre_state[1] == 1):
                    if action > 14 and action < 18:
                        reward = 10
                    else:
                        reward = -10
                else:
                    if (action > 6 or action < 15):
                        reward = -10
                    else:
                        reward = 10
        pre_state = obs
        print('obs:   ', obs, '       reward:', reward)

        # 20step이 1episode가 되도록 설정함, 추후에 변경가능
        print('step_cnt:',step_cnt)
        step_cnt += 1
        self.cnt += 1
        self.done = self.cnt > 9

        return obs, reward, self.done, {}  # state, reward, episode종료여부 반환


def build_model(state_size, num_actions):
    # Sequential()은 층을 나열해서 쌓을 때 사용, 이전층의 출력이 다음층의 출력으로 이어짐 (Linear stack layer)
    model = Sequential()
    # Flatten()은 state_size가 (10,) 10차원이므로 (1,10)로 일렬화해주는(1차원으로 바꿔주는) 레이어
    model.add(Flatten(input_shape=(1, state_size)))
    # 각 은닉층의 역할 뭔지???일수있나??
    model.add(Dense(30, activation='relu'))
    model.add(Dense(10, activation='relu'))
    #model.add(Dropout(0.3))
    # 출력노드의 개수는 num_actions=20개, linear활성화함수는 input을 그대
    # 로 return하는 함수
    # 각 action별 q값 그대로 출력
    model.add(Dense(num_actions, activation='linear'))
    # model.summary()
    return model


def build_callbacks(env_name):
    checkpoint_weights_filename = './weight/dqn_' + env_name + '_weights_{step}.h5f'
    log_filename = './weight/dqn_{}_log.json'.format(env_name)
    callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=500)]
    callbacks += [FileLogger(log_filename, interval=500)]
    return callbacks


def recvMsg(sock, cv_recv):
    global recv_packet
    global mode
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            recv_packet = []
            for data in data.decode().split(','):
                recv_packet.append(data)
            # print("face:",faceDetect())
            # mode.append(faceDetect())
            #print("recv::", recv_packet)#,"face:",Face_Detect)

            cv_recv.acquire()
            cv_recv.notifyAll()
            cv_recv.release()

            # for packet in recv_packet:
            #     # print (packet)
            #     if packet != 'ID:':
            #
            #     else:
            #         break
            #     cv_recv.acquire()
            #     cv_recv.notifyAll()
            #     cv_recv.release()
        except:
            pass


def sendMsg(sock, cv_send):
    global mode
    sock.send("rei".encode())
    while True:
        with cv_send:
            cv_send.acquire()
            cv_send.wait()
            cv_send.release()
            sock.send(str(mode[0]).encode())

def ReinForceThread(cv_send, cv_recv):
    global mode, recv_packet
    global Hungry_Para, Tired_Para, Touch_Sensor, Force_Sensor, Lift_Sensor, Oled_State, Fin_State, Tail_State, Face_Detect, Reward, STT_Mode
    while True:
        # Receive Mutex
        # cv_recv.acquire()
        # cv_recv.wait()
        # cv_recv.release()
        # Hungry_Para     = recv_packet[1]
        # Tired_Para      = recv_packet[2]
        # Touch_Sensor    = recv_packet[3]
        # Force_Sensor    = recv_packet[4]
        # Lift_Sensor     = recv_packet[5]
        # Oled_State      = recv_packet[6]
        # Fin_State       = recv_packet[7]
        # Tail_State      = recv_packet[8]
        # Face_Detect     = recv_packet[10]
        # Reward          = recv_packet[11]
        # STT_Mode     = recv_packet[12]
        # # Input
        # # Mode Control
        # if mode == 6:
        #     mode = 17
        # else :
        #     mode = 6
        # # Receive Mutex
        # cv_send.acquire()
        # cv_send.notifyAll()
        # cv_send.release()
        env = ComebotEnv(cv_send, cv_recv, mode)  # 코미봇환경 불러오기

        num_actions = env.action_space.n  # action 20가지
        state_space = env.observation_space.shape[0]  # state 10개 parameter
        # print(num_actions, state_space)

        model = build_model(state_space, num_actions)

        memory = SequentialMemory(limit=10000, window_length=1)

        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps',
                                      value_max=.8, value_min=.2, value_test=.1,
                                      nb_steps=10000)

        dqn = DQNAgent(model=model, nb_actions=num_actions,
                       gamma=0.7, batch_size=32,
                       memory=memory, nb_steps_warmup=700,
                       target_model_update=1e-7, policy=policy)
        # target_model_update 1e-2 --> 1e-7로 수정
        #dqn.compile(Adam(lr=0.01), metrics=['categorical_crossentropy'])
        dqn.compile(Adam(lr=0.01), metrics=['mse'])
        dqn.load_weights('./weight/dqn_comebot_weights(stt).h5f')
        dqn.test(env, nb_episodes=1000, visualize=False)
        # lr 0.01-->0.1로 수정 학습step수가 감소함에 따라
        # callbacks = build_callbacks('comebot_touch')
        # # 학습step수 1000단위로 학습되가는지 확인해보고 늘리기
        # hist = dqn.fit(env, nb_steps=10000,
        #                visualize=False,
        #                verbose=2,
        #                callbacks=callbacks)



        plt.show()



def TcpThread():
    # global recv_packet,mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        # Thread Init
        thread_recv = Thread(target=recvMsg, args=(sock, condition_recv))
        thread_send = Thread(target=sendMsg, args=(sock, condition_send))
        thread_rein = Thread(target=ReinForceThread, args=(condition_send, condition_recv))
        # thread_rein = Thread(target=reinforce, args=(condition_send, condition_recv,recv_packet,mode))
        thread_recv.daemon = True
        thread_send.daemon = True
        thread_rein.daemon = True
        thread_recv.start()
        thread_send.start()
        thread_rein.start()
        while (1):
            pass


if __name__ == "__main__":
    TcpThread()