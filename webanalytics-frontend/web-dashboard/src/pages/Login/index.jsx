import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../../context/auth-context";
import DialogModal from "../../components/Dialog";

function Login(){
    const navigate = useNavigate();
    
    const { currentUser, login, setIsGlobalLoading } = useContext(AuthContext) 

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [showPassword, setShowPassword] = useState(false);
    const [showLoginDialog, setShowLoginDialog] = useState(false);

    const handleLogin = async (event) => {
        event.preventDefault();
        try{
            setIsGlobalLoading(true);
            const res = await login(username, password);
            if(res.status === 200){
                console.log('Logged in');
                setShowLoginDialog(true);
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
            open={showLoginDialog}
            onClose={() => setShowLoginDialog(false)}
            header={<div className="font-bold text-center">Notification</div>}            
            confirmButtonText="OK"
            onConfirm={() => {
                setShowLoginDialog(false)
                navigate('/home')
            }}
        >
            <div className="font-normal px-8 py-2 text-center">Login Success!</div>
        </DialogModal>
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="p-6 shadow-md rounded-2xl bg-white">                
                {/* login form */}
                <div className="w-screen max-w-lg p-12">
                    <h1 className="text-3xl font-bold mb-6 text-center">Login</h1>
                    <form onSubmit={handleLogin} className="space-y-6">
                        <input 
                            type="text" 
                            placeholder="Username" 
                            onChange={(e) => setUsername(e.target.value)} 
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                        <div className="relative">
                            <input 
                                type={showPassword ? "text" : "password"} 
                                placeholder="Password" 
                                onChange={(e) => setPassword(e.target.value)} 
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
                            className="w-full p-2 bg-slate-700 text-white rounded hover:bg-slate-500" 
                        >
                            Login
                        </button>
                        <button 
                            type="button" 
                            onClick={() => navigate('/register')}
                            className="w-full p-2 text-center font-medium hover:underline hover:text-blue-300 text-blue-500"
                        >
                            Create new account
                        </button>
                    </form>
                </div>

            </div>
        </div>
    </>
    )
}

export default Login;