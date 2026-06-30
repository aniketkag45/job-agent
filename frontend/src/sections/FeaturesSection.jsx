import {
  BrainCircuit,
  BellRing,
  FileCheck,
  Search,
} from "lucide-react";

const features = [
  {
    icon: BrainCircuit,
    title: "Semantic Matching",
    description:
      "Our AI understands skills, experience and career intent instead of relying on simple keyword matching.",
    bg: "bg-card-lavender",
    accent: "text-accent-purple",
  },
  {
    icon: BellRing,
    title: "Instant Alerts",
    description:
      "Get notified the moment relevant opportunities appear so you can apply before everyone else.",
    bg: "bg-card-peach",
    accent: "text-accent-orange",
  },
  {
    icon: FileCheck,
    title: "AI Applications",
    description:
      "Generate tailored application content and cover letters in seconds.",
    bg: "bg-card-blue",
    accent: "text-[#3B82F6]",
  },
  {
    icon: Search,
    title: "Career Discovery",
    description:
      "Surface opportunities you would never discover through manual searching.",
    bg: "bg-card-peach",
    accent: "text-accent-orange",
  },
];

function FeaturesSection() {
  return (
    <section className="relative bg-[#FAF8F6] py-24 lg:py-32 overflow-hidden">

      <div className="absolute top-0 right-0 w-[500px] h-[500px] rounded-full bg-accent-purple/5 blur-[140px]" />

      <div className="max-w-[1280px] mx-auto px-8 lg:px-16">

        {/* Heading */}

        <div className="text-center max-w-3xl mx-auto mb-24">

          <p className="text-xs uppercase tracking-[0.25em] text-accent-orange font-medium mb-6">
            Why JobAgent
          </p>

          <h2 className="font-serif text-4xl lg:text-5xl text-navy-light leading-[1.08]">
            Built to make job searching
            feel effortless.
          </h2>

          <p className="mt-6 text-body leading-relaxed">
            Every feature is designed to reduce noise,
            save time and help you focus on the opportunities
            that actually matter.
          </p>

        </div>

        {/* Alternating Features */}

        <div className="space-y-10">

          {features.map((feature, index) => {

            const reverse = index % 2 !== 0;

            return (
              <div
                key={index}
                className={`grid lg:grid-cols-2 gap-8 items-center ${
                  reverse ? "lg:[&>*:first-child]:order-2" : ""
                }`}
              >

                {/* Visual Card */}

                <div
                  className={`${feature.bg}
                  rounded-[24px]
                  border border-navy/5
                  shadow-[0_8px_30px_rgba(0,0,0,.03)]
                  p-8 lg:p-10`}
                >

                  <div className="w-12 h-12 rounded-2xl bg-white flex items-center justify-center mb-8">

                    <feature.icon
                      size={20}
                      className={feature.accent}
                    />

                  </div>

                  <div className="h-[160px] flex items-center justify-center">

                    <p className={`font-serif text-5xl ${feature.accent}`}>
                      0{index + 1}
                    </p>

                  </div>

                </div>

                {/* Content */}

                <div className="max-w-lg">

                  <h3 className="font-serif text-3xl text-navy-light">
                    {feature.title}
                  </h3>

                  <p className="mt-5 text-body leading-[1.9]">
                    {feature.description}
                  </p>

                </div>

              </div>
            );
          })}

        </div>

      </div>

    </section>
  );
}

export default FeaturesSection;

