import { useContext } from "react"
import { SavedJobsContext } from "../context/savedjobscontext"
import JobCard from "../components/jobs/JobCard"
import { BookmarkCheck } from "lucide-react"

function SavedJobsPage() {
  const { savedJobs } = useContext(SavedJobsContext)

  return (
    <div className="bg-cream min-h-screen">
      <div className="max-w-[1280px] mx-auto px-8 lg:px-16 py-12">
        
        <div className="mb-12">
          <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-4">Saved</p>
          <h1 className="font-serif text-4xl lg:text-5xl text-navy-light">Saved Jobs</h1>
          <p className="mt-2 text-body">Jobs you've bookmarked for later.</p>
        </div>

        {savedJobs.length > 0 ? (
          <div className="grid lg:grid-cols-2 gap-5">
            {savedJobs.map((job, i) => (
              <JobCard key={i} company={job.company} role={job.role} source={job.source}
                location={job.location} match={job.match} skills={job.skills || []} applyLink={job.applyLink} score={job.score} />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-3xl border border-border p-16 text-center shadow-[0_10px_40px_rgba(0,0,0,.03)]">
            <div className="w-16 h-16 rounded-full bg-card-lavender flex items-center justify-center mx-auto mb-6">
              <BookmarkCheck size={28} className="text-accent-purple" />
            </div>
            <h2 className="font-serif text-2xl text-navy-light mb-2">No saved jobs yet</h2>
            <p className="text-body">Start bookmarking opportunities from the jobs page.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default SavedJobsPage