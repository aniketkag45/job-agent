import { motion } from "framer-motion"

import {

  CheckCircle2,

  Clock3,

  Globe,

  Database

} from "lucide-react"


function SourceStatusCard({

  source,

  status,

  jobsFetched,

  lastSync,

  region,

  health
}) {

  return (

    <motion.div

      whileHover={{
        y: -5
      }}

      transition={{
        duration: 0.25
      }}

      className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-7 backdrop-blur-xl shadow-2xl"
    >


      {/* Hover Glow */}

      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 bg-gradient-to-br from-cyan-400/5 to-blue-500/5"></div>


      <div className="relative z-10">


        {/* Header */}

        <div className="flex items-start justify-between gap-4">


          <div>

            <h2 className="text-2xl font-black text-white">

              {source}

            </h2>


            <p className="mt-2 text-sm text-gray-400">

              Global Job Source Monitoring

            </p>

          </div>


          {/* Status */}

          <div className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold ${
            status === "Active"
              ? "bg-green-400/10 text-green-300"
              : "bg-red-400/10 text-red-300"
          }`}>

            <CheckCircle2 size={16} />

            {status}

          </div>

        </div>


        {/* Metrics */}

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-5">


          {/* Jobs Fetched */}

          <div className="rounded-2xl border border-white/10 bg-black/20 p-5">

            <div className="flex items-center gap-3 text-cyan-300">

              <Database size={20} />

              <span className="text-sm font-medium">

                Jobs Fetched

              </span>

            </div>


            <h3 className="mt-4 text-3xl font-black text-white">

              {jobsFetched}

            </h3>

          </div>


          {/* Last Sync */}

          <div className="rounded-2xl border border-white/10 bg-black/20 p-5">

            <div className="flex items-center gap-3 text-yellow-300">

              <Clock3 size={20} />

              <span className="text-sm font-medium">

                Last Sync

              </span>

            </div>


            <h3 className="mt-4 text-lg font-bold text-white">

              {lastSync}

            </h3>

          </div>

        </div>


        {/* Bottom Info */}

        <div className="mt-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">


          <div className="flex items-center gap-3 text-gray-400">

            <Globe size={18} />

            <span>

              Monitoring Region: {region}

            </span>

          </div>


          <div className="inline-flex items-center gap-2 rounded-full bg-cyan-400/10 px-4 py-2 text-sm font-semibold text-cyan-300">

            Health Score: {health}

          </div>

        </div>

      </div>

    </motion.div>
  )
}

export default SourceStatusCard