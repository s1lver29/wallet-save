import React, { useState, useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';


const LoginPage = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
        
            const response = await axios.post('http://localhost:8000/login', formData, {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'accept': 'application/json'
              }
            });
        
            const accessToken = response.data.access_token;
            localStorage.setItem('token', accessToken);

            if (response.status == 200) {
                navigate('/expenses');
            } else {
                navigate('/')
                console.error('Ошибка авторизации');
            }

        } catch (error) {
          console.error('Ошибка авторизации:', error);
        };
  };

  return (
    <div>
      <h1>Вход</h1>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Войти</button>
      </form>
    </div>
  );
};

export default LoginPage;
