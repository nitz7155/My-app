// 배포 버전의 fastapi 주소 또는 로컬 fastapi 주소를 받아오는 함수

const getAPIBaseURL = () => {
    // Endpoint 직전 주소 (Base URL)
    const fastAPIHost = import.meta.env.VITE_FASTAPI_HOST;

    if (fastAPIHost.startsWith('http')) {
        // 로컬 환경 ex) http://localhost:8000
        return fastAPIHost;
    }

    // render의 web service의 도메인은
    // https://{host name}.onrender.com
    // ex) https://fastapi-ddddd.onrender.com
    // 이것이 리턴되면 App.jsx에서 배포된 fastapi 서버로 요청할 수 있음
    return `https://${fastAPIHost}.onrender.com`;
}

export const API_BASE_URL = getAPIBaseURL();