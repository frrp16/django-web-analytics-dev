import axios from 'axios';

const BASE_API_URL = 'http://127.0.0.1:8000/'


export const addNewConnection = async (newConnection, accessToken) => {
    const response = await axios.post(`${BASE_API_URL}connection/`, newConnection, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;     
}

export const addNewDataset = async (newDataset, accessToken) => {
    const response = await axios.post(`${BASE_API_URL}dataset/`, newDataset, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}