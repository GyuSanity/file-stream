# file-stream




# 1. 도커 실행
> docker-compose up -d

# 2. fastapi 실행 (가상환경 생성 및 셋팅, WSL 전용)
> python3 -m venv venv --without-pip
> source venv/bin/activate
> pip install -r requirement.txt
> sudo apt remove python3-apt
> sudo apt install python3-apt
> export PATH=$PATH:$HOME/.local/bin
> pip install cffi --upgrade
> uvicorn main:app --reload --host 0.0.0.0 --port 8000

# FE 실행
 $ npm install -g @vue/cli
 $ vue create video-player-fe
 $ cd video-player-fe
 $ npm run serve