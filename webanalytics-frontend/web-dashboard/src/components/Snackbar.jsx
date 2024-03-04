import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

import { useState } from 'react';

export default function CustomizedSnackbars({
  children, open, onClose, severity
}) {    
  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    onClose(event, reason);
  };

  return (
    <div style={{ position: 'fixed', bottom: '10px', left: '10px', zIndex:999 }}>
      <Snackbar 
        open={open} 
        autoHideDuration={5000} 
        onClose={handleClose}        
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}     
      >
        <Alert
          onClose={handleClose}
          severity={severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {children}
        </Alert>
      </Snackbar>
    </div>
  );
}