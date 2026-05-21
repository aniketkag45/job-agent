import { motion } from "framer-motion"

import {

  Brain,

  Briefcase,

  Bell,

  SearchCheck,

  Sparkles

} from "lucide-react"


const features = [

  {

    icon: Brain,

    title:
    "AI-Powered Matching",

    description:
    "Receive highly personalized job recommendations intelligently ranked for your profile.",
  },

  {

    icon: Briefcase,

    title:
    "Automated Discovery",

    description:
    "Continuously scan multiple platforms and discover fresh opportunities instantly.",
  },

  {

    icon: Bell,

    title:
    "Real-Time Alerts",

    description:
    "Stay updated with instant notifications whenever highly relevant jobs appear.",
  },

  {

    icon: SearchCheck,

    title:
    "Smart Tracking",

    description:
    "Track saved jobs, monitor applications, and organize your career workflow.",
  },
]


function FeaturesSection() {

  return (

    <section className="relative overflow-hidden bg-[#050816] py-32 px-6 text-white">


      {/* Background Glow */}

      <div className="absolute top-[-150px] left-[15%] w-[400px] h-[400px] bg-blue-500/10 blur-3xl rounded-full"></div>

      <div className="absolute bottom-[-150px] right-[15%] w-[400px] h-[400px] bg-cyan-400/10 blur-3xl rounded-full"></div>


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

          className="text-center mb-24"
        >

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-500/20 bg-blue-500/10 text-blue-300 mb-8">

            <Sparkles size={18} />

            Intelligent Platform Features

          </div>


          <h2 className="text-5xl lg:text-6xl font-black leading-tight">

            Everything You Need

            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">

              To Accelerate Careers

            </span>

          </h2>


          <p className="mt-8 text-xl text-gray-400 leading-relaxed max-w-3xl mx-auto">

            Powerful AI-driven tools designed to simplify job discovery,
            automate workflows, and improve career decisions.

          </p>

        </motion.div>


        {/* Feature Grid */}

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

          {features.map((feature, index) => {

            const Icon =
            feature.icon

            return (

              <motion.div

                key={index}

                initial={{
                  opacity: 0,
                  y: 50
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
                  y: -12,
                  scale: 1.02
                }}

                className="group relative overflow-hidden rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl p-8 shadow-2xl"
              >


                {/* Hover Glow */}

                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 bg-gradient-to-br from-blue-500/10 to-cyan-400/10"></div>


                {/* Icon */}

                <div className="relative z-10 w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center mb-8 shadow-xl">

                  <Icon size={30} />

                </div>


                {/* Content */}

                <div className="relative z-10">

                  <h3 className="text-2xl font-bold">

                    {feature.title}

                  </h3>


                  <p className="mt-5 text-gray-400 leading-relaxed">

                    {feature.description}

                  </p>

                </div>


                {/* Decorative Blur */}

                <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-blue-500/10 blur-3xl rounded-full"></div>

              </motion.div>
            )
          })}
        </div>

      </div>

    </section>
  )
}

export default FeaturesSection