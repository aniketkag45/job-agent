import { motion } from "framer-motion"

import {

  Database,

  BellRing,

  Sparkles,

  Activity,

  Clock3

} from "lucide-react"


const activities = [

  {

    id: 1,

    title: "Fetched 284 new jobs from RemoteOK",

    time: "2 mins ago",

    icon: Database,

    iconBg: "bg-cyan-400/10",

    iconColor: "text-cyan-300"
  },

  {

    id: 2,

    title: "AI ranked 42 high-match opportunities",

    time: "5 mins ago",

    icon: Sparkles,

    iconBg: "bg-blue-400/10",

    iconColor: "text-blue-300"
  },

  {

    id: 3,

    title: "Telegram alerts sent successfully",

    time: "8 mins ago",

    icon: BellRing,

    iconBg: "bg-green-400/10",

    iconColor: "text-green-300"
  },

  {

    id: 4,

    title: "Pipeline synchronization completed",

    time: "12 mins ago",

    icon: Activity,

    iconBg: "bg-purple-400/10",

    iconColor: "text-purple-300"
  }
]


function ActivityFeed() {

  return (

    <motion.div

      initial={{
        opacity: 0,
        y: 20
      }}

      animate={{
        opacity: 1,
        y: 0
      }}

      transition={{
        duration: 0.6
      }}

      className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur-xl"
    >


      {/* Glow */}

      <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/5 to-blue-500/5"></div>


      <div className="relative z-10">


        {/* Header */}

        <div className="flex items-center justify-between gap-4">


          <div>

            <h2 className="text-3xl font-black text-white">

              Agent Activity Feed

            </h2>


            <p className="mt-2 text-gray-400">

              Real-time autonomous pipeline events and AI operations.

            </p>

          </div>


          <div className="hidden sm:flex items-center gap-2 rounded-full bg-green-400/10 px-4 py-2 text-sm font-semibold text-green-300">

            <div className="w-2.5 h-2.5 rounded-full bg-green-400 animate-pulse"></div>

            Live Monitoring

          </div>

        </div>


        {/* Activities */}

        <div className="mt-10 space-y-5">


          {activities.map((activity) => {

            const Icon = activity.icon

            return (

              <motion.div

                key={activity.id}

                whileHover={{
                  x: 4
                }}

                className="group flex items-start gap-5 rounded-2xl border border-white/10 bg-black/20 p-5 transition"
              >


                {/* Icon */}

                <div
                  className={`w-14 h-14 rounded-2xl flex items-center justify-center ${activity.iconBg}`}
                >

                  <Icon
                    size={24}
                    className={activity.iconColor}
                  />

                </div>


                {/* Content */}

                <div className="flex-1 min-w-0">


                  <h3 className="text-lg font-bold text-white leading-relaxed">

                    {activity.title}

                  </h3>


                  <div className="mt-3 flex items-center gap-2 text-sm text-gray-500">

                    <Clock3 size={16} />

                    {activity.time}

                  </div>

                </div>

              </motion.div>
            )
          })}

        </div>

      </div>

    </motion.div>
  )
}

export default ActivityFeed