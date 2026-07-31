import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://127.0.0.1:8000/api' : '/api');

export const fetchStockData = async (ticker) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stock?ticker=${ticker}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching stock data:", error);
    throw error;
  }
};

export const fetchNewsData = async (ticker) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/news?ticker=${ticker}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching news data:", error);
    throw error;
  }
};

export const analyzeStock = async (analyzeRequest) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, analyzeRequest);
    return response.data;
  } catch (error) {
    console.error("Error analyzing stock:", error);
    throw error;
  }
};
