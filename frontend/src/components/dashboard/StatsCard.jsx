import { motion } from "framer-motion"


function StatsCard({

  title,

  value,

  description,

  icon: Icon,

  gradient,
}) {

  return (

    <motion.div

      whileHover={{
        y: -6
      }}

      className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl"
    >


      {/* Glow */}

      <div className={`absolute inset-0 opacity-10 bg-gradient-to-br ${gradient}`}></div>


      <div className="relative z-10">


        {/* Icon */}

        <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${gradient} flex items-center justify-center shadow-2xl`}>

          <Icon
            size={30}
            className="text-black"
          />

        </div>


        {/* Value */}

        <h2 className="mt-8 text-5xl font-black text-white">

          {value}

        </h2>


        {/* Title */}

        <h3 className="mt-3 text-2xl font-bold text-white">

          {title}

        </h3>


        {/* Description */}

        <p className="mt-4 text-gray-400 leading-relaxed">

          {description}

        </p>

      </div>

    </motion.div>
  )
}

export default StatsCard