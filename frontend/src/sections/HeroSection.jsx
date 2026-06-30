import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";

function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-cream">

      {/* Background Glow */}
      <div className="absolute top-[-250px] right-[-150px] w-[700px] h-[700px] rounded-full bg-accent-purple/5 blur-[140px]" />

      <div className="absolute bottom-[-250px] left-[-150px] w-[600px] h-[600px] rounded-full bg-accent-orange/5 blur-[140px]" />

      <div className="relative max-w-[1280px] mx-auto px-8 lg:px-16 pt-24 lg:pt-32 pb-20">

        <div className="grid lg:grid-cols-[1.1fr_.9fr] gap-16 xl:gap-24 items-center">

          {/* LEFT */}

          <div>

            <p className="text-xs font-medium tracking-[0.25em] uppercase text-accent-orange mb-8">
              AI-Powered Job Discovery
            </p>

            <h1 className="font-serif text-[56px] sm:text-[68px] xl:text-[72px] leading-[0.98] text-navy-light tracking-[-0.03em]">
              Jobs find{" "}
              <span className="italic text-accent-orange">
                you
              </span>
              ,
              <br />
              not the other
              <br />
              way around.
            </h1>

            <p className="mt-8 max-w-xl text-[18px] lg:text-[21px] leading-[1.9] text-body">
              Upload your resume once. Our AI continuously scans
              job boards, ATS systems and company career pages to
              surface only the opportunities that genuinely match
              your skills and experience.
            </p>

            <div className="mt-12 flex flex-wrap items-center gap-8">

              <Link
                to="/signup"
                className="inline-flex items-center gap-3 px-8 py-4 rounded-full bg-navy text-white hover:bg-navy-light transition-all duration-300 shadow-[0_10px_30px_rgba(0,0,0,.06)]"
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

            <p className="mt-12 text-body max-w-md leading-relaxed">
              Built for professionals who want to spend less time
              searching and more time applying.
            </p>

          </div>

          {/* RIGHT */}

          <div className="relative">

            {/* Main Showcase */}

            <div className="relative bg-white rounded-[28px] border border-border p-8 shadow-[0_25px_80px_rgba(0,0,0,.05)]">

              <div className="inline-flex items-center px-4 py-2 rounded-full bg-card-peach text-accent-orange text-sm font-medium">
                Live AI Discovery
              </div>

              <h3 className="mt-8 font-serif text-5xl text-navy-light leading-tight">
                Opportunities
                <br />
                curated for you.
              </h3>

              <p className="mt-5 text-body leading-relaxed">
                Intelligent matching across job boards,
                ATS platforms and company career pages.
              </p>

              {/* Elegant Divider */}

              <div className="my-10 h-px bg-border" />

              <div className="flex items-end justify-between">

  <div>
    <p className="text-sm text-body">
      New opportunities today
    </p>

    <p className="font-serif text-[56px] leading-none text-navy mt-2">
      87
    </p>
  </div>

  <div className="text-right">
    <p className="text-sm text-body">
      Powered by
    </p>

    <p className="font-serif text-3xl text-accent-purple mt-2">
      Semantic AI
    </p>
  </div>

</div>

            </div>

          

          </div>

        </div>

      </div>
    </section>
  );
}

export default HeroSection;

