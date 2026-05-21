import React from 'react'
import { Toaster } from "react-hot-toast"
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import AuthProvider from './context/AuthContext.jsx';
import SavedJobsProvider from './context/SavedJobsContext.jsx'



ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <SavedJobsProvider>
        <App />
      </SavedJobsProvider>
      <Toaster
  position="top-right"
  toastOptions={{
    style: {
      background: "#111827",
      color: "#fff",
      border: "1px solid rgba(255,255,255,0.1)",
      padding: "16px",
      borderRadius: "16px",
    },
  }}
/>
    </AuthProvider>
  </React.StrictMode>,
)
