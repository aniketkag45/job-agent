import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import ProtectedRoute from './routes/ProtectedRoute';
import HomePage from './pages/HomePage';
import JobsPage from './pages/JobsPage';
import SavedJobsPage from './pages/SavedJobsPage';


function App() {

  return (

    <BrowserRouter>
    
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        } />
        <Route path="/jobs" element={
          <ProtectedRoute>
            <JobsPage />
          </ProtectedRoute>
        } />
        <Route path="/saved-jobs" element={
          <ProtectedRoute>
            <SavedJobsPage />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App