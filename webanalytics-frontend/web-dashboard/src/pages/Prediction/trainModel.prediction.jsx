import React, { useState, useContext, useEffect } from 'react';
import Select from 'react-select';

import DialogModal from '../../components/Dialog';

import { addNewTrainingModel } from '../../services/prediction.service';

import { AuthContext } from '../../context/auth-context';
import { set } from 'date-fns';


export const AddTrainingModel = ({
    showAddTrainingModelDialog, setShowAddTrainingModelDialog, 
    selectedDataset, selectedDatasetColumns, selectedDatasetColumnsType
}) => {

    const { currentUser, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const [selectedFeatures, setSelectedFeatures] = useState([]);
    const [selectedTarget, setSelectedTarget] = useState([]);    
        

    const [newTrainingModel, setNewTrainingModel] = useState({
        algorithm: '',
        dataset_id: selectedDataset?.id,
        model_name: '',
        features: selectedFeatures,
        target: selectedTarget,
        scaler: 'None',
        task: 'regression',
        hidden_layers: [100,100],
        epochs: 100,
        batch_size: 32,
        timesteps: 1
    })

    const [advancedOptions, setAdvancedOptions] = useState(false);

    // useEffect for handling selectedDataset changes
    useEffect(() => {
        setNewTrainingModel(prevState => ({...prevState, dataset_id: selectedDataset?.id}));        
    }, [selectedDataset])   

    useEffect(() => {
        // setSelectedFeatures(selectedFeatures);
        setNewTrainingModel(prevState => ({...prevState, features: selectedFeatures}));
    }, [selectedFeatures])

    useEffect(() => {
        // setSelectedTarget(selectedTarget);
        setNewTrainingModel(prevState => ({...prevState, target: selectedTarget}));
    }, [selectedTarget])    
        

    useEffect(() => {
        setNewTrainingModel(newTrainingModel)        
    }, [newTrainingModel])
    


    // Add database connection
    const handleAddTrainingModel = async () => {        
        try {
            setIsGlobalLoading(true);
            const response = await addNewTrainingModel(newTrainingModel, currentUser);
            if (response.status === 201 || response.status === 200) {
                alert('Training Model added successfully');
            }
        } catch (error) {
            alert('Error adding Training Model');
            console.error(error);
            setIsGlobalLoading(false);
        } finally {
            setIsGlobalLoading(false);
            setShowAddTrainingModelDialog(false);            
        }        
    }

    return (
        <>
            <DialogModal
                open={showAddTrainingModelDialog}
                onClose={() => {setShowAddTrainingModelDialog(false);}}
                header={<div className="font-bold">Add Training Model</div>}                            
                showCancelButton={true}
                onCancel={() => {setShowAddTrainingModelDialog(false);}}
                confirmButtonText="Save"
                onConfirm={() => {handleAddTrainingModel();}}   
                isSubmitButton={true}   
                closeOnBackdropClick={false}                  
            >
                <div className="font-normal">Add a new training model for dataset {selectedDataset?.name}</div>                
                {/* Add database connection form */}
                <div className="w-screen max-w-xl p-8">
                    <form className="space-y-6" onSubmit={handleAddTrainingModel}>
                        <Select
                            onChange={(e) => setNewTrainingModel(prevState => ({...prevState, algorithm: e.value}))}
                            className="w-full border border-gray-300 rounded"
                            placeholder="Algorithm*"
                            required    
                            options={
                                [
                                    { value: 'MLP', label: 'MultiLayer Perceptron' },  
                                    { value: 'LSTM', label: 'Long Short Term Memory' },                              
                                ]
                            }                                                                                                           
                        />   
                        <input 
                            type="text" 
                            placeholder="Model Name*" 
                            onChange={(e) => {
                                setNewTrainingModel(prevState => ({...prevState, model_name: e.target.value}));
                            }}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />                                                                          
                        <Select
                            onChange={(selectedOption) => {
                                setSelectedFeatures(selectedOption.map(option => option.value)); 
                                
                            }}
                            className="w-full border border-gray-300 rounded"
                            placeholder="Features*"
                            required    
                            options={
                                selectedDatasetColumns.map(column => ({value: column, label: column}))                                                                
                            }
                            isMulti
                        />
                        <Select
                            onChange={(selectedOption) => {
                                setSelectedTarget(selectedOption.map(option => option.value));
                                // setNewTrainingModel(prevState => ({...prevState, target: selectedOption.map(option => option.value)}));
                                // console.log(newTrainingModel)
                            }}
                            className="w-full border border-gray-300 rounded"
                            placeholder="Target*"
                            required    
                            options={
                                selectedDatasetColumns.map((column, i) => ({value: column, label: column}))                                                                                            
                            }
                            isMulti
                        />
                        <Select
                            onChange={(e) => setNewTrainingModel(prevState => ({...prevState, scaler: e.value}))}
                            className="w-full border border-gray-300 rounded"
                            placeholder="Scaler*"
                            required    
                            options={
                                [
                                    { value: 'standard', label: 'Standard Scaler' },  
                                    { value: 'minmax', label: 'MinMax Scaler' },    
                                    { value: '', label: 'None'}                          
                                ]
                            }
                        />
                        <Select
                            onChange={(e) => setNewTrainingModel(prevState => ({...prevState, task: e.value}))}
                            className="w-full border border-gray-300 rounded"
                            placeholder="Task*"
                            required    
                            options={
                                [
                                    { value: 'regression', label: 'Regression' },  
                                    { value: 'classification', label: 'Classification' },                              
                                ]
                            }
                        />    
                        <div className="flex flex-row gap-4 items-center">
                            <input
                                type="checkbox"
                                onChange={(e) => setAdvancedOptions(e.target.checked)}
                                className="w-4 h-4"
                            />                            
                            <label>Advanced Options</label>
                        </div>  

                        {advancedOptions && (
                            <div className="flex flex-col gap-4">
                                <input 
                                    type="number" 
                                    placeholder="Epochs" 
                                    onChange={(e) => setNewTrainingModel(prevState => ({...prevState, epochs: e.target.value}))}
                                    className="w-full p-2 border border-gray-300 rounded"
                                />
                                <input 
                                    type="number" 
                                    placeholder="Batch Size" 
                                    onChange={(e) => setNewTrainingModel(prevState => ({...prevState, batch_size: e.target.value}))}
                                    className="w-full p-2 border border-gray-300 rounded"
                                />
                                <input 
                                    type="number" 
                                    placeholder="Timesteps (for LSTM)" 
                                    onChange={(e) => setNewTrainingModel(prevState => ({...prevState, timesteps: e.target.value}))}
                                    className="w-full p-2 border border-gray-300 rounded"
                                />
                                <input 
                                    type="text" 
                                    placeholder="Hidden Layers. e.g. 64,64,64,64"                                     
                                    onChange={(e) => {
                                        // enclose e.target.value with square brackets                                                                                
                                        setNewTrainingModel(prevState => ({
                                            ...prevState, hidden_layers: e.target.value.split(',').map(layer => parseInt(layer))
                                        }));                                                                          
                                    }}
                                    className="w-full p-2 border border-gray-300 rounded"
                                />
                            </div>
                        )}              
                    </form>
                </div>
            </DialogModal>  
        </>
    )
}