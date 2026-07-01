import { useContext } from "react"
import { SavedJobsContext } from "../../context/savedjobscontext"
import { MapPin, Bookmark, BookmarkCheck, ArrowRight } from "lucide-react"

function JobCard({ company, role, source, location, match, skills = [], applyLink, score }) {
  const { savedJobs, toggleSaveJob } = useContext(SavedJobsContext)

  const isSaved = savedJobs.some(j => j.role === role && j.company === company)

  return (
    <div className="group bg-white rounded-2xl border border-border p-6 hover:border-accent-orange/30 hover:shadow-[0_10px_30px_rgba(0,0,0,.04)] transition-all duration-200">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-navy leading-snug">{role}</h3>
          <p className="text-sm text-body mt-1">{company}</p>
        </div>
        <div className={`shrink-0 px-3 py-1 rounded-full text-xs font-medium ${
          match >= 70 ? "bg-emerald-50 text-emerald-700" : match >= 40 ? "bg-amber-50 text-amber-700" : "bg-red-50 text-red-700"
        }`}>
          {match}% Match
        </div>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-body">
        <span className="flex items-center gap-1"><MapPin size={13} />{location}</span>
        <span className="px-2 py-0.5 rounded-full bg-cream border border-border text-body/70">{source}</span>
        {score != null && <span className="text-body/50">Score: {score}</span>}
      </div>

      {skills.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {skills.slice(0, 4).map((s, i) => (
            <span key={i} className="px-2.5 py-1 rounded-full bg-cream border border-border text-xs text-body">{s}</span>
          ))}
          {skills.length > 4 && <span className="px-2.5 py-1 text-xs text-body/50">+{skills.length - 4}</span>}
        </div>
      )}

      <div className="mt-5 flex items-center gap-3">
        <a href={applyLink} target="_blank" rel="noopener noreferrer"
          className="flex-1 inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-navy hover:bg-navy-light text-white text-sm font-medium rounded-full transition-colors">
          Apply Now <ArrowRight size={14} />
        </a>
        <button onClick={() => toggleSaveJob({ company, role, source, location, match, skills, applyLink, score })}
          className={`w-10 h-10 rounded-full border flex items-center justify-center transition-all ${
            isSaved ? "bg-accent-orange/10 border-accent-orange/30 text-accent-orange" : "border-border text-body/50 hover:text-accent-orange hover:border-accent-orange/30"
          }`}>
          {isSaved ? <BookmarkCheck size={16} /> : <Bookmark size={16} />}
        </button>
      </div>
    </div>
  )
}

export default JobCard