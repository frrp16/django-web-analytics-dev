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
            <div className="fixed w-full h-full inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
                <Spinner className="h-16 w-16 text-blue-700" />
            </div>
      )}
        <Navbar  />  
        <div className='w-screen h-[70px]'></div>
        <div className='flex'>
          <Sidebar isOpen={isSidebarOpen} />
          <div
            className={`overflow-auto px-6 pb-2 ${isSidebarOpen ? 'translate-x-64' : 'translate-x-0'} min-w-[200px]`}
            style={{ width: isSidebarOpen ? 'calc(100% - 256px)' : '100%'}}
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
