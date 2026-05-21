import { useContext, useEffect } from "react"

import { useNavigate } from "react-router-dom"

import { AuthContext } from "../context/authContext"

import DashboardLayout from "../components/dashboard/DashboardLayout"

import api from "../api/axios"

import {


  BriefcaseBusiness,

  Bookmark,

  BrainCircuit,
  TrendingUp,
  Activity,
  Target

} from "lucide-react"
import StatsCard from "../components/dashboard/StatsCard"


function DashboardPage() {

  const { logout } =
  useContext(AuthContext)

  const navigate = useNavigate()


  useEffect(() => {

    const fetchUser = async () => {

      try {

        const response =
        await api.get("/me")

        console.log(response.data)

      } catch (error) {

        console.log(error)
      }
    }

    fetchUser()

  }, [])


  const handleLogout = () => {

    logout()

    navigate("/login")
  }


  return (

    <DashboardLayout>


  {/* Analytics Section */}

  <div className="grid lg:grid-cols-3 gap-8">


    <StatsCard
      title="Recommended Jobs"
      value="128"
      description="AI-matched opportunities based on your profile and skills."
      icon={BriefcaseBusiness}
      gradient="from-blue-500 to-cyan-400"
    />


    <StatsCard
      title="Applications"
      value="24"
      description="Track your recent applications and hiring progress."
      icon={TrendingUp}
      gradient="from-purple-500 to-pink-400"
    />


    <StatsCard
      title="Profile Strength"
      value="92%"
      description="Your AI profile optimization score is performing strongly."
      icon={Target}
      gradient="from-green-500 to-emerald-400"
    />

  </div>


  {/* Main Dashboard Grid */}

  <div className="mt-10 grid lg:grid-cols-3 gap-8">


    {/* AI Recommendations */}

    <div className="lg:col-span-2 rounded-3xl border border-white/10 bg-white/5 p-8 text-white">


      <div className="flex items-center justify-between mb-8">

        <div>

          <h2 className="text-3xl font-black">

            AI Recommendations

          </h2>

          <p className="text-gray-400 mt-2">

            Intelligent opportunities curated for your profile.

          </p>

        </div>


        <div className="w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center">

          <BrainCircuit
            className="text-black"
            size={30}
          />

        </div>

      </div>


      <div className="space-y-5">


        <div className="rounded-2xl border border-white/10 bg-white/5 p-6 hover:bg-white/10 transition">

          <div className="flex items-center justify-between">

            <div>

              <h3 className="text-xl font-bold">

                Frontend Engineer

              </h3>

              <p className="text-gray-400 mt-2">

                Google • Remote • ₹28 LPA

              </p>

            </div>


            <span className="px-4 py-2 rounded-full bg-green-500/20 text-green-300 text-sm font-semibold">

              98% Match

            </span>

          </div>

        </div>


        <div className="rounded-2xl border border-white/10 bg-white/5 p-6 hover:bg-white/10 transition">

          <div className="flex items-center justify-between">

            <div>

              <h3 className="text-xl font-bold">

                AI Developer

              </h3>

              <p className="text-gray-400 mt-2">

                Microsoft • Hybrid • ₹35 LPA

              </p>

            </div>


            <span className="px-4 py-2 rounded-full bg-cyan-500/20 text-cyan-300 text-sm font-semibold">

              95% Match

            </span>

          </div>

        </div>


        <div className="rounded-2xl border border-white/10 bg-white/5 p-6 hover:bg-white/10 transition">

          <div className="flex items-center justify-between">

            <div>

              <h3 className="text-xl font-bold">

                React Engineer

              </h3>

              <p className="text-gray-400 mt-2">

                Amazon • Bangalore • ₹24 LPA

              </p>

            </div>


            <span className="px-4 py-2 rounded-full bg-purple-500/20 text-purple-300 text-sm font-semibold">

              93% Match

            </span>

          </div>

        </div>

      </div>

    </div>


    {/* Activity Feed */}

    <div className="rounded-3xl border border-white/10 bg-white/5 p-8 text-white">


      <div className="flex items-center justify-between mb-8">

        <div>

          <h2 className="text-2xl font-black">

            Activity Feed

          </h2>

          <p className="text-gray-400 mt-2">

            Recent account activity

          </p>

        </div>


        <Activity className="text-cyan-300" />

      </div>


      <div className="space-y-6">


        <div className="border-l-2 border-cyan-400 pl-5">

          <h3 className="font-bold">

            Applied to AI Engineer

          </h3>

          <p className="text-gray-400 mt-1 text-sm">

            2 hours ago

          </p>

        </div>


        <div className="border-l-2 border-blue-400 pl-5">

          <h3 className="font-bold">

            Saved Frontend Developer

          </h3>

          <p className="text-gray-400 mt-1 text-sm">

            Yesterday

          </p>

        </div>


        <div className="border-l-2 border-purple-400 pl-5">

          <h3 className="font-bold">

            Profile updated successfully

          </h3>

          <p className="text-gray-400 mt-1 text-sm">

            2 days ago

          </p>

        </div>

      </div>


      {/* Logout */}

      <button
        onClick={handleLogout}
        className="w-full mt-10 bg-red-500 hover:bg-red-600 transition py-4 rounded-2xl font-bold flex items-center justify-center gap-3"
      >

        <Bookmark size={20} />

        Logout

      </button>

    </div>

  </div>

</DashboardLayout>
  )
}

export default DashboardPage