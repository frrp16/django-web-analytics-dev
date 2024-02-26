import React, { useState, useContext } from 'react';
import Select from 'react-select';

import DialogModal from '../../components/Dialog';

import { AuthContext } from '../../context/auth-context';
import { addNewDataset } from '../../services/connection.service';

export const AddDataset = ({showAddDatasetDialog, setShowAddDatasetDialog}) => {
    const { currentUser, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const [ newDataset, setNewDataset ] = useState({
        name: '',
        description: '',
        table_name: '',
    });

    const handleAddDataset = async () => {
        setIsGlobalLoading(true);
        try {
            const response = await addNewDataset(newDataset, currentUser);
            if (response.status === 201 || response.status === 200) {
                alert('Dataset added successfully');
            }
        } catch (error) {
            alert('Error adding dataset');
            console.error(error);
            setIsGlobalLoading(false);
        } finally {
            setIsGlobalLoading(false);
            setShowAddDatasetDialog(false);              
            window.location.reload();          
        }
    }

    return (
        <>
            <DialogModal
                open={showAddDatasetDialog}
                onClose={() => {setShowAddDatasetDialog(false);}}
                header={<div className="font-bold">Add Dataset</div>}
                showCancelButton={true}
                onCancel={() => {setShowAddDatasetDialog(false);}}
                confirmButtonText="Save"
                onConfirm={() => {handleAddDataset();}}
                isSubmitButton={true}
                closeOnBackdropClick={false}
            >
                <div className="font-normal">Add a new dataset</div>
                <div className="w-screen max-w-lg p-8">
                    <form className="space-y-6" onSubmit={handleAddDataset}>
                        <input 
                            type="text" 
                            placeholder="Name*" 
                            onChange={(e) => setNewDataset(prevState => ({...prevState, name: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />  
                        <input 
                            type="text" 
                            placeholder="Description" 
                            onChange={(e) => setNewDataset(prevState => ({...prevState, description: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                        />
                        <input 
                            type="text" 
                            placeholder="Table Name*" 
                            onChange={(e) => setNewDataset(prevState => ({...prevState, table_name: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />                    
                    </form>
                </div>
            </DialogModal>
        </>
    )

    
}