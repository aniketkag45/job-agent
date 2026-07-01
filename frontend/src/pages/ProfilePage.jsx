import { useState, useEffect, useRef } from "react"
import api from "../api/axios"
import {
  User, Phone, MapPin, Link2, BookOpen, Settings,
  Plus, Trash2, Save, Loader2, FileText, Upload
} from "lucide-react"

function ProfilePage() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState("")
  const [resumes, setResumes] = useState([])
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  useEffect(() => { fetchProfile(); fetchResumes() }, [])

  function fetchProfile() {
    api.get("/profile").then(r => { if (r.data.success) setProfile(r.data.data) }).finally(() => setLoading(false))
  }
  function fetchResumes() {
    api.get("/resumes").then(r => { if (r.data.success) setResumes(r.data.data) })
  }

  function handleResumeUpload(e) {
    var file = e.target.files && e.target.files[0]
    if (!file) return
    setUploading(true)
    var fd = new FormData()
    fd.append("file", file)
    api.post("/resume/upload", fd, { headers: { "Content-Type": "multipart/form-data" } })
      .then(r => { if (r.data.success) fetchResumes() })
      .finally(() => setUploading(false))
  }

  function handleAutoFill(resume) {
    var skills = []
    try { skills = typeof resume.skills === "string" ? JSON.parse(resume.skills) : (resume.skills || []) } catch (e) {}
    var domains = []
    try { domains = typeof resume.domains === "string" ? JSON.parse(resume.domains) : (resume.domains || []) } catch (e) {}
    var level = resume.experience_level || ""
    var role = "Developer"
    if (skills.indexOf("react") !== -1 || skills.indexOf("javascript") !== -1) role = "Full Stack Developer"
    if (skills.indexOf("fastapi") !== -1 || skills.indexOf("django") !== -1) role = "Backend Developer"
    if (skills.indexOf("tensorflow") !== -1 || skills.indexOf("pytorch") !== -1) role = "ML Engineer"
    var headline = (level ? (level.charAt(0).toUpperCase() + level.slice(1)) : "") + " " + role + " | " + (domains.length > 0 ? domains.map(d => d.charAt(0).toUpperCase() + d.slice(1)).join(" & ") : "Technology")
    var bio = "Experienced in " + skills.slice(0, 5).join(", ") + ". Looking for opportunities to apply my skills and grow professionally."
    setProfile(prev => ({ ...prev, headline, bio, preferred_keywords: skills, preferred_locations: ["India", "Remote"] }))
  }

  function handleChange(field, value) {
    setProfile(prev => ({ ...prev, [field]: value }))
  }

  function handleSave() {
    setSaving(true)
    setMessage("")
    function clean(val) {
      if (val === "" || val === undefined || val === null) return null
      if (typeof val === "string" && (val.startsWith("[") || val.startsWith("{"))) { try { val = JSON.parse(val) } catch (e) {} }
      if (Array.isArray(val) && val.length === 0) return null
      return val
    }
    var fields = {
      full_name: clean(profile.full_name), headline: clean(profile.headline), bio: clean(profile.bio),
      mobile: clean(profile.mobile), location: clean(profile.location),
      linkedin_url: clean(profile.linkedin_url), github_url: clean(profile.github_url), portfolio_url: clean(profile.portfolio_url),
      preferred_keywords: clean(profile.preferred_keywords), excluded_keywords: clean(profile.excluded_keywords),
      preferred_locations: clean(profile.preferred_locations), remote_only: profile.remote_only || false,
      education_degree: clean(profile.education_degree), education_field: clean(profile.education_field),
      education_school: clean(profile.education_school), education_year: clean(profile.education_year)
    }
    var payload = {}
    Object.keys(fields).forEach(k => { if (fields[k] !== null && fields[k] !== undefined) payload[k] = fields[k] })
    if (Object.keys(payload).length === 0) { setMessage("Nothing to save."); setSaving(false); return }
    api.put("/profile", payload)
      .then(() => { setMessage("Profile saved successfully!"); setSaving(false); setTimeout(() => setMessage(""), 3000) })
      .catch(err => { setMessage("Failed to save."); setSaving(false) })
  }

  if (loading) return (
    <div className="min-h-screen bg-cream flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-navy border-t-transparent rounded-full animate-spin"></div>
    </div>
  )
  if (!profile) return null

  return (
    <div className="bg-cream min-h-screen">
      <div className="max-w-[960px] mx-auto px-8 lg:px-16 py-12">
        
        {/* Page Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-4">Profile</p>
            <h1 className="font-serif text-4xl lg:text-5xl text-navy-light">Your Profile</h1>
            <p className="mt-2 text-body">Manage your personal and professional information.</p>
          </div>
          <button onClick={handleSave} disabled={saving}
            className="inline-flex items-center gap-2 px-6 py-3 bg-navy hover:bg-navy-light text-white font-medium rounded-full transition-all disabled:opacity-50">
            {saving ? <Loader2 className="animate-spin" size={16} /> : <Save size={16} />}
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>

        {message && (
          <div className={`mb-8 p-4 rounded-2xl text-sm font-medium ${message.indexOf("success") !== -1 ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>
            {message}
          </div>
        )}

        {/* Personal Information */}
        <section className="bg-white rounded-3xl border border-border p-8 mb-6 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <h2 className="font-serif text-xl text-navy-light mb-6 flex items-center gap-2">
            <User size={18} className="text-accent-orange" /> Personal Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <Field label="Full Name" value={profile.full_name} onChange={v => handleChange("full_name", v)} />
            <Field label="Headline" value={profile.headline} onChange={v => handleChange("headline", v)} placeholder="Python Backend Developer | AI Enthusiast" />
            <Field label="Mobile" value={profile.mobile} onChange={v => handleChange("mobile", v)} icon={<Phone size={15} />} />
            <Field label="Location" value={profile.location} onChange={v => handleChange("location", v)} icon={<MapPin size={15} />} />
          </div>
        </section>

        {/* Resumes */}
        <section className="bg-white rounded-3xl border border-border p-8 mb-6 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-serif text-xl text-navy-light flex items-center gap-2">
              <FileText size={18} className="text-accent-orange" /> Resumes
            </h2>
            <div>
              <input type="file" ref={fileInputRef} onChange={handleResumeUpload} accept=".pdf" className="hidden" />
              <button onClick={() => fileInputRef.current && fileInputRef.current.click()} disabled={uploading}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-navy hover:bg-navy-light text-white text-sm font-medium rounded-full transition-all disabled:opacity-50">
                {uploading ? <Loader2 className="animate-spin" size={14} /> : <Upload size={14} />}
                {uploading ? "Uploading..." : "Upload Resume"}
              </button>
            </div>
          </div>
          {resumes.length === 0 ? (
            <p className="text-body text-sm py-8 text-center border-2 border-dashed border-border rounded-2xl">
              No resumes uploaded yet. Upload your first resume to enable AI-powered job matching.
            </p>
          ) : (
            <div className="space-y-3">
              {resumes.map(resume => {
                var skills = []
                try { skills = typeof resume.skills === "string" ? JSON.parse(resume.skills) : (resume.skills || []) } catch (e) {}
                return (
                  <div key={resume.id} className={`flex items-center justify-between p-4 rounded-2xl border ${resume.is_active ? "border-accent-orange/30 bg-card-peach" : "border-border"}`}>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <FileText size={14} className="text-body/50" />
                        <span className="font-medium text-navy truncate">{resume.filename}</span>
                        {resume.is_active && <span className="px-2 py-0.5 bg-accent-orange/10 text-accent-orange rounded-full text-xs font-medium">Active</span>}
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-body">{skills.length} skills</span>
                        <span className="text-xs text-body/30">·</span>
                        <span className="text-xs text-body">{resume.experience_level || "unknown"}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      <button onClick={() => handleAutoFill(resume)} className="px-3 py-1.5 text-xs font-medium text-accent-orange hover:bg-accent-orange/10 rounded-lg transition-colors">Auto-fill</button>
                      <button onClick={() => { api.put("/resume/" + resume.id + "/activate").then(() => fetchResumes()) }} className="px-3 py-1.5 text-xs font-medium text-body hover:text-navy rounded-lg transition-colors">Set Active</button>
                      <button onClick={() => { if (confirm("Delete?")) { api.delete("/resume/" + resume.id).then(() => fetchResumes()) } }} className="p-1.5 text-body/40 hover:text-red-500 rounded-lg transition-colors"><Trash2 size={12} /></button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </section>

        {/* Professional Links */}
        <section className="bg-white rounded-3xl border border-border p-8 mb-6 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <h2 className="font-serif text-xl text-navy-light mb-6 flex items-center gap-2">
            <Link2 size={18} className="text-accent-orange" /> Professional Links
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <Field label="LinkedIn URL" value={profile.linkedin_url} onChange={v => handleChange("linkedin_url", v)} />
            <Field label="GitHub URL" value={profile.github_url} onChange={v => handleChange("github_url", v)} />
            <Field label="Portfolio URL" value={profile.portfolio_url} onChange={v => handleChange("portfolio_url", v)} />
          </div>
        </section>

        {/* Bio */}
        <section className="bg-white rounded-3xl border border-border p-8 mb-6 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <h2 className="font-serif text-xl text-navy-light mb-6 flex items-center gap-2">
            <BookOpen size={18} className="text-accent-orange" /> Professional Bio
          </h2>
          <textarea value={profile.bio || ""} onChange={e => handleChange("bio", e.target.value)}
            placeholder="Write a short professional summary. This will be used in cover letters." rows={4}
            className="w-full px-4 py-3 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all resize-none text-sm" />
        </section>

        {/* Education */}
        <section className="bg-white rounded-3xl border border-border p-8 mb-6 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <h2 className="font-serif text-xl text-navy-light mb-6 flex items-center gap-2">
            <BookOpen size={18} className="text-accent-orange" /> Education
          </h2>
          <p className="text-sm text-body mb-4">Add your educational qualifications.</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label className="block text-sm font-medium text-navy mb-2">Degree</label>
              <input type="text" value={profile.education_degree || ""} onChange={e => handleChange("education_degree", e.target.value)}
                placeholder="Bachelor of Technology"
                className="w-full px-4 py-3 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-navy mb-2">Field of Study</label>
              <input type="text" value={profile.education_field || ""} onChange={e => handleChange("education_field", e.target.value)}
                placeholder="Computer Science"
                className="w-full px-4 py-3 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-navy mb-2">School / University</label>
              <input type="text" value={profile.education_school || ""} onChange={e => handleChange("education_school", e.target.value)}
                placeholder="University of Mumbai"
                className="w-full px-4 py-3 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-navy mb-2">Graduation Year</label>
              <input type="text" value={profile.education_year || ""} onChange={e => handleChange("education_year", e.target.value)}
                placeholder="2026"
                className="w-full px-4 py-3 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all text-sm" />
            </div>
          </div>
        </section>

        {/* Job Preferences */}
        <section className="bg-white rounded-3xl border border-border p-8 mb-6 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <h2 className="font-serif text-xl text-navy-light mb-6 flex items-center gap-2">
            <Settings size={18} className="text-accent-orange" /> Job Preferences
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <TagField label="Preferred Keywords" tags={profile.preferred_keywords || []} onChange={v => handleChange("preferred_keywords", v)} placeholder="python, backend, intern" />
            <TagField label="Excluded Keywords" tags={profile.excluded_keywords || []} onChange={v => handleChange("excluded_keywords", v)} placeholder="senior, manager" />
            <TagField label="Preferred Locations" tags={profile.preferred_locations || []} onChange={v => handleChange("preferred_locations", v)} placeholder="India, Remote" />
            <div className="flex items-center gap-3 pt-6">
              <input type="checkbox" checked={profile.remote_only || false}
                onChange={e => handleChange("remote_only", e.target.checked)}
                className="w-4 h-4 rounded border-border text-accent-orange focus:ring-accent-orange/20" />
              <label className="text-sm font-medium text-navy">Remote Only</label>
            </div>
          </div>
        </section>

      </div>
    </div>
  )
}

// ── Reusable Input Field ──────────────────────────────────
function Field({ label, value, onChange, placeholder, icon }) {
  return (
    <div>
      <label className="block text-sm font-medium text-navy mb-2">{label}</label>
      <div className="relative">
        {icon && <div className="absolute left-4 top-1/2 -translate-y-1/2 text-body/50">{icon}</div>}
        <input type="text" value={value || ""} onChange={e => onChange(e.target.value)}
          placeholder={placeholder}
          className={`w-full px-4 py-3 rounded-2xl border border-border text-navy placeholder:text-body/50 focus:outline-none focus:border-accent-orange focus:ring-2 focus:ring-accent-orange/10 transition-all text-sm ${icon ? "pl-10" : ""}`} />
      </div>
    </div>
  )
}

// ── Tag Input Field ───────────────────────────────────────
function TagField({ label, tags, onChange, placeholder }) {
  var [input, setInput] = useState("")
  var safeTags = typeof tags === "string" ? (() => { try { return JSON.parse(tags) } catch (e) { return [] } })() : (Array.isArray(tags) ? tags : [])
  function addTag() {
    var trimmed = input.trim().toLowerCase()
    if (trimmed && safeTags.indexOf(trimmed) === -1) { onChange(safeTags.concat([trimmed])) }
    setInput("")
  }
  function removeTag(index) { onChange(safeTags.filter((_, i) => i !== index)) }
  function handleKeyDown(e) { if (e.key === "Enter" || e.key === ",") { e.preventDefault(); addTag() } }
  return (
    <div>
      <label className="block text-sm font-medium text-navy mb-2">{label}</label>
      <div className="flex flex-wrap gap-2 mb-2">
        {safeTags.map((tag, i) => (
          <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-cream border border-border rounded-full text-sm text-navy">
            {tag}
            <button onClick={() => removeTag(i)} className="hover:text-accent-orange transition-colors"><Trash2 size={11} /></button>
          </span>
        ))}
      </div>
      <div className="flex gap-2">
        <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="flex-1 px-4 py-2.5 rounded-2xl border border-border text-navy text-sm placeholder:text-body/50 focus:outline-none focus:border-accent-orange transition-all" />
        <button onClick={addTag}
          className="px-3 py-2.5 rounded-2xl border border-border text-body hover:text-navy hover:border-accent-orange/30 transition-all"><Plus size={15} /></button>
      </div>
    </div>
  )
}

export default ProfilePage