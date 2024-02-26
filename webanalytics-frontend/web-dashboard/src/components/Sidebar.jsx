import HomeIcon from '@mui/icons-material/Home';
import TableChartIcon from '@mui/icons-material/TableChart';
import EqualizerIcon from '@mui/icons-material/Equalizer';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import { Link } from 'react-router-dom';

function Sidebar({ isOpen }){
    return(
        <div>
            <div className={`overflow-auto fixed top-0 -left-64 w-64 min-h-full py-6 bg-slate-900 shadow transition-transform duration-500 ease-in-out ${isOpen ? 'translate-x-full' : 'translate-x-0'}`}>
                <div className='h-[60px]'></div>
                <div className="flex-col justify-start items-start gap-4 inline-flex">
                    <Link to="/home"><div className="self-stretch h-10 px-10 py-8 min-w-64 justify-start items-center gap-[2vw] inline-flex 
                    hover:bg-slate-500 hover:transition-colors duration-300">
                        <HomeIcon sx={{color: "white"}}/>                    
                        <div className="text-zinc-100 text-base font-medium font-['Montserrat']">Home</div>
                    </div></Link>
                    <Link to="/datasets"><div className="self-stretch h-10 px-10 py-10 min-w-64 justify-start items-center gap-[2vw] inline-flex
                     hover:bg-slate-500 hover:transition-colors duration-300">
                        <TableChartIcon sx={{color: "white"}}/>
                        <div className="text-zinc-100 text-base font-medium font-['Montserrat']">Dataset</div>
                    </div></Link>
                    <Link to="/visualization"><div className="self-stretch h-10 px-10 py-10 min-w-64 justify-start items-center gap-[2vw] inline-flex 
                    hover:bg-slate-500 hover:transition-colors duration-300">
                        <EqualizerIcon sx={{color: "white"}}/>
                        <div className="text-zinc-100 text-base font-medium font-['Montserrat']">Visualization</div>
                    </div></Link>
                    <Link to="/prediction"><div className="self-stretch h-10 px-10 py-10 min-w-64 justify-start items-center gap-[2vw] inline-flex 
                    hover:bg-slate-500 hover:transition-colors duration-300">
                        <AutoGraphIcon sx={{color: "white"}}/>
                        <div className="text-zinc-100 text-base font-medium font-['Montserrat']">Prediction</div>
                    </div></Link>
                </div>
            </div>
        </div>
    )
}

export default Sidebar