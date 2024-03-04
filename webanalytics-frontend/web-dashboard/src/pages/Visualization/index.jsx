import { useEffect, useContext, useState } from 'react'
import Select from 'react-select';

import { AuthContext } from '../../context/auth-context';
import { getDatasetColumns } from '../../services/datasets.service';
import { getPairSPJSON, getTSPlotJSON } from '../../services/visualization.service';

function PlotBody(plotRendered){
    return (
        <div className={`${plotRendered ? 'grid grid-cols-3' : 'hidden'} h-full w-full justify-between mt-6`}>
            <div id="plot" className="h-full w-full"></div>
        </div>
    );   
}

function Visualization(){
    // const array = fs.readFileSync('../assets/temp/BTC-USD.csv').toString().split('\r')
    const { currentUser, currentUserInformation, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);
    const userDatasets = currentUserInformation ? currentUserInformation?.datasets : [];

    const [selectedDataset, setSelectedDataset] = useState({
      label: '',
      value: null     
    });

    const [plotRendered, setPlotRendered] = useState(false);


    const [selectedDatasetColumns, setSelectedDatasetColumns] = useState(JSON.parse(sessionStorage.getItem('datasetColumns')) || []); 
    const [selectedDatasetData, setSelectedDatasetData] = useState(JSON.parse(sessionStorage.getItem('v_datasetData')) || []);

    const [selectedColumns, setSelectedColumns] = useState([]);
    const [isLoading, setIsLoading] = useState(false)

    const handleTimeSeriesPlot = async () => {
        try{
            setIsLoading(true);
            const response = await getTSPlotJSON(selectedDataset.value.id, currentUser, selectedColumns);
            if (response.status === 200) {
                const plotJSON = JSON.parse(response.data);
                window.Bokeh.embed.embed_item(plotJSON, 'plot');
            }  
            setPlotRendered(true);
            setIsLoading(false);
        }      
        catch (error) {
            console.error(error);
            alert('Error fetching time series plot');
            setIsLoading(false);
        }
    }

    const handlePairScatterPlot = async () => {
        try{
            setIsLoading(true);
            const response = await getPairSPJSON(selectedDataset.value.id, currentUser, selectedColumns);
            if (response.status === 200) {
                const plotJSON = JSON.parse(response.data);
                window.Bokeh.embed.embed_item(plotJSON, 'plot');
            }  
            setPlotRendered(true);
            setIsLoading(false);
        }      
        catch (error) {
            console.error(error);
            alert('Error fetching time series plot');
            setIsLoading(false);
        }
    }
       
    const handleDatasetChange = async () => {
      try {
        if (selectedDataset.value !== null) {
            setIsLoading(true);
            const columnsResponse = await getDatasetColumns(selectedDataset.value.id, currentUser);
            // make string from array of column names with comma separated
            const col_test = [columnsResponse.data[0], columnsResponse.data[1], columnsResponse.data[2]]
            const columnsString = col_test.map(column => column).join(',');
            // const dataResponse = await getAllDatasetsData(selectedDataset.value.id, currentUser, columnsString);
            if (columnsResponse.status === 200) {
                setSelectedDatasetColumns(columnsResponse.data);  
                // setSelectedDatasetData(dataResponse.data);
                sessionStorage.setItem('datasetColumns', JSON.stringify(columnsResponse.data));                
            }
            setIsLoading(false);
            // reload page            
          }
      } catch (error) {
          console.error(error);
          setIsLoading(false);
          alert('Error fetching dataset columns and data');
      }
  }

  useEffect(() => {    
    if (plotRendered){
        setPlotRendered(false);
        // window.location.reload();
    }
    if (selectedDataset.value !== null) {        
        handleDatasetChange();
    }
  }, [selectedDataset]);

  useEffect(() => {
    if (sessionStorage.getItem('datasetColumns') !== null) {
        setSelectedDatasetColumns(JSON.parse(sessionStorage.getItem('datasetColumns')));        
    }
    // if (sessionStorage.getItem('datasetData') !== null) {
    //     setSelectedDatasetData(JSON.parse(sessionStorage.getItem('v_datasetData')));
    //     console.log(selectedDatasetData)
    // }
    } , []);     

    useEffect(() => {
        setSelectedColumns(selectedColumns);        
    }
    , [selectedColumns]);

    return(
        <div>
            <div className="flex flex-col w-full h-full min-h-[500px]">
                <div className="font-bold font-['Montserrat'] my-4">
                  Visualization Page
                </div>
                {/* DROPDOWN TO SELECT DATASET */}
                <div className="flex flex-row mb-4 w-full h-full">
                    <Select
                        options={userDatasets.map(dataset => ({value: dataset, label: dataset.name}))}
                        onChange={(selectedOption) => {
                          setSelectedDataset(selectedOption);                          
                          if (selectedDataset.value !== null) {
                              handleDatasetChange();
                          }                                                                         
                        }}
                        placeholder="Select a dataset"                        
                        
                    />                
                </div>                   
               {/* MAKE PLOT FROM selectedDatasetData */}   
               <div className='h-full w-full min-w-fit min-h[600px] rounded-lg shadow-md p-4 mt-4 flex flex-col'>  
                {isLoading ? (
                    <div className="flex justify-center items-center h-40">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                ) : (
                    selectedDatasetColumns?.length > 0 ? 
                    <div className='h-full w-full flex flex-row gap-8'>                                
                        <Select
                            className='w-full h-full'
                            options={selectedDatasetColumns.map(column => ({value: column, label: column}))}
                            isMulti
                            onChange={(selectedOption) => {
                                setSelectedColumns(selectedOption.map(option => option.value));                                
                            }}  
                            placeholder="Select columns to plot"
                        /> 
                        <button
                            className="bg-slate-900 text-white text-sm rounded-md px-4 py-2"
                            onClick={handleTimeSeriesPlot}
                        >Get Time Series Plot
                        </button>   
                        <button
                            className="bg-slate-900 text-white text-sm rounded-md px-4 py-2"
                            onClick={handlePairScatterPlot}
                        >Get Pair Scatter Plot
                        </button>                                                                                                                        
                    </div>                 
                    : 
                    <div className='h-full w-fit rounded-lg shadow-md p-4 mt-4 flex flex-col'>
                        <p>No data to plot</p>
                    </div>
                )}
                </div>   
                <PlotBody plotRendered={plotRendered}/>
            </div>
        </div>
    )
}

export default Visualization