import { motion } from "framer-motion"

import { Link } from "react-router-dom"

import {

  Sparkles,

  Briefcase,

  TrendingUp,

  Bell

} from "lucide-react"


function HeroSection() {

  return (

    <section className="relative min-h-screen overflow-hidden bg-[#050816] text-white flex items-center px-6 pt-32">

      {/* Background Glow */}

      <div className="absolute top-[-200px] left-[-150px] w-[500px] h-[500px] bg-blue-500/30 rounded-full blur-3xl"></div>

      <div className="absolute bottom-[-200px] right-[-150px] w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-3xl"></div>


      <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center relative z-10">


        {/* LEFT CONTENT */}

        <motion.div

          initial={{
            opacity: 0,
            x: -80
          }}

          animate={{
            opacity: 1,
            x: 0
          }}

          transition={{
            duration: 0.8
          }}
        >

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-300 mb-8">

            <Sparkles size={18} />

            AI-Powered Career Intelligence

          </div>


          <h1 className="text-6xl lg:text-7xl font-black leading-tight">

            Find Better Jobs

            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">

              Faster With AI

            </span>

          </h1>


          <p className="mt-8 text-xl text-gray-300 leading-relaxed max-w-2xl">

            Discover opportunities intelligently, receive personalized recommendations,
            automate your search workflow, and accelerate your career growth.

          </p>


          <div className="mt-10 flex flex-col sm:flex-row gap-5">

            <Link
              to="/signup"
              className="bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-bold px-8 py-4 rounded-2xl shadow-2xl hover:scale-105 transition"
            >

              Start Free

            </Link>


            <Link
              to="/login"
              className="border border-white/20 px-8 py-4 rounded-2xl font-semibold hover:bg-white/10 transition"
            >

              Login

            </Link>

          </div>


          <div className="mt-12 flex flex-wrap gap-8 text-gray-400">

            <div>

              <h3 className="text-3xl font-bold text-white">

                10K+

              </h3>

              <p className="mt-1">

                Jobs Analyzed

              </p>

            </div>


            <div>

              <h3 className="text-3xl font-bold text-white">

                AI

              </h3>

              <p className="mt-1">

                Smart Recommendations

              </p>

            </div>


            <div>

              <h3 className="text-3xl font-bold text-white">

                Real-Time

              </h3>

              <p className="mt-1">

                Opportunity Tracking

              </p>

            </div>

          </div>

        </motion.div>


        {/* RIGHT SIDE */}

        <motion.div

          initial={{
            opacity: 0,
            x: 80
          }}

          animate={{
            opacity: 1,
            x: 0
          }}

          transition={{
            duration: 0.8
          }}

          className="relative flex justify-center"
        >


          {/* Main Dashboard Card */}

          <div className="relative w-full max-w-xl rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl p-8 shadow-2xl">


            <div className="flex items-center justify-between mb-8">

              <div>

                <h3 className="text-2xl font-bold">

                  AI Job Dashboard

                </h3>

                <p className="text-gray-400 mt-1">

                  Personalized insights

                </p>

              </div>


              <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center">

                <Briefcase />

              </div>

            </div>


            <div className="space-y-5">


              <div className="bg-white/5 border border-white/10 rounded-2xl p-5">

                <div className="flex justify-between items-center">

                  <div>

                    <h4 className="font-bold text-lg">

                      AI Engineer

                    </h4>

                    <p className="text-gray-400">

                      Remote • High Match

                    </p>

                  </div>


                  <div className="text-green-400 font-bold">

                    98%

                  </div>

                </div>

              </div>


              <div className="bg-white/5 border border-white/10 rounded-2xl p-5">

                <div className="flex justify-between items-center">

                  <div>

                    <h4 className="font-bold text-lg">

                      Full Stack Developer

                    </h4>

                    <p className="text-gray-400">

                      Hybrid • Trending

                    </p>

                  </div>


                  <div className="text-blue-400 font-bold">

                    92%

                  </div>

                </div>

              </div>


              <div className="bg-white/5 border border-white/10 rounded-2xl p-5">

                <div className="flex justify-between items-center">

                  <div>

                    <h4 className="font-bold text-lg">

                      React Developer

                    </h4>

                    <p className="text-gray-400">

                      Remote • Recommended

                    </p>

                  </div>


                  <div className="text-cyan-400 font-bold">

                    95%

                  </div>

                </div>

              </div>

            </div>

          </div>


          {/* Floating Card 1 */}

          <motion.div

            animate={{
              y: [0, -15, 0]
            }}

            transition={{
              repeat: Infinity,
              duration: 4
            }}

            className="absolute -top-10 -left-8 bg-white text-black rounded-2xl shadow-2xl p-5 w-52"
          >

            <div className="flex items-center gap-3">

              <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">

                <TrendingUp className="text-blue-600" />

              </div>


              <div>

                <h4 className="font-bold">

                  89% Faster

                </h4>

                <p className="text-sm text-gray-500">

                  Job Discovery

                </p>

              </div>

            </div>

          </motion.div>


          {/* Floating Card 2 */}

          <motion.div

            animate={{
              y: [0, 15, 0]
            }}

            transition={{
              repeat: Infinity,
              duration: 5
            }}

            className="absolute -bottom-8 right-[-20px] bg-gradient-to-r from-blue-500 to-cyan-400 rounded-2xl shadow-2xl p-5 w-56"
          >

            <div className="flex items-center gap-3">

              <Bell />

              <div>

                <h4 className="font-bold">

                  Instant Alerts

                </h4>

                <p className="text-sm text-blue-100">

                  Real-time job updates

                </p>

              </div>

            </div>

          </motion.div>

        </motion.div>

      </div>

    </section>
  )
}

export default HeroSection