import axios from "axios";
// import { Readable } from 'stream';

const BASE_API_URL = 'http://127.0.0.1:8000/'

export const getDatasetColumns = async (datasetId, accessToken) => {
    const response = await axios.get(`${BASE_API_URL}dataset/${datasetId}/columns/`, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}

export const getDatasetColumnsType = async (datasetId, accessToken) =>{
    const response = await axios.get(`${BASE_API_URL}dataset/${datasetId}/columns_type/`, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;

}

export const getDatasetData = async (datasetId, accessToken, page = 1, page_size = 50, order = false, asc = false, columns = []) => {
    console.log('getDatasetData', datasetId, page, page_size, order, asc, columns);
    const response = await axios.get(`${BASE_API_URL}dataset/${datasetId}/data/`, {        
        params: {
            'page': page, 
            'page_size': page_size, 
            'order': order, 
            'asc': asc.toString(),
            'column': columns
        },
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}

export const getPreviosNextPage = async (url, accessToken) => {
    const response = await axios.get(url, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}

export const getAllDatasetsData = async (datasetId, accessToken, select, page_size = 50, sample = true ) => {
    const total_pages = await axios.get(`${BASE_API_URL}dataset/${datasetId}/pages_count/`, {                     
        params: {
            'page_size': page_size,
            'sample': sample.toString(),            
        },
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });

    let urls = `${BASE_API_URL}dataset/${datasetId}/data/`;

    let requests = [];
    for (let i = 1; i <= total_pages.data; i++){
        requests.push(axios.get(urls, {
            params: {
                'page': i, 
                'page_size': page_size, 
                'order': false, 
                'asc': false.toString(),
                'col_select': select
            },
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        }));
    }

    const response = await axios.all(requests);
    // get response status for all requests and check if all requests are successful
    let status = response.map(response => response.status);

    if (status.includes(400) || status.includes(500)){
        return {
            status: 400,
            data: []
        }
    }

    let data = [];
    for (let i = 0; i < response.length; i++){
        data.push(response[i].data.results);
    }   
    // response.data.results is array of json objects, flatten the array
    data = data.flat(); 
    return {
        status: 200,
        data: data
    }
    
}

export const updateMonitorLog = async (datasetId, accessToken) => {
    const response = await axios.get(`${BASE_API_URL}dataset/${datasetId}/monitor/`, {
        headers: {  
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}