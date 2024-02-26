import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';

const DialogModal = ({ 
    children, open, onClose, header,  
    onConfirm, onCancel, 
    showCancelButton=false, showConfirmButton=true, 
    cancelButtonText="Cancel", confirmButtonText="Confirm",
    isSubmitButton=false, closeOnBackdropClick=true
 }) => {
    const handleClose = (event, reason) => {
        if (closeOnBackdropClick || reason !== 'backdropClick') {
            onClose(event, reason);
        }
    };
    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{header}</DialogTitle>
            <DialogContent>{children}</DialogContent>
            <DialogActions>
                {showCancelButton && (
                    <button onClick={onCancel} className='border-2 border-red-500 text-red-600 font-semibold mb-2 mr-2
                    hover:transition-colors hover:bg-red-600 hover:text-white py-2 px-6 rounded-lg'>{cancelButtonText}</button>
                )}
                {showConfirmButton && (
                    <button onClick={onConfirm} type={isSubmitButton ? 'submit' : 'button'} className='bg-slate-900 hover:transition-colors mb-2 mr-2
                    hover:bg-slate-500 text-white py-2 px-6 rounded-lg'>{confirmButtonText}</button>
                )}
            </DialogActions>
        </Dialog>
    );
};

export default DialogModal;
