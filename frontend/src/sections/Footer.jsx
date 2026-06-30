import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="bg-[#FAF8F6] border-t border-border">

      <div className="max-w-[1280px] mx-auto px-8 lg:px-16 py-16">

        <div className="grid md:grid-cols-4 gap-10">

          <div className="md:col-span-2">

            <h3 className="font-serif text-2xl text-navy-light">
              JobAgent
            </h3>

            <p className="mt-4 text-body max-w-md leading-relaxed">
              AI-powered job discovery built for professionals
              who value their time.
            </p>

          </div>

          <div>

            <p className="text-xs uppercase tracking-[0.2em] text-body mb-5">
              Product
            </p>

            <div className="space-y-3">

              <Link
                to="/dashboard"
                className="block text-body hover:text-navy"
              >
                Dashboard
              </Link>

              <Link
                to="/jobs"
                className="block text-body hover:text-navy"
              >
                Jobs
              </Link>

              <Link
                to="/profile"
                className="block text-body hover:text-navy"
              >
                Profile
              </Link>

            </div>

          </div>

          <div>

            <p className="text-xs uppercase tracking-[0.2em] text-body mb-5">
              Account
            </p>

            <div className="space-y-3">

              <Link
                to="/signup"
                className="block text-body hover:text-navy"
              >
                Sign Up
              </Link>

              <Link
                to="/login"
                className="block text-body hover:text-navy"
              >
                Login
              </Link>

            </div>

          </div>

        </div>

        <div className="mt-12 pt-6 border-t border-border flex flex-col sm:flex-row justify-between gap-4">

          <p className="text-sm text-body">
            © 2026 JobAgent
          </p>

          <p className="text-sm text-body">
            Built with AI • India
          </p>

        </div>

      </div>

    </footer>
  );
}

export default Footer;

