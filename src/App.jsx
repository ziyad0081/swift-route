import './App.css'
import { MapContainer, Marker, Popup, TileLayer, useMapEvents, useMap, Polyline } from 'react-leaflet'
import "leaflet/dist/leaflet.css"
import Navbar from './components/navbar/navbar';
import UserForm from './components/userForm/UserForm';
import { useEffect, useRef, useState } from 'react';


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

  
  const [userLatitude, setLatitude] = useState(null)
  const [userLongitude, setLongitude] = useState(null)
  const [loading, setLoading] = useState(true);
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
  
  
  return (
    <>
    <Navbar/>
    <div className="flex w-lvw pt-16 h-lvh flex-row font-mono items-center justify-between">
      
    <UserForm  latitude = {[userLatitude,setLatitude]} longitude={[userLongitude,setLongitude]}/>
    
    {
    !loading && <MapContainer ref={mapRef} center={[userLatitude,userLongitude]} zoom={13} scrollWheelZoom={false}>
      <ClickHandler/>
      <MapRecenter lat={userLatitude} lng={userLongitude} zoomLevel={13}/>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    {
     userLatitude && <Marker position={[userLatitude,userLongitude]} draggable={true}>
      <Popup>
        A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
    </Marker> }
    <Polyline pathOptions={{ color: 'blue' }} positions={coordinates} />
    </MapContainer>
  }

    </div>
    </>
  )
}

export default App
