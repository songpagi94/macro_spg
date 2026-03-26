"""로그인/텔레그램/카드/역/옵션 설정 핸들러."""

import logging
import re

import inquirer

from ...config.constants import DEFAULT_STATIONS, STATIONS
from ...config.settings import (
    delete_rail_credential, delete_telegram_config,
    get_card_info, get_options, get_rail_credential,
    get_station_setting, get_telegram_config,
    set_card_info, set_options, set_rail_credential,
    set_station_setting, set_telegram_config,
)
from ...service.notification import send_telegram
from ..prompts import (
    card_prompt, login_prompt, options_checkbox_prompt,
    station_checkbox_prompt, station_text_prompt, telegram_prompt,
)

logger = logging.getLogger(__name__)


def _create_with_creds(rail_type: str, user_id: str, password: str, debug: bool):
    if rail_type == "SRT":
        from ...rail.srt.client import SRT
        return SRT(user_id, password, verbose=debug)
    else:
        from ...rail.ktx.client import Korail
        return Korail(user_id, password, verbose=debug)


def handle_set_login(rail_type: str, debug: bool = False) -> bool:
    print(f"\n--- {rail_type} 로그인 설정 ---")
    try:
        user_id = input(f"{rail_type} 아이디 (멤버십/이메일/번호): ").strip()
        password = input(f"{rail_type} 패스워드: ").strip()
        
        if not user_id or not password:
            return False

        rail = _create_with_creds(rail_type, user_id, password, debug)
        if not rail.is_login:
            raise RuntimeError("로그인에 실패했습니다.")
            
        set_rail_credential(rail_type, user_id, password)
        print("✅ 로그인 설정 완료!")
        return True
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def handle_set_telegram() -> bool:
    token, chat_id = get_telegram_config()
    result = inquirer.prompt(telegram_prompt(token or "", chat_id or ""))
    if not result:
        return False
    try:
        set_telegram_config(result["token"], result["chat_id"])
        send_telegram("[SRTGO] 텔레그램 설정 완료")
        return True
    except Exception as e:
        logger.error("텔레그램 설정 실패: %s", e)
        print(str(e))
        delete_telegram_config()
        return False


def handle_set_card() -> bool:
    print("\n--- 신용카드 설정 ---")
    try:
        number = input("신용카드 번호 (하이픈 제외): ").strip()
        password = input("카드 비밀번호 앞 2자리: ").strip()
        birthday = input("생년월일 (YYMMDD) / 사업자번호: ").strip()
        expire = input("카드 유효기간 (YYMM): ").strip()
        
        if not all([number, password, birthday, expire]):
            print("입력되지 않은 정보가 있어 설정을 취소합니다.")
            return False

        set_card_info(number, password, birthday, expire)
        logger.info("카드 설정 완료")
        print("✅ 카드 정보가 성공적으로 저장되었습니다.")
        return True
    except EOFError: # Ctrl+C 대응
        return False


def handle_set_station(rail_type: str) -> bool:
    stations = STATIONS[rail_type]
    station_key_str = get_station_setting(rail_type)
    default = station_key_str.split(",") if station_key_str else DEFAULT_STATIONS[rail_type]

    result = inquirer.prompt(station_checkbox_prompt(stations, default))
    if not result:
        return False
    selected = result["stations"]
    if not selected:
        print("선택된 역이 없습니다.")
        return False
    set_station_setting(rail_type, ",".join(selected))
    print(f"선택된 역: {','.join(selected)}")
    return True


def handle_edit_station(rail_type: str) -> bool:
    station_key_str = get_station_setting(rail_type) or ""
    result = inquirer.prompt(station_text_prompt(station_key_str))
    if not result:
        return False
    raw = result["stations"]
    if not raw:
        print("선택된 역이 없습니다.")
        return False

    selected = [s.strip() for s in raw.split(",")]
    hangul = re.compile("[가-힣]+")
    for station in selected:
        if not hangul.search(station):
            print(f"'{station}'는 잘못된 입력입니다. 기본 역으로 설정합니다.")
            selected = DEFAULT_STATIONS[rail_type]
            break

    set_station_setting(rail_type, ",".join(selected))
    print(f"선택된 역: {','.join(selected)}")
    return True


def handle_set_options() -> bool:
    current = get_options()
    result = inquirer.prompt(options_checkbox_prompt(current))
    if result is None:
        return False
    set_options(result.get("options", []))
    return True
