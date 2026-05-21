import { useState } from "react"

import { motion } from "framer-motion"

import { Link } from "react-router-dom"

import {

  Sparkles,

  User,

  Mail,

  Lock,

  ArrowRight,

  EyeOff,

  Eye,

  Loader2

} from "lucide-react"

import api from "../api/axios"

import toast from "react-hot-toast"


function SignupPage() {

  const [formData, setFormData] = useState({

    username: "",

    email: "",

    password: "",
  })

  const [loading, setLoading] = useState(false)

  const [showPassword, setShowPassword] = useState(false)

  const [errors, setErrors] = useState({})


  const handleChange = (e) => {

    setFormData({

      ...formData,

      [e.target.name]: e.target.value,
    })
  }


  const validateForm = () => {

    let newErrors = {}


    if (!formData.username.trim()) {

      newErrors.username = "Username is required"

    } else if (formData.username.length < 3) {

      newErrors.username =
        "Username must be at least 3 characters"
    }


    if (!formData.email.trim()) {

      newErrors.email = "Email is required"

    } else if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)
    ) {

      newErrors.email =
        "Enter a valid email address"
    }


    if (!formData.password) {

      newErrors.password = "Password is required"

    } else if (formData.password.length < 6) {

      newErrors.password =
        "Password must be at least 6 characters"
    }


    setErrors(newErrors)

    return Object.keys(newErrors).length === 0
  }


  const handleSubmit = async (e) => {

    e.preventDefault()

    if (!validateForm()) return

    setLoading(true)

    try {

      const response =
      await api.post("/signup", formData)

      console.log(response.data)

      toast.success(
        "Signup successful. Verify your email."
      )

    } catch (error) {

      console.error(error)

      toast.error("Signup failed")

    } finally {

      setLoading(false)
    }
  }


  return (

    <section className="relative min-h-screen overflow-hidden bg-[#030712] text-white flex items-center justify-center px-6 py-20">


      <div className="absolute top-[-150px] left-[-100px] w-[400px] h-[400px] bg-blue-500/20 blur-3xl rounded-full"></div>

      <div className="absolute bottom-[-150px] right-[-100px] w-[400px] h-[400px] bg-cyan-400/10 blur-3xl rounded-full"></div>


      <div className="relative z-10 max-w-7xl w-full grid lg:grid-cols-2 rounded-[40px] overflow-hidden border border-white/10 bg-white/5 backdrop-blur-xl shadow-2xl">


        {/* LEFT */}

        <div className="relative p-12 lg:p-16 flex flex-col justify-center bg-gradient-to-br from-blue-500/10 to-cyan-400/5 border-r border-white/10">


          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 text-cyan-300 w-fit mb-10">

            <Sparkles size={18} />

            AI Career Platform

          </div>


          <h1 className="text-5xl lg:text-6xl font-black leading-tight">

            Start Your

            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">

              AI Career Journey

            </span>

          </h1>


          <p className="mt-8 text-xl text-gray-300 leading-relaxed">

            Join a next-generation AI-powered platform designed to automate job discovery,
            optimize applications, and accelerate career growth.

          </p>

        </div>


        {/* RIGHT */}

        <motion.div

          initial={{
            opacity: 0,
            x: 50
          }}

          animate={{
            opacity: 1,
            x: 0
          }}

          transition={{
            duration: 0.7
          }}

          className="p-10 lg:p-16 flex items-center"
        >

          <div className="w-full">


            <h2 className="text-4xl font-black mb-3">

              Create Account

            </h2>


            <p className="text-gray-400 mb-10">

              Enter your details to start exploring AI-powered opportunities.

            </p>


            <form
              onSubmit={handleSubmit}
              className="space-y-6"
            >


              {/* Username */}

              <div>

                <label className="text-sm text-gray-300 mb-2 block">

                  Username

                </label>


                <div className={`flex items-center gap-3 border rounded-2xl px-5 py-4 bg-white/5 transition ${
                  errors.username
                    ? "border-red-500"
                    : "border-white/10 focus-within:border-cyan-400"
                }`}>

                  <User
                    size={20}
                    className="text-cyan-300"
                  />

                  <input
                    type="text"
                    name="username"
                    placeholder="Enter username"
                    onChange={handleChange}
                    className="bg-transparent outline-none w-full text-white placeholder:text-gray-500"
                  />

                </div>


                {errors.username && (

                  <p className="text-red-400 text-sm mt-2">

                    {errors.username}

                  </p>
                )}

              </div>


              {/* Email */}

              <div>

                <label className="text-sm text-gray-300 mb-2 block">

                  Email

                </label>


                <div className={`flex items-center gap-3 border rounded-2xl px-5 py-4 bg-white/5 transition ${
                  errors.email
                    ? "border-red-500"
                    : "border-white/10 focus-within:border-cyan-400"
                }`}>

                  <Mail
                    size={20}
                    className="text-cyan-300"
                  />

                  <input
                    type="email"
                    name="email"
                    placeholder="Enter email"
                    onChange={handleChange}
                    className="bg-transparent outline-none w-full text-white placeholder:text-gray-500"
                  />

                </div>


                {errors.email && (

                  <p className="text-red-400 text-sm mt-2">

                    {errors.email}

                  </p>
                )}

              </div>


              {/* Password */}

              <div>

                <label className="text-sm text-gray-300 mb-2 block">

                  Password

                </label>


                <div className={`flex items-center gap-3 border rounded-2xl px-5 py-4 bg-white/5 transition ${
                  errors.password
                    ? "border-red-500"
                    : "border-white/10 focus-within:border-cyan-400"
                }`}>

                  <Lock
                    size={20}
                    className="text-cyan-300"
                  />

                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    placeholder="Enter password"
                    onChange={handleChange}
                    className="bg-transparent outline-none w-full text-white placeholder:text-gray-500"
                  />


                  <button
                    type="button"
                    onClick={() =>
                      setShowPassword(!showPassword)
                    }
                    className="text-gray-400 hover:text-cyan-300 transition"
                  >

                    {showPassword ? (

                      <EyeOff size={20} />

                    ) : (

                      <Eye size={20} />

                    )}

                  </button>

                </div>


                {errors.password && (

                  <p className="text-red-400 text-sm mt-2">

                    {errors.password}

                  </p>
                )}

              </div>


              {/* Button */}

              <button
                type="submit"
                disabled={loading}
                className="group w-full mt-4 bg-gradient-to-r from-blue-500 to-cyan-400 text-black font-black py-4 rounded-2xl shadow-2xl hover:scale-[1.02] transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >

                {loading ? (

                  <>

                    <Loader2
                      size={20}
                      className="animate-spin"
                    />

                    Creating Account...

                  </>

                ) : (

                  <>

                    Create Account

                    <ArrowRight
                      size={20}
                      className="group-hover:translate-x-1 transition"
                    />

                  </>
                )}

              </button>

            </form>


            <p className="mt-8 text-center text-gray-400">

              Already have an account?

              <Link
                to="/login"
                className="text-cyan-300 hover:text-cyan-200 ml-2"
              >

                Login

              </Link>

            </p>

          </div>

        </motion.div>

      </div>

    </section>
  )
}

export default SignupPage