import { Navbar } from "./components/ui/navbar";
import { HeroSection } from "./sections/HeroSection";
import { PipelineSection } from "./sections/PipelineSection";
import { DemoSection } from "./sections/DemoSection";
import { MetricsDashboard } from "./sections/MetricsDashboard";
import { FeatureCards } from "./sections/FeatureCards";
import { BlogPreviews } from "./sections/BlogPreviews";
import { Footer } from "./sections/Footer";

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans antialiased selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar />
      
      <main>
        <HeroSection />
        <FeatureCards />
        <PipelineSection />
        <DemoSection />
        <MetricsDashboard />
        <BlogPreviews />
      </main>

      <Footer />
    </div>
  );
}

export default App;
