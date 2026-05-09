import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// Flag to prevent multiple refresh attempts
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: unknown) => void;
  reject: (reason?: unknown) => void;
}> = [];

const processQueue = (error: unknown = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve();
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config;
    
    // If it's a 401 and not already retrying
    if (err.response?.status === 401 && !originalRequest._retry) {
      // Don't try to refresh on auth endpoints to prevent infinite loops
      if (originalRequest.url?.includes('/auth/login') || 
          originalRequest.url?.includes('/auth/register') ||
          originalRequest.url?.includes('/auth/refresh')) {
        return Promise.reject(err);
      }
      
      if (isRefreshing) {
        // Queue the request while refresh is in progress
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => {
          // isRefreshing is already false at this point (set in finally below)
          return api(originalRequest);
        }).catch((err) => {
          return Promise.reject(err);
        });
      }
      
      originalRequest._retry = true;
      isRefreshing = true;
      
      try {
        await api.post("/auth/refresh/");
        processQueue();        // resolve all queued promises
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError); // reject all queued promises
        // Only redirect to login if not already there
        if (!window.location.pathname.includes('/login') && 
            !window.location.pathname.includes('/register')) {
          window.location.href = "/login";
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    
    return Promise.reject(err);
  }
);

export default api;