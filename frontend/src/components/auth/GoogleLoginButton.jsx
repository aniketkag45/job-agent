import { useEffect, useRef, useState, useContext } from "react"
import { useNavigate } from "react-router-dom"
import api from "../../api/axios"
import { AuthContext } from "../../context/authContext"

function GoogleLoginButton() {
  const navigate = useNavigate()
  const { login } = useContext(AuthContext)
  const googleBtnRef = useRef(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleGoogleResponse(response) {
    const id_token = response?.credential
    if (!id_token) {
      setError("Google login failed")
      return
    }
    setLoading(true)
    setError("")
    try {
      const res = await api.post("/auth/google", { id_token })
      login(res.data.access_token)
      navigate("/dashboard")
    } catch (err) {
      setError(err.response?.data?.detail || "Google login failed. Try again.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
    if (!clientId) {
      setError("Google Client ID not configured. Add VITE_GOOGLE_CLIENT_ID to frontend/.env")
      return
    }

    const initGoogle = () => {
      if (!window.google?.accounts?.id) return
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: handleGoogleResponse,
      })
      if (googleBtnRef.current) {
        // Clear previous button if any
        googleBtnRef.current.innerHTML = ""
        window.google.accounts.id.renderButton(googleBtnRef.current, {
          theme: "outline",
          size: "large",
          shape: "pill",
          width: 350,
          text: "continue_with",
          logo_alignment: "left",
        })
      }
    }

    // If already loaded
    if (window.google?.accounts?.id) {
      initGoogle()
      return
    }

    // Load script once
    if (document.getElementById("google-gsi-script")) {
      // Wait for it to load
      const interval = setInterval(() => {
        if (window.google?.accounts?.id) {
          initGoogle()
          clearInterval(interval)
        }
      }, 200)
      return () => clearInterval(interval)
    }

    const script = document.createElement("script")
    script.id = "google-gsi-script"
    script.src = "https://accounts.google.com/gsi/client"
    script.async = true
    script.defer = true
    script.onload = initGoogle
    script.onerror = () => setError("Failed to load Google sign-in. Check internet or disable ad blocker.")
    document.body.appendChild(script)
  }, [])

  return (
    <div className="w-full">
      {error && (
        <div className="mb-4 p-3 rounded-2xl bg-red-50 border border-red-100 text-red-600 text-sm">
          {error}
        </div>
      )}

      {/* ONLY ONE BUTTON - Official Google button */}
      <div ref={googleBtnRef} className="w-full flex justify-center min-h-[44px]" />

      {loading && (
        <p className="mt-3 text-center text-sm text-body">Signing you in...</p>
      )}

      <p className="mt-3 text-[11px] text-body/60 text-center">
        Secure OAuth via Google — we never see your password
      </p>
    </div>
  )
}

export default GoogleLoginButton