import { useContext, useEffect ,useState} from "react"

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
  Target,
  ShieldAlert,
Database,
ServerCrash

} from "lucide-react"
import StatsCard from "../components/dashboard/StatsCard"
import ResumeUpload from "../components/dashboard/ResumeUpload"


function DashboardPage() {

  const { logout } =
  useContext(AuthContext)

  const [overviewData, setOverviewData] =
  useState(null)

  const [recommendedJobs, setRecommendedJobs] = 
  useState([])

  const [loading, setLoading] =
  useState(true)

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

  // useEffect(() => {
    
  //   const fetchOverview = async () => {
  //     try {

  //       const response = await api.get("/agent/overview")
        
  //       setOverviewData(response.data.data)
  //       // const jobsresponse =await api.get("/jobs?page=1&page_size=3")
  //       const jobsresponse =await api.get("/jobs/recommendations?limit=3")
  //       setRecommendedJobs(jobsresponse.data.data)
  //     } catch (error) {
        
  //       console.error("Error fetching agent overview:", error)
  //     }
  //     finally {
  //       setLoading(false)
  //     }
  //   }

  //   fetchOverview()
  // }, [])

    useEffect(() => {
    
    const fetchOverview = async () => {
      try {
        
        const overviewResponse = await api.get("/agent/overview")
        setOverviewData(overviewResponse.data.data)

        let jobsResponse
        try {
          jobsResponse = await api.get("/jobs/for-me?top_k=3")
          if (jobsResponse.data && jobsResponse.data.success === false) {
           
            jobsResponse = await api.get("/jobs/recommendations?limit=3")
          }
        } catch (aiError) {
          
          console.log("AI matching unavailable, using generic recommendations:", aiError)
          jobsResponse = await api.get("/jobs/recommendations?limit=3")
        }

        setRecommendedJobs(jobsResponse.data.data)
      } catch (error) {
        console.error("Error fetching dashboard data:", error)
      }
      finally {
        setLoading(false)
      }
    }

    fetchOverview()
  }, [])


  const handleLogout = () => {

    logout()

    navigate("/login")
  }

if(loading) {

  return (
    <DashboardLayout>

      <div className="flex items-center justify-center h-64">

        <p className="text-gray-400 text-lg">

          Loading dashboard...

        </p>

      </div>

    </DashboardLayout>
  )
}
  return (

    <DashboardLayout>


  {/* Analytics Section */}

  <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-8">


        <StatsCard
      title="Total Jobs Collected"
      value={overviewData?.total_jobs || 0}
      description="Total opportunities collected by the AI agent."
      icon={BriefcaseBusiness}
      gradient="from-blue-500 to-cyan-400"
    />

    <StatsCard
      title="Jobs Fetched"
      value={overviewData?.latest_run?.jobs_fetched || 0}
      description="Jobs fetched during the latest pipeline execution."
      icon={TrendingUp}
      gradient="from-purple-500 to-pink-400"
    />

    <StatsCard
      title="Alerts Sent"
      value={overviewData?.latest_run?.alerts_sent || 0}
      description="Telegram alerts sent from latest job matches."
      icon={Bookmark}
      gradient="from-green-500 to-emerald-400"
    />

    <StatsCard
      title="Pipeline Status"
      value={overviewData?.latest_run?.status || "UNKNOWN"}
      description="Current health status of the automation pipeline."
      icon={Activity}
      gradient="from-orange-500 to-yellow-400"
    />

    <StatsCard
      title="Execution Time"
      value={`${Math.round(
        overviewData?.latest_run?.execution_time_seconds || 0
      )}s`}
      description="Latest pipeline execution duration."
      icon={BrainCircuit}
      gradient="from-cyan-500 to-blue-500"
    />

    <StatsCard
      title="Successful Runs"
      value={overviewData?.successful_runs || 0}
      description="Total successful automated pipeline executions."
      icon={Target}
      gradient="from-pink-500 to-rose-400"
    />

        <StatsCard
      title="Jobs Filtered"
      value={
        overviewData?.latest_run?.jobs_filtered || 0
      }
      description="Irrelevant jobs rejected by domain intelligence."
      icon={ShieldAlert}
      gradient="from-red-500 to-orange-400"
    />

        <StatsCard
      title="Duplicates Skipped"
      value={
        overviewData?.latest_run?.duplicates_skipped || 0
      }
      description="Duplicate jobs prevented from re-entering database."
      icon={Database}
      gradient="from-yellow-500 to-amber-400"
    />

        <StatsCard
      title="Scraper Failures"
      value={
        overviewData?.latest_run?.scraper_failures || 0
      }
      description="Sources that failed during latest pipeline execution."
      icon={ServerCrash}
      gradient="from-rose-500 to-pink-500"
    />

  </div>

        {/* Resume Upload */}
      <div className="mt-10">
        <ResumeUpload />
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


      <div className="space-y-6">

  {recommendedJobs.map((job) => (

    <div
      key={job.id}
      className="rounded-3xl border border-white/10 bg-white/5 p-6"
    >

      <div className="flex items-start justify-between gap-4">

        <div>

          <h3 className="text-2xl font-black text-white">

            {job.title}

          </h3>

          <p className="mt-2 text-cyan-300 font-semibold">

            {job.company}

          </p>

          <p className="mt-3 text-gray-400">

            {job.location}

          </p>

        </div>


        <div className="px-4 py-2 rounded-full bg-green-500/20 text-green-300 font-bold">

          {job.hybrid_score ? Math.round(job.hybrid_score * 100) : job.score || 0}% Match

        </div>

      </div>


      <div className="mt-6 flex items-center justify-between">

        <span className="text-sm text-gray-500">

          Source: {job.source}

        </span>


        <a
          href={job.apply_link}
          target="_blank"
          rel="noopener noreferrer"
          className="px-5 py-3 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-black hover:scale-105 transition"
        >

          Apply Now

        </a>

      </div>

    </div>
  ))}
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