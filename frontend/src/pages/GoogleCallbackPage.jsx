import { useEffect, useContext } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import { AuthContext } from "../context/authContext"
import { Loader2 } from "lucide-react"

function GoogleCallbackPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { login } = useContext(AuthContext)

  useEffect(() => {
    const token = searchParams.get("token")
    const error = searchParams.get("error")

    if (error) {
      console.error("Google OAuth error:", error)
      navigate(`/login?error=${error}`, { replace: true })
      return
    }

    if (token) {
      login(token)
      navigate("/dashboard", { replace: true })
    } else {
      navigate("/login?error=google_no_token", { replace: true })
    }
  }, [searchParams, login, navigate])

  return (
    <section className="min-h-screen bg-cream flex items-center justify-center px-6">
      <div className="text-center bg-white rounded-3xl border border-border p-10 shadow-[0_10px_40px_rgba(0,0,0,.04)]">
        <Loader2 className="animate-spin mx-auto mb-4 text-navy" size={32} />
        <h2 className="font-serif text-xl text-navy-light">Completing Google sign-in</h2>
        <p className="mt-2 text-body text-sm">Please wait...</p>
      </div>
    </section>
  )
}

export default GoogleCallbackPage