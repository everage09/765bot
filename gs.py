import gspread  # 구글 스프레드 시트 모듈
from google.oauth2.service_account import Credentials  # 보안인증 모듈


def GS():  # 스프레드 시트 불러오기
    gc = gspread.service_account(filename="Your file directory")
    sh = gc.open("전칠협이벤트기록")
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        '/Users/X5967T/AppData/Roaming/gspread/lucky-monument-320311-c8a8babc62f2.json',
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    return sh  # 스프레드 시트 오브젝트
