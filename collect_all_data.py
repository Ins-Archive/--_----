# -*- coding: utf-8 -*-

import os
import re
import time
import traceback
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------
# 공통 설정
# -----------------------------
KEYWORDS = ["민원", "분쟁", "유의사항", "사례"]
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime.now()
SAVE_DIR = "보험_보도자료_아카이브"
TIMEOUT = 25
SLEEP_SHORT = 1.0
SLEEP_LONG = 2.0
MIN_FULL_LOAD_WAIT = 10.0


def ensure_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def create_driver():
    options = Options()
    # 헤드리스 모드를 일부러 끄고 실제 브라우저 창이 뜨게 설정합니다.
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--lang=ko-KR")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(TIMEOUT + 10)
    return driver


def safe_url(url: str) -> str:
    if not url:
        return ""
    clean = str(url).strip()
    parsed = urlparse(clean)
    if parsed.scheme not in ("http", "https"):
        return ""
    return clean


def safe_driver_get(driver: webdriver.Chrome, url: str):
    target = safe_url(url)
    if not target:
        raise ValueError(f"유효하지 않은 URL입니다: {url}")
    driver.get(target)
    wait_for_full_page_load(driver, reason=f"URL 이동: {target}")


def wait_for_full_page_load(driver: webdriver.Chrome, reason: str = ""):
    start = time.time()
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    # 요청사항: 페이지 전체 로딩을 최소 10초 이상 충분히 기다립니다.
    elapsed = time.time() - start
    if elapsed < MIN_FULL_LOAD_WAIT:
        time.sleep(MIN_FULL_LOAD_WAIT - elapsed)
    else:
        time.sleep(SLEEP_SHORT)
    title = (driver.title or "").strip()
    print(f"[로딩완료] 현재 페이지 제목은 [{title}]입니다. ({reason})")


def switch_to_best_frame_if_needed(driver: webdriver.Chrome):
    driver.switch_to.default_content()
    frames = driver.find_elements(By.XPATH, "//frame|//iframe")
    if not frames:
        print("[프레임탐색] 프레임이 없어 기본 문서에서 진행합니다.")
        return
    print(f"[프레임탐색] frame/iframe {len(frames)}개 발견, 목록이 많은 프레임으로 진입 시도")
    best_idx = -1
    best_count = -1
    for i in range(len(frames)):
        try:
            driver.switch_to.default_content()
            frames_now = driver.find_elements(By.XPATH, "//frame|//iframe")
            driver.switch_to.frame(frames_now[i])
            count = len(driver.find_elements(By.XPATH, "//a[string-length(normalize-space(text())) > 0]"))
            print(f"[프레임탐색] 프레임 {i} 내 텍스트 링크 {count}개")
            if count > best_count:
                best_count = count
                best_idx = i
        except Exception:
            continue
    if best_idx >= 0:
        driver.switch_to.default_content()
        frames_now = driver.find_elements(By.XPATH, "//frame|//iframe")
        driver.switch_to.frame(frames_now[best_idx])
        print(f"[프레임진입] 프레임 {best_idx}로 진입 완료")
    else:
        driver.switch_to.default_content()
        print("[프레임진입] 유효 프레임을 찾지 못해 기본 문서 유지")


def force_scroll_and_click(driver: webdriver.Chrome, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.4)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)
    wait_for_full_page_load(driver, reason="버튼 클릭 후")


def collect_text_links_anywhere(driver: webdriver.Chrome):
    # 요청사항: 특정 테이블 경로 대신 '글자가 포함된 모든 링크'를 넓게 탐색합니다.
    elems = driver.find_elements(By.XPATH, "//a[@href and string-length(normalize-space(text())) > 0]")
    links = []
    for e in elems:
        href = (e.get_attribute("href") or "").strip()
        text = (e.text or "").strip()
        if href and text and href.lower().startswith(("http://", "https://")):
            links.append((href, text))

    uniq = []
    seen = set()
    for href, text in links:
        key = (href, text)
        if key not in seen:
            seen.add(key)
            uniq.append((href, text))
    print(f"[목록탐색] 목록을 {len(uniq)}개 발견했습니다.")
    return uniq


def sanitize_name(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:120]


def has_keyword(title: str) -> bool:
    return any(k in (title or "") for k in KEYWORDS)


def parse_date(text: str):
    if not text:
        return None
    m = re.search(r"(20\d{2})[.\-/년\s]*(\d{1,2})[.\-/월\s]*(\d{1,2})", text)
    if not m:
        return None
    y, mm, dd = map(int, m.groups())
    try:
        return datetime(y, mm, dd)
    except ValueError:
        return None


def in_range(dt: datetime) -> bool:
    return dt is not None and START_DATE <= dt <= END_DATE


def download_pdf(pdf_url: str, file_path: str):
    safe_pdf = safe_url(pdf_url)
    if not safe_pdf:
        print(f"[건너뜀] 잘못된 PDF URL: {pdf_url}")
        return
    try:
        with requests.get(safe_pdf, timeout=TIMEOUT, stream=True) as resp:
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"[저장완료] {file_path}")
    except Exception as e:
        print(f"[다운로드실패] {safe_pdf} / {e}")


def extract_title_and_date(soup: BeautifulSoup):
    title_candidates = [
        "h3", ".subject", ".title", ".view_tit", ".board_view_title", "th.subject",
    ]
    date_candidates = [
        ".date", ".regDate", ".info", ".view_info", ".board_view_info", "td", "li",
    ]

    title = ""
    for sel in title_candidates:
        node = soup.select_one(sel)
        if node and node.get_text(strip=True):
            title = node.get_text(" ", strip=True)
            break

    date_text = ""
    for sel in date_candidates:
        node = soup.select_one(sel)
        if node and node.get_text(strip=True):
            txt = node.get_text(" ", strip=True)
            if re.search(r"20\d{2}", txt):
                date_text = txt
                break

    return title, parse_date(date_text)


def save_detail_pdfs(source_prefix: str, post_url: str, title: str, post_date: datetime):
    try:
        res = requests.get(post_url, timeout=TIMEOUT)
        res.raise_for_status()
    except Exception as e:
        print(f"[상세요청실패] {post_url} / {e}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    pdf_links = soup.select("a[href$='.pdf'], a[href*='download'], a[href*='fileDown']")
    if not pdf_links:
        return

    date_part = post_date.strftime("%Y%m%d")
    safe_title = sanitize_name(title)

    for idx, a in enumerate(pdf_links, 1):
        href = (a.get("href") or "").strip()
        full_pdf = urljoin(post_url, href)
        suffix = f"_{idx}" if len(pdf_links) > 1 else ""
        filename = f"{source_prefix}{date_part}_{safe_title}{suffix}.pdf"
        file_path = os.path.join(SAVE_DIR, filename)
        download_pdf(full_pdf, file_path)
        time.sleep(SLEEP_SHORT)


def crawl_fss():
    print("\n===== 금감원 수집 시작 =====")
    driver = create_driver()
    visited = set()
    list_url = "https://www.fss.or.kr/fss/bbs/B0000188/list.do?menuNo=200218"

    try:
        safe_driver_get(driver, list_url)
        switch_to_best_frame_if_needed(driver)

        while True:
            wait_for_full_page_load(driver, reason="금감원 목록 페이지")
            post_links = collect_text_links_anywhere(driver)
            if not post_links:
                break

            stop_old = False
            for post_url, link_text in post_links:
                if post_url in visited:
                    continue
                visited.add(post_url)

                try:
                    r = requests.get(post_url, timeout=TIMEOUT)
                    r.raise_for_status()
                    dsoup = BeautifulSoup(r.text, "html.parser")
                    title, pdate = extract_title_and_date(dsoup)
                    if not title:
                        title = link_text
                    if pdate and pdate < START_DATE:
                        stop_old = True
                        continue
                    if not title or not has_keyword(title) or not in_range(pdate):
                        continue
                    save_detail_pdfs("[금감원]", post_url, title, pdate)
                except Exception as e:
                    print(f"[금감원-게시글오류] {post_url} / {e}")

            if stop_old:
                print("[금감원] 기간 이전 자료 발견으로 종료")
                break

            try:
                next_candidates = driver.find_elements(
                    By.XPATH,
                    "//a[contains(@class,'next') or contains(.,'다음') or contains(@title,'다음') or contains(.,'>')]",
                )
                if not next_candidates:
                    break
                print("[페이지이동] 다음 버튼을 찾아 스크롤 후 클릭합니다.")
                force_scroll_and_click(driver, next_candidates[0])
                switch_to_best_frame_if_needed(driver)
            except TimeoutException:
                break
    finally:
        driver.quit()
        print("===== 금감원 수집 종료 =====")


def collect_association_post_links(driver):
    return collect_text_links_anywhere(driver)


def crawl_association(name: str, prefix: str, list_url: str):
    print(f"\n===== {name} 수집 시작 =====")
    driver = create_driver()
    visited = set()

    try:
        safe_driver_get(driver, list_url)
        page_count = 0
        while True:
            page_count += 1
            wait_for_full_page_load(driver, reason=f"{name} 목록 페이지")
            post_links = collect_association_post_links(driver)
            if not post_links:
                print(f"[{name}] 목록 링크를 찾지 못했습니다. URL 또는 구조를 확인하세요.")
                break

            stop_old = False
            for post_url, title_text in post_links:
                if post_url in visited:
                    continue
                visited.add(post_url)

                try:
                    r = requests.get(post_url, timeout=TIMEOUT)
                    r.raise_for_status()
                    dsoup = BeautifulSoup(r.text, "html.parser")
                    title, pdate = extract_title_and_date(dsoup)
                    if not title:
                        title = title_text
                    if pdate and pdate < START_DATE:
                        stop_old = True
                        continue
                    if not has_keyword(title) or not in_range(pdate):
                        continue
                    save_detail_pdfs(prefix, post_url, title, pdate)
                except Exception as e:
                    print(f"[{name}-게시글오류] {post_url} / {e}")

            if stop_old:
                print(f"[{name}] 기간 이전 자료 발견으로 종료")
                break

            # 다음 페이지 이동도 XPath로 폭넓게 탐색합니다.
            next_xpath = (
                "//a[contains(@class,'next') or contains(.,'다음') or contains(@title,'다음') or contains(.,'>')]"
            )
            next_buttons = driver.find_elements(By.XPATH, next_xpath)
            if not next_buttons:
                break

            try:
                print(f"[{name}] 다음 버튼을 스크롤해서 클릭합니다.")
                force_scroll_and_click(driver, next_buttons[0])
            except WebDriverException:
                break

            # 무한 루프 방지용 안전장치입니다.
            if page_count >= 100:
                print(f"[{name}] 페이지 상한(100) 도달로 종료")
                break
    finally:
        driver.quit()
        print(f"===== {name} 수집 종료 =====")


def main():
    ensure_dir()

    agencies = [
        ("금감원", crawl_fss),
        ("손보협", lambda: crawl_association("손보협", "[손보협]", "https://www.knia.or.kr/home/board/boardList.do?menuId=57")),
        ("생보협", lambda: crawl_association("생보협", "[생보협]", "https://www.klia.or.kr/service/board/list.do?bbsId=BBSMSTR_000000000001")),
    ]

    for agency_name, runner in agencies:
        try:
            runner()
        except Exception as e:
            print(f"\n[기관오류] {agency_name} 수집 중 오류 발생: {e}")
            traceback.print_exc()
            print(f"[진행계속] {agency_name} 실패 후 다음 기관으로 이동합니다.")
            continue

    print("\n모든 기관 수집 작업이 종료되었습니다.")


if __name__ == "__main__":
    main()
