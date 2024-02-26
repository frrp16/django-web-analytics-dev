import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/auth-context";


import DialogModal from "../../components/Dialog";

function Register(){

    const { currentUser, register, setIsGlobalLoading } = useContext(AuthContext) 

    const navigate = useNavigate();
    
    const [userDetails, setUserDetails] = useState({
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        password: ''
      });

    const [showPassword, setShowPassword] = useState(false);
    const [showRegisterDialog, setShowRegisterDialog] = useState(false);
    // const [showRegister, setShowRegister] = useState(false);

    const handleRegister = async (event) => {
        event.preventDefault();
        console.log(userDetails)
        try{
            setIsGlobalLoading(true);
            const { first_name, last_name, email, username, password } = userDetails;
            const res = await register(first_name, last_name, username, email,  password);
            if(res.status === 200 || res.status === 201){
                setShowRegisterDialog(true);
            }            
            setIsGlobalLoading(false);
        }
        catch(error){
            alert('Error')
            setIsGlobalLoading(false)
        }

    }

    return(   
    <>        
        <DialogModal
            open={showRegisterDialog}
            onClose={() => setShowRegisterDialog(false)}
            header={<div className="font-bold">Notification</div>}            
            confirmButtonText="OK"
            onConfirm={() => {
                setShowRegisterDialog(false)
                navigate('/home')
            }}
        >
            <div className="font-normal">Register Success!</div>
        </DialogModal> 
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="p-6 shadow-md rounded-2xl bg-white">                 
                {/* login form */}
                <div className="w-screen max-w-lg p-12">
                    <h1 className="text-3xl font-bold mb-6 text-center">Register</h1>
                    <form onSubmit={handleRegister} className="space-y-6">
                        <input 
                            type="text" 
                            placeholder="First Name*" 
                            onChange={(e) => setUserDetails(prevState => ({...prevState, first_name: e.target.value}))} 
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                        <input 
                            type="text" 
                            placeholder="Last Name" 
                            onChange={(e) => setUserDetails(prevState => ({...prevState, last_name: e.target.value}))} 
                            className="w-full p-2 border border-gray-300 rounded"
                        />
                        <input 
                            type="email" 
                            placeholder="Email" 
                            onChange={(e) => setUserDetails(prevState => ({...prevState, email: e.target.value}))} 
                            className="w-full p-2 border border-gray-300 rounded"
                            
                        />
                        <input 
                            type="text" 
                            placeholder="Username*" 
                            onChange={(e) => setUserDetails(prevState => ({...prevState, username: e.target.value}))} 
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                        <div className="relative">
                            <input 
                                type={showPassword ? "text" : "password"} 
                                placeholder="Password*" 
                                onChange={(e) => setUserDetails(prevState => ({...prevState, password: e.target.value}))} 
                                className="w-full p-2 border border-gray-300 rounded"
                                required
                            />
                            <button 
                                type="button" 
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm font-medium text-gray-600"
                            >
                                {showPassword ? "Hide" : "Show"}
                            </button>
                        </div>
                        <button 
                            type="submit" 
                            className="w-full p-2 bg-slate-700 text-white rounded"
                        >
                            Create Account
                        </button>
                        <button 
                            type="button" 
                            onClick={() => {navigate('/login')}}
                            className="w-full p-2 text-center font-medium hover:underline hover:text-blue-300 text-blue-500"
                        >
                            Login with existing account
                        </button>
                    </form>
                </div>

            </div>
        </div>
    </>
    )
}

export default Register;