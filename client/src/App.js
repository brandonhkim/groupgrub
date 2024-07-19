import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import {SocketContext, socket} from './context/socket';
import { Toaster } from 'react-hot-toast';
import ConditionalLobbyRoute from './components/ConditionalLobbyRoute/ConditionalLobbyRoute';
import HomePage from './pages/HomePage/HomePage';
import SetupPage from './pages/SetupPage/SetupPage';
import CategoriesPage from './pages/CategoriesPage/CategoriesPage';
import SwipingPage from './pages/SwipingPage/SwipingPage';
import ResultsPage from './pages/ResultsPage/ResultsPage';
import ErrorPage from './pages/ErrorPage/ErrorPage';
import styles from "./styles/App.module.css";

const SetupRoute = ConditionalLobbyRoute(SetupPage, 'setup');
const CategoriesRoute = ConditionalLobbyRoute(CategoriesPage, 'categories');
const SwipingRoute = ConditionalLobbyRoute(SwipingPage, 'swiping');
const ResultsRoute = ConditionalLobbyRoute(ResultsPage, 'results');

function App() {
    return (
        <div>
            <SocketContext.Provider value={socket}>
                <Toaster />
                <BrowserRouter>
                    <Routes>
                        <Route 
                            path="/" 
                            element={<HomePage />}
                        />
                        <Route 
                            path="/lobby/:lobbyID/setup" 
                            element={<SetupRoute />} 
                        />
                        <Route 
                            path="/lobby/:lobbyID/categories" 
                            element={<CategoriesRoute />} 
                        />
                        <Route
                            path="/lobby/:lobbyID/swiping"
                            element={<SwipingRoute />}
                        />
                        <Route
                            path="/lobby/:lobbyID/results"
                            element={<ResultsRoute />}
                        />
                        <Route 
                            path="*" 
                            element={<ErrorPage />} />
                    </Routes>
                </BrowserRouter>
            </SocketContext.Provider>
        </div>
    );
}

export default App;