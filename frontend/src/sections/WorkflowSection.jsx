import { motion } from "framer-motion"

import {

  UserPlus,

  BrainCircuit,

  Sparkles,

  BriefcaseBusiness

} from "lucide-react"


const steps = [

  {

    icon: UserPlus,

    title: "Create Your Profile",

    description:
      "Build your personalized profile with skills, experience, and career interests.",
  },

  {

    icon: BrainCircuit,

    title: "AI Analyzes Opportunities",

    description:
      "Our AI engine scans thousands of jobs and intelligently filters the best matches.",
  },

  {

    icon: Sparkles,

    title: "Receive Smart Recommendations",

    description:
      "Get highly personalized recommendations ranked by compatibility and relevance.",
  },

  {

    icon: BriefcaseBusiness,

    title: "Track Your Career Journey",

    description:
      "Manage saved jobs, monitor applications, and optimize your career workflow.",
  },
]


function WorkflowSection() {

  return (

    <section className="relative overflow-hidden bg-[#030712] py-32 px-6 text-white">


      {/* Glow Effects */}

      <div className="absolute top-[-150px] left-[10%] w-[350px] h-[350px] bg-blue-500/10 blur-3xl rounded-full"></div>

      <div className="absolute bottom-[-150px] right-[10%] w-[350px] h-[350px] bg-cyan-400/10 blur-3xl rounded-full"></div>


      <div className="relative z-10 max-w-7xl mx-auto">


        {/* Header */}

        <motion.div

          initial={{
            opacity: 0,
            y: 40
          }}

          whileInView={{
            opacity: 1,
            y: 0
          }}

          transition={{
            duration: 0.7
          }}

          viewport={{
            once: true
          }}

          className="text-center mb-28"
        >

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 text-cyan-300 mb-8">

            <Sparkles size={18} />

            AI Career Workflow

          </div>


          <h2 className="text-5xl lg:text-6xl font-black leading-tight">

            How The Platform

            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">

              Works Intelligently

            </span>

          </h2>


          <p className="mt-8 text-xl text-gray-400 leading-relaxed max-w-3xl mx-auto">

            A streamlined AI-powered workflow designed to automate and optimize your job search experience.

          </p>

        </motion.div>


        {/* Timeline Workflow */}

        <div className="relative">


          {/* Center Line */}

          <div className="hidden lg:block absolute top-1/2 left-0 w-full h-[2px] bg-gradient-to-r from-blue-500/20 via-cyan-400/40 to-blue-500/20 -translate-y-1/2"></div>


          <div className="grid lg:grid-cols-4 gap-10 relative z-10">

            {steps.map((step, index) => {

              const Icon = step.icon

              return (

                <motion.div

                  key={index}

                  initial={{
                    opacity: 0,
                    y: 60
                  }}

                  whileInView={{
                    opacity: 1,
                    y: 0
                  }}

                  transition={{
                    duration: 0.6,
                    delay: index * 0.15
                  }}

                  viewport={{
                    once: true
                  }}

                  whileHover={{
                    y: -10
                  }}

                  className="group relative"
                >


                  {/* Card */}

                  <div className="rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl p-8 shadow-2xl overflow-hidden relative min-h-[420px] flex flex-col">


                    {/* Hover Glow */}

                    <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 bg-gradient-to-br from-blue-500/10 to-cyan-400/10"></div>


                    {/* Step Number */}

                    <div className="relative z-10 w-14 h-14 rounded-full bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black shadow-2xl mb-8">

                      {index + 1}

                    </div>


                    {/* Icon */}

                    <div className="relative z-10 w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center mb-8 shadow-xl">

                      <Icon size={30} />

                    </div>


                    {/* Content */}

                    <div className="relative z-10">

                      <h3 className="text-2xl font-bold leading-snug">

                        {step.title}

                      </h3>


                      <p className="mt-5 text-gray-400 leading-relaxed text-lg">

                        {step.description}

                      </p>

                    </div>


                    {/* Decorative Blur */}

                    <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-cyan-400/10 blur-3xl rounded-full"></div>

                  </div>

                </motion.div>
              )
            })}
          </div>

        </div>

      </div>

    </section>
  )
}

export default WorkflowSection