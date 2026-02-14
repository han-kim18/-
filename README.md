# 🍗 배그 치킨 벌칙 디스코드 봇

배그에서 꼴등한 팀은 치킨을 먹어야 합니다! 디스코드에서 바로바로 벌칙 관리하세요.

## 📋 기능

- `/벌칙추가` - 게임 끝나고 꼴등 팀 바로 등록
- `/인증` - 치킨 먹고 인증하기
- `/벌칙목록` - 누가 아직 안 먹었는지 확인
- `/치킨통계` - 개인별 치킨 먹은 횟수 통계
- `/인증취소` - 실수로 인증했을 때 취소
- `/벌칙삭제` - 잘못 등록한 벌칙 삭제 (관리자만)

---

## 🚀 Railway로 무료 배포하기 (추천! 24시간 작동)

### 1단계: GitHub 저장소 만들기

1. https://github.com 로그인
2. 오른쪽 위 **"+" → "New repository"** 클릭
3. Repository name: `chicken-bot` 입력
4. **Public** 선택
5. **"Create repository"** 클릭
6. 이 파일들 업로드:
   - `discord_chicken_bot.py`
   - `requirements.txt`
   - `.env.example`
   - `README.md`

### 2단계: 디스코드 봇 만들기

1. https://discord.com/developers/applications 접속
2. **"New Application"** 클릭
3. 이름: "치킨벌칙봇" 입력
4. 왼쪽 메뉴 **"Bot"** 클릭
5. **"Reset Token"** 클릭하고 토큰 복사 (나중에 사용!)
6. 아래로 스크롤:
   - ✅ **MESSAGE CONTENT INTENT** 켜기
   - ✅ **SERVER MEMBERS INTENT** 켜기
7. 왼쪽 메뉴 **"OAuth2" → "URL Generator"** 클릭
8. SCOPES:
   - ✅ `bot`
   - ✅ `applications.commands`
9. BOT PERMISSIONS:
   - ✅ `Send Messages`
   - ✅ `Embed Links`
   - ✅ `Read Message History`
10. 맨 아래 생성된 URL 복사 → 브라우저 새 탭에 붙여넣기
11. 봇 추가할 서버 선택

### 3단계: Railway 배포

1. https://railway.app 접속
2. **"Login With GitHub"** 클릭 (GitHub 계정으로 로그인)
3. **"New Project"** 클릭
4. **"Deploy from GitHub repo"** 선택
5. 방금 만든 **`chicken-bot`** 저장소 선택
6. 자동으로 배포 시작! (1~2분 소요)

### 4단계: 환경 변수 설정

1. Railway 대시보드에서 프로젝트 클릭
2. **"Variables"** 탭 클릭
3. **"New Variable"** 클릭
4. Variable name: `DISCORD_TOKEN`
5. Value: 2단계에서 복사한 봇 토큰 붙여넣기
6. **"Add"** 클릭
7. 자동으로 재배포됨

### 5단계: 확인

- Railway 대시보드에서 **"Deployments"** 탭 확인
- "Success" 표시 뜨면 성공!
- 디스코드 서버에서 봇이 온라인 상태인지 확인
- `/치킨도움말` 입력해서 테스트

🎉 **완료!** 이제 24시간 봇이 작동합니다!

---

## 💻 로컬에서 테스트하기 (선택사항)

### 설치

```bash
# 패키지 설치
pip install -r requirements.txt

# .env 파일 만들기
cp .env.example .env
# .env 파일 열어서 봇 토큰 입력
```

### 실행

```bash
python discord_chicken_bot.py
```

---

## 💡 사용 예시

### 게임 끝나고 꼴등 팀 등록
```
/벌칙추가 팀원들:철수,영희,민수,지혜
```
또는 날짜 지정:
```
/벌칙추가 팀원들:철수,영희 날짜:2024-01-15
```

### 치킨 먹고 인증
```
/인증 벌칙id:1
```
(벌칙 ID는 `/벌칙목록`에서 확인)

### 미인증 벌칙 확인
```
/벌칙목록 상태:미인증
```

### 개인별 통계
```
/치킨통계
```

---

## 📊 데이터 저장

모든 데이터는 `chicken_penalties.json` 파일에 자동 저장됩니다.
Railway에서는 영구 저장소를 사용하지 않으므로, 중요한 데이터는 주기적으로 백업하세요.

**백업 방법:**
1. Railway 대시보드에서 프로젝트 클릭
2. "Data" 탭에서 `chicken_penalties.json` 다운로드

---

## 🔧 문제 해결

**봇이 온라인 안 돼요**
- Railway Variables에서 `DISCORD_TOKEN` 확인
- Discord Developer Portal에서 토큰이 맞는지 확인
- Railway Deployments 탭에서 에러 로그 확인

**명령어가 안 나와요**
- 봇이 온라인인지 확인
- 슬래시 명령어 `/`로 시작하는지 확인
- 봇에게 메시지 보낼 권한이 있는지 확인

**Railway 무료 크레딧이 부족해요**
- 매월 $5 크레딧 제공 (작은 봇은 충분함)
- 다른 무료 대안: Render.com, Fly.io

---

## 🎮 꿀팁

1. **전용 채널 만들기**: "치킨-벌칙" 채널 만들어서 여기서만 사용
2. **역할 설정**: 관리자만 삭제할 수 있게 권한 설정
3. **알림 설정**: 미인증 벌칙 있으면 @멘션으로 알림 (추후 추가 가능)

---

## 📝 라이선스

자유롭게 사용하세요! 수정도 가능합니다.

## 🆘 도움이 필요하면

- GitHub Issues에 문의
- 디스코드 서버 관리자에게 연락
