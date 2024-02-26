import AddIcon from '@mui/icons-material/Add';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import Select from 'react-select';

import { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../../context/auth-context';

import { getDatasetColumns, getDatasetData, getPreviosNextPage } from '../../services/datasets.service';
import { AddDataset } from '../Home/addDataset.home'


function Datasets(){
    const { currentUser, currentUserInformation, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);
    const [page, setPage] = useState(1)
    const [page_size, setPage_size] = useState(50)

    const page_sizeOptions = [25, 50, 100, 200]

    const [isLoading, setIsLoading] = useState(false)
    const [showAddDatasetDialog, setShowAddDatasetDialog] = useState(false);

    const userDatasets = currentUserInformation ? currentUserInformation?.datasets : [];
    
    const [selectedDataset, setSelectedDataset] = useState({
        label: '',
        value: null     
    });

    const [datasetColumns, setDatasetColumns] = useState(JSON.parse(sessionStorage.getItem('datasetColumns')) || []);
    const [datasetData, setDatasetData] = useState(JSON.parse(sessionStorage.getItem('datasetData')) || []);
    const [isAscending, setIsAscending] = useState(true);

    const handleDatasetChange = async () => {
        try {
            if (selectedDataset.value !== null) {
                setIsLoading(true);
                const columnsResponse = await getDatasetColumns(selectedDataset.value.id, currentUser);
                const dataResponse = await getDatasetData(selectedDataset.value.id, currentUser, 1, page_size);
                if (columnsResponse.status === 200 && dataResponse.status === 200) {
                    setDatasetColumns(columnsResponse.data);
                    setDatasetData(dataResponse.data);
                    sessionStorage.setItem('datasetColumns', JSON.stringify(columnsResponse.data));
                    sessionStorage.setItem('datasetData', JSON.stringify(dataResponse.data));
                }
                setIsLoading(false);
            }
        } catch (error) {
            console.error(error);
            setIsLoading(false);
            alert('Error fetching dataset columns and data');
        }
    }

    const handlePagination = async (url) => {
        try {
            setIsLoading(true);            
            const response = await getPreviosNextPage(url, currentUser);
            if (response.status === 200) {
                setDatasetData(response.data);
                sessionStorage.setItem('datasetData', JSON.stringify(response.data));
            }
            setIsLoading(false);
        } catch (error) {
            console.error(error);
            setIsLoading(false);
            alert('Error fetching dataset data');
        }
    }

    const handleSort = async (column, asc) => {
        try {
            setIsLoading(true);
            console.log('sort', column)
            const response = await getDatasetData(selectedDataset.value.id, currentUser, 1, page_size, "true", asc, column);
            if (response.status === 200) {
                setDatasetData(response.data);
                sessionStorage.setItem('datasetData', JSON.stringify(response.data));
            }
            setIsLoading(false);
        } catch (error) {
            console.error(error);
            setIsLoading(false);
            alert('Error fetching dataset data');
        }
    }

    // useEffect if there is a change in selectedDataset, then call handleDatasetChange
    useEffect(() => {
        console.log('dataset change')
        if (selectedDataset.value !== null) {
            console.log(selectedDataset.value.id)
            handleDatasetChange();
        }
    }, [selectedDataset]);

    // useEffect if there is a change in page_size, then call handleDatasetChange
    useEffect(() => {
        console.log('page_size change')
        handleDatasetChange();
    }, [page_size]);

    // useEffect to load datasetColumns and datasetData from sessionStorage to state
    useEffect(() => {
        if (sessionStorage.getItem('datasetColumns') !== null) {
            setDatasetColumns(JSON.parse(sessionStorage.getItem('datasetColumns')));
            console.log(datasetColumns)
        }
        if (sessionStorage.getItem('datasetData') !== null) {
            setDatasetData(JSON.parse(sessionStorage.getItem('datasetData')));
            console.log(datasetData)
        }
    }
    , []);

    return (
        <>
            <div className="flex flex-col overflow-auto">
                <div className="font-bold font-['Montserrat'] my-4">
                    Datasets
                </div>
                {/* DROPDOWN TO SELECT DATASET */}
                {<div className="flex flex-row items-center mb-4">
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
                </div>}

                {/* DATASET COLUMNS */}
                {
                userDatasets.length === 0 ? (
                    <div className="flex flex-col h-40 w-fit">
                        <div className="text-blue-500 font-bold py-4">
                            No dataset
                        </div>                    
                        <div onClick={() => {
                            if (currentUserInformation?.connection != null)
                                setShowAddDatasetDialog(true)}
                            } className={`${currentUserInformation?.connection != null ? 'bg-slate-900 cursor-pointer' :'bg-slate-600 cursor-not-allowed'} py-2 px-4 rounded-md flex flex-row gap-4 items-center align-middle hover:bg-slate-600 hover:transition-colors duration-300 text-white`}>
                                <AddIcon/>
                                <div>Add Dataset</div>
                        </div>
                        <AddDataset showAddDatasetDialog={showAddDatasetDialog} setShowAddDatasetDialog={setShowAddDatasetDialog} />

                    </div>
                    
                ) : (
                <div className="flex flex-col items-center mb-4">
                    <div className="flex flex-row items-center w-full">
                        <div className="h-full w-full overflow-auto rounded-lg shadow-lg py-4 flex flex-col">
                            {isLoading ? (
                                <div className="flex justify-center items-center h-[400px]">
                                    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                                </div>
                            ) : (
                                <div className='flex flex-col gap-4 w-full'>
                                    {selectedDataset.value != null ? 
                                    <div className='w-full rounded-lg border min-h-fit max-h-[400px] overflow-auto no-scrollbar'>
                                        <table className='table-auto text-left overflow-clip rounded-lg w-full'>                                            
                                            <thead className='bg-slate-900 border-b text-white border-blue-gray-100
                                                bg-blue-gray-50 p-4 text-sm sticky top-0 z-1'>
                                                {/* map array datasetColumns */
                                                datasetColumns.map((column, index) => (
                                                    <th key={index} className='border-b border-blue-gray-100 py-4 px-2 text-sm'>
                                                        <div className='flex flex-row justify-between items-center'>
                                                            <div>{column}</div>
                                                            <KeyboardArrowDownIcon className='ml-1 cursor-pointer' 
                                                            onClick={() =>{
                                                                console.log('sort', column)
                                                                console.log(selectedDataset)
                                                                setIsAscending(!isAscending)
                                                                handleSort(column, isAscending)
                                                            }}/>
                                                        </div>                                                      
                                                    </th>
                                                ))}
                                            </thead>
                                            <tbody className='bg-white'>
                                                {/* map datasetData that contains array of Objects with key same as datasetColumns */}
                                                {datasetData.results?.map((data, index) => (
                                                    <tr key={index} className='border-b border-blue-gray-100'>
                                                        {datasetColumns.map((column, index) => (
                                                            <td key={index} className='p-4 border text-sm'>
                                                                {data[column]}
                                                            </td>
                                                        ))}
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div> : 
                                    <div className='h-full w-fit rounded-lg p-4 mt-4 flex flex-col'>
                                        Select a Dataset
                                    </div>}
                                    
                                    {selectedDataset.value != null && (
                                        <div className="flex flex-row justify-center gap-4">
                                            <button
                                                className="bg-blue-500 text-white rounded-lg p-2"
                                                onClick={() => {
                                                    if (page >= 1)
                                                        setPage(page - 1);
                                                    handlePagination(datasetData.previous);
                                                }}
                                            >
                                                Previous
                                            </button>
                                            {/* PAGE NUMBER INPUT */}                
                                            {/* <input
                                                type="number"
                                                id="page"
                                                value={page}
                                                onChange={(e) => setPage(e.target.value)}
                                                className="border border-gray-300 rounded-md p-2 text-center w-20"
                                                onKeyDown={(e) => {
                                                    if (e.key === 'Enter') {
                                                        handlePagination(datasetData.previous);
                                                    }                                
                                                }}
                                            />       */}
                                            <div className="flex flex-row items-center">
                                                <label htmlFor="page_size" className="mr-2">
                                                    Page Size:
                                                </label>
                                                <select
                                                    id="page_size"
                                                    value={page_size}
                                                    onChange={(e) => {
                                                        setPage_size(e.target.value);                                                        
                                                    }}
                                                    className="border border-gray-300 rounded-md p-2 text-center w-20"
                                                >
                                                    {page_sizeOptions.map((option) => (
                                                        <option key={option} value={option}>
                                                            {option}
                                                        </option>
                                                    ))}
                                                </select>
                                            </div>              
                                            <button
                                                className="bg-blue-500 text-white rounded-lg p-2"
                                                onClick={() => {
                                                    setPage(page + 1);
                                                    handlePagination(datasetData.next);
                                                }}
                                            >
                                                Next
                                            </button>
                                        </div>
                                    )}                    
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                )}            
            </div>
        </>
    )
}

export default Datasets