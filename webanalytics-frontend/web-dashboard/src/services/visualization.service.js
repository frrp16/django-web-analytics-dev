import axios from "axios"

const BASE_API_URL = 'http://127.0.0.1:8000/'

export const getPlotHtml = async (datasetId, accessToken, columns = []) => {
    const response = await axios.get(`${BASE_API_URL}plot/`, {                    
        params: {
            dataset_id: datasetId,
            columns: encodeURIComponent(JSON.stringify(columns)),
            test: 'true'
        },
        headers: {
            Authorization: `Bearer ${accessToken}`
        },
        
        })
    return response
}

export const getTSPlotJSON = async (datasetId, accessToken, columns = []) => {
    const response = await axios.get(`${BASE_API_URL}plot/time_series_plot`, {                    
        params: {
            dataset_id: datasetId,
            columns: columns.map(column => column).join(',')  
        },
        headers: {
            Authorization: `Bearer ${accessToken}`
        },
        
        })
    return response
}

export const getPairSPJSON = async (datasetId, accessToken, columns = []) => {
    const response = await axios.get(`${BASE_API_URL}plot/pair_scatter_plot`, {                    
        params: {
            dataset_id: datasetId,
            // convert array of column to string with comma separated, without space and quotes
            columns: columns.map(column => column).join(',')                        
        },
        headers: {
            Authorization: `Bearer ${accessToken}`
        },
        
        })
    return response
}