import { motion } from "framer-motion"


function AnalyticsCard({

  title,

  value,

  icon: Icon,

  iconBg,

  iconColor,

  growth,

  subtitle
}) {

  return (

    <motion.div

      whileHover={{
        y: -6,
        scale: 1.02
      }}

      transition={{
        duration: 0.25
      }}

      className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl shadow-2xl"
    >


      {/* Hover Glow */}

      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 bg-gradient-to-br from-cyan-400/5 to-blue-500/5"></div>


      <div className="relative z-10">


        {/* Top */}

        <div className="flex items-start justify-between gap-4">


          <div>

            <p className="text-sm text-gray-400">

              {title}

            </p>


            <h2 className="mt-4 text-4xl font-black text-white">

              {value}

            </h2>

          </div>


          {/* Icon */}

          <div
            className={`w-16 h-16 rounded-2xl flex items-center justify-center ${iconBg}`}
          >

            <Icon
              size={28}
              className={iconColor}
            />

          </div>

        </div>


        {/* Bottom */}

        <div className="mt-6 flex items-center justify-between">


          {growth && (

            <div className="inline-flex items-center gap-2 rounded-full bg-green-400/10 px-3 py-1 text-sm font-semibold text-green-300">

              {growth}

            </div>

          )}


          {subtitle && (

            <p className="text-sm text-gray-500">

              {subtitle}

            </p>

          )}

        </div>

      </div>

    </motion.div>
  )
}

export default AnalyticsCard