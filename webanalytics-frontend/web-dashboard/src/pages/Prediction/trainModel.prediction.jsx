

export const TrainModel = ({showTrainModelDialog, setShowTrainModelDialog, dataset_id}) => {
    const { currentUser, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const [ newModel, setNewModel ] = useState({
        name: '',
        description: '',
        dataset: '',
    });

    const handleTrainModel =  () => {
        console.log('Pressed')
        // setIsGlobalLoading(true);
        // try {
        //     const response = await trainNewModel(newModel, currentUser);
        //     if (response.status === 201 || response.status === 200) {
        //         alert('Model trained successfully');
        //     }
        // } catch (error) {
        //     alert('Error training model');
        //     console.error(error);
        //     setIsGlobalLoading(false);
        // } finally {
        //     setIsGlobalLoading(false);
        //     setShowTrainModelDialog(false);              
        //     window.location.reload();          
        // }
    }

    return (
        <>
            <DialogModal
                open={showTrainModelDialog}
                onClose={() => {setShowTrainModelDialog(false);}}
                header={<div className="font-bold">Train Model</div>}
                showCancelButton={true}
                onCancel={() => {setShowTrainModelDialog(false);}}
                confirmButtonText="Save"
                onConfirm={() => {handleTrainModel();}}
                isSubmitButton={true}
                closeOnBackdropClick={false}
            >
                <div className="font-normal">Train a new model</div>
                <div className="w-screen max-w-lg p-8">
                    <form className="space-y-6" onSubmit={handleTrainModel}>
                        <input 
                            type="text" 
                            placeholder="Name*" 
                            onChange={(e) => setNewModel(prevState => ({...prevState, name: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />  
                        <input 
                            type="text" 
                            placeholder="Description" 
                            onChange={(e) => setNewModel(prevState => ({...prevState, description: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                        />
                        <input 
                            type="text" 
                            placeholder="Dataset*" 
                            onChange={(e) => setNewModel(prevState => ({...prevState, dataset: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                    </form>
                </div>
            </DialogModal>
        </>
    )        
    

}