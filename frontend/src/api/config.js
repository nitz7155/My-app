const getAPIBaseURL = () => {
  // 1. 환경변수에서 FastAPI 호스트명 가져오기
  const fastApiHost = import.meta.env.VITE_FASTAPI_HOST;
  
  // 2. http로 시작하면 개발환경 FastAPI 주소 사용
  if (fastApiHost.startsWith('http')) {
    return fastApiHost;
  }

  // 3. http로 시작하지 않으면 배포 환경 FastAPI 주소 사용
  return `https://${fastApiHost}.onrender.com`;
  
};

export const API_BASE_URL = getAPIBaseURL();
