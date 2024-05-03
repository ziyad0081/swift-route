import './App.css'
import { MapContainer, Marker, Popup, TileLayer, useMapEvents, useMap, Polyline } from 'react-leaflet'
import "leaflet/dist/leaflet.css"
import Navbar from './components/navbar/navbar';
import UserForm from './components/userForm/UserForm';
import { useEffect, useRef, useState } from 'react';
import data from './assets/data/hospital_info.json'
import services from './assets/data/hospitals.json'
import { Icon, icon } from 'leaflet';
import DetailsPopup from './components/DetailsPopup/DetailsPopup';
function App() {
  const mapRef = useRef()
  function ClickHandler() {
    const map = useMapEvents({
        click(e) {
            setLatitude(e.latlng.lat);
            setLongitude(e.latlng.lng);
        },
        
    });
    return null;

}

  const hospital_icon = icon({
    iconUrl: 'https://i.imgur.com/i0sha8g.png',
    iconSize: [32, 32],
  })
  const [userLatitude, setLatitude] = useState(null)
  const [userLongitude, setLongitude] = useState(null)
  const [loading, setLoading] = useState(true);
  const [points,  setPoints] = useState([])
  const [search_details, setDetails] = useState(null)
  const [togglePopup, setTogglePopup] = useState(false)
  const coordinates = [
    [51.505, -0.09],
    [51.51, -0.1],
    [51.51, -0.12]
  ];
  const MapRecenter= ({ lat, lng, zoomLevel }) => {
    const map = useMap();
  
    useEffect(() => {
      // Fly to that coordinates and set new zoom level
      map.flyTo([lat, lng], zoomLevel );
    }, [lat, lng]);
    return null;
  
  };
  useEffect(()=>console.log(points),[points])  
  useEffect(() => {
    
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(position.coords.latitude);
        setLongitude(position.coords.longitude);
        setLoading(false);
      },
      (error) => {
        console.error('Error getting geolocation:', error);
        setLoading(false);
      }
    );
  }, []);
  
  const markers = Object.entries(data).map(([id, { name , lat, lng }]) => ( 
    <Marker icon={hospital_icon} key={id} position={[lat, lng]}> 
      <Popup>
        <div  className='font-bold logo-font text-center'><span>{name}</span></div>
      </Popup>
    </Marker>
  ));
  const user_marker = <Marker position={[userLatitude, userLongitude]}> 
  <Popup>
    <p className=' font-bold logo-font'>You are here !</p>
  </Popup>
</Marker>
  return (
    <>
    <Navbar/>
    <div className="flex w-lvw pt-16 h-lvh flex-row font-mono items-center justify-between">
    
    <UserForm  latitude = {[userLatitude,setLatitude]} longitude={[userLongitude,setLongitude]} setPoints = {setPoints} details={[search_details, setDetails]} toggle={[togglePopup, setTogglePopup]}/>
    
    {
    !loading && <MapContainer ref={mapRef} center={[userLatitude,userLongitude]} zoom={13} scrollWheelZoom={false}>
      <ClickHandler/>
      <MapRecenter lat={userLatitude} lng={userLongitude} zoomLevel={16}/>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    {markers}
    {user_marker}
    { points.length && <Polyline positions={points}/>}
    </MapContainer>
  }
    { togglePopup && search_details ?
      <DetailsPopup details={search_details} toggle={setTogglePopup}/>:
      null
    }
    </div>
    </>
  )
}

export default App
