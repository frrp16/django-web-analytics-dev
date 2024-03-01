import { useState, useContext } from 'react';

import { format, parseISO } from 'date-fns';

import { AuthContext } from '../../context/auth-context';

import AddIcon from '@mui/icons-material/Add';
import CachedIcon from '@mui/icons-material/Cached';
import DeleteIcon from '@mui/icons-material/Delete';
import TableChartIcon from '@mui/icons-material/TableChart';
import EditIcon from '@mui/icons-material/Edit';

import { Tooltip } from '@mui/material';

import { AddConnection } from './addConnection.home';
import { AddDataset } from './addDataset.home';

import { updateMonitorLog } from '../../services/datasets.service';

function Home() {
    const { currentUser, currentUserInformation, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const [showAddDatabaseDialog, setShowAddDatabaseDialog] = useState(false);
    const [showAddDatasetDialog, setShowAddDatasetDialog] = useState(false);

    const [newConnection, setNewConnection] = useState({
        database_type: '',
        host: '',
        database: '',
        port: '',
        username: '',
        password: '',
        ssl: false
    });    

    const connectionDetails = currentUserInformation ? [
        { label: 'Engine', value: currentUserInformation?.connection?.database_type},
        { label: 'Host', value: currentUserInformation?.connection?.host },
        { label: 'Database', value: currentUserInformation?.connection?.database },
        { label: 'Username', value: currentUserInformation?.connection?.username },
    ] : [];        

    return (
        <div>            
            <div className="flex flex-col">
                <div className="font-bold font-['Montserrat'] my-4">
                    Welcome, {currentUserInformation?.first_name} {currentUserInformation?.last_name}
                </div>                                  
                    {currentUserInformation?.connection != null ?  (
                    // IF DATABASE CONNECTION IS EXISTS
                    <>                        
                        <div className="h-full w-fit rounded-lg shadow-lg p-4 flex flex-col">     
                            <div className='flex flex-row gap-4'>                   
                                <div className='w-full rounded-lg border overflow-clip'>                            
                                    <table className='table-auto text-left w-full rounded-lg w-full'>
                                        <thead className='bg-slate-900'>
                                            <tr>
                                                <th className='border-b text-white
                                                border-blue-gray-100 bg-blue-gray-50 p-4 text-sm'>
                                                    Connection Details:
                                                </th>   
                                                <th className='border-b text-white border-blue-gray-100 bg-blue-gray-50 px-4 text-sm'>     
                                                    <div className='flex w-full flex-row-reverse'>  
                                                    <Tooltip title="Edit Connection">                                           
                                                        <div className="bg-blue-500 w-fit text-white p-1 rounded-md cursor-pointer
                                                         hover:bg-blue-300 hover:transition-colors duration-300">                                                        
                                                            <EditIcon/>                                                            
                                                        </div> 
                                                    </Tooltip>
                                                    </div>                                                                                                     
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {connectionDetails.map((detail, index) => (
                                                <tr key={index}>
                                                    <td className='border-b font-bold border-blue-gray-100 px-4 py-2 text-sm'>{detail.label}</td>
                                                    <td className='border-b border-blue-gray-100 px-4 py-2 text-sm'>{detail.value}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>  
                                </div> 
                                <div>
                                    <div onClick={() => setShowAddDatasetDialog(true)} className="bg-slate-900 text-white py-2 px-4 rounded-md cursor-pointer
                                    hover:bg-slate-600 hover:transition-colors duration-300 items-center align-middle 
                                    flex flex-row w-full gap-4">
                                        <AddIcon/>
                                        <div>Add Dataset</div>
                                    </div>                            
                                </div>
                            </div>                                                
                        </div>   
                        <div className="h-full w-full min-w-fit rounded-lg shadow-lg p-4 mt-4 flex flex-col">
                            <div className='flex flex-row gap-4'>
                                <div className='w-full rounded-lg border mt-2'>
                                    <table className='table-auto text-left overflow-clip rounded-lg w-full'>
                                        <thead className='bg-slate-900'>
                                            <tr>
                                                <th colSpan={8} className='border-b text-white border-blue-gray-100
                                                 bg-blue-gray-50 p-4 text-sm'>
                                                    Recent Datasets:
                                                </th>                                                  
                                            </tr>                                            
                                        </thead>    
                                        <thead>
                                            <tr>
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Name</th>
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Description</th>
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Date Created</th>
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Table Name</th>  
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Date Updated</th>
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Column Count</th>  
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Row Count</th>                                                                                     
                                                <th className='border border-blue-gray-100 px-6 py-2 text-sm text-center'>Actions</th>                                                
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
                                                    <td className='border border-blue-gray-100 px-4 py-2 text-sm flex flex-row gap-4'>                                                
                                                <Tooltip title="View Dataset">
                                                    <div className="bg-slate-900 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                     hover:bg-slate-600 hover:transition-colors duration-300">                                                            
                                                        <TableChartIcon/>                                                            
                                                    </div>
                                                </Tooltip>
                                                <Tooltip title="Refresh">
                                                    <div onClick={() => updateMonitorLog(dataset.id, currentUser)}
                                                    className="bg-green-500 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                    hover:bg-green-300 hover:transition-colors duration-300">                                                            
                                                        <CachedIcon/>                                                            
                                                    </div>
                                                </Tooltip>
                                                <Tooltip title="Remove">
                                                    <div className="bg-red-600 text-white py-2.5 px-4 rounded-md cursor-pointer
                                                    hover:bg-red-300 hover:transition-colors duration-300">                                                        
                                                        <DeleteIcon/>                                                            
                                                    </div>
                                                </Tooltip>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>                                  
                                    </table>
                                </div>
                            </div>   
                        </div>
                        <AddDataset showAddDatasetDialog={showAddDatasetDialog}
                            setShowAddDatasetDialog={setShowAddDatasetDialog}
                        />
                    </>    
                                                                             
                    ) :  (
                        // IF DATABASE CONNECTION IS NOT EXISTS
                    <>
                        <div className="h-full w-full min-w-fit rounded-lg shadow-lg p-4 flex">  
                            <div className='flex flex-col p-6'>
                                <p className="text-sm font-['Montserrat']">
                                    You are not connected to any database. Please connect to a database to get started.
                                </p>
                                <div>
                                    <button onClick={() => setShowAddDatabaseDialog(true)} 
                                    className="bg-slate-900 text-white py-2 px-4 rounded-md mt-4
                                    hover:bg-slate-600 hover:transition-colors duration-300 ">
                                        Connect to Database
                                    </button>
                                </div>
                            </div>
                        </div>
                        <AddConnection showAddDatabaseDialog={showAddDatabaseDialog}
                            setShowAddDatabaseDialog={setShowAddDatabaseDialog}
                        />                                              
                    </>
                    )}                
            </div>
        </div>
    );
}

export default Home;