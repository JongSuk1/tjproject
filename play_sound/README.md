Sound with speaker
=======================

### 블루투스 페어링 상태와 카메라 상태의 변경사항을 스피커로 출력해줍니다.

## 사용법

## version 1.0

#### BLE_check(a)
블루투스 페어링이 해제되었을 때는 0, 연결되었을 때는 1을 입력해주면 상황에 맞는 음성을 출력합니다.

#### CAM_check(a)
카메라가 풍경모드로 전환되었을 때는 0, 셀카모드로 전환되었을 때는 1을 입력해주면 상황에 맞는 음성을 출력합니다. 

## version 1.0.1
#### play_music(sound)
기존에는 일정 시간 기다리도록 한 것을 sound파일의 길이에 맞게 재생되도록 수정하였습니다.

## 음성 파일 다운로드
Link : www.soundoftext.com

## 필요한 Library
pygame
> installing pygame : **sudo apt-get install python-pygame**