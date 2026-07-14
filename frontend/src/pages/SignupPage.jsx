import { useState } from "react"
import { Link } from "react-router-dom"
import { ArrowRight, Loader2, Eye, EyeOff } from "lucide-react"
import api from "../api/axios"
import GoogleLoginButton from "../components/auth/GoogleLoginButton"

function SignupPage() {
  const [formData, setFormData] = useState({ username: "", email: "", password: "" })
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState(false)

  function handleChange(e) {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!formData.username.trim() || !formData.email.trim() || !formData.password.trim()) {
      setError("Please fill in all fields.")
      return
    }
    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters.")
      return
    }
    setLoading(true)
    setError("")
    try {
      const response = await api.post("/signup", formData)
      if (response.data && response.data.id) {
        setSuccess(true)
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="min-h-screen bg-cream flex items-center justify-center px-6 py-20">
      <div className="max-w-md w-full">
        <div className="text-center mb-12">
          <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-6">Get Started</p>
          <h1 className="font-serif text-4xl text-navy-light">Create your account</h1>
          <p className="mt-4 text-body leading-relaxed">Start your journey with AI-powered job matching.</p>
        </div>

        <div className="bg-white rounded-3xl border border-border p-8 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          {success ? (
            <div className="text-center py-8">
              <div className="w-16 h-16 rounded-full bg-emerald-50 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
              </div>
              <h3 className="text-xl font-semibold text-navy mb-2">Account created!</h3>
              <p className="text-body mb-6">Check your email for a verification link.</p>
              <Link to="/login" className="inline-flex items-center gap-2 px-6 py-3 bg-navy text-white rounded-full font-medium">
                Go to Login <ArrowRight size={16} />
              </Link>
            </div>
          ) : (
            <>
              {error && (
                <div className="mb-6 p-4 rounded-2xl bg-red-50 border border-red-100 text-red-600 text-sm">{error}</div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-navy mb-2">Username</label>
                  <input type="text" name="username" value={formData.username} onChange={handleChange}
                    placeholder="Your name"
                    className="w-full px-5 py-3.5 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-navy mb-2">Email</label>
                  <input type="email" name="email" value={formData.email} onChange={handleChange}
                    placeholder="you@example.com"
                    className="w-full px-5 py-3.5 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-navy mb-2">Password</label>
                  <div className="relative">
                    <input type={showPassword ? "text" : "password"} name="password" value={formData.password} onChange={handleChange}
                      placeholder="Min 6 characters"
                      className="w-full px-5 py-3.5 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all pr-12" />
                    <button type="button" onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-body/50 hover:text-body transition-colors">
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>
                <button type="submit" disabled={loading}
                  className="w-full inline-flex items-center justify-center gap-2 px-6 py-4 bg-navy hover:bg-navy-light text-white font-medium rounded-full transition-all shadow-[0_10px_30px_rgba(0,0,0,.08)] disabled:opacity-50">
                  {loading ? <Loader2 className="animate-spin" size={18} /> : null}
                  {loading ? "Creating..." : "Create Account"}
                  {!loading && <ArrowRight size={18} />}
                </button>
              </form>

              <div className="my-8 flex items-center gap-4">
                <div className="h-[1px] flex-1 bg-border"></div>
                <span className="text-xs tracking-widest uppercase text-body/50">or</span>
                <div className="h-[1px] flex-1 bg-border"></div>
              </div>

              <GoogleLoginButton />

              <p className="mt-8 text-center text-body text-sm">
                Already have an account?{" "}
                <Link to="/login" className="text-accent-orange hover:text-orange-600 font-medium transition-colors">Sign in</Link>
              </p>
            </>
          )}
        </div>
      </div>
    </section>
  )
}

export default SignupPage