import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json

# 검색 기간 설정 (최근 7일)
today = datetime.date.today()
from_date = (today - datetime.timedelta(days=7)).strftime('%Y/%m/%d')
to_date = today.strftime('%Y/%m/%d')

# 핵심 키워드
keywords = ['재해예방기술지도']

# 결과 저장 리스트
results = []
page_no = 1

while True:
    url = 'https://www.g2b.go.kr:8101/ep/tbid/tbidList.do'
    params = {
        'bidSearchType': '1',
        'fromBidDt': from_date,
        'toBidDt': to_date,
        'recordCountPerPage': '100',
        'currentPageNo': str(page_no),
        'taskClCds': '5',  # 용역
        'searchType': '1',
        'searchDtType': '1',
        'radOrgan': '1',
        'regYn': 'Y',
        'useTotalCount': 'Y'
    }

    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'summary': '입찰공고 목록'})
    if not table:
        break

    df = pd.read_html(str(table))[0]

    df_filtered = df[df['공고명'].str.contains('|'.join(keywords), na=False)]

    for _, row in df_filtered.iterrows():
        result = {
            'title': row['공고명'],
            'organization': row['수요기관'],
            'budget': row.get('배정예산', ''),
            'dueDate': row['입찰마감일시']
        }
        results.append(result)

    page_no += 1

# JSON 저장
with open('bid-data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
