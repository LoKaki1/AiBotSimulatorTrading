import React from "react";
import { useLoader } from "../../../../../Hooks/Context/LoaderContext";
import './Loader.css'

export default function Loader() {
  const { loader } = useLoader();
  return (loader ? <div style={{position: 'relative', bottom: '80%', left: '78%'}} className="loader"></div> : <div></div>);
}
