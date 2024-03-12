import { useState, useContext, useEffect, useRef, memo } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket'; 

import MenuIcon from '@mui/icons-material/Menu';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import NotificationsIcon from '@mui/icons-material/Notifications';

import { AuthContext } from '../context/auth-context';
import DialogModal from './Dialog';



function Navbar({ toggleSidebar }){
    const [isSpinning, setIsSpinning] = useState(false);
    const [showDialog, setShowDialog] = useState(false);

    const notificationMessage = useRef([])
    

    const { 
        currentUserInformation, logout, 
        socketURL, socketConncted, setSocketConnected 
    } = useContext(AuthContext);
    
    const {
        sendMessage,
        lastMessage,
        readyState,
        getWebSocket,
    } = useWebSocket(socketURL);

    useEffect(() => {
        if (readyState === ReadyState.OPEN && !socketConncted) {
            console.log('Connected');
            setSocketConnected(true);
        }
    }
    , [readyState]);

    // useEffect(() => {
    //     if (socketURL ) {
    //         getWebSocket(socketURL);
    //     }
    // }
    // , [socketURL]);

    useEffect(() => {
        if (lastMessage) {
            // console.log(lastMessage.data);
            // setNotificationMessage((prev) => [...prev, lastMessage.data]);            
            notificationMessage.current.push(lastMessage.data);
            console.log(notificationMessage.current);
        }
    }
    , [lastMessage]);

    useEffect(() => {
        if (socketConncted) {
            sendMessage('Hello');
        }
    }
    , [socketConncted]);


        // Clean up function
        // Only re-run the effect if socketURL changes

    // useEffect(() => {
    //     if (notificationMessage) {
    //         setNotificationMessage(notificationMessage);
    //         console.log(notificationMessage)
    //     }
    // }
    // , [notificationMessage]);

    const handleClick = () => {
        setIsSpinning(true);
        toggleSidebar();
        setTimeout(() => setIsSpinning(false), 500); // Set back to false after 500ms
    };

    return(
        <div>     
            <DialogModal 
                open={showDialog}
                onClose={() => setShowDialog(false)}
                header={<div className='font-bold'>Logout</div>}                
                showCancelButton={true}
                onConfirm={() => {
                    logout();
                    setShowDialog(false);
                }}
                onCancel={() => setShowDialog(false)}
            >
                <div className='font-normal'>Are you sure you want to logout?</div>                
            </DialogModal>       
            <div className="w-screen h-[70px] px-[30px] py-5 bg-zinc-100 shadow 
            justify-between top-0 left-0 fixed items-center inline-flex z-50">
                <div className='inline-flex gap-[2vw] items-center'>
                    {toggleSidebar != null ? <div className={`${isSpinning ? 'animate-spin' : ''}
                     hover:bg-slate-300 hover:transition-colors duration-300 p-3 rounded-full`} onClick={handleClick}>
                        <MenuIcon sx={{height: 30, width: 30}}/>
                    </div>
                    : <div></div>}
                    {/* hide when in mobile size */}
                    <h1 className='text-2xl font-semibold md:block hidden'>Web Analytics</h1>
                </div>
                <div className='inline-flex w-72 h-7 justify-end items-center gap-[1.5vw]'>
                    <div className='inline-flex gap-4 items-center hover:bg-slate-300 
                    hover:transition-colors duration-300 px-6 py-3 rounded-full'>
                        <AccountCircleIcon/>                        
                        <div className='font-semibold'>{currentUserInformation?.username}</div>                            
                    </div>
                    <div
                        className="hover:bg-slate-300 hover:transition-colors duration-300 p-3 rounded-full">
                        <NotificationsIcon/>
                    </div>
                    <div onClick={() => setShowDialog(true)} 
                        className="hover:bg-slate-300 hover:transition-colors duration-300 p-3 rounded-full">
                        <LogoutIcon/>
                    </div>                            
                </div>
            </div>          
        </div>
    )
}

export default memo(Navbar)