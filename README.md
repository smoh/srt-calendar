# srt-calendar

Script to generate an iCalendar file (.ics) for booked trains on SRT (수서고속철도).

[SRTrain](https://github.com/ryanking13/SRT)을 이용하여 구매/예약한 열차 일정을 ics 파일로 생성합니다.
이 파일을 호스팅하면 구글 캘린더 등에서 구독할 수 있습니다.

## Usage
SRT_IDEN=your_id SRT_PASSWORD=your_password python generate_ics.py --out calendar.ics

일정 제목 형식: [<예약>]출발→도착: 호차-(좌석)
