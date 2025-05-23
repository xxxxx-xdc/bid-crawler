import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json

# ✅ 1. 최근 1일 설정
today = datetime.date.today()
from_date = (today - datetime.timedelta(days=1)).strftime('%Y/%m/%d')
to_date = today.strftime('%Y/%m/%d')

# ✅ 2. 검색 키워드: 재해예방기술지도
keyword = '재해예방기술지도'

# ✅ 3. 지역 필터: 충남, 충북, 세종, 대전
regions = ['충남', '충북', '세종', '대전']

results = []
page_no = 1
max_pages = 2

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

    try:
        response = requests.get(url, params=params, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'summary': '입찰공고 목록'})
        if not table:
            break

        df = pd.read_html(str(table))[0]

        # ✅ 공고명에 키워드 포함 + 수요기관에 지역 포함 필터링
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

    except Exception as e:
        print(f"페이지 {page_no} 처리 중 오류 발생: {e}")
        break

    page_no += 1

with open('bid-data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
