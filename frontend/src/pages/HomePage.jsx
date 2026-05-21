import Navbar from "../sections/Navbar";
import HeroSection from "../sections/HeroSection";
import AIShowcaseSection from "../sections/AIShowcaseSection";
import FeaturesSection from "../sections/FeaturesSection";
import WorkflowSection from "../sections/WorkflowSection";
import CTASection from "../sections/CTASection";
import Footer from "../sections/Footer";

function HomePage() {
  return (
    <div >
      <Navbar />
      <HeroSection />
      <AIShowcaseSection />
      <FeaturesSection />
      <WorkflowSection />
      <CTASection />
      <Footer />
    </div>
  );
}

export default HomePage;