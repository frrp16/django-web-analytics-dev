import { useState, useContext, useEffect } from "react"

import { AuthContext } from '../../context/auth-context';
import { format, parseISO, set } from 'date-fns';

import Select from 'react-select';
import CachedIcon from '@mui/icons-material/Cached';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';

import { Tooltip } from '@mui/material';

import { updateMonitorLog, getDatasetColumns, getDatasetColumnsType } from "../../services/datasets.service";
import { getTrainingModels } from "../../services/prediction.service";

import { AddTrainingModel } from "./trainModel.prediction";
import CustomizedSnackbars from "../../components/Snackbar";

function Prediction(){

    const { currentUser, currentUserInformation, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const userDatasets = currentUserInformation ? currentUserInformation?.datasets : [];

    const [selectedDataset, setSelectedDataset] = useState(null);
    const [selectedDatasetColumns, setSelectedDatasetColumns] = useState(JSON.parse(sessionStorage.getItem('datasetColumns')) || []); 
    const [selectedDatasetColumnsType, setSelectedDatasetColumnsType] = useState(JSON.parse(sessionStorage.getItem('datasetColumnsType')) || []);
    
    const [selectedPredictionDataset, setSelectedPredictionDataset] = useState(null);
    const [showAddTrainingModelDialog, setShowAddTrainingModelDialog] = useState(false);
    const [showRefreshSnackbar, setShowRefreshSnackbar] = useState(false);

    const [datasetModel, setDatasetModel] = useState([])
    
    const handleDatasetChange = async () => {
        try {
            if (selectedDataset !== null) {                
                const columnsResponse = await getDatasetColumns(selectedDataset.id, currentUser);
                const columnsTypeResponse = await getDatasetColumnsType(selectedDataset.id, currentUser);
                                                            
                if (columnsResponse.status === 200 && columnsTypeResponse.status === 200) {
                    setSelectedDatasetColumns(columnsResponse.data);   
                    setSelectedDatasetColumnsType(columnsTypeResponse.data);                 
                    sessionStorage.setItem('datasetColumns', JSON.stringify(columnsResponse.data));           
                    sessionStorage.setItem('datasetColumnsType', JSON.stringify(columnsTypeResponse.data));     
                }                
            }
        } catch (error) {
            console.error(error);            
            alert('Error fetching dataset columns and data');
        }
    }

    const handlePredictonDatasetChange = async  () => {
        try {
            // setIsGlobalLoading(true);
            if (selectedPredictionDataset !== null) {
                const response = await getTrainingModels(selectedPredictionDataset.id, currentUser);
                if (response.status === 200) {
                    setDatasetModel(response.data);
                    console.log(datasetModel);
                }
            }
            // setIsGlobalLoading(false);
        } catch (error) {
            console.error(error);
            alert('Error fetching dataset training models');
            // setIsGlobalLoading(false);
        }
    }

    const handleRefreshDataset = async (dataset_id) => {
        try {
            const response = await updateMonitorLog(dataset_id, currentUser);
            if (response.status === 200) {
                setShowRefreshSnackbar(true);
            }
        } catch (error) {
            console.error(error);
            alert('Error updating dataset monitor log');
        }
    }

    useEffect(() => {
        setDatasetModel(datasetModel);
    }, [datasetModel]);


    useEffect(() => {        
        if (selectedDataset !== null) {            
            handleDatasetChange();
        }
      }, [selectedDataset]);

    useEffect(() => {
        if (selectedPredictionDataset !== null) {
            handlePredictonDatasetChange();            
        }
    }, [selectedPredictionDataset]);

    useEffect(() => {
        if (sessionStorage.getItem('datasetColumns') !== null) {
            setSelectedDatasetColumns(JSON.parse(sessionStorage.getItem('datasetColumns')));      
            setSelectedDatasetColumnsType(JSON.parse(sessionStorage.getItem('datasetColumnsType')));      
        }
    }, []);     

    return(
        <div>
             <div className="flex flex-col overflow-auto">
                <div className="font-bold font-['Montserrat'] my-4">
                    Training Datasets
                </div>
                <div className="h-full w-full rounded-lg flex flex-col">
                    <div className='flex flex-row gap-4'>
                        <div className='w-full rounded-lg border mt-2'>
                            <table className=' text-left overflow-clip rounded-lg min-w-fit w-full'>
                                <thead className='bg-slate-900'>
                                    <tr>
                                        <th colSpan={10} className='border-b text-white border-blue-gray-100
                                            bg-blue-gray-50 p-4 text-sm'>
                                            Datasets:
                                        </th>                                                  
                                    </tr>                                            
                                </thead>    
                                <thead>
                                    <tr>
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Name</th>
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Description</th>
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Date Created</th>
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Table Name</th>  
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Date Updated</th>
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Column Count</th>  
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Row Count</th>                                                                                     
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Training status</th>
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Update Status</th>           
                                        <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Action</th>                                                
                                    </tr>
                                </thead>  
                                <tbody>
                                    {currentUserInformation?.datasets.map((dataset, index) => (
                                        <tr key={index}>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>{dataset.name}</td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>{dataset.description}</td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                {format(parseISO(dataset.created_at), 'dd-MM-yyyy HH:mm:ss')}
                                            </td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>{dataset.table_name}</td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                {format(parseISO(dataset.monitor_logs[dataset.monitor_logs.length-1].timestamp), 'dd-MM-yyyy HH:mm:ss')}
                                            </td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                {dataset.monitor_logs[dataset.monitor_logs.length-1].column_count}
                                            </td>  
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                {dataset.monitor_logs[dataset.monitor_logs.length-1].row_count}                                                                                        
                                            </td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm gap-4'>  
                                                {dataset.is_trained}
                                            </td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm gap-4'>  
                                                {dataset.status}
                                            </td>
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm '>
                                                <div className="flex flex-row gap-4">
                                                    
                                                <Tooltip title="Refresh">
                                                    <div onClick={() => handleRefreshDataset(dataset.id)}
                                                    className="bg-green-500 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                    hover:bg-green-300 hover:transition-colors duration-300">                                                            
                                                        <CachedIcon/>                                                            
                                                    </div>
                                                </Tooltip> 
                                                <Tooltip title={`${dataset.status === 'STABLE' ? 'No Change Detected' : 'Acknowledge Change'}`}>
                                                    <div className={`text-white py-2.5 px-4 rounded-md 
                                                        ${dataset.status === 'STABLE' ? 'bg-gray-400 cursor-not-allowed' : 'bg-yellow-500 cursor-pointer hover:bg-yellow-200 hover:transition-colors duration-300'}`}>
                                                        <AssignmentTurnedInIcon/>
                                                    </div>
                                                </Tooltip>
                                                <Tooltip title="Train Dataset">
                                                    <div onClick={() => {       
                                                        setSelectedDataset(dataset);                                                                                                                                                                  
                                                        handleDatasetChange(dataset);
                                                        setShowAddTrainingModelDialog(true);                                                    
                                                    }} 
                                                        className="bg-blue-700 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                        hover:bg-blue-400 hover:transition-colors duration-300">                                                            
                                                        <AutoGraphIcon/>                                                        
                                                    </div>
                                                </Tooltip> 
                                                </div>

                                            </td>                                        
                                        </tr>
                                    ))}
                                </tbody>                                  
                            </table>
                        </div>
                    </div>   
                    <div className="h-full rounded-lg shadow-lg mb-20 p-4 w-full flex flex-col">  
                    <div className="font-bold font-['Montserrat'] my-4">
                        Prediction
                    </div>
                        <div className="flex flex-col gap-4 ">
                            <Select
                                options={userDatasets.map(dataset => ({value: dataset, label: dataset.name}))}
                                onChange={(selectedOption) => {
                                    setSelectedPredictionDataset(selectedOption.value);
                                    handlePredictonDatasetChange();
                                }}
                                placeholder="Select a dataset"                        
                                
                            />      
                            {datasetModel.length > 0 ? (
                                <table className=' text-left overflow-clip rounded-lg min-w-fit w-full'>
                                    <thead className='bg-slate-900'>
                                        <tr>
                                            <th colSpan={6} className='border-b text-white border-blue-gray-100
                                                bg-blue-gray-50 p-4 text-sm'>
                                                Training Models:
                                            </th>                                                  
                                        </tr>                                            
                                    </thead>    
                                    <thead>
                                        <tr>
                                            <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Name</th>
                                            <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Algorithm</th>
                                            <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Features</th>
                                            <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Target</th>  
                                            <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Created At</th>          
                                            <th className='border border-blue-gray-100 px-4 py-2 text-sm text-center'>Action</th>                                                
                                        </tr>
                                    </thead>  
                                    <tbody>
                                        {datasetModel.map((model, index) => (
                                            <tr key={index}>
                                                <td className='border border-blue-gray-100 px-4 py-2 text-sm'>{model.name}</td>
                                                <td className='border border-blue-gray-100 px-4 py-2 text-sm'>{model.algorithm}</td>
                                                <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                    {model.features}
                                                </td>
                                                <td className='border border-blue-gray-100 px-4 py-2 text-sm'>{model.target}</td>
                                                <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                    {model.created_at}
                                                </td>
                                                <td className='border border-blue-gray-100 px-4 py-2 text-sm'>
                                                    <div className="flex flex-row gap-4">
                                                        <Tooltip title="Train Model">
                                                            <div className="bg-blue-700 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                            hover:bg-blue-400 hover:transition-colors duration-300">                                                            
                                                                <AutoGraphIcon/>                                                        
                                                            </div>
                                                        </Tooltip> 
                                                    </div>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>

                            ) : null}
                        </div>
                    </div>

                </div>
            </div>

            <AddTrainingModel
                showAddTrainingModelDialog={showAddTrainingModelDialog}
                setShowAddTrainingModelDialog={setShowAddTrainingModelDialog}
                selectedDataset={selectedDataset}
                selectedDatasetColumns={selectedDatasetColumns}
                selectedDatasetColumnsType={selectedDatasetColumnsType}
            />            
            <CustomizedSnackbars
                open={showRefreshSnackbar}
                onClose={() => setShowRefreshSnackbar(false)}
                severity="info"
            >
                Sending Refresh Signals
            </CustomizedSnackbars>
        
        </div>
    )
}

export default Prediction