# 실험실 재고 현황

-80℃ deepfreezer 재고(Cell line · Bacteria · Reagent · siRNA)를 박스 그리드로 보고, 웹에서 바로 수정하는 사이트.

- 원본 데이터: `data/*.csv` (4개)
- 화면: `site/index.html` → GitHub Pages로 배포
- 엑셀: `stock.xlsx` — CSV가 바뀔 때마다 GitHub Actions가 자동 생성 (직접 수정하지 말 것)

## 처음 설정 (관리자, 1회)

1. **저장소 만들기**: github.com → New repository → 이름 `lab-stock` → **Public** 선택
   (Private + Pages는 유료 플랜 필요)
2. **이 폴더 올리기**: 저장소 안내에 나오는 `git remote add origin …` / `git push -u origin main` 실행
3. **Settings → Pages** → Source: **GitHub Actions**
4. **Settings → Actions → General** → Workflow permissions: **Read and write permissions** → Save
5. **Actions** 탭 → "build xlsx & deploy site" → **Run workflow** (첫 배포, 1~2분)
   → 사이트 주소: `https://<계정>.github.io/lab-stock/`
6. **공용 토큰 발급**: Settings(계정) → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate
   - Repository access: **Only select repositories → lab-stock**
   - Permissions → Repository → **Contents: Read and write** (나머지 없음)
   - Expiration: 1년 권장
7. 연구원들에게 **사이트 주소 + 토큰**을 전달 (메신저 공개 채널 금지)

## 연구원 사용법

1. 사이트 열기 → 우측 상단 **⚙ 편집 설정** → 이름, 토큰 입력 → 저장 (컴퓨터마다 1회)
2. 칸 클릭 → **수정** → 값 변경 → **저장**  /  빈 칸 클릭 → 바로 입력 → 저장
3. 엑셀이 필요하면 **⬇ 엑셀** (저장 후 1~2분 뒤 최신본 반영)

- 공용 PC에서는 사용 후 ⚙ 편집 설정 → **지우기**
- 수정 기록: 저장소의 Commits 목록 (`cell_stock1 D-1 수정 (홍길동)`) — 잘못 고친 경우 해당 커밋을 되돌리면 됨
- 동시에 다른 칸을 고쳐도 서로 덮어쓰지 않음 (저장 직전 최신본을 다시 읽어 해당 칸만 교체)

## 주의

- 사이트 주소를 아는 사람은 **조회 가능** (검색엔진 노출은 차단). 수정은 토큰이 있어야 가능.
- 토큰이 유출되면 GitHub에서 해당 토큰을 **Revoke** 후 새로 발급해 다시 배포.
