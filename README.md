# 1. proot-distro 설치
pkg install proot-distro
proot-distro install ubuntu
proot-distro login ubuntu

# --- 아래부터 Ubuntu 안 ---

# 2. 기본 패키지
apt update && apt install -y python3 python3-pip git curl

# 3. uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 4. 레포 클론 및 설치 (tls-client/curl_cffi 제외)
git clone https://github.com/elikese/myTrail && cd srtgo
uv pip install -e .

# 5. 실행
srtgo
