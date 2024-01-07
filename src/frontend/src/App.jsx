import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import ExpensesPage from './components/ExpensesPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
  const token = localStorage.getItem('token');

  return (
    <Router>
      <Routes>
        <Route path='/' exact component={ExpensesPage} element={token ? <Navigate to='/expenses'/> : <LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/expenses" element={<ExpensesPage />} />
      </Routes>
      <ToastContainer />
    </Router>
  );
};

export default App;
