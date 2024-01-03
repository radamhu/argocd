import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Deployments from "./pages/Deployments";
import Logo from "./components/Logo";
import SwaggerUI from './pages/Swagg';
import Status from './pages/Status';
import Application from './pages/Application';

export default props => (
  <div>
    <Logo/>
    <Router>
      <Routes>
        <Route path="/" element={<Deployments/>}/>
        <Route path="/api-docs" element={<SwaggerUI />} />
        <Route path="/status" element={<Status />} />
        <Route path="/app/:id" element={<Application />} />
      </Routes>
    </Router>
  </div>
);
 