import { motion } from "framer-motion"

import {

  Sparkles,

  Activity,

  Database,

  BellRing

} from "lucide-react"
import AnalyticsCard from "./AnalyticsCard"


function AgentHero() {

  return (

    <motion.div

      initial={{
        opacity: 0,
        y: 30
      }}

      animate={{
        opacity: 1,
        y: 0
      }}

      transition={{
        duration: 0.7
      }}

      className="relative overflow-hidden rounded-[32px] border border-white/10 bg-gradient-to-br from-[#111827] to-[#0B1120] p-6 sm:p-8 lg:p-10 shadow-2xl"
    >


      {/* Background Glow */}

      <div className="absolute inset-0 bg-gradient-to-r from-cyan-400/10 via-blue-500/10 to-purple-500/10"></div>


      {/* Floating Glow */}

      <div className="absolute -top-20 -right-20 w-72 h-72 bg-cyan-400/10 blur-3xl rounded-full"></div>

      <div className="absolute -bottom-20 -left-20 w-72 h-72 bg-blue-500/10 blur-3xl rounded-full"></div>


      <div className="relative z-10">


        {/* Top Badge */}

        <div className="inline-flex items-center gap-3 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-5 py-2 text-cyan-300 font-semibold">

          <Sparkles size={18} />

          AI Agent Active

        </div>


        {/* Main Heading */}

        <div className="mt-8 max-w-4xl">

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black leading-tight text-white">

            Autonomous AI Job Intelligence System

          </h1>


          <p className="mt-6 text-lg text-gray-400 leading-relaxed max-w-3xl">

            Continuously scraping, filtering, scoring, and monitoring global job opportunities in real-time to help you apply faster than everyone else.

          </p>

        </div>


        {/* Stats Grid */}

        <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 2xl:grid-cols-4 gap-6">


        <AnalyticsCard
            title="Jobs Scraped Today"
            value="1,284"
            icon={Database}
            iconBg="bg-cyan-400/10"
            iconColor="text-cyan-300"
            growth="+18%"
            subtitle="vs yesterday"
        />


        <AnalyticsCard
            title="Alerts Sent"
            value="326"
            icon={BellRing}
            iconBg="bg-green-400/10"
            iconColor="text-green-300"
            growth="+9%"
            subtitle="real-time notifications"
        />


        <AnalyticsCard
            title="Active Sources"
            value="1"
            icon={Activity}
            iconBg="bg-purple-400/10"
            iconColor="text-purple-300"
            growth="Stable"
            subtitle="RemoteOK monitoring"
        />


        <AnalyticsCard
            title="Avg Match Score"
            value="91%"
            icon={Sparkles}
            iconBg="bg-blue-400/10"
            iconColor="text-blue-300"
            growth="+4%"
            subtitle="AI relevance engine"
        />

        </div>


        {/* Bottom Status */}

        <div className="mt-10 flex flex-col sm:flex-row sm:flex-wrap sm:items-center gap-4 sm:gap-6 text-sm text-gray-400">


          <div className="flex items-center gap-2">

            <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>

            Pipeline Running

          </div>


          <div>

            Last Scrape: 2 minutes ago

          </div>


          <div>

            Monitoring: RemoteOK

          </div>


          <div>

            Notification Engine Active

          </div>

        </div>

      </div>

    </motion.div>
  )
}

export default AgentHero