import '../../App.css';
function Navbar(){
    return(
        <div className=" flex logo-font text-4xl justify-center text-sky-600 items-center fixed h-16 bg-slate-800 w-lvw shadow-md">
            <h1>SwiftRoute</h1>
            <img src="../../../public/logo.png" width={"50rem"} alt="" />
        </div>
    )
}

export default Navbar;