import React, { useState, useContext } from 'react';
import Select from 'react-select';

import DialogModal from '../../components/Dialog';

import { addNewConnection } from '../../services/connection.service';

import { AuthContext } from '../../context/auth-context';


export const AddConnection = ({showAddDatabaseDialog, setShowAddDatabaseDialog}) => {

    const { currentUser, isGlobalLoading, setIsGlobalLoading } = useContext(AuthContext);

    const [newConnection, setNewConnection] = useState({
        database_type: '',
        host: '',
        database: '',
        port: '',
        username: '',
        password: '',
        ssl: false
    });   

    // Add database connection
    const handleAddDatabase = async () => {
        setIsGlobalLoading(true);
        try{
            const response = await addNewConnection(newConnection, currentUser);
            if (response.status === 201 || response.status === 200){                
                alert('Database connection added successfully');          
            }        
        }
        catch(error){
            alert('Error adding database connection');
            console.error(error);
            setIsGlobalLoading(false);
        }
        finally{
            setIsGlobalLoading(false);
            setShowAddDatabaseDialog(false);
            // refresh screen
            window.location.reload();
        }
    }

    return (
        <>
            <DialogModal
                open={showAddDatabaseDialog}
                onClose={() => {setShowAddDatabaseDialog(false);}}
                header={<div className="font-bold">Add Database</div>}                            
                showCancelButton={true}
                onCancel={() => {setShowAddDatabaseDialog(false);}}
                confirmButtonText="Save"
                onConfirm={() => {handleAddDatabase();}}   
                isSubmitButton={true}   
                closeOnBackdropClick={false}                  
            >
                <div className="font-normal">Add a new database connection</div>
                {/* Add database connection form */}
                <div className="w-screen max-w-lg p-8">
                    <form className="space-y-6" onSubmit={handleAddDatabase}>
                        <Select
                            onChange={(e) => setNewConnection(prevState => ({...prevState, database_type: e.value}))}
                            className="w-full border border-gray-300 rounded"
                            placeholder="Database Type*"
                            required    
                            options={
                                [
                                    { value: 'mysql', label: 'MySQL' },
                                    { value: 'postgresql', label: 'PostgreSQL' },                                        
                                    { value: 'sqlite', label: 'SQLite' },
                                    { value: 'oracle', label: 'Oracle' },
                                    { value: 'mariadb', label: 'MariaDB' },                                                                                                
                                ]
                            }                                                                                                           
                        />                                                                             
                        <input 
                            type="text" 
                            placeholder="Host*" 
                            onChange={(e) => setNewConnection(prevState => ({...prevState, host: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />                                    
                        <input 
                            type="number" 
                            placeholder="Port*" 
                            onChange={(e) => setNewConnection(prevState => ({...prevState, port: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                        <input 
                            type="text" 
                            placeholder="Database Name*" 
                            onChange={(e) => setNewConnection(prevState => ({...prevState, database: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                        <input 
                            type="text" 
                            placeholder="Username*" 
                            onChange={(e) => setNewConnection(prevState => ({...prevState, username: e.target.value}))}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                        <div className="relative">
                            <input 
                                type="password" 
                                placeholder="Password*" 
                                onChange={(e) => setNewConnection(prevState => ({...prevState, password: e.target.value}))}
                                className="w-full p-2 border border-gray-300 rounded"
                                required
                            />
                        </div>   
                        <div className="flex flex-row items-center gap-4">
                            <input 
                                type="checkbox" 
                                onChange={(e) => setNewConnection(prevState => ({...prevState, ssl: e.target.checked}))}
                                className="w-4 h-4"
                            />
                            <label>Always use SSL connection</label>
                        </div>                                 
                    </form>
                </div>
            </DialogModal>  
        </>
    )
}