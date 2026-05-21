import { motion } from "framer-motion"

import { Link } from "react-router-dom"

import {

  Sparkles,

  ArrowRight

} from "lucide-react"


function Navbar() {

  return (

    <motion.nav

      initial={{
        opacity: 0,
        y: -50
      }}

      animate={{
        opacity: 1,
        y: 0
      }}

      transition={{
        duration: 0.7
      }}

      className="fixed top-6 left-0 right-0 z-50 px-6"
    >

      <div className="relative max-w-7xl mx-auto overflow-hidden rounded-3xl border border-white/10 bg-black/30 backdrop-blur-xl shadow-2xl">


        {/* Background Glow */}

        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-cyan-400/5 to-blue-500/5"></div>


        <div className="relative z-10 flex items-center justify-between px-8 py-5">


          {/* Logo */}

          <Link
            to="/"
            className="flex items-center gap-3"
          >

            <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center shadow-xl">

              <Sparkles className="text-black" />

            </div>


            <div>

              <h1 className="text-2xl font-black text-white">

                AI Job Agent

              </h1>

              <p className="text-xs text-gray-400">

                Intelligent Career Platform

              </p>

            </div>

          </Link>


          {/* Navigation Links */}

          <div className="hidden md:flex items-center gap-10 text-gray-300 font-medium">


           <Link to="/">
  Features
</Link>


            <Link to="/">
  AI Workflow
</Link>


           <Link
  to="/dashboard"
  className="hover:text-cyan-300 transition"
>

  Dashboard

</Link>


           <Link to="/jobs">
  Careers
</Link>

          </div>


          {/* Right Buttons */}

          <div className="flex items-center gap-4">


            <Link
              to="/login"
              className="hidden sm:flex px-6 py-3 rounded-2xl border border-white/10 text-gray-300 hover:bg-white/10 transition"
            >

              Login

            </Link>


            <Link
              to="/signup"
              className="group inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-bold px-7 py-3 rounded-2xl shadow-2xl hover:scale-105 transition"
            >

              Get Started

              <ArrowRight
                size={18}
                className="group-hover:translate-x-1 transition"
              />

            </Link>

          </div>

        </div>

      </div>

    </motion.nav>
  )
}

export default Navbar