import { useState, useContext } from "react"
import { Link, useNavigate } from "react-router-dom"
import { ArrowRight, Loader2, Eye, EyeOff } from "lucide-react"
import api from "../api/axios"
import { AuthContext } from "../context/authContext"

function LoginPage() {
  const navigate = useNavigate()
  const { login } = useContext(AuthContext)

  const [formData, setFormData] = useState({ username: "", password: "" })
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")

  function handleChange(e) {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Please fill in all fields.")
      return
    }
    setLoading(true)
    setError("")
    try {
      const response = await api.post("/login",
        new URLSearchParams({ grant_type: "password", username: formData.username, password: formData.password })
      )
      login(response.data.access_token)
      navigate("/dashboard")
    } catch (err) {
      setError("Invalid credentials. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="min-h-screen bg-cream flex items-center justify-center px-6 py-20">
      <div className="max-w-md w-full">
        
        {/* Heading */}
        <div className="text-center mb-12">
          <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-6">Welcome Back</p>
          <h1 className="font-serif text-4xl text-navy-light">Sign in to your account</h1>
          <p className="mt-4 text-body leading-relaxed">
            Continue your journey with AI-powered job matching.
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-3xl border border-border p-8 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          
          {error && (
            <div className="mb-6 p-4 rounded-2xl bg-red-50 border border-red-100 text-red-600 text-sm">{error}</div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-navy mb-2">Email</label>
              <input type="text" name="username" value={formData.username} onChange={handleChange}
                placeholder="you@example.com"
                className="w-full px-5 py-3.5 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all" />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-navy mb-2">Password</label>
              <div className="relative">
                <input type={showPassword ? "text" : "password"} name="password" value={formData.password} onChange={handleChange}
                  placeholder="Enter your password"
                  className="w-full px-5 py-3.5 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all pr-12" />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-body/50 hover:text-body transition-colors">
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* Submit */}
            <button type="submit" disabled={loading}
              className="w-full inline-flex items-center justify-center gap-2 px-6 py-4 bg-navy hover:bg-navy-light text-white font-medium rounded-full transition-all shadow-[0_10px_30px_rgba(0,0,0,.08)] disabled:opacity-50">
              {loading ? <Loader2 className="animate-spin" size={18} /> : null}
              {loading ? "Signing in..." : "Sign In"}
              {!loading && <ArrowRight size={18} />}
            </button>
          </form>

          <p className="mt-8 text-center text-body text-sm">
            Don't have an account?{" "}
            <Link to="/signup" className="text-accent-orange hover:text-orange-600 font-medium transition-colors">
              Create one
            </Link>
          </p>
        </div>
      </div>
    </section>
  )
}

export default LoginPage