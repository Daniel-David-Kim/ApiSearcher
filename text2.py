import requests, json, datetime, os
KAKAO_TOKEN_FILENAME = "./resource/json/kakao_token.json"

def save_tokens(filename, tokens):
    with open(filename, 'w') as fp:
        json.dump(tokens, fp)

def load_tokens(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        tokens = json.load(fp)
        return tokens

def update_tokens(app_key, filename):
    tokens = load_tokens(filename)

    url = "https://kauth.kakao.com/oauth/token"
    data={
        "grant_type" : "refresh_token",
        "client_id" : app_key,
        "refresh_token" : tokens['refresh_token']
        }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Error : ", response.json())
        tokens = None
        # 요청 실패시
    else :
        # 기존 파일 백업
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = filename+"."+now
        os.rename(filename, backup_filename)
        tokens['access_token'] = response.json()['access_token']
        save_tokens(filename, tokens)
    return tokens

# 토큰 업데이트 예시
KAKAO_APP_KEY = "91f3461574c70ead1dd419c4c84ee728"
tokens = update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)
save_tokens(KAKAO_TOKEN_FILENAME, tokens)