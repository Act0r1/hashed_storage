import './App.css';
import { Routes, Route } from "react-router-dom";
import Login from "./login";
import Profile from "./profile";
// import logo from ".logo"



function App() {
  return (
    <div className="App">
    <Routes>
      <Route path="/" element = {<Login/>}/>
      <Route path="/profile" element = {<Profile/>}/>
    </Routes>
    </div>
  );
}

export default App;
