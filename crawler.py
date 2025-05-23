import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json
import time

# 오늘 날짜 기준 최근 1일
today = datetime.date.today()
from_date = (today - datetime.timedelta(days=1)).strftime('%Y/%m/%d')
to_date = today.strftime('%Y/%m/%d')

# 조건
keyword = '재해예방기술지도'
regions = ['충남', '충북', '세종', '대전']
results = []
page_no = 1
max_pages = 2
max_retries = 3

while page_no <= max_pages:
    url = 'https://www.g2b.go.kr:8101/ep/tbid/tbidList.do'
    params = {
        'bidSearchType': '1',
        'fromBidDt': from_date,
        'toBidDt': to_date,
        'recordCountPerPage': '100',
        'currentPageNo': str(page_no),
        'taskClCds': '5',
        'searchType': '1',
        'searchDtType': '1',
        'radOrgan': '1',
        'regYn': 'Y',
        'useTotalCount': 'Y'
    }

    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url, params=params, timeout=20)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'summary': '입찰공고 목록'})
            if not table:
                print("공고 테이블이 없습니다. 종료합니다.")
                break

            df = pd.read_html(str(table))[0]

            df_filtered = df[
                df['공고명'].str.contains(keyword, na=False) &
                df['수요기관'].str.contains('|'.join(regions), na=False)
            ]

            for _, row in df_filtered.iterrows():
                results.append({
                    'title': row['공고명'],
                    'organization': row['수요기관'],
                    'budget': row.get('배정예산', ''),
                    'dueDate': row['입찰마감일시']
                })
            break  # 성공하면 retry 루프 종료

        except Exception as e:
            attempt += 1
            print(f"{attempt}번째 시도 실패: {e}")
            time.sleep(5)

    page_no += 1

# 결과 저장
with open('bid-data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
