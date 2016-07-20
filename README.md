# Nanum



## 프로젝트 복사

#### Repository 복사
```
$ git clone https://github.com/LandvibeDev/Nanum-backend.git
```
#### dev branch 변경
```
$ cd Nanum-backend
$ git branch
*master
$ git checkout dev
```
#### 변경된 branch 확인
```
$ git branch
* dev
master
```

#### 가상환경 생성 (pyenv 사용)
```
$ pyenv virtualenv 3.5.1 nanum
$ pyenv activate nanum

```
#### 의존성 관리
```
(nanum)$ pip install -r requirements.txt

```

## 배포 (Deployment)

>DB 서버가 실행 중이어야 한다!!! (실수 자주함)
```
(nanum)$ python manage.py runserver --settings=nanum.settings.local
```


> 모든 python manage.py [command] 사용시 뒤에 --settings=nanum.settings.local 붙혀야함
```
예시)
(nanum)$ python manage.py makemigrations --settings=nanum.settings.local
```

## 변경사항 커밋
```
$ git commit -a -m 'message'
$ git push origin dev
```





markdown 문법
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet