# WeatherOfToday

오늘의 날씨 정보를 가져오고 AI로 응원 메시지를 생성하는 도구입니다.

## 개요

기상청 API를 사용하여 현재 날씨 정보를 가져오고, OpenAI API를 사용하여 날씨에 맞는 응원 메시지를 생성합니다.

## 주요 기능

- 기상청 초단기 예보 API 연동
- 날씨 정보 파싱 (기온, 습도, 하늘상태, 강수형태)
- OpenAI API를 통한 응원 메시지 생성
- XML 데이터 파싱

## 사용 방법

```bash
python WofT.py
```

## 요구사항

- Python 3.12
- requests
- xmltodict
- openai

## 설치

### uv 설치

#### Windows
```powershell
# PowerShell에서 실행
irm https://astral.sh/uv/install.ps1 | iex
```

#### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 후 터미널을 재시작하거나 다음 명령어로 PATH에 추가:
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

### 가상환경 설정

```bash
# Python 3.12 가상환경 생성
uv venv --python 3.12

# 가상환경 활성화
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 패키지 설치

```bash
# uv를 사용한 패키지 설치
uv pip install -r requirements.txt
```

## API 키 설정

### 기상청 API
코드 내에 기상청 API 키가 하드코딩되어 있습니다. 실제 사용 시 환경 변수로 관리하는 것을 권장합니다.

### OpenAI API
코드 내에 OpenAI API 키가 하드코딩되어 있습니다. 실제 사용 시:
1. 환경 변수로 설정: `export OPENAI_API_KEY='your-key'`
2. 또는 코드에서 직접 수정

## 파일 구조

- `WofT.py`: 메인 스크립트

## 기능 설명

1. **날씨 정보 수집**: 기상청 API에서 초단기 예보 데이터를 가져옵니다.
2. **데이터 파싱**: XML 형식의 데이터를 딕셔너리로 변환합니다.
3. **날씨 정보 포맷팅**: 사용자 친화적인 형식으로 날씨 정보를 표시합니다.
4. **AI 응원 메시지**: OpenAI API를 사용하여 날씨에 맞는 응원 메시지를 생성합니다.

## 참고

- 기상청 API는 무료이지만 사용량 제한이 있을 수 있습니다.
- OpenAI API는 사용량에 따라 비용이 발생합니다.
- API 키는 안전하게 관리하세요.

---

해당 프로젝트는 Examples-Python의 Private Repository에서 공개 가능한 수준의 소스를 Public Repository로 변환한 것입니다.

