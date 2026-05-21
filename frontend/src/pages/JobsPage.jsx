import DashboardLayout from "../components/dashboard/DashboardLayout"

import { useState, useEffect } from "react"

import JobCard from "../components/jobs/JobCard"

import {

  Search,

  SlidersHorizontal

} from "lucide-react"

import api from "../api/axios"


function JobsPage() {

  /* ---------------- STATES ---------------- */

  const [jobs, setJobs] = useState([])

  const [loading, setLoading] =
  useState(true)

  const [error, setError] =
  useState("")

  const [searchTerm, setSearchTerm] =
  useState("")

  const [selectedLocation, setSelectedLocation] =
  useState("All")

  const [currentPage, setCurrentPage] =
  useState(1)


  /* ---------------- FETCH JOBS ---------------- */

  useEffect(() => {

    const fetchFilteredJobs = async () => {

      try {

        setLoading(true)

        const params =
        new URLSearchParams()


        /* Pagination */

        params.append(
          "page",
          currentPage
        )

        params.append(
          "page_size",
          10
        )


        /* Search */

        if (searchTerm.trim()) {

          params.append(
            "keyword",
            searchTerm
          )
        }


        /* Location */

        if (
          selectedLocation !== "All"
        ) {

          params.append(
            "location",
            selectedLocation
          )
        }


        /* Detect Filters */

        const hasFilters =

          searchTerm.trim() ||

          selectedLocation !== "All"


        let response


        /* Query Endpoint */

        if (hasFilters) {

          response = await api.get(

            `/jobs/query?${params.toString()}`
          )

        }

        /* Default Jobs Endpoint */

        else {

          response = await api.get(

            `/jobs?page=${currentPage}&page_size=10`
          )
        }


        setJobs(response.data.data)

        setError("")

      } catch (err) {

        console.error(
          "Error fetching jobs:",
          err
        )

        setError(
          "Failed to fetch jobs"
        )

      } finally {

        setLoading(false)
      }
    }


    /* Debounce */

    const debounceTimer =
    setTimeout(() => {

      fetchFilteredJobs()

    }, 500)


    return () =>
      clearTimeout(debounceTimer)

  }, [

    searchTerm,

    selectedLocation,

    currentPage
  ])


  /* ---------------- RESET PAGE ---------------- */

  useEffect(() => {

    setCurrentPage(1)

  }, [

    searchTerm,

    selectedLocation
  ])


  /* ---------------- LOADING UI ---------------- */

  if (loading) {

    return (

      <DashboardLayout>

        <div className="flex items-center justify-center min-h-[70vh]">

          <h1 className="text-4xl font-black text-white">

            Loading Jobs...

          </h1>

        </div>

      </DashboardLayout>
    )
  }


  /* ---------------- ERROR UI ---------------- */

  if (error) {

    return (

      <DashboardLayout>

        <div className="flex items-center justify-center min-h-[70vh]">

          <h1 className="text-3xl font-black text-red-400 text-center">

            {error}

          </h1>

        </div>

      </DashboardLayout>
    )
  }


  /* ---------------- MAIN UI ---------------- */

  return (

    <DashboardLayout>


      {/* Header */}

      <div className="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-6 mb-10">


        {/* Left */}

        <div>

          <h1 className="text-5xl font-black text-white">

            Explore Jobs

          </h1>


          <p className="mt-3 text-gray-400 text-lg">

            Discover AI-powered opportunities tailored to your career goals.

          </p>

        </div>


        {/* Filters */}

        <div className="flex flex-col sm:flex-row items-center gap-4">


          {/* Search */}

          <div className="flex items-center gap-3 bg-white/5 border border-white/10 rounded-2xl px-5 py-4 w-full sm:w-[320px]">

            <Search
              size={20}
              className="text-gray-400"
            />

            <input
              type="text"
              placeholder="Search jobs..."
              value={searchTerm}
              onChange={(e) =>
                setSearchTerm(e.target.value)
              }
              className="bg-transparent outline-none text-white placeholder:text-gray-500 w-full"
            />

          </div>


          {/* Location Filter */}

          <select
            value={selectedLocation}
            onChange={(e) =>
              setSelectedLocation(e.target.value)
            }
            className="bg-white/5 border border-white/10 rounded-2xl px-5 py-4 text-white outline-none w-full sm:w-auto"
          >

            <option
              value="All"
              className="bg-[#0B1120]"
            >

              All Locations

            </option>

            <option
              value="Remote"
              className="bg-[#0B1120]"
            >

              Remote

            </option>

            <option
              value="Hybrid"
              className="bg-[#0B1120]"
            >

              Hybrid

            </option>

            <option
              value="Bangalore"
              className="bg-[#0B1120]"
            >

              Bangalore

            </option>

          </select>


          {/* Filter Button */}

          <button className="w-16 h-16 rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center text-gray-300 hover:bg-white/10 transition">

            <SlidersHorizontal size={22} />

          </button>

        </div>

      </div>


      {/* Jobs Grid */}

      {jobs.length > 0 ? (

        <>

          <div className="grid lg:grid-cols-2 gap-8">

            {jobs.map((job) => (

              <JobCard
                key={job.id}
                company={job.company}
                role={job.title}
                salary={job.salary || "Not Disclosed"}
                location={job.location}
                type="Full Time"
                match={job.score || 0}
                skills={job.skills || []}
                applyLink={job.apply_link}
              />

            ))}

          </div>


          {/* Pagination */}

          <div className="mt-16 flex items-center justify-center gap-6">


            {/* Previous */}

            <button

              onClick={() =>
                setCurrentPage(

                  (prev) =>
                    Math.max(prev - 1, 1)
                )
              }

              disabled={currentPage === 1}

              className={`px-6 py-3 rounded-2xl font-bold transition ${
                currentPage === 1
                  ? "bg-white/5 text-gray-500 cursor-not-allowed"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >

              Previous

            </button>


            {/* Current Page */}

            <div className="px-6 py-3 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-black">

              Page {currentPage}

            </div>


            {/* Next */}

            <button

              onClick={() =>
                setCurrentPage(

                  (prev) => prev + 1
                )
              }

              disabled={jobs.length < 10}

              className={`px-6 py-3 rounded-2xl font-bold transition ${
                jobs.length < 10
                  ? "bg-white/5 text-gray-500 cursor-not-allowed"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >

              Next

            </button>

          </div>

        </>

      ) : (

        <div className="mt-20 text-center">

          <h2 className="text-4xl font-black text-white">

            No Jobs Found

          </h2>

          <p className="mt-4 text-gray-400 text-lg">

            Try searching with different keywords or filters.

          </p>

        </div>

      )}

    </DashboardLayout>
  )
}

export default JobsPage