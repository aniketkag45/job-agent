import { useState, useRef } from "react"
import api from "../../api/axios"
import { Upload, CheckCircle, Loader2, X } from "lucide-react"

function ResumeUpload() {
  // Track what state the upload is in
  const [status, setStatus] = useState("idle")  // idle | uploading | success | error
  const [profile, setProfile] = useState(null)   // The response from backend
  const [errorMsg, setErrorMsg] = useState("")
  const fileInputRef = useRef(null)

  const handleFileSelect = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate PDF
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setStatus("error")
      setErrorMsg("Only PDF files are accepted.")
      return
    }

    // Start upload
    setStatus("uploading")
    setErrorMsg("")

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await api.post("/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })

      if (response.data.success) {
        setProfile(response.data.data.profile)
        setStatus("success")
      } else {
        setStatus("error")
        setErrorMsg(response.data.message || "Upload failed.")
      }
    } catch (error) {
      setStatus("error")
      setErrorMsg(error.response?.data?.detail || "Network error. Try again.")
    }
  }

  // 👇 WHAT THE USER SEES

  // STATE 1: No resume yet — show upload area
  if (status === "idle") {
    return (
      <div
        onClick={() => fileInputRef.current?.click()}
        className="rounded-3xl border-2 border-dashed border-white/20 bg-white/5 p-8 text-center cursor-pointer hover:border-cyan-400/50 hover:bg-white/[0.07] transition"
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".pdf"
          className="hidden"
        />

        <div className="w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500/20 to-cyan-400/20 flex items-center justify-center mx-auto mb-4">
          <Upload className="text-cyan-300" size={28} />
        </div>

        <h3 className="text-xl font-black text-white mb-2">
          Upload Your Resume
        </h3>
        <p className="text-gray-400 text-sm">
          Drop your PDF resume here or click to browse.
          <br />
          The AI will analyze your skills for personalized job matching.
        </p>
      </div>
    )
  }

  // STATE 2: Uploading — show spinner
  if (status === "uploading") {
    return (
      <div className="rounded-3xl border border-white/10 bg-white/5 p-8 text-center">
        <Loader2 className="animate-spin mx-auto text-cyan-300 mb-4" size={32} />
        <h3 className="text-xl font-black text-white mb-2">Analyzing Resume...</h3>
        <p className="text-gray-400 text-sm">Extracting skills, domains, and experience level.</p>
      </div>
    )
  }

  // STATE 3: Error — show error with retry
  if (status === "error") {
    return (
      <div className="rounded-3xl border border-red-500/30 bg-red-500/5 p-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <X className="text-red-400" size={24} />
            <h3 className="text-xl font-black text-white">Upload Failed</h3>
          </div>
          <button
            onClick={() => setStatus("idle")}
            className="px-4 py-2 rounded-xl bg-white/10 text-white text-sm hover:bg-white/20 transition"
          >
            Try Again
          </button>
        </div>
        <p className="text-red-300 text-sm">{errorMsg}</p>
      </div>
    )
  }

  // STATE 4: Success — show detected skills
  if (status === "success" && profile) {
    return (
      <div className="rounded-3xl border border-green-500/30 bg-green-500/5 p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <CheckCircle className="text-green-400" size={24} />
            <h3 className="text-xl font-black text-white">Resume Processed</h3>
          </div>
          <button
            onClick={() => {
              setStatus("idle")
              setProfile(null)
            }}
            className="px-4 py-2 rounded-xl bg-white/10 text-white text-sm hover:bg-white/20 transition"
          >
            Replace
          </button>
        </div>

        {/* Skills */}
        <div className="mb-4">
          <p className="text-gray-400 text-sm mb-2">
            Skills ({profile.skills.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {profile.skills.map((skill, i) => (
              <span
                key={i}
                className="px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/20 text-cyan-300 text-xs"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        {/* Domains */}
        <div className="mb-4">
          <p className="text-gray-400 text-sm mb-2">Domains</p>
          <div className="flex flex-wrap gap-2">
            {profile.domains.map((d, i) => (
              <span
                key={i}
                className="px-3 py-1 rounded-full bg-purple-400/10 border border-purple-400/20 text-purple-300 text-xs"
              >
                {d}
              </span>
            ))}
          </div>
        </div>

        {/* Experience */}
        <div>
          <p className="text-gray-400 text-sm mb-2">Experience Level</p>
          <span className="px-3 py-1 rounded-full bg-green-400/10 border border-green-400/20 text-green-300 text-xs capitalize">
            {profile.experience_level}
          </span>
        </div>
      </div>
    )
  }

  return null
}

export default ResumeUpload