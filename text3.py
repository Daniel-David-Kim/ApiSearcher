import requests, json
KAKAO_TOKEN_FILENAME = "./resource/json/kakao_token.json"

def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)
    return tokens

def send_message(text):
    tokens = load_tokens(KAKAO_TOKEN_FILENAME)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # Bearer 뒤에 띄어쓰기 한 칸 주의. 반드시 한 칸 띄워야 한다.
    headers ={
        "Authorization" : "Bearer " + tokens['access_token']
    }
    data ={
        "template_object" : json.dumps({
            "object_type" : "text",
            "text" : text,
            "link" : {
                "web_url" : "www.naver.com"
            }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)

    # requests 전송 성공시 200 코드값을 반환한다.
    if response.status_code != 200:
        print("Error : ", response.json())
    else :
        print("메시지 전송 성공")