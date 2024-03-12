import { useContext, useState } from 'react'
import { createBrowserRouter, RouterProvider, Outlet, Navigate } from 'react-router-dom';

import { Spinner } from '@material-tailwind/react'

import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'

import Home from './pages/Home'
import Datasets from './pages/Datasets'
import Visualization from './pages/Visualization';
import Prediction from './pages/Prediction';
import Login from './pages/Login';
import Register from './pages/Register';
import { AuthContext } from './context/auth-context';

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const { currentUser, isGlobalLoading } = useContext(AuthContext)
  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);



  const ProtectedRoute = ({ children }) => {    
    if(!currentUser){
      return <Navigate to='/login' />;
    }
    else{
      
      return children;
    }
  }

  const Layout = () => {
      return (
      <>
      {isGlobalLoading && (
            // create loading with spinner
            <div className='fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 z-50 flex justify-center items-center'>
              <div class="border-t-transparent border-solid animate-spin rounded-full border-blue-500 border-8 h-32 w-32"></div>
            </div>
      )}
        <Navbar />  
        <div className='w-screen h-[70px]'></div>
        <div className='flex flex-row'>
          <Sidebar isOpen={isSidebarOpen} />
          <div className='min-w-64'></div>
          <div
            className={`overflow-auto px-6 pb-2 w-full min-w-[200px]`}
            // className={`overflow-auto pb-2 min-w-[200px] px-6 w-full transition-transform duration-500 ease-in-out ${isSidebarOpen ? 'translate-x-64' : 'translate-x-0'}`}            
            // style={{ width: isSidebarOpen ? 'calc(100% - 256px)' : '100%'}}
          >
            <Outlet />
          </div>
        </div>
      </>
    ) 
  }

  const router = [
    { 
      path: '/', 
      element: (
        <ProtectedRoute>
          <Layout /> 
        </ProtectedRoute>
      ), 
      children: [
        { path: '/home', element: <Home /> },
        { path: '/datasets', element: <Datasets /> },
        { path: '/visualization', element: <Visualization /> },
        { path: '/prediction', element: <Prediction /> },

        { path: '/', element: <Navigate to='/home' /> },
      ]
    },
    { path: '/login', element: <Login /> },
    { path: '/register', element: <Register/>},
    { path: '/', element: <Navigate to='/login' /> }
  ];

  return(
    <>
      <RouterProvider router={createBrowserRouter(router)}/>
    </> 
  )
}

export default App
