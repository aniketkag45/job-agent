import {
  Upload,
  BrainCircuit,
  Search,
  BellRing,
} from "lucide-react";

const steps = [
  {
    number: "01",
    title: "Upload Your Resume",
    description:
      "Drop your resume once. Our AI extracts experience, skills, technologies and career preferences.",
    icon: Upload,
    color: "text-accent-orange",
  },
  {
    number: "02",
    title: "AI Understands Your Profile",
    description:
      "Semantic analysis builds a deeper understanding of your background beyond simple keywords.",
    icon: BrainCircuit,
    color: "text-accent-purple",
  },
  {
    number: "03",
    title: "Discover Relevant Opportunities",
    description:
      "Jobs are continuously matched from multiple sources including ATS platforms and career pages.",
    icon: Search,
    color: "text-[#3B82F6]",
  },
  {
    number: "04",
    title: "Apply Faster",
    description:
      "Receive alerts instantly and apply with AI-generated application support.",
    icon: BellRing,
    color: "text-accent-orange",
  },
];

function WorkflowSection() {
  return (
    <section className="bg-cream py-28 lg:py-36">

      <div className="max-w-[1000px] mx-auto px-8">

        {/* Heading */}

        <div className="text-center mb-24">

          <p className="text-xs uppercase tracking-[0.25em] text-accent-purple font-medium mb-8">
            How It Works
          </p>

          <h2 className="font-serif text-4xl lg:text-5xl text-navy-light leading-[1.08]">
            A simpler path
            <br />
            from resume
            <br />
            to opportunity.
          </h2>

        </div>

        {/* Timeline */}

        <div className="relative">

          {/* Vertical Line */}

          <div className="absolute left-[26px] top-0 bottom-0 w-px bg-border hidden md:block" />

          <div className="space-y-16">

            {steps.map((step) => (
              <div
                key={step.number}
                className="grid md:grid-cols-[80px_1fr] gap-10 items-start"
              >

                {/* Number */}

                <div className="relative">

                  <div className="w-[52px] h-[52px] rounded-full bg-white border border-border flex items-center justify-center text-sm font-medium text-navy z-10 relative">
                    {step.number}
                  </div>

                </div>

                {/* Content */}

                <div className="bg-white border border-border rounded-[24px] p-6 lg:p-7  border-navy/5 shadow-[0_8px_30px_rgba(0,0,0,.03)]">

                  <div className="flex items-center gap-4 mb-5">

                    <step.icon
                      size={22}
                      className={step.color}
                    />

                    <h3 className="text-xl font-semibold text-navy">
                      {step.title}
                    </h3>

                  </div>

                  <p className="text-body leading-[1.9] max-w-2xl">
                    {step.description}
                  </p>

                </div>

              </div>
            ))}

          </div>

        </div>

      </div>

    </section>
  );
}

export default WorkflowSection;

