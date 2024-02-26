// table.Datasets.js
import React from 'react';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

function TableDatasets({ datasetColumns, datasetData, isLoading, handleSort, isAscending, handlePagination }) {
    
    // Table-related logic goes here

    return (
        <div className="h-full w-full overflow-auto rounded-lg shadow-lg py-4 flex flex-col">
            {isLoading ? (
                <div className="flex justify-center items-center h-40">
                    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                </div>
            ) : (
                <div className='flex flex-col gap-4 items-center w-full'>
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
                    </div>
                    {/* Button for pagination navigation */}
                    {<div className='flex flex-row justify-center gap-4'>
                        <button className='bg-blue-500 text-white rounded-lg p-2' onClick={() => {
                            handlePagination(datasetData.previous)
                            }
                        }>
                            Previous
                        </button>
                        <button className='bg-blue-500 text-white rounded-lg p-2' onClick={() => {
                            handlePagination(datasetData.next)                                            
                        }}>
                            Next
                        </button>
                    </div>}
                </div>
            )}
        </div>
    );
}

export default TableDatasets;