import axios from "axios";

const baseURL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

console.log("API Base URL:", baseURL);

const api = axios.create({
  baseURL: baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("Adding auth token to request:", config.url);
    } else {
      console.warn("No access token found for request:", config.url);
    }
    return config;
  },
  (error) => Promise.reject(error),
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          // Note: Since we are using standard axios for retry, be handled carefully to avoid loops
          // Here we use a separate instance or direct call to avoid interceptor loop if refresh fails 401
          const baseURL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";
          const response = await axios.post(`${baseURL}/auth/refresh`, null, {
            params: { refresh_token: refreshToken },
          });
          const { access_token, refresh_token: new_refresh_token } =
            response.data;
          localStorage.setItem("access_token", access_token);
          localStorage.setItem("refresh_token", new_refresh_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh token failed, logout
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  },
);

export default api;
