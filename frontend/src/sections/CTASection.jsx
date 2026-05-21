import { motion } from "framer-motion"

import { Link } from "react-router-dom"

import {

  Sparkles,

  ArrowRight,

  BrainCircuit

} from "lucide-react"


function CTASection() {

  return (

    <section className="relative overflow-hidden bg-[#050816] py-36 px-6 text-white">


      {/* Background Glows */}

      <div className="absolute top-[-150px] left-[20%] w-[400px] h-[400px] bg-blue-500/20 blur-3xl rounded-full"></div>

      <div className="absolute bottom-[-150px] right-[20%] w-[400px] h-[400px] bg-cyan-400/10 blur-3xl rounded-full"></div>


      <motion.div

        initial={{
          opacity: 0,
          y: 50
        }}

        whileInView={{
          opacity: 1,
          y: 0
        }}

        transition={{
          duration: 0.8
        }}

        viewport={{
          once: true
        }}

        className="relative z-10 max-w-6xl mx-auto"
      >


        {/* Main CTA Card */}

        <div className="relative overflow-hidden rounded-[40px] border border-white/10 bg-white/5 backdrop-blur-xl px-10 py-20 lg:px-20 text-center shadow-2xl">


          {/* Decorative Glow */}

          <div className="absolute top-[-100px] left-[-100px] w-[250px] h-[250px] bg-blue-500/20 blur-3xl rounded-full"></div>

          <div className="absolute bottom-[-100px] right-[-100px] w-[250px] h-[250px] bg-cyan-400/20 blur-3xl rounded-full"></div>


          {/* Badge */}

          <div className="relative z-10 inline-flex items-center gap-2 px-5 py-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 text-cyan-300 mb-10">

            <Sparkles size={18} />

            AI Career Acceleration Platform

          </div>


          {/* Heading */}

          <h2 className="relative z-10 text-5xl lg:text-7xl font-black leading-tight">

            Let AI Transform

            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 mt-3">

              Your Career Journey

            </span>

          </h2>


          {/* Description */}

          <p className="relative z-10 mt-10 text-xl text-gray-300 leading-relaxed max-w-3xl mx-auto">

            Stop manually searching through endless job listings.
            Let intelligent automation discover, rank, and track opportunities for you.

          </p>


          {/* Buttons */}

          <div className="relative z-10 mt-14 flex flex-col sm:flex-row justify-center gap-6">


            <Link
              to="/signup"
              className="group inline-flex items-center justify-center gap-3 bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-black px-10 py-5 rounded-2xl shadow-2xl hover:scale-105 transition"
            >

              Start Free Today

              <ArrowRight
                className="group-hover:translate-x-1 transition"
              />

            </Link>


            <Link
              to="/login"
              className="inline-flex items-center justify-center gap-3 border border-white/20 px-10 py-5 rounded-2xl font-bold hover:bg-white/10 transition"
            >

              Login

            </Link>

          </div>


          {/* Bottom Stats */}

          <div className="relative z-10 mt-16 grid md:grid-cols-3 gap-8 text-center">


            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">

              <h3 className="text-4xl font-black text-cyan-300">

                AI

              </h3>

              <p className="mt-2 text-gray-400">

                Smart Recommendations

              </p>

            </div>


            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">

              <h3 className="text-4xl font-black text-blue-300">

                Real-Time

              </h3>

              <p className="mt-2 text-gray-400">

                Automated Job Discovery

              </p>

            </div>


            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">

              <h3 className="text-4xl font-black text-cyan-300">

                24/7

              </h3>

              <p className="mt-2 text-gray-400">

                Intelligent Monitoring

              </p>

            </div>

          </div>


          {/* Floating AI Icon */}

          <motion.div

            animate={{
              y: [0, -15, 0]
            }}

            transition={{
              repeat: Infinity,
              duration: 4
            }}

            className="absolute top-10 right-10 hidden lg:flex w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 items-center justify-center shadow-2xl"
          >

            <BrainCircuit className="text-black" />

          </motion.div>

        </div>

      </motion.div>

    </section>
  )
}

export default CTASection