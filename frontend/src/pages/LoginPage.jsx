import {useState} from 'react';
import api from '../api/axios';
import { useContext } from 'react';
import { AuthContext } from '../context/authContext';
import { useNavigate } from 'react-router-dom';



function LoginPage() {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });
    const {login} = useContext(AuthContext);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const params = new URLSearchParams();
            params.append('username', formData.username);
            params.append('password', formData.password);
            const response = await api.post("/login", params,{headers: {'Content-Type': 'application/x-www-form-urlencoded'}});
            console.log(response.data);
            login(response.data.access_token);
            alert("Login successful!");
            navigate("/");
        } catch (error) {
            console.error("Error logging in:", error);
            alert("Login failed. Please check your credentials and try again.");
        }
    };

  return (

     <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-md w-[400px]"
      >

        <h1 className="text-3xl font-bold mb-6 text-center">

          Login

        </h1>


        <input
          type="text"
          name="username"
          placeholder="Email"
          onChange={handleChange}
          className="w-full border p-3 rounded-lg mb-4"
        />


        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          className="w-full border p-3 rounded-lg mb-6"
        />


        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded-lg"
        >

          Login

        </button>

      </form>

    </div>
  )
}

export default LoginPage