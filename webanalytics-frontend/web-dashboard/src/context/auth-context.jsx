import { createContext, useEffect, useState } from "react";

import axios from "axios";
import Cookies from "js-cookie";

const BASE_API_URL = "http://127.0.0.1:8000/";

export const AuthContext = createContext();

export const AuthContextProvider = ({ children }) => {
    const accessTokenCookie = Cookies.get('accessToken');
    const [currentUser, setCurrentUser] = useState(accessTokenCookie ? JSON.parse(accessTokenCookie) : null);
    const [currentUserInformation, setCurrentUserInformation] = useState(JSON.parse(sessionStorage.getItem('currentUserInformation')) || null);
    const [isGlobalLoading, setIsGlobalLoading] = useState(false);

    const login = async (username, password) => {    
         
        try {
            setIsGlobalLoading(true)   
            const response = await axios.post(`${BASE_API_URL}login/`, {
                username,
                password
            });

            if (response.status === 200){
                Cookies.set(
                    'accessToken', JSON.stringify(response.data.access),
                    { expires: 1/2, secure: false, sameSite: 'lax'}
                )
                setCurrentUser(response.data.access)
            }
            return response
        } catch (error) {
            console.error(error);
        }
        finally{
            setIsGlobalLoading(false)
        }
    };

    const register = async (first_name, last_name, username, email, password) => {
        try { 
            setIsGlobalLoading(true)              
            const response = await axios.post(`${BASE_API_URL}register/`,{
                first_name, last_name, username, email, password
            })
            if (response.status === 200){
                Cookies.set(
                    'accessToken', JSON.stringify(response.data.access),
                    { expires: 1/2, secure: false, sameSite: 'lax'}
                )
                setCurrentUser(response.data.access)
            }
            return response
        } catch (err){
            console.log(err)
        }
        finally{
            setIsGlobalLoading(false)
        }   
    }

    const logout = () => {
        Cookies.remove('accessToken');
        sessionStorage.clear()
        setCurrentUser(null);
        setCurrentUserInformation(null);
    };

    useEffect(() => {        
        Cookies.set(
            'accessToken', JSON.stringify(currentUser),
            { expires: 1/2, secure: false, sameSite: 'lax'}
        )
    }, [currentUser]);

    useEffect(() => {        
        async function fetchCurrentUserInformation(){
            try {                
                setIsGlobalLoading(true)
                const response = await axios.get(`${BASE_API_URL}users/`, {
                    headers: {
                        Authorization: `Bearer ${currentUser}`
                    }
                });
                if (response.status === 200){
                    sessionStorage.setItem('currentUserInformation', JSON.stringify(response.data))
                    setCurrentUserInformation(response.data)
                }
            } catch (error) {
                console.error(error);
            }
            finally{
                setIsGlobalLoading(false)
            }
            
        }
        if(currentUser){
            fetchCurrentUserInformation()
        }
    }, [currentUser])

    return (
        <AuthContext.Provider value={
            { 
                currentUser, setCurrentUser, 
                currentUserInformation, setCurrentUserInformation,  
                isGlobalLoading, setIsGlobalLoading,               
                login, register, logout }
        }>
            {children}
        </AuthContext.Provider>
    );
}