function TrustedSection() {
  const logos = ["Stripe", "Discord", "RemoteOK", "Greenhouse"]

  return (
    <section className="bg-cream border-y border-border py-12">
      <div className="max-w-[1440px] mx-auto px-8 lg:px-16">
        <p className="text-xs font-medium text-body/60 uppercase tracking-[0.2em] text-center mb-8">
          Integrated With Leading Platforms
        </p>
        <div className="flex flex-wrap items-center justify-center gap-12">
          {logos.map((name, i) => (
            <span key={i} className="text-xl font-semibold text-body/40 hover:text-body/70 transition-colors cursor-default select-none">
              {name}
            </span>
          ))}
        </div>
      </div>
    </section>
  )
}

export default TrustedSection