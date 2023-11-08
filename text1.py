import requests, json

url = "https://kauth.kakao.com/oauth/token"

data={
    "grant_type" : "authorization_code",
    "client_id" : "91f3461574c70ead1dd419c4c84ee728",
    "redirect_uri" : "https://localhost.com",
    "code" : "h-JgEvHTALXRTnL9wnRJkaFZn2Yg-9ydswIJA2_khQpvuQWrIyt7TglMZpTeC-34RSbwfwo9dRkAAAGBqD-6lw"
}
response = requests.post(url, data=data)

if response.status_code != 200:
    print("Error : ", response.json())
    # 요청 실패시 출력
else :
    token = response.json()
    print(token)
    # 성공시 토큰 출력
    
KAKAO_TOKEN_FILENAME = "./kakao_token.json"

def  save_tokens(filename, tokens):
    with open(filename, 'w') as fp :
        json.dump(tokens, fp)
        
save_tokens(KAKAO_TOKEN_FILENAME, token)