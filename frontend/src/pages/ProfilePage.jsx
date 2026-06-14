import { useState, useEffect, useRef } from "react"
import DashboardLayout from "../components/dashboard/DashboardLayout"
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

  useEffect(function () {
    fetchProfile()
    fetchResumes()
  }, [])

  function fetchProfile() {
    api.get("/profile")
      .then(function (res) {
        if (res.data.success) setProfile(res.data.data)
      })
      .catch(function (err) {
        console.error("Failed to load profile:", err)
      })
      .finally(function () {
        setLoading(false)
      })
  }

  function fetchResumes() {
    api.get("/resumes")
      .then(function (res) {
        if (res.data.success) setResumes(res.data.data)
      })
      .catch(function (err) {
        console.error("Failed to load resumes:", err)
      })
  }

  function handleResumeUpload(e) {
    var file = e.target.files && e.target.files[0]
    if (!file) return
    setUploading(true)
    var fd = new FormData()
    fd.append("file", file)
    api.post("/resume/upload", fd, {
      headers: { "Content-Type": "multipart/form-data" }
    })
      .then(function (res) {
        if (res.data.success) fetchResumes()
      })
      .catch(function (err) {
        console.error("Upload failed:", err)
      })
      .finally(function () {
        setUploading(false)
      })
  }

  function handleAutoFill(resume) {
    var skills = []
    try {
      skills = typeof resume.skills === "string"
        ? JSON.parse(resume.skills)
        : (resume.skills || [])
    } catch (e) { skills = [] }

    var domains = []
    try {
      domains = typeof resume.domains === "string"
        ? JSON.parse(resume.domains)
        : (resume.domains || [])
    } catch (e) { domains = [] }

    var level = resume.experience_level || ""

    var role = "Developer"
    if (skills.indexOf("react") !== -1 || skills.indexOf("javascript") !== -1) role = "Full Stack Developer"
    if (skills.indexOf("fastapi") !== -1 || skills.indexOf("django") !== -1) role = "Backend Developer"
    if (skills.indexOf("tensorflow") !== -1 || skills.indexOf("pytorch") !== -1) role = "Machine Learning Engineer"

    var headline = (level ? (level.charAt(0).toUpperCase() + level.slice(1)) : "") + " " + role + " | " + (domains.length > 0 ? domains.map(function (d) { return d.charAt(0).toUpperCase() + d.slice(1) }).join(" & ") : "Technology")
    var bio = "Experienced in " + skills.slice(0, 5).join(", ") + ". Looking for opportunities to apply my skills and grow professionally."

    setProfile(function (prev) {
      return Object.assign({}, prev, {
        headline: headline,
        bio: bio,
        preferred_keywords: skills,
        preferred_locations: ["India", "Remote"]
      })
    })
  }

  function handleChange(field, value) {
    setProfile(function (prev) {
      var updated = Object.assign({}, prev)
      updated[field] = value
      return updated
    })
  }

  function handleSave() {
    setSaving(true)
    setMessage("")

    function clean(val) {
      if (val === "" || val === undefined || val === null) return null
      if (Array.isArray(val) && val.length === 0) return null
      return val
    }

    var payload = {
      full_name: clean(profile.full_name),
      headline: clean(profile.headline),
      bio: clean(profile.bio),
      mobile: clean(profile.mobile),
      location: clean(profile.location),
      linkedin_url: clean(profile.linkedin_url),
      github_url: clean(profile.github_url),
      portfolio_url: clean(profile.portfolio_url),
      preferred_keywords: clean(profile.preferred_keywords),
      excluded_keywords: clean(profile.excluded_keywords),
      preferred_locations: clean(profile.preferred_locations),
      remote_only: profile.remote_only || false,
      education_degree: clean(profile.education_degree),
      education_field: clean(profile.education_field),
      education_school: clean(profile.education_school),
      education_year: clean(profile.education_year)
    }

    api.put("/profile", payload)
      .then(function () {
        setMessage("Profile saved successfully!")
        setSaving(false)
        setTimeout(function () { setMessage("") }, 3000)
      })
      .catch(function (err) {
        console.error("Save failed:", err)
        setMessage("Failed to save. " + (err.response && err.response.data && err.response.data.detail ? err.response.data.detail : "Try again."))
        setSaving(false)
      })
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <Loader2 className="animate-spin text-blue-500" size={32} />
        </div>
      </DashboardLayout>
    )
  }

  if (!profile) return null

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="flex items-center justify-between mb-10">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
            <p className="text-gray-500 mt-1">Manage your personal and professional information.</p>
          </div>
          <button onClick={handleSave} disabled={saving}
            className="flex items-center gap-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition disabled:opacity-50">
            {saving ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>

        {message && (
          <div className={"mb-6 p-4 rounded-xl text-sm font-medium " + (message.indexOf("success") !== -1 ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700")}>
            {message}
          </div>
        )}

        {/* Personal Information */}
        <section className="bg-white rounded-2xl border border-gray-200 p-8 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
            <User size={20} className="text-blue-500" />
            Personal Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Field label="Full Name" value={profile.full_name} onChange={function (v) { handleChange("full_name", v) }} />
            <Field label="Headline" value={profile.headline} onChange={function (v) { handleChange("headline", v) }} placeholder="Python Backend Developer | AI Enthusiast" />
            <Field label="Mobile" value={profile.mobile} onChange={function (v) { handleChange("mobile", v) }} icon={<Phone size={16} />} />
            <Field label="Location" value={profile.location} onChange={function (v) { handleChange("location", v) }} icon={<MapPin size={16} />} />
          </div>
        </section>

        {/* Resumes */}
        <section className="bg-white rounded-2xl border border-gray-200 p-8 mb-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <FileText size={20} className="text-blue-500" />
              Resumes
            </h2>
            <div>
              <input type="file" ref={fileInputRef} onChange={handleResumeUpload} accept=".pdf" className="hidden" />
              <button onClick={function () { fileInputRef.current && fileInputRef.current.click() }} disabled={uploading}
                className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl text-sm font-medium transition disabled:opacity-50">
                {uploading ? <Loader2 className="animate-spin" size={16} /> : <Upload size={16} />}
                {uploading ? "Uploading..." : "Upload Resume"}
              </button>
            </div>
          </div>

          {resumes.length === 0 ? (
            <p className="text-gray-400 text-sm py-8 text-center border-2 border-dashed border-gray-200 rounded-xl">
              No resumes uploaded yet. Upload your first resume to enable AI-powered job matching.
            </p>
          ) : (
            <div className="space-y-3">
              {resumes.map(function (resume) {
                var skills = []
                try {
                  skills = typeof resume.skills === "string" ? JSON.parse(resume.skills) : (resume.skills || [])
                } catch (e) { }

                return (
                  <div key={resume.id} className={"flex items-center justify-between p-4 rounded-xl border " + (resume.is_active ? "border-blue-200 bg-blue-50" : "border-gray-200")}>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <FileText size={16} className="text-gray-400" />
                        <span className="font-medium text-gray-900 truncate">{resume.filename}</span>
                        {resume.is_active && (
                          <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">Active</span>
                        )}
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-gray-500">{skills.length} skills</span>
                        <span className="text-xs text-gray-300">•</span>
                        <span className="text-xs text-gray-500">{resume.experience_level || "unknown"}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      <button onClick={function () { handleAutoFill(resume) }}
                        className="px-3 py-1.5 text-xs font-medium text-blue-600 hover:bg-blue-100 rounded-lg transition">
                        Auto-fill Profile
                      </button>
                      <button onClick={function () {
                        api.put("/resume/" + resume.id + "/activate").then(function () { fetchResumes() }).catch(function () { })
                      }}
                        className="px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-100 rounded-lg transition">
                        Set Active
                      </button>
                      <button onClick={function () {
                        if (confirm("Delete this resume?")) {
                          api.delete("/resume/" + resume.id).then(function () { fetchResumes() }).catch(function () { })
                        }
                      }}
                        className="p-1.5 text-gray-400 hover:text-red-500 rounded-lg transition">
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </section>

        {/* Professional Links */}
        <section className="bg-white rounded-2xl border border-gray-200 p-8 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
            <Link2 size={20} className="text-blue-500" />
            Professional Links
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Field label="LinkedIn URL" value={profile.linkedin_url} onChange={function (v) { handleChange("linkedin_url", v) }} />
            <Field label="GitHub URL" value={profile.github_url} onChange={function (v) { handleChange("github_url", v) }} />
            <Field label="Portfolio URL" value={profile.portfolio_url} onChange={function (v) { handleChange("portfolio_url", v) }} />
          </div>
        </section>

        {/* Bio */}
        <section className="bg-white rounded-2xl border border-gray-200 p-8 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
            <BookOpen size={20} className="text-blue-500" />
            Professional Bio
          </h2>
          <textarea value={profile.bio || ""} onChange={function (e) { handleChange("bio", e.target.value) }}
            placeholder="Write a short professional summary. This will be used in cover letters." rows={4}
            className="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none" />
        </section>

        {/* Education */}
        <section className="bg-white rounded-2xl border border-gray-200 p-8 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
            <BookOpen size={20} className="text-blue-500" />
            Education
          </h2>
          <p className="text-sm text-gray-500 mb-4">Add your educational qualifications.</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Degree</label>
              <input type="text" value={profile.education_degree || ""} onChange={function (e) { handleChange("education_degree", e.target.value) }}
                placeholder="Bachelor of Technology"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Field of Study</label>
              <input type="text" value={profile.education_field || ""} onChange={function (e) { handleChange("education_field", e.target.value) }}
                placeholder="Computer Science"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">School / University</label>
              <input type="text" value={profile.education_school || ""} onChange={function (e) { handleChange("education_school", e.target.value) }}
                placeholder="University of Mumbai"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Graduation Year</label>
              <input type="text" value={profile.education_year || ""} onChange={function (e) { handleChange("education_year", e.target.value) }}
                placeholder="2026"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" />
            </div>
          </div>
        </section>

        {/* Job Preferences */}
        <section className="bg-white rounded-2xl border border-gray-200 p-8 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
            <Settings size={20} className="text-blue-500" />
            Job Preferences
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <TagField label="Preferred Keywords" tags={profile.preferred_keywords || []} onChange={function (v) { handleChange("preferred_keywords", v) }} placeholder="python, backend, intern" />
            <TagField label="Excluded Keywords" tags={profile.excluded_keywords || []} onChange={function (v) { handleChange("excluded_keywords", v) }} placeholder="senior, manager" />
            <TagField label="Preferred Locations" tags={profile.preferred_locations || []} onChange={function (v) { handleChange("preferred_locations", v) }} placeholder="India, Remote" />
            <div className="flex items-center gap-3 pt-6">
              <input type="checkbox" checked={profile.remote_only || false}
                onChange={function (e) { handleChange("remote_only", e.target.checked) }}
                className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500" />
              <label className="text-sm font-medium text-gray-700">Remote Only</label>
            </div>
          </div>
        </section>

      </div>
    </DashboardLayout>
  )
}

// ── Reusable Input Field ──────────────────────────────────
function Field(props) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1.5">{props.label}</label>
      <div className="relative">
        {props.icon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">{props.icon}</div>
        )}
        <input type="text" value={props.value || ""} onChange={function (e) { props.onChange(e.target.value) }}
          placeholder={props.placeholder}
          className={"w-full px-4 py-2.5 border border-gray-200 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 " + (props.icon ? "pl-10" : "")} />
      </div>
    </div>
  )
}

// ── Tag Input Field ───────────────────────────────────────
function TagField(props) {
  var tags = props.tags
  var onChange = props.onChange
  var placeholder = props.placeholder

  var _inputState = useState("")
  var input = _inputState[0]
  var setInput = _inputState[1]

  var safeTags = typeof tags === "string"
    ? (function () { try { return JSON.parse(tags) } catch (e) { return [] } })()
    : (Array.isArray(tags) ? tags : [])

  function addTag() {
    var trimmed = input.trim().toLowerCase()
    if (trimmed && safeTags.indexOf(trimmed) === -1) {
      onChange(safeTags.concat([trimmed]))
    }
    setInput("")
  }

  function removeTag(index) {
    onChange(safeTags.filter(function (_, i) { return i !== index }))
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault()
      addTag()
    }
  }

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1.5">{props.label}</label>
      <div className="flex flex-wrap gap-2 mb-2">
        {safeTags.map(function (tag, i) {
          return (
            <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
              {tag}
              <button onClick={function () { removeTag(i) }} className="hover:text-blue-900">
                <Trash2 size={12} />
              </button>
            </span>
          )
        })}
      </div>
      <div className="flex gap-2">
        <input type="text" value={input} onChange={function (e) { setInput(e.target.value) }}
          onKeyDown={handleKeyDown} placeholder={placeholder}
          className="flex-1 px-4 py-2 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none focus:border-blue-500" />
        <button onClick={addTag} className="px-3 py-2 border border-gray-200 rounded-xl hover:bg-gray-50 text-gray-500">
          <Plus size={16} />
        </button>
      </div>
    </div>
  )
}

export default ProfilePage