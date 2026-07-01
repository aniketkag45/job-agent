import { useState, useEffect } from "react"
import { Search, Sparkles } from "lucide-react"
import api from "../api/axios"
import JobCard from "../components/jobs/JobCard"

function extractTechPills(text) {
  if (!text) return []
  const TECH_KEYWORDS = ["python", "java", "javascript", "typescript", "react", "node", "fastapi", "flask", "django", "docker", "kubernetes", "aws", "postgresql", "mysql", "mongodb", "redis", "graphql", "rest", "golang", "rust", "kotlin", "swift", "tensorflow", "pytorch", "machine learning", "ai", "llm", "rag", "linux", "terraform"]
  const textLower = text.toLowerCase()
  const found = TECH_KEYWORDS.filter(kw => textLower.includes(kw))
  return [...new Set(found)].slice(0, 5)
}

function JobsPage() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedLocation] = useState("All")
  const [currentPage, setCurrentPage] = useState(1)
  const [useSemantic, setUseSemantic] = useState(false)

  useEffect(() => {
    async function fetchJobs() {
      setLoading(true)
      try {
        let response
        if (useSemantic && searchTerm.trim()) {
          const semParams = new URLSearchParams()
          semParams.append("query", searchTerm)
          semParams.append("top_k", "10")
          if (selectedLocation !== "All") semParams.append("source", selectedLocation)
          response = await api.get(`/jobs/semantic-search?${semParams.toString()}`)
        } else if (searchTerm.trim() || selectedLocation !== "All") {
          const params = new URLSearchParams()
          params.append("page", currentPage)
          params.append("page_size", "10")
          if (searchTerm.trim()) params.append("keyword", searchTerm)
          if (selectedLocation !== "All") params.append("location", selectedLocation)
          response = await api.get(`/jobs/query?${params.toString()}`)
        } else {
          response = await api.get(`/jobs?page=${currentPage}&page_size=10`)
        }
        setJobs(response.data.data)
        setError("")
      } catch (err) {
        setError("Failed to load jobs")
      } finally {
        setLoading(false)
      }
    }

    const timer = setTimeout(fetchJobs, 500)
    return () => clearTimeout(timer)
  }, [searchTerm, selectedLocation, currentPage, useSemantic])

  return (
    <div className="bg-cream min-h-screen">
      <div className="max-w-[1280px] mx-auto px-8 lg:px-16 py-12">
        
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 mb-12">
          <div>
            <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-4">Browse</p>
            <h1 className="font-serif text-4xl lg:text-5xl text-navy-light">Explore Jobs</h1>
            <p className="mt-2 text-body">Discover AI-powered opportunities.</p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 bg-white border border-border rounded-full px-5 py-3 w-full sm:w-[300px]">
              <Search size={18} className="text-body/50" />
              <input type="text" placeholder="Search jobs..." value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="bg-transparent outline-none text-navy placeholder:text-body/50 w-full text-sm" />
            </div>

            <button onClick={() => setUseSemantic(!useSemantic)}
              className={`px-4 py-3 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                useSemantic ? "bg-navy text-white" : "bg-white border border-border text-body hover:text-navy"
              }`}>
              <Sparkles size={15} /> AI
            </button>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-navy border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : error ? (
          <div className="text-center py-24">
            <p className="text-red-500">{error}</p>
          </div>
        ) : jobs.length > 0 ? (
          <>
            <div className="grid lg:grid-cols-2 gap-5">
              {jobs.map(job => (
                <JobCard key={job.id} company={job.company} role={job.title} source={job.source}
                  location={job.location} match={job.score || 0}
                  skills={job.searchable_text ? extractTechPills(job.searchable_text) : (job.tech_stack || [])}
                  applyLink={job.apply_link} score={job.score} />
              ))}
            </div>

            <div className="mt-12 flex items-center justify-center gap-4">
              <button onClick={() => setCurrentPage(p => Math.max(p - 1, 1))} disabled={currentPage === 1}
                className="px-5 py-2.5 rounded-full border border-border text-body hover:text-navy disabled:opacity-30 transition-colors text-sm font-medium">Previous</button>
              <span className="text-sm font-medium text-navy">Page {currentPage}</span>
              <button onClick={() => setCurrentPage(p => p + 1)} disabled={jobs.length < 10}
                className="px-5 py-2.5 rounded-full border border-border text-body hover:text-navy disabled:opacity-30 transition-colors text-sm font-medium">Next</button>
            </div>
          </>
        ) : (
          <div className="text-center py-24">
            <p className="text-navy font-serif text-2xl mb-2">No jobs found</p>
            <p className="text-body">Try different keywords or toggle AI search.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default JobsPage