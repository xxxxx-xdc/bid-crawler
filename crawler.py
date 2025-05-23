
import json
from datetime import datetime

# 더미 데이터 생성 (실제 크롤링으로 교체 가능)
data = [
    {
        "title": "충남 천안시 보도블럭 정비공사",
        "region": "충남",
        "field": "토목",
        "amount": "2.1억",
        "dueDate": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "title": "서울시청 본관 내진보강 공사",
        "region": "서울",
        "field": "건축",
        "amount": "5.8억",
        "dueDate": (datetime.now().replace(day=datetime.now().day + 1)).strftime("%Y-%m-%d")
    }
]

# JSON 저장
with open("bid-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
