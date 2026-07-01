import { useState, useRef } from "react"
import api from "../../api/axios"
import { Upload, CheckCircle, Loader2, X } from "lucide-react"

function ResumeUpload() {
  const [status, setStatus] = useState("idle")
  const [profile, setProfile] = useState(null)
  const [errorMsg, setErrorMsg] = useState("")
  const fileInputRef = useRef(null)

  async function handleFileSelect(e) {
    const file = e.target.files?.[0]
    if (!file) return
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setStatus("error")
      setErrorMsg("Only PDF files are accepted.")
      return
    }
    setStatus("uploading")
    setErrorMsg("")
    try {
      const formData = new FormData()
      formData.append("file", file)
      const response = await api.post("/resume/upload", formData, { headers: { "Content-Type": "multipart/form-data" } })
      if (response.data.success) {
        setProfile(response.data.data.profile)
        setStatus("success")
      } else {
        setStatus("error")
        setErrorMsg(response.data.message || "Upload failed.")
      }
    } catch (err) {
      setStatus("error")
      setErrorMsg(err.response?.data?.detail || "Upload failed. Try again.")
    }
  }

  if (status === "idle") {
    return (
      <div onClick={() => fileInputRef.current?.click()}
        className="bg-white rounded-2xl border-2 border-dashed border-border hover:border-accent-orange/40 p-10 text-center cursor-pointer transition-all">
        <input type="file" ref={fileInputRef} onChange={handleFileSelect} accept=".pdf" className="hidden" />
        <div className="w-14 h-14 rounded-2xl bg-card-peach flex items-center justify-center mx-auto mb-5">
          <Upload size={22} className="text-accent-orange" />
        </div>
        <h3 className="font-serif text-xl text-navy-light mb-2">Upload Your Resume</h3>
        <p className="text-body text-sm">Drop your PDF or click to browse. AI will analyze your skills.</p>
      </div>
    )
  }

  if (status === "uploading") {
    return (
      <div className="bg-white rounded-2xl border border-border p-10 text-center">
        <Loader2 className="animate-spin mx-auto text-accent-orange mb-5" size={28} />
        <h3 className="font-serif text-xl text-navy-light mb-2">Analyzing Resume...</h3>
        <p className="text-body text-sm">Extracting skills, domains, and experience level.</p>
      </div>
    )
  }

  if (status === "error") {
    return (
      <div className="bg-white rounded-2xl border border-red-200 p-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3"><X size={20} className="text-red-400" /><h3 className="font-semibold text-navy">Upload Failed</h3></div>
          <button onClick={() => setStatus("idle")} className="text-sm text-body hover:text-navy">Try Again</button>
        </div>
        <p className="text-red-500 text-sm">{errorMsg}</p>
      </div>
    )
  }

  if (status === "success" && profile) {
    return (
      <div className="bg-white rounded-2xl border border-emerald-200 p-8">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3"><CheckCircle size={20} className="text-emerald-500" /><h3 className="font-semibold text-navy">Resume Processed</h3></div>
          <button onClick={() => { setStatus("idle"); setProfile(null) }} className="text-sm text-body hover:text-navy">Replace</button>
        </div>
        <div className="flex flex-wrap gap-2">
          {(profile.skills || []).slice(0, 10).map((s, i) => (
            <span key={i} className="px-3 py-1.5 rounded-full bg-cream border border-border text-sm text-body">{s}</span>
          ))}
          {(profile.skills || []).length > 10 && <span className="px-3 py-1.5 text-sm text-body/50">+{profile.skills.length - 10} more</span>}
        </div>
      </div>
    )
  }

  return null
}

export default ResumeUpload