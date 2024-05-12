import { useState } from "react"

function DetailsPopup(props){

    const details = props.details
    const toggle = props.toggle
    const [toggleInner , setToggleInner] = useState(false)
    return(
    <div className="fixed w-lvw mt-16 h-lvh logo-font bg-black z-50 bg-opacity-50" id="outer" onClick={(e)=>{
        if(e.target.id == "outer"){
            toggle(false)
        }
    }}>
        
        <div className="flex flex-col bg-slate-300 bg-opacity-100 rounded-xl p-2 fixed left-1/2 opacity-100 -translate-x-1/2 top-1/2 -translate-y-1/2   z-50 h-4/6 w-1/2 ring-2 ring-sky-600 ring-offset-4 ring-offset-transparent ">
            <h1 className="self-center font-bold text-xl">Search Details</h1>
            <div className="flex flex-col justify-around p-2 font-bold h-full">
                <h1>Used pathfinder algorithm : <span className="text-sky-600">{details.algorithm}</span></h1>
                <h1>Is the returned node a goal ? <span className="text-sky-600">{String(details.found_goal).toUpperCase()}</span> </h1>
                <h1> Search time in <span className="text-sky-600">seconds : </span> {details.search_time.toFixed(4)} </h1>
                <h1>Peak memory consumption during search in <span className="text-sky-600">MB : </span> {details.peak_mem.toFixed(4)} </h1>
                <h1>Total expanded nodes: {details.expanded_nodes}/{details.max_nodes} ({((details.expanded_nodes/details.max_nodes)*100).toFixed(4)} % of search space) </h1>
                <h1>Cost of returned (solution / node) <span className="text-sky-600">(length in meters)</span> : {details.solution_cost.toFixed(2)} </h1>
                <button className={"text-white  transition-all ease-linear w-max p-2 rounded self-center " + (!details.viz_available ? "bg-slate-500 cursor-not-allowed" : " bg-sky-600 hover:bg-sky-700")} onClick={details.viz_available ? (()=>setToggleInner(true)) : undefined}>Show search space</button>
                
            </div>
        </div>

        {toggleInner && <div className="flex flex-col px-4 py-2  bg-slate-300 w-11/12 h-3/4 fixed z-50 left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-xl ring-2 ring-sky-600 ring-offset-4 ring-offset-transparent">
        <div className="flex  gap-4">
            <div className="font-bold text-center w-2/3">
                <h1 className="mb-4">Overall search space</h1>
                <img className="rounded-xl w-full h-5/6" src={"data:image/png;base64,"+details.overall_img} alt="" srcset="" />
            </div>
            <div className="font-bold text-center w-1/3">
                <h1 className="mb-4">close-up search space</h1>
                <img className="w-full h-5/6 rounded-xl" src={"data:image/png;base64,"+details.detailed_img} alt="" srcset=""/>
            </div>
        </div>
        <h1 className="absolute font-bold text-sm bottom-2">*Open Images in new tab for better visibility</h1>
        <button className="absolute left-1/2 bottom-2 -translate-x-1/2 p-2 bg-sky-600 rounded-xl font-bold text-white hover:bg-sky-700 transition-all" onClick={()=>setToggleInner(false)}>Close</button>
        </div>}
    </div>
    )
}




export default DetailsPopup