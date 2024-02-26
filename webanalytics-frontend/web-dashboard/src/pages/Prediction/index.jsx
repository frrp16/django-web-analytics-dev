import { useState, useContext } from "react"

import { AuthContext } from '../../context/auth-context';
import { format, parseISO } from 'date-fns';

import Select from 'react-select';
import CachedIcon from '@mui/icons-material/Cached';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';

import { Tooltip } from '@mui/material';

function Prediction(){

    const { currentUser, currentUserInformation, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const userDatasets = currentUserInformation ? currentUserInformation?.datasets : [];

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
                                            <td className='border border-blue-gray-100 px-4 py-2 text-sm flex flex-row gap-4'>                                             
                                                <Tooltip title="Refresh">
                                                    <div className="bg-green-500 text-white py-2.5 px-4 rounded-md cursor-pointer
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
                                                    <div onClick={() => {console.log(dataset)}} 
                                                        className="bg-blue-700 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                        hover:bg-blue-400 hover:transition-colors duration-300">                                                            
                                                        <AutoGraphIcon/>                                                        
                                                    </div>
                                                </Tooltip> 

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
                        <div className="flex flex-row items-center">
                            <Select
                                options={userDatasets.map(dataset => ({value: dataset, label: dataset.name}))}
                                onChange={(selectedOption) => {
                                    setSelectedDataset(selectedOption);
                                    console.log('selectedOption', selectedOption);
                                    if (selectedDataset.value !== null) {
                                        handleDatasetChange();
                                    }                                                 
                                }}
                                placeholder="Select a dataset"                        
                                
                            />                
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}

export default Prediction