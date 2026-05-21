import {

  Bell,

  Search,

  Sparkles

} from "lucide-react"


function DashboardHeader() {

  return (

    <header className="h-[90px] border-b border-white/10 bg-[#0B1120]/80 backdrop-blur-xl px-8 flex items-center justify-between">


      {/* Left */}

      <div>

        <h1 className="text-3xl font-black text-white">

          Dashboard

        </h1>

        <p className="text-gray-400 mt-1">

          Welcome back to your AI career workspace

        </p>

      </div>


      {/* Right */}

      <div className="flex items-center gap-5">


        {/* Search */}

        <div className="hidden md:flex items-center gap-3 bg-white/5 border border-white/10 rounded-2xl px-5 py-3 w-[320px]">

          <Search
            size={20}
            className="text-gray-400"
          />

          <input
            type="text"
            placeholder="Search jobs, skills..."
            className="bg-transparent outline-none text-white placeholder:text-gray-500 w-full"
          />

        </div>


        {/* Notification */}

        <button className="w-14 h-14 rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center text-gray-300 hover:bg-white/10 transition">

          <Bell size={22} />

        </button>


        {/* User */}

        <div className="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 px-5 py-3">


          <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center">

            <Sparkles className="text-black" />

          </div>


          <div className="hidden sm:block">

            <h3 className="text-white font-bold">

              Aniket

            </h3>

            <p className="text-gray-400 text-sm">

              AI Enthusiast

            </p>

          </div>

        </div>

      </div>

    </header>
  )
}

export default DashboardHeader