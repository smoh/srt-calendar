# srt-calendar

Script to generate an iCalendar file (.ics) for booked trains on SRT (수서고속철도).

[SRTrain](https://github.com/ryanking13/SRT)을 이용하여 구매/예약한 열차 일정을 ics 파일로 생성합니다.
이 파일을 호스팅하면 구글 캘린더 등에서 구독할 수 있습니다.

## Usage
```sh
SRT_IDEN=your_id SRT_PASSWORD=your_password python generate_ics.py --out calendar.ics
```

일정 제목 형식: `[<예약>]출발→도착: 호차-(좌석)`

github / gitlab CI/CD 워크플로우 예시가 있습니다.

NOTE: 구글 캘린더 구독은 자주 변하지 않는 일정을 가정해 개발되었기 때문에 소스파일 업데이트 이후 동기화까지 최대 24시간이 걸릴 수 있습니다.
