# 🔵 **빌드 스테이지**: 애플리케이션을 빌드하는 단계
FROM node:22-alpine AS builder

# 📁 작업 디렉토리 설정 (빌드 스테이지에서 사용)
WORKDIR /frontend

# 🔑 빌드 시점에 환경변수 받기 (중요!)
# React는 빌드 타임에 환경변수를 정적 파일에 포함시킴
# 런타임에는 이미 컴파일된 JS 파일이므로 환경변수 변경 불가
# 따라서 Docker 빌드할 때 반드시 환경변수를 전달해야 함
# 
# ARG: 빌드 시점에만 사용 (render.yaml에서 전달)
# ENV: 빌드된 애플리케이션 내부에서 사용할 환경변수로 설정
ARG API_SERVER_URL
ENV VITE_API_URL=$API_SERVER_URL

# 📦 package.json과 package-lock.json만 먼저 복사
# 이유: 의존성이 변경되지 않으면 Docker 캐시를 재사용하여 빌드 속도 향상
COPY package*.json ./

# 🔧 package-lock.json을 기준으로 정확한 버전의 패키지 설치
# npm ci는 npm install보다 빠르고 안정적 (CI/CD 환경에 최적화)
RUN npm ci 

# 📂 소스 코드 전체를 컨테이너로 복사
COPY . .

# 🏗️ 프로덕션 빌드 실행 (dist 또는 build 폴더에 결과물 생성)
# Vite의 경우 /frontend/dist에 빌드 결과가 생성됨
RUN npm run build

# ============================================================
# 🟢 **프로덕션 스테이지**: 실제로 실행될 최종 이미지
# ============================================================
FROM node:22-alpine

# 📁 작업 디렉토리 설정 (프로덕션 스테이지에서 사용)
# WORKDIR /app
WORKDIR /frontend

# 🌐 serve 패키지를 전역으로 설치 (정적 파일 서빙용)
# serve는 가볍고 빠른 정적 파일 서버
RUN npm install -g serve

# 📦 빌드 스테이지에서 빌드된 결과물만 복사
# /frontend/dist (builder 스테이지) → /frontend/dist (현재 스테이지)
# 이렇게 하면 node_modules, 소스 코드 등 불필요한 파일은 제외됨
COPY --from=builder /frontend/dist ./dist

# 🔓 3000번 포트를 외부에 노출
# 실제로 포트를 여는 것은 아니고, 문서화 목적 (docker-compose에서 매핑 필요)
EXPOSE 3000

# 🚀 컨테이너 시작 시 실행할 명령어
# serve -s dist: dist 폴더를 SPA(Single Page Application) 모드로 서빙
# -l 3000: 3000번 포트에서 실행
CMD ["serve", "-s", "dist", "-l", "3000"]