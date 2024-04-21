/* eslint-disable react/prop-types */
import { useState } from "react";
import '../../App.css'
import axios from "axios";
import { useMap } from "react-leaflet";


function UserForm(props){
    const [userLat, setUserLat] = props.latitude 
    const [userLng, setUserLng] = props.longitude
    const [userAddress, setAddress] = useState("")
    const flyTo = props.flyTo
    const [userReqService, setUserRequestedService] = useState('General')
    async function handleGeocoderResult(){
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
            console.log(req)
        }
    }
    return (
    <div className='flex  logo-font flex-col items-center h-full p-4 w-1/2'>
        <h1 className="font-bold text-center text-sky-600 text-3xl w-80"> Enter your address and requested service below and hit go !</h1>
        <p className="mt-10 mb-2">Alternatively you can drop a marker on the map to locate your current position</p>
        <hr className="w-full h-px bg-gray-200 border-none  mb-10"/>
        <label htmlFor="adress" className=" self-start ml-4 mb-4 font-bold text-xl"> Adress </label>
        <input type="text" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" name="adress" value={userAddress} onChange={(e)=>setAddress(e.target.value)} placeholder="Jane Ave, John City, Jeffrson Country..."/>
        <hr className="w-full h-px bg-gray-200 border-none mt-4 mb-4"/>
        <label htmlFor="adress" className=" self-start ml-4 mb-4 font-bold text-xl"> Emergency Service </label>
        <input type="text" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" name="adress" placeholder="Some Service ..."/>
        <button className="p-2 mt-4 rounded bg-sky-500 text-yellow-50 font-bold hover:bg-sky-700 transition-all ease-in" onClick={handleGeocoderResult}>Locate Address</button>
        {
          userLat && <h2 className="font-bold mt-10"> Your current chosen coordinates are <span className="text-sky-600">({userLat.toFixed(5)},{userLng.toFixed(5)})</span> </h2>
        }
    </div>
    )
}
export default UserForm;