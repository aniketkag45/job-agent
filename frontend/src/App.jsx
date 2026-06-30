import { useContext } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import DashboardPage from "./pages/DashboardPage"
import SignupPage from "./pages/SignupPage"
import LoginPage from "./pages/LoginPage"
import ProtectedRoute from "./routes/ProtectedRoute"
import HomePage from "./pages/HomePage"
import JobsPage from "./pages/JobsPage"
import SavedJobsPage from "./pages/SavedJobsPage"
import VerifyEmailPage from "./pages/VerifyEmailPage"
import ProfilePage from "./pages/ProfilePage"
import Navbar from "./components/Navbar"
import { AuthContext } from "./context/authContext"

function App() {
  const { isAuthenticated, logout } = useContext(AuthContext)

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-surface-50">
        <Navbar isAuthenticated={isAuthenticated} onLogout={logout} />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/verify-email" element={<VerifyEmailPage />} />
          <Route path="/dashboard" element={
            <ProtectedRoute><DashboardPage /></ProtectedRoute>
          } />
          <Route path="/jobs" element={
            <ProtectedRoute><JobsPage /></ProtectedRoute>
          } />
          <Route path="/saved-jobs" element={
            <ProtectedRoute><SavedJobsPage /></ProtectedRoute>
          } />
          <Route path="/profile" element={
            <ProtectedRoute><ProfilePage /></ProtectedRoute>
          } />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App