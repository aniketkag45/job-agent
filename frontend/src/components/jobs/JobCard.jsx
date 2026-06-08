import { motion } from "framer-motion"

import { useContext } from "react"

import { SavedJobsContext } from "../../context/savedjobscontext"

import {

  MapPin,

  Bookmark,

  BookmarkCheck,

  ArrowRight

} from "lucide-react"


function JobCard({
  company,
  role,
  source,        // ← NEW — replaces type
  location,
  match,
  skills = [],
  applyLink,
  score,          // ← NEW — for color coding
}) {

  const {

    savedJobs,

    toggleSaveJob

  } = useContext(SavedJobsContext)


  const isSaved = savedJobs.some(

    (savedJob) =>

      savedJob.role === role &&

      savedJob.company === company
  )


  return (

    <motion.div

      whileHover={{
        y: -6
      }}

      className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl transition"
    >


      {/* Glow */}

      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 bg-gradient-to-br from-blue-500/10 to-cyan-400/10"></div>


      <div className="relative z-10">


        {/* Top Section */}

        <div className="flex items-start justify-between gap-4">


          <div className="flex-1 min-w-0">

            <h2 className="text-2xl font-black text-white leading-tight line-clamp-2">

              {role}

            </h2>


            <p className="mt-2 text-cyan-300 font-semibold">

              {company}

            </p>

          </div>


          {/* Match Score */}

                    <div className={`shrink-0 px-4 py-2 rounded-full text-sm font-bold ${
            match >= 70 ? "bg-green-500/20 text-green-300" :
            match >= 40 ? "bg-yellow-500/20 text-yellow-300" :
            "bg-red-500/20 text-red-300"
          }`}>
            {match}% Match
          </div>

        </div>


        {/* Info */}

                <div className="mt-8 flex flex-wrap gap-5 text-gray-400">
          <div className="flex items-center gap-2">
            <MapPin size={18} />
            <span>{location}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400">
              {source}
            </span>
          </div>
          {score != null && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-gray-500">
                Relevance Score: {score}
              </span>
            </div>
          )}
        </div>


        {/* Skills */}

        {skills.length > 0 && (

          <div className="mt-8 flex flex-wrap gap-3">

            {skills.map((skill, index) => (

              <span
                key={index}
                className="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-gray-300"
              >

                {skill}

              </span>
            ))}

          </div>

        )}


        {/* Buttons */}

        <div className="mt-10 flex items-center gap-4">


          {/* Apply Button */}

          <button

            onClick={() => {

              if (applyLink) {

                window.open(

                  applyLink,

                  "_blank"
                )

              } else {

                alert(
                  "Apply link not available"
                )
              }
            }}

            className="group/apply flex-1 bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-black py-4 rounded-2xl flex items-center justify-center gap-2 hover:scale-[1.02] transition"
          >

            Apply Now

            <ArrowRight
              size={20}
              className="group-hover/apply:translate-x-1 transition"
            />

          </button>


          {/* Save Button */}

          <button

            onClick={() =>
              toggleSaveJob({
              company,
              role,
              source,
              location,
              match,
              score,
              skills,
              applyLink
            })
              }

            className={`w-16 h-16 rounded-2xl border flex items-center justify-center transition ${
              isSaved
                ? "bg-cyan-400 text-black border-cyan-400"
                : "border-white/10 bg-white/5 text-gray-300 hover:bg-white/10"
            }`}
          >

            {isSaved ? (

              <BookmarkCheck size={22} />

            ) : (

              <Bookmark size={22} />

            )}

          </button>

        </div>

      </div>

    </motion.div>
  )
}

export default JobCard