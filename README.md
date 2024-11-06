# 파이썬을 이용한 넷플릭스 데이터 수집하기

파이썬을 이용하여 넷플릭스 영화, TV 정보를 나라별로 수집합니다.

## 나라별 데이터 수집

🇦🇷 아르헨티나 argentina
🇦🇺 호주 australia
🇦🇹 오스트리아 austria
🇧🇸 바하마 bahamas
🇧🇭 바레인 bahrain
🇧🇩 방그라데시 bangladesh
🇧🇪 벨기에 belgium
🇧🇴 볼리비아 bolivia
🇧🇷 브라질 brazil
🇧🇬 불가리아 bulgaria
🇨🇦 캐나다 canada
🇨🇱 칠레 chile
🇨🇴 콜롬비아 colombia
🇨🇷 코스타리카 costa-rica
🇭🇷 크로아티아 croatia
🇨🇾 키프로스 cyprus
🇨🇿 체코 czech-republic
🇩🇰 덴마크 denmark
🇩🇴 도미니카 공화국 dominican-republic
🇪🇨 에콰도르 ecuador
🇪🇬 이집트 egypt
🇸🇻 엘살바도르 el-salvador
🇪🇪 에스토니아 estonia
🇫🇮 핀란드 finland
🇫🇷 프랑스 france
🇩🇪 독일 germany
🇬🇷 그리스 greece
🇬🇹 과테말라 guatemala
🇭🇳 온두라스 honduras
🇭🇰 홍콩 hong-kong
🇭🇺 헝가리 hungary
🇮🇸 아이슬란드 iceland
🇮🇳 인도 india
🇮🇩 인도네시아 indonesia
🇮🇱 이스라엘 israel
🇮🇹 이탈리아 italy
🇯🇲 자메이카 jamaica
🇯🇵 일본 japan
🇯🇴 요르단 jordan
🇰🇪 케냐 kenya
🇰🇼 쿠웨이트 kuwait
🇱🇻 라트비아 latvia
🇱🇧 레바논 lebanon
🇱🇹 리투아니아 lithuania
🇱🇺 룩셈부르크 luxembourg
🇲🇾 말레아시아 malaysia
🇲🇻 몰디브 maldives
🇲🇹 몰타 malta
🇲🇺 모리셔스 mauritius
🇲🇽 멕시코 mexico
🇲🇦 모로코 morocco
🇳🇱 네덜란드 netherlands
🇳🇿 뉴질랜드 new-zealand
🇳🇮 니카라과 nicaragua
🇳🇬 나이지리아 nigeria
🇳🇴 노르웨이 norway
🇴🇲 오만 oman
🇵🇰 파키스탄 pakistan
🇵🇦 파나마 panama
🇵🇾 파라과이 paraguay
🇵🇪 페루 peru
🇵🇭 필리핀 philippines
🇵🇱 폴란드 poland
🇵🇹 포르투갈 portugal
🇶🇦 카타르 qatar
🇷🇴 루마니아 romania
🇸🇦 사우디아라비아 saudi-arabia
🇷🇸 세르바이 serbia
🇸🇬 싱가포르 singapore
🇸🇰 슬로바키아 slovakia
🇸🇮 슬로베니아 slovenia
🇿🇦 남아프리카 공화국 south-africa
🇰🇷 대한민국 south-korea
🇪🇸 스페인 spain
🇱🇰 스링랑카 sri-lanka
🇸🇪 스웨덴 sweden
🇨🇭 스위스 switzerland
🇹🇼 대만 taiwan
🇹🇭 태국 thailand
🇹🇹 트리니다드 토바고 trinidad
🇹🇷 튀르키예 turkey
🇺🇦 우크라이나 ukraine
🇦🇪 아랍에미리트 united-arab-emirates
🇬🇧 영국 united-kingdom
🇺🇸 미국 united-states
🇺🇾 우루과이 uruguay
🇻🇪 베넬수엘라 venezuela
🇻🇳 베트남 vietnam

### Requests

HTTP 요청을 쉽게 할 수 있도록 해주는 라이브러리입니다. 이를 통해 웹 API와의 상호작용, 웹 페이지 데이터 수집 등 다양한 HTTP 작업을 간편하게 수행할 수 있습니다

```bash
pip install requests
```

### Selenium

Selenium은 웹 브라우저를 자동화하는 도구로, 웹 애플리케이션을 테스트하거나 데이터를 수집하는 데 많이 사용됩니다.

```bash
pip install selenium
```

### BeautifulSoup

BeautifulSoup은 HTML이나 XML 파일을 파싱하여 원하는 정보를 쉽게 추출할 수 있게 해주는 도구입니다. BeautifulSoup은 웹 크롤링과 스크래핑 작업에서 많이 사용되며, HTML 문서 구조를 파싱하여 특정 태그, 속성, 클래스 등을 통해 데이터를 추출할 수 있습니다.

```bash
pip install beautifulsoup4
```
