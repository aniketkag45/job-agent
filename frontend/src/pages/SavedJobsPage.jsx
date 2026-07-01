// import {

//   useContext

// } from "react"

// import DashboardLayout from "../components/dashboard/DashboardLayout"

// import JobCard from "../components/jobs/JobCard"

// import {

//   SavedJobsContext

// } from "../context/savedjobscontext"

// import {

//   BookmarkCheck

// } from "lucide-react"


// function SavedJobsPage() {

//   const {

//     savedJobs

//   } = useContext(SavedJobsContext)


//   return (

//     <DashboardLayout>


//       {/* Header */}

//       <div className="mb-12">


//         <div className="flex items-center gap-4">


//           <div className="w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center shadow-2xl">

//             <BookmarkCheck
//               className="text-black"
//               size={30}
//             />

//           </div>


//           <div>

//             <h1 className="text-5xl font-black text-white">

//               Saved Jobs

//             </h1>


//             <p className="mt-2 text-gray-400 text-lg">

//               Manage and track your bookmarked opportunities.

//             </p>

//           </div>

//         </div>

//       </div>


//       {/* Jobs */}

//       {savedJobs.length > 0 ? (

//         <div className="grid lg:grid-cols-2 gap-8">

//           {savedJobs.map((job, index) => (

//             <JobCard
//               key={index}
//               company={job.company}
//               role={job.role}
//               salary={job.salary}
//               location={job.location}
//               type={job.type}
//               match={job.match}
//               skills={job.skills}
//             />

//           ))}

//         </div>

//       ) : (

//         <div className="rounded-[40px] border border-white/10 bg-white/5 p-16 text-center">


//           <div className="w-24 h-24 rounded-3xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center mx-auto shadow-2xl">

//             <BookmarkCheck
//               className="text-black"
//               size={40}
//             />

//           </div>


//           <h2 className="mt-10 text-4xl font-black text-white">

//             No Saved Jobs Yet

//           </h2>


//           <p className="mt-5 text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">

//             Start bookmarking opportunities from the jobs page to build your personalized AI-powered career workspace.

//           </p>

//         </div>

//       )}

//     </DashboardLayout>
//   )
// }

// export default SavedJobsPage

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