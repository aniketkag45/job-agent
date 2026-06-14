import {useSearchParams,Link} from "react-router-dom";
import {CheckCircle2,XCircle,ArrowRight} from "lucide-react";

function VerifyEmailPage() {
    const [searchParams] = useSearchParams();
    const status = searchParams.get("status");
    const isSuccess = status === "success";
    
      return (
    <section className="min-h-screen bg-[#030712] flex items-center justify-center px-6">
      <div className="max-w-md w-full text-center">
        {/* Icon */}
        <div className={`w-20 h-20 rounded-full mx-auto mb-6 flex items-center justify-center ${
          isSuccess ? "bg-green-500/10" : "bg-red-500/10"
        }`}>
          {isSuccess ? (
            <CheckCircle2 className="text-green-400" size={40} />
          ) : (
            <XCircle className="text-red-400" size={40} />
          )}
        </div>

        {/* Message */}
        <h1 className="text-3xl font-black text-white mb-3">
          {isSuccess ? "Email Verified!" : "Verification Failed"}
        </h1>
        <p className="text-gray-400 text-lg mb-10">
          {isSuccess
            ? "Your email has been verified. You can now log in and start using the AI Job Agent."
            : "This verification link is invalid or has expired. Please sign up again or request a new verification email."}
        </p>

        {/* Action */}
        <Link
          to={isSuccess ? "/login" : "/signup"}
          className="inline-flex items-center gap-2 px-8 py-4 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-2xl transition"
        >
          {isSuccess ? "Go to Login" : "Sign Up Again"}
          <ArrowRight size={20} />
        </Link>
      </div>
    </section>
  )
}

export default VerifyEmailPage