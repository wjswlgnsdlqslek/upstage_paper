# 요구 사항

0. 전체 파일 확인 해보기
1. fastapi 프로젝트 리팩토링 하고 싶어
2. fastapi를 처음 해봐서 main.py 파일에 로직 등을 다 작성했어.
3. 현재 프로젝트 구조는 생성해놨음
4. 생성된 프로젝트 구조에 맞춰서 리팩토링해줘


---
user(
{
id : int autoencrement primarykey not null,
name : varchar(50) not null,
email : varchar(100) unique not null,
created_at : datetime not null
})

chat(
{
id : int autoencrement primarykey not null,
user_id : varchar(50) not null,
role : varchar(50) not null,
message : varchar(500) not null,
created_at : datetime not null
})

todo(
{
id : int autoencrement primarykey not null,
content : varchar(100) not null,
created_at : datetime not null
})