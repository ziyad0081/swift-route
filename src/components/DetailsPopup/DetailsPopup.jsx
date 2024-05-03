
function DetailsPopup(props){

    const details = props.details
    const toggle = props.toggle
    
    return(
    <div className="fixed w-lvw mt-16 h-lvh logo-font bg-black z-50 bg-opacity-50" id="outer" onClick={(e)=>{
        if(e.target.id == "outer"){
            toggle(false)
        }
    }}>
        
        <div className="flex flex-col bg-slate-300 bg-opacity-100 rounded-xl p-2 fixed left-1/2 opacity-100 -translate-x-1/2 top-1/2 -translate-y-1/2   z-50 h-4/6 w-1/2 ring-2 ring-sky-600 ring-offset-4 ring-offset-transparent ">
            <h1 className="self-center font-bold text-xl">Search Details</h1>
            <div className="flex flex-col justify-around p-2 font-bold h-full">
                <h1>Is the returned node a goal ? <span className="text-sky-600">{String(details.found_goal).toUpperCase()}</span> </h1>
                <h1> Search time in <span className="text-sky-600">seconds : </span> {details.search_time.toFixed(4)} </h1>
                <h1>Peak memory consumption during search in <span className="text-sky-600">MB : </span> {details.peak_mem.toFixed(4)} </h1>
                <h1>Total expanded nodes: {details.expanded_nodes}/{details.max_nodes} ({((details.expanded_nodes/details.max_nodes)*100).toFixed(4)} % of search space) </h1>
                <h1>Cost of returned (solution / node) <span className="text-sky-600">(length in meters)</span> : {details.solution_cost.toFixed(2)} </h1>
            </div>
        </div>
    </div>
    )
}




export default DetailsPopup