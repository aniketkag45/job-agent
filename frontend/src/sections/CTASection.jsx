import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";

function CTASection() {
  return (
    <section className="bg-cream py-24 lg:py-32">

      <div className="max-w-[900px] mx-auto px-8 text-center">

        <p className="text-xs uppercase tracking-[0.25em] text-accent-orange font-medium mb-6">
          Start Today
        </p>

        <h2 className="font-serif text-4xl lg:text-5xl text-navy-light leading-[1.08]">
          Let opportunities
          come to you.
        </h2>

        <p className="mt-6 text-body leading-[1.9] max-w-xl mx-auto">
          Upload your resume once and let AI continuously discover
          relevant opportunities on your behalf.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-6">

          <Link
            to="/signup"
            className="inline-flex items-center gap-3 px-7 py-3.5 rounded-full bg-navy text-white hover:bg-navy-light transition-all duration-300"
          >
            Start Matching
            <ArrowRight size={18} />
          </Link>

          <Link
            to="/login"
            className="text-body hover:text-navy transition-colors duration-300"
          >
            Already have an account?
          </Link>

        </div>

      </div>

    </section>
  );
}

export default CTASection;

