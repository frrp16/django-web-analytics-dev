import axios  from "axios";

const BASE_API_URL = 'http://127.0.0.1:8000/'

export const addNewTrainingModel = async (newTrainingModel, accessToken) => {
    console.log(newTrainingModel);
    const response = await axios.post(`${BASE_API_URL}train/`, {
        dataset_id: newTrainingModel.dataset_id,
        algorithm: newTrainingModel.algorithm,
        name: newTrainingModel.model_name,
        features: newTrainingModel.features,
        target: newTrainingModel.target,
        scaler: newTrainingModel.scaler,
        hidden_layers: newTrainingModel.hidden_layers,
        epochs: newTrainingModel.epochs,
        batch_size: newTrainingModel.batch_size,
        timesteps: newTrainingModel.timesteps,        
    }, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}


export const getTrainingModels = async (dataset_id, accessToken) => {
    const response = await axios.get(`${BASE_API_URL}mlmodel/dataset/${dataset_id}`, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    return response;
}