# fastapi pjt structure refactoring
강의 및 실습에서 진행한 fastapi 프로젝트 구조로 리팩토링한 프로젝트입니다.(+ 로깅도 추가했습니다.)

## 사용 방법
1. 도커 -> mysql 실행
2. datagrip db 연결
3. 터미널 -> LOG_LEVEL=DEBUG LOG_TO_FILE=1 LOG_FILE_PATH=app.log uv run uvicorn main:app --reload 입력
4. postman 또는 터미널 curl 명령어 사용으로 CRUD 진행

## 터미널 curl 명령어
curl -X POST -H "Content-Type: application/json" -d '{"name": "새로운 사용자", "email": "newuser@example.com"}' http://localhost:8000/users
