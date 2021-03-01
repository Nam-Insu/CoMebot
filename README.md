# ComEBot

Communication_Emotion_Bot

## Project : Communication_Emotion_Bot (feat.BARAM)  
  
지도 교수 : 박광현 교수님  
참여 인원 : 16 강동운, 16 김찬혁, 16 남인수, 18 김예린, 18 이혜진  
참여 기간 : 2019.12 ~ 2020.6

## Development Background  
1인 가구가 급증함에 따라 반려동물을 찾는 사람들이 늘어났고,  
반려동물을 키우는 데에는 제약조건이 많아 Youtube랜선집사, 로봇펫 등의 수요가 늘어남.  
  
기존의 로봇펫의 동작이 특정상황에 있어 정해진 행동만을 수행하여  
시간이 지남에 따라 사용자의 관심도가 떨어지는 문제를 해결하기 위해   
강화학습을 이용하여 실제 애완동물을 훈련시키는 것처럼  
시간이 지남에 따라 행동이 학습되는 학습프로그램을 제작함  
  
## Main Feature  
1. 고래모양의 펫 하드웨어 모델링  
2. 모델링 파일을 불러와 V-rep 가상환경에 적용  
3. Keras Library를 사용한 강화학습(DQN) 환경구축 및 학습  
4. 펫의 상태를 확인하고 Reward를 줄 수 있는 GUI 제작  
5. Google STT API  
6. User FaceDetection  
7. 프로그램 간 Packet 통신
  
## Using Language  
1. V-rep Simulation : C++, Lua Script
2. ReinForce : Python
3. DataServer : Python
  
## System Architecture (BEFORE)
<img src="https://user-images.githubusercontent.com/52673977/73717132-40538480-475c-11ea-8513-fb641a1aa128.png" width="800" height="500" />  
  
## System Architecture (AFTER)
<img src="https://user-images.githubusercontent.com/52377778/86989541-962dcc00-c1d5-11ea-8c95-35a59bc03dde.PNG" width="800" height="500" />  
  
## Hardware Architecture
<img width="582" alt="hw" src="https://user-images.githubusercontent.com/52673977/77333956-83e36b80-6d67-11ea-809c-83a00d6180e6.png">  
  
## Project GIF  
학습프로그램 GUI  
![Comebot](https://user-images.githubusercontent.com/52377778/86989198-da6c9c80-c1d4-11ea-82a9-291e643d15d4.gif)  

