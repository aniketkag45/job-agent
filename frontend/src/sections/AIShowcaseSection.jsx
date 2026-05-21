import { motion } from "framer-motion"

import {

  BrainCircuit,

  TrendingUp,

  Sparkles,

  BarChart3

} from "lucide-react"


function AIShowcaseSection() {

  return (

    <section className="relative overflow-hidden bg-[#030712] py-32 px-6 text-white">

      {/* Background Glow */}

      <div className="absolute top-[-150px] left-[10%] w-[400px] h-[400px] bg-blue-500/20 blur-3xl rounded-full"></div>

      <div className="absolute bottom-[-150px] right-[10%] w-[400px] h-[400px] bg-cyan-400/10 blur-3xl rounded-full"></div>


      <div className="relative z-10 max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center">


        {/* LEFT SIDE */}

        <motion.div

          initial={{
            opacity: 0,
            x: -80
          }}

          whileInView={{
            opacity: 1,
            x: 0
          }}

          transition={{
            duration: 0.8
          }}

          viewport={{
            once: true
          }}
        >

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-300 mb-8">

            <BrainCircuit size={18} />

            Intelligent AI Engine

          </div>


          <h2 className="text-5xl lg:text-6xl font-black leading-tight">

            Smarter Career

            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">

              Decision Making

            </span>

          </h2>


          <p className="mt-8 text-xl text-gray-300 leading-relaxed">

            Our AI continuously analyzes job relevance, skill alignment,
            market trends, and opportunity quality to help you focus on the best matches.

          </p>


          <div className="mt-12 space-y-6">


            <div className="flex items-start gap-4">

              <div className="w-12 h-12 rounded-2xl bg-blue-500/20 flex items-center justify-center">

                <Sparkles className="text-blue-400" />

              </div>

              <div>

                <h3 className="text-xl font-bold">

                  Personalized AI Matching

                </h3>

                <p className="text-gray-400 mt-2">

                  Tailored recommendations based on your skills and interests.

                </p>

              </div>

            </div>


            <div className="flex items-start gap-4">

              <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 flex items-center justify-center">

                <TrendingUp className="text-cyan-400" />

              </div>

              <div>

                <h3 className="text-xl font-bold">

                  Market Trend Analysis

                </h3>

                <p className="text-gray-400 mt-2">

                  Understand which opportunities are growing fastest in the market.

                </p>

              </div>

            </div>


            <div className="flex items-start gap-4">

              <div className="w-12 h-12 rounded-2xl bg-purple-500/20 flex items-center justify-center">

                <BarChart3 className="text-purple-400" />

              </div>

              <div>

                <h3 className="text-xl font-bold">

                  Intelligent Scoring

                </h3>

                <p className="text-gray-400 mt-2">

                  AI-generated match scores prioritize the most relevant jobs.

                </p>

              </div>

            </div>

          </div>

        </motion.div>


        {/* RIGHT SIDE */}

        <motion.div

          initial={{
            opacity: 0,
            x: 80
          }}

          whileInView={{
            opacity: 1,
            x: 0
          }}

          transition={{
            duration: 0.8
          }}

          viewport={{
            once: true
          }}

          className="relative"
        >


          {/* Main Analytics Card */}

          <div className="bg-white/5 border border-white/10 backdrop-blur-xl rounded-[32px] p-8 shadow-2xl">


            <div className="flex items-center justify-between mb-10">

              <div>

                <h3 className="text-2xl font-bold">

                  AI Insights

                </h3>

                <p className="text-gray-400 mt-1">

                  Career intelligence overview

                </p>

              </div>


              <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center">

                <BrainCircuit />

              </div>

            </div>


            {/* Match Score */}

            <div className="mb-8">

              <div className="flex justify-between mb-3">

                <span className="text-gray-300">

                  AI Match Score

                </span>

                <span className="font-bold text-cyan-400">

                  96%

                </span>

              </div>


              <div className="w-full h-4 rounded-full bg-white/10 overflow-hidden">

                <motion.div

                  initial={{
                    width: 0
                  }}

                  whileInView={{
                    width: "96%"
                  }}

                  transition={{
                    duration: 1.5
                  }}

                  viewport={{
                    once: true
                  }}

                  className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 rounded-full"
                />

              </div>

            </div>


            {/* Analytics Cards */}

            <div className="grid grid-cols-2 gap-5">


              <div className="bg-white/5 rounded-2xl p-5 border border-white/10">

                <p className="text-gray-400 text-sm">

                  Jobs Analyzed

                </p>

                <h4 className="text-3xl font-black mt-2">

                  12.4K

                </h4>

              </div>


              <div className="bg-white/5 rounded-2xl p-5 border border-white/10">

                <p className="text-gray-400 text-sm">

                  Saved Time

                </p>

                <h4 className="text-3xl font-black mt-2">

                  85%

                </h4>

              </div>


              <div className="bg-white/5 rounded-2xl p-5 border border-white/10">

                <p className="text-gray-400 text-sm">

                  AI Accuracy

                </p>

                <h4 className="text-3xl font-black mt-2">

                  94%

                </h4>

              </div>


              <div className="bg-white/5 rounded-2xl p-5 border border-white/10">

                <p className="text-gray-400 text-sm">

                  Live Alerts

                </p>

                <h4 className="text-3xl font-black mt-2">

                  Real-Time

                </h4>

              </div>

            </div>

          </div>


          {/* Floating Recommendation Card */}

          <motion.div

            animate={{
              y: [0, -15, 0]
            }}

            transition={{
              repeat: Infinity,
              duration: 4
            }}

            className="absolute -top-8 -right-8 bg-gradient-to-r from-blue-500 to-cyan-400 text-black rounded-2xl p-5 shadow-2xl w-60"
          >

            <p className="text-sm font-semibold">

              AI Recommendation

            </p>

            <h4 className="text-xl font-black mt-2">

              Senior AI Engineer

            </h4>

            <p className="mt-2 text-sm">

              98% profile compatibility match

            </p>

          </motion.div>

        </motion.div>

      </div>

    </section>
  )
}

export default AIShowcaseSection