import { useState,useEffect } from "react";
import { AuthContext } from "./authContext";

function AuthProvider({ children }) {
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        if (storedToken) {
            setToken(storedToken);
        }
        setLoading(false);
    }, []);

    const login = (newToken) => {
        localStorage.setItem("token", newToken);
        setToken(newToken);
    };  

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
    };
    
    return (
        <AuthContext.Provider value={{ token, setToken, login, logout, isAuthenticated: !!token, loading }}>
            {children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;
