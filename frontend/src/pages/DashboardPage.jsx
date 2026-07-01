
import { useEffect, useState } from "react"

import api from "../api/axios"
import { BriefcaseBusiness, TrendingUp, BellRing, Activity, BrainCircuit, Target } from "lucide-react"
// import ResumeUpload from "../components/dashboard/ResumeUpload"

function DashboardPage() {
  const [overviewData, setOverviewData] = useState(null)
  const [recommendedJobs, setRecommendedJobs] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    async function fetchData() {
      try {
        const overview = await api.get("/agent/overview")
        setOverviewData(overview.data.data)

        let jobsRes
        try {
          jobsRes = await api.get("/jobs/for-me?top_k=3")
          if (jobsRes.data && jobsRes.data.success === false) {
            jobsRes = await api.get("/jobs/recommendations?limit=3")
          }
        } catch {
          jobsRes = await api.get("/jobs/recommendations?limit=3")
        }
        setRecommendedJobs(jobsRes.data.data)
      } catch (err) {
        console.error("Error fetching dashboard:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-navy border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return (
    <div className="bg-cream min-h-screen">
      <div className="max-w-[1280px] mx-auto px-8 lg:px-16 py-12">
        
        {/* Page Header */}
        <div className="mb-12">
          <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-4">Dashboard</p>
          <h1 className="font-serif text-4xl lg:text-5xl text-navy-light">Good morning.</h1>
          <p className="mt-3 text-body text-lg">Here's what's happening with your job search.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-5 mb-12">
          <StatCard icon={BriefcaseBusiness} color="bg-card-lavender" accent="text-accent-purple" label="Total Jobs Collected" value={overviewData?.total_jobs || 0} />
          <StatCard icon={TrendingUp} color="bg-card-blue" accent="text-[#3B82F6]" label="Jobs Fetched (Latest)" value={overviewData?.latest_run?.jobs_fetched || 0} />
          <StatCard icon={BellRing} color="bg-card-peach" accent="text-accent-orange" label="Alerts Sent" value={overviewData?.latest_run?.alerts_sent || 0} />
          <StatCard icon={Activity} color="bg-card-lavender" accent="text-accent-purple" label="Pipeline Status" value={overviewData?.latest_run?.status || "N/A"} />
          <StatCard icon={Target} color="bg-card-blue" accent="text-[#3B82F6]" label="Successful Runs" value={overviewData?.successful_runs || 0} />
          <StatCard icon={BrainCircuit} color="bg-card-peach" accent="text-accent-orange" label="Execution Time" value={`${Math.round(overviewData?.latest_run?.execution_time_seconds || 0)}s`} />
        </div>

        {/* Resume Upload
        <div className="mb-12">
          <ResumeUpload />
        </div> */}

        {/* AI Recommendations */}
        <div className="bg-white rounded-3xl border border-border p-8 shadow-[0_10px_40px_rgba(0,0,0,.03)]">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="font-serif text-2xl text-navy-light">AI Recommendations</h2>
              <p className="text-body mt-1">Curated for your profile</p>
            </div>
            <BrainCircuit size={22} className="text-accent-purple" />
          </div>

          {recommendedJobs.length > 0 ? (
            <div className="space-y-4">
              {recommendedJobs.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-5 rounded-2xl border border-border hover:border-accent-orange/30 hover:bg-cream/50 transition-all">
                  <div>
                    <h3 className="font-semibold text-navy">{job.title}</h3>
                    <p className="text-sm text-body mt-0.5">{job.company} · {job.location}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-medium text-body">{job.source}</span>
                    <a href={job.apply_link} target="_blank" rel="noopener noreferrer"
                      className="px-4 py-2 bg-navy hover:bg-navy-light text-white text-sm font-medium rounded-full transition-colors">
                      Apply
                    </a>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-body text-center py-8">No recommendations yet. Upload your resume to get started.</p>
          )}
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon: Icon, color, accent, label, value }) {
  return (
    <div className="bg-white rounded-2xl border border-border p-6 hover:shadow-[0_10px_40px_rgba(0,0,0,.04)] transition-all">
      <div className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center mb-4`}>
        <Icon size={18} className={accent} />
      </div>
      <div className="text-2xl font-semibold text-navy">{value}</div>
      <div className="text-sm text-body mt-1">{label}</div>
    </div>
  )
}

export default DashboardPage