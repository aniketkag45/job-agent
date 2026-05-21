import {

  GitBranch,

  Mail,

  Bell,

  Briefcase

} from "lucide-react"


function Footer() {

  return (

    <footer className="relative overflow-hidden bg-black text-white px-6 pt-24 pb-10">


      {/* Background Glow */}

      <div className="absolute top-[-100px] left-[20%] w-[300px] h-[300px] bg-blue-500/10 blur-3xl rounded-full"></div>

      <div className="absolute bottom-[-100px] right-[20%] w-[300px] h-[300px] bg-cyan-400/10 blur-3xl rounded-full"></div>


      <div className="relative z-10 max-w-7xl mx-auto">


        {/* Top Footer */}

        <div className="grid lg:grid-cols-4 gap-14 border-b border-white/10 pb-16">


          {/* Brand */}

          <div className="lg:col-span-2">

            <h2 className="text-4xl font-black">

              AI Job Agent

            </h2>


            <p className="mt-6 text-gray-400 leading-relaxed max-w-xl">

              A modern AI-powered platform designed to automate job discovery,
              deliver intelligent recommendations, and simplify career growth.

            </p>


            {/* Socials */}

            <div className="mt-8 flex gap-4">


              <a
                href="#"
                className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-blue-500/20 transition"
              >

                <GitBranch size={20} />

              </a>


              <a
                href="#"
                className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-cyan-500/20 transition"
              >

                <Bell size={20} />

              </a>


              <a
                href="#"
                className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-blue-400/20 transition"
              >

                <Briefcase size={20} />

              </a>


              <a
                href="#"
                className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-purple-500/20 transition"
              >

                <Mail size={20} />

              </a>

            </div>

          </div>


          {/* Navigation */}

          <div>

            <h3 className="text-xl font-bold mb-6">

              Platform

            </h3>


            <ul className="space-y-4 text-gray-400">

              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  Features

                </a>

              </li>


              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  AI Workflow

                </a>

              </li>


              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  Dashboard

                </a>

              </li>


              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  Smart Tracking

                </a>

              </li>

            </ul>

          </div>


          {/* Company */}

          <div>

            <h3 className="text-xl font-bold mb-6">

              Company

            </h3>


            <ul className="space-y-4 text-gray-400">

              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  About

                </a>

              </li>


              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  Careers

                </a>

              </li>


              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  Privacy Policy

                </a>

              </li>


              <li>

                <a
                  href="#"
                  className="hover:text-white transition"
                >

                  Contact

                </a>

              </li>

            </ul>

          </div>

        </div>


        {/* Bottom Footer */}

        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-gray-500 text-sm">

          <p>

            © 2026 AI Job Agent. All rights reserved.

          </p>


          <p>

            Built with AI-driven vision and modern SaaS architecture.

          </p>

        </div>

      </div>

    </footer>
  )
}

export default Footer