import '../../App.css';
import logo from '../../assets/logo.png'   
function Navbar(){
    return(
        <div className=" flex logo-font text-4xl justify-center text-sky-600 items-center fixed h-16 bg-slate-800 w-lvw shadow-md">
            <h1>SwiftRoute</h1>
            <img src={logo} width={"50rem"} alt="" />
        </div>
    )
}

export default Navbar;