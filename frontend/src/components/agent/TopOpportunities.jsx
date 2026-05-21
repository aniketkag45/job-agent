import { motion } from "framer-motion"

import {

  ArrowRight,

  Sparkles,

  MapPin,

  Building2

} from "lucide-react"


const opportunities = [

  {

    id: 1,

    title: "AI Backend Engineer",

    company: "OpenAI Labs",

    location: "Remote",

    score: 98
  },

  {

    id: 2,

    title: "Frontend React Developer",

    company: "Google",

    location: "Hybrid",

    score: 95
  },

  {

    id: 3,

    title: "LLM Engineer",

    company: "Anthropic",

    location: "Worldwide",

    score: 97
  }
]


function TopOpportunities() {

  return (

    <motion.div

      initial={{
        opacity: 0,
        y: 20
      }}

      animate={{
        opacity: 1,
        y: 0
      }}

      transition={{
        duration: 0.6
      }}

      className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur-xl"
    >


      {/* Glow */}

      <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/5 to-blue-500/5"></div>


      <div className="relative z-10">


        {/* Header */}

        <div className="flex items-center justify-between gap-4">


          <div>

            <h2 className="text-3xl font-black text-white">

              Top AI Opportunities

            </h2>


            <p className="mt-2 text-gray-400">

              Highest ranked opportunities detected by the AI engine.

            </p>

          </div>


          <div className="hidden sm:flex items-center gap-2 rounded-full bg-cyan-400/10 px-4 py-2 text-sm font-semibold text-cyan-300">

            <Sparkles size={16} />

            AI Ranked

          </div>

        </div>


        {/* Opportunities */}

        <div className="mt-10 space-y-5">


          {opportunities.map((job) => (

            <motion.div

              key={job.id}

              whileHover={{
                x: 4
              }}

              className="group flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 rounded-2xl border border-white/10 bg-black/20 p-6 transition"
            >


              {/* Left */}

              <div className="flex-1">


                <div className="flex flex-wrap items-center gap-3">


                  <h3 className="text-2xl font-black text-white">

                    {job.title}

                  </h3>


                  <div className="rounded-full bg-green-400/10 px-3 py-1 text-sm font-bold text-green-300">

                    {job.score}% Match

                  </div>

                </div>


                <div className="mt-4 flex flex-wrap items-center gap-5 text-gray-400">


                  <div className="flex items-center gap-2">

                    <Building2 size={18} />

                    {job.company}

                  </div>


                  <div className="flex items-center gap-2">

                    <MapPin size={18} />

                    {job.location}

                  </div>

                </div>

              </div>


              {/* Button */}

              <button className="group inline-flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-cyan-400 to-blue-500 px-6 py-4 font-black text-black transition hover:scale-[1.02]">

                Apply Fast

                <ArrowRight
                  size={18}
                  className="transition group-hover:translate-x-1"
                />

              </button>

            </motion.div>
          ))}

        </div>

      </div>

    </motion.div>
  )
}

export default TopOpportunities