/* eslint-disable react/prop-types */
import { useState } from "react";
import '../../App.css'
import axios from "axios";
import { useMap } from "react-leaflet";
import services from '../../assets/data/hospitals.json'
import DetailsPopup from "../DetailsPopup/DetailsPopup";
import spinner from "../../assets/180-ring.svg"



const methods = ["Uniform Cost Search","AStar", "Breadth First Search", "Iterative-Deepening Search","Hill Climbing Search", "K-Local Beam Search", "Simulated Annealing"]    
const values = ["UCS","A*","BFS","IDS","HC","KLBS", "SA"]
function UserForm(props){
    const [search_method, setMethod] = useState("UCS")
    const [selectedValue, setSelected] = useState('')
    const [useLocalServer, setLocalServer] = useState(false)
    const [GenerateViz, setViz] = useState(false)
    const options = Object.keys(services.services).sort()
    const setPoints = props.setPoints
    const select = <select className="shadow font-bold appearance-none border rounded transition-all ease-linear hover:ring-4 hover:ring-sky-500 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" value={selectedValue} onChange={(e)=>{
        setSelected(e.target.value)
        if(search_details){
            setDetails(null)
         }
        }}>
        <option disabled selected value="">Choose a service</option>
    {options.map((option) => (
      <option className="text-gray-700 font-logo font-bold" key={option} value={option}>
        {option}
      </option>
    ))}
  </select>
    const select_method = <select className="shadow font-bold appearance-none border rounded transition-all ease-linear hover:ring-4 hover:ring-sky-500 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" value={search_method} onChange={(e)=>{
        setMethod(e.target.value)    
        if(search_details){
            setDetails(null)
         }
        }}>
    {values.map((method,i) => (
      <option className="text-gray-700 font-logo font-bold" key={i}  value={method}>
        {method}
      </option>
    ))}
  </select>
    
  
    const [search_details, setDetails] = props.details
    const [toggle, setToggle] = props.toggle    
    const [userLat, setUserLat] = props.latitude 
    const [userLng, setUserLng] = props.longitude
    const [targetHospital, setTargetHospital] = useState(null)
    const [userAddress, setAddress] = useState("")
    const flyTo = props.flyTo
    const [userReqService, setUserRequestedService] = useState(null)
    const [loading, setLoading] = useState(false)
    
    async function handleGeocoderResult(){
        setLoading(true)
        const api_response = await axios.get('https://nominatim.openstreetmap.org/search?q='+ userAddress +'&format=json')
        const data = api_response.data
        
        if(data.length > 0){
            setUserLat(parseFloat(data[0].lat))
            setUserLng(parseFloat(data[0].lon))
            console.log(data[0].lat,data[0].lon);
            const req = await axios.post("http://127.0.0.1:5000/endpoint",{
                data: {
                    "lat":userLat,
                    "lng" : userLng
                }
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            } )
        }
        setLoading(false)
    }
    async function handleUserReq(){
        setLoading(true)
        try {
            let endpoint = useLocalServer ? "http://127.0.0.1:5000/get_nearest" : "http://ziyeus.pythonanywhere.com/get_nearest";

            let api_res = await axios.post(endpoint, {
            data: {
                "serv" : selectedValue,
                "lat":userLat,
                "lng" : userLng,
                "method": search_method,
                "viz" : GenerateViz
            }
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })    
        
        api_res.data.details.algorithm = search_method
        api_res.data.details["viz_available"] = GenerateViz
        setDetails(api_res.data.details)
        setLoading(false)
        setPoints(api_res.data.iter.map(point=>[point.lat, point.lng]))
        setTargetHospital(api_res.data.hos_name)
        } catch (error) {
            setLoading(false)
        }
        
        
        
    }
    return (
    <div className='flex  logo-font flex-col items-center h-full p-4 w-1/2'>
        <h1 className="font-bold text-center text-sky-600 text-2xl w-11/12"> Enter your address and requested service below and hit go !</h1>
        <p className="mt-5">Alternatively you can <span className="font-bold text-sky-500">drop a marker</span> on the map to locate your current position</p>
        <hr className="w-full h-px bg-gray-200 border-none mt-4 mb-4"/>
        <label htmlFor="service" className=" self-start ml-4 mb-4 font-bold text-xl"> Emergency Service </label>
        {select}
        <label htmlFor="method" className=" self-start ml-4 m-4 font-bold text-xl"> Pathfinder Method </label>
        {select_method}
        
        
        <div className="flex gap-2 w-full px-2 mt-2 " title="Flask app MUST be listening on 127.0.0.1:5000/get_nearest. Speeds up response time CONSIDERABLY.">
            <input name="local" type="checkbox" onChange={(e)=>setLocalServer(e.target.checked)}/>
            <h2 className="font-bold">Use local Flask server </h2>
        </div>
        <div className="flex gap-2 w-full px-2 " title="(Slows up response time CONSIDERABLY)">
            <input name="local" type="checkbox" onChange={(e)=>setViz(e.target.checked)}/>
            <h2 className="font-bold">Generate search space visualization</h2>
        </div>
        <div className="flex w-full justify-around">
            <button className={ "p-2 mt-4 rounded text-yellow-50 font-bold transition-all ease-in " + (loading ? "bg-slate-500" : "bg-sky-500 hover:bg-sky-600") } onClick={loading ? undefined:handleUserReq}> { loading ? <object type="image/svg+xml" data={spinner}></object> : "Generate Path" } </button>
            <button className={ "p-2 mt-4 rounded text-yellow-50 font-bold transition-all ease-in " + (loading || !search_details ? "bg-slate-500 cursor-not-allowed" : "bg-sky-500 hover:bg-sky-600") } onClick={loading || !search_details ? undefined : ()=>setToggle(true) }> Search Details </button>
        </div>
        {
            targetHospital && <h2  className="mt-2 mb-2"> Closest hospital meeting criterion :  <span className= "text-rose-600 font-bold"> {targetHospital} </span> </h2>
        }
        {
          userLat && <h2 className="font-bold "> Your current chosen coordinates are <span className="text-sky-600 font-bold">({userLat.toFixed(5)},{userLng.toFixed(5)})</span> </h2>
        }
        
    </div>
    )
}
export default UserForm;