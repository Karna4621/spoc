/**
 * API Service
 * Centralized API client for all backend communications
 * Uses Axios for HTTP requests
 */

import axios from 'axios';

// Base API URL - change this based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Request interceptor - add auth token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * SPOC API calls
 */
export const spocApi = {
  // Get all SPOCs with optional filtering
  getAll: (params = {}) => {
    return apiClient.get('/spocs', { params });
  },

  // Get specific SPOC by ID
  getById: (spocId) => {
    return apiClient.get(`/spocs/${spocId}`);
  },

  // Get SPOC availability
  getAvailability: (spocId, startDate, endDate) => {
    return apiClient.get(`/spocs/${spocId}/availability`, {
      params: { start_date: startDate, end_date: endDate }
    });
  },

  // Create new SPOC (admin only)
  create: (spocData) => {
    return apiClient.post('/spocs', spocData);
  },
};

/**
 * Client API calls
 */
export const clientApi = {
  // Create new client
  create: (clientData) => {
    return apiClient.post('/clients', clientData);
  },

  // Get client by ID
  getById: (clientId) => {
    return apiClient.get(`/clients/${clientId}`);
  },

  // List all clients
  getAll: (skip = 0, limit = 100) => {
    return apiClient.get('/clients', { params: { skip, limit } });
  },

  // Update client
  update: (clientId, clientData) => {
    return apiClient.put(`/clients/${clientId}`, clientData);
  },
};

/**
 * Booking API calls
 */
export const bookingApi = {
  // Create new booking
  create: (bookingData) => {
    return apiClient.post('/bookings', bookingData);
  },

  // Get booking by ID
  getById: (bookingId) => {
    return apiClient.get(`/bookings/${bookingId}`);
  },

  // List bookings with filters
  getAll: (params = {}) => {
    return apiClient.get('/bookings', { params });
  },

  // Cancel booking
  cancel: (bookingId) => {
    return apiClient.post(`/bookings/${bookingId}/cancel`);
  },
};

/**
 * Health check
 */
export const healthCheck = () => {
  return axios.get(`${API_BASE_URL.replace('/api/v1', '')}/health`);
};

export default apiClient;
