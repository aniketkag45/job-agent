import {

  LayoutDashboard,

  BriefcaseBusiness,

  Bookmark,

  User,

  Settings,

  Sparkles

} from "lucide-react"

import { NavLink } from "react-router-dom"


const navItems = [

  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },

  {
    name: "Jobs",
    icon: BriefcaseBusiness,
    path: "/jobs",
  },

  {
    name: "Saved Jobs",
    icon: Bookmark,
    path: "/saved-jobs",
  },

  {
    name: "Profile",
    icon: User,
    path: "/profile",
  },

  {
    name: "Settings",
    icon: Settings,
    path: "/settings",
  },
]


function Sidebar() {

  return (

    <aside className="w-[280px] min-h-screen border-r border-white/10 bg-[#070B18] text-white p-6 flex flex-col">


      {/* Logo */}

      <div className="flex items-center gap-3 mb-14">


        <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center shadow-2xl">

          <Sparkles className="text-black" />

        </div>


        <div>

          <h1 className="text-2xl font-black">

            AI Job Agent

          </h1>

          <p className="text-gray-400 text-sm">

            Career Intelligence

          </p>

        </div>

      </div>


      {/* Navigation */}

      <nav className="flex flex-col gap-3">

        {navItems.map((item) => {

          const Icon = item.icon

          return (

            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-4 px-5 py-4 rounded-2xl transition font-medium ${
                  isActive
                    ? "bg-gradient-to-r from-blue-500 to-cyan-400 text-black shadow-xl"
                    : "text-gray-300 hover:bg-white/5 hover:text-white"
                }`
              }
            >

              <Icon size={22} />

              {item.name}

            </NavLink>
          )
        })}
      </nav>


      {/* Bottom Card */}

      <div className="mt-auto rounded-3xl border border-white/10 bg-gradient-to-br from-blue-500/10 to-cyan-400/10 p-6">

        <h3 className="text-xl font-bold">

          AI Career Insights

        </h3>

        <p className="mt-3 text-gray-400 text-sm leading-relaxed">

          Discover smarter opportunities powered by advanced AI recommendations.

        </p>

      </div>

    </aside>
  )
}

export default Sidebar