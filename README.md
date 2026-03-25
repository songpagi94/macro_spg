# 0. termux 다운로드 및 초기세팅
https://f-droid.org/ko/packages/com.termux/  
https://f-droid.org/ko/packages/com.termux.api/  
termux.api는 푸쉬알람 원하면 설치 (설정 > "play" 검색 > Google play 프로텍트에서 검사 일시중지해야 설치됨)  
termux-setup-storage  
pkg upgrade  

# 1. proot-distro 설치
pkg install proot-distro  
pd install ubuntu  
pd login ubuntu  

# 2. 기본 패키지
apt-get update && upgrade -y  
apt install python3 python3-pip git curl -y  

# 3. uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh  
source ~/.bashrc  

# 4. 레포 클론 및 설치 (tls-client/curl_cffi 제외)
git clone https://github.com/songpagi94/macro_spg  
uv pip install -e .  

# 5. 실행
srtgo  
