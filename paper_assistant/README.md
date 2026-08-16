# 연구실 논문 보조 AI

PDF 또는 초록을 업로드하면 Claude API로 목적/방법/결과/한계/후속 아이디어를 구조화하여
정리하고, 저장된 논문들을 검색·비교할 수 있는 Streamlit 웹앱입니다.

## 설치

```bash
cd paper_assistant
pip install -r requirements.txt
```

## API 키 설정

Anthropic API 키가 필요합니다.

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

환경변수를 설정하지 않으면 앱 사이드바에서 직접 입력할 수 있습니다 (세션에만 유지되며 저장되지 않음).

## 실행

```bash
streamlit run app.py
```

## 기능

- **업로드**: PDF 또는 텍스트를 업로드하면 목적/방법/결과/한계/후속 아이디어로 구조화된 요약을 생성해 저장합니다.
- **논문 목록 / 검색**: 저장된 논문을 검색하고 상세 내용을 확인·삭제합니다.
- **비교**: 2편 이상의 논문을 선택해 항목별로 나란히 비교합니다.

## 데이터

논문 요약은 `data/papers.db` (SQLite)에 로컬로 저장됩니다. 이 파일은 git에 커밋되지 않습니다.
