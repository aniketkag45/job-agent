import { useContext} from 'react';
import { AuthContext } from '../context/authContext';
import { useNavigate } from 'react-router-dom';
import {useEffect} from 'react';
import api from '../api/axios';

function DashboardPage() {
    const{logout} = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {

  const fetchUser =
  async () => {

    try {

      const response =
      await api.get("/me")

      console.log(
        response.data
      )

    } catch (error) {

      console.log(error)
    }
  }

  fetchUser()

}, [])


    const handleLogout = () => {
        logout();
        navigate('/login');
    };
  return (
    <div className="min-h-screen bg-gray-100 p-10">

      <div className="flex justify-between items-center mb-10">

        <h1 className="text-4xl font-bold">

          Dashboard

        </h1>


        <button

          onClick={handleLogout}

          className="bg-red-500 text-white px-4 py-2 rounded-lg"
        >

          Logout

        </button>

      </div>

    </div>
  );
}

export default DashboardPage;