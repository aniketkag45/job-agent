import HeroSection from "../sections/HeroSection";
// import AIShowcaseSection from "../sections/AIShowcaseSection";
import TrustedSection from "../sections/TrustedSection";
import FeaturesSection from "../sections/FeaturesSection";
import WorkflowSection from "../sections/WorkflowSection";
import CTASection from "../sections/CTASection";
import Footer from "../sections/Footer";

function HomePage() {
  return (
    <div >
      <HeroSection />
      {/* <AIShowcaseSection /> */}
      <TrustedSection />
      <FeaturesSection />
      <WorkflowSection />
      <CTASection />
      <Footer />
    </div>
  );
}

export default HomePage;