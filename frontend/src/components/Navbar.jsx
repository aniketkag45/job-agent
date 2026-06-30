import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { Menu, X, Sparkles } from "lucide-react"

function Navbar({ isAuthenticated, onLogout }) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const navigate = useNavigate()

  function handleLogout() {
    if (onLogout) onLogout()
    navigate("/login")
  }

  const linkClass = "text-sm font-medium text-body hover:text-navy transition-colors duration-200"

  return (
    <nav className="sticky top-0 z-50 bg-[#FAF8F6]/80 backdrop-blur-md border-b border-border">
      <div className="max-w-[1440px] mx-auto px-8 lg:px-16">
        <div className="flex items-center justify-between h-[72px]">
          
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-9 h-9 rounded-xl bg-navy flex items-center justify-center group-hover:bg-navy-light transition-colors">
              <Sparkles size={16} className="text-cream" />
            </div>
            <span className="text-lg font-semibold text-navy tracking-tight">JobAgent</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-10">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className={linkClass}>Dashboard</Link>
                <Link to="/jobs" className={linkClass}>Browse Jobs</Link>
                <Link to="/profile" className={linkClass}>Profile</Link>
                <button onClick={handleLogout} className="text-sm font-medium text-accent-orange hover:text-orange-600 transition-colors">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className={linkClass}>Sign In</Link>
                <Link to="/signup" className="inline-flex items-center px-7 py-3 bg-navy hover:bg-navy-light text-white text-sm font-medium rounded-full transition-all duration-200">
                  Get Started
                </Link>
              </>
            )}
          </div>

          {/* Mobile toggle */}
          <button className="md:hidden p-2 text-body" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden border-t border-border py-6 space-y-3 pb-6">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="block px-4 py-3 text-body hover:text-navy rounded-xl hover:bg-cream transition-colors">Dashboard</Link>
                <Link to="/jobs" className="block px-4 py-3 text-body hover:text-navy rounded-xl hover:bg-cream transition-colors">Browse Jobs</Link>
                <Link to="/profile" className="block px-4 py-3 text-body hover:text-navy rounded-xl hover:bg-cream transition-colors">Profile</Link>
                <button onClick={handleLogout} className="block w-full text-left px-4 py-3 text-accent-orange rounded-xl hover:bg-cream transition-colors">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="block px-4 py-3 text-body hover:text-navy rounded-xl hover:bg-cream transition-colors">Sign In</Link>
                <Link to="/signup" className="block px-4 py-3 bg-navy text-white rounded-full text-center">Get Started</Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar