import React from 'react';
import { Play, TrendingUp, Search, PenTool, BarChart3, ChevronDown } from 'lucide-react';
import { Button } from '../components/ui/button';
import { ParticleTextEffect } from '../components/ui/particle-text-effect';

export function HeroSection() {
  const scrollToDemo = () => {
    document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section id="home" className="relative min-h-screen flex flex-col items-center justify-center pt-20 pb-10 overflow-hidden">

      {/* Background radial gradient */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-indigo-500/20 blur-[150px] rounded-[100%] pointer-events-none z-0"></div>

      {/* Dot Grid Background Overlay */}
      <div className="absolute inset-0 bg-dot-pattern opacity-30 z-0 mask-image-gradient-b"></div>

      <div className="container relative z-10 px-4 flex flex-col items-center text-center mt-10">


        {/* Particle Canvas Area (Fixed Height) */}
        <div className="w-full h-[180px] md:h-[250px] mb-2 animate-fade-in" style={{ animationDelay: '200ms' }}>
          <ParticleTextEffect
            words={["BLOGY", "AI BLOGS", "SEO WINS", "RANK #1", "INDIA"]}
            particleColor1="#6366f1"
            particleColor2="#ec4899"
          />
        </div>

        {/* Main Typography */}
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold font-serif leading-tight mb-6 mt-4 animate-fade-up tracking-tight" style={{ animationDelay: '400ms' }}>
          India's Most Powerful <br />
          <span className="text-gradient">AI Blog Engine</span>
        </h1>

        <p className="text-lg md:text-xl text-gray-400 max-w-3xl mb-10 animate-fade-up leading-relaxed" style={{ animationDelay: '500ms' }}>
          From one keyword to a fully ranked, GEO-optimized, conversion-ready blog in under 60 seconds. Powered by Groq & LLaMA 3.3.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center gap-4 mb-16 animate-fade-up" style={{ animationDelay: '600ms' }}>
          <Button
            size="lg"
            className="bg-gradient-primary w-full sm:w-auto h-14 px-8 text-lg font-medium group"
            onClick={scrollToDemo}
          >
            Generate Your First Blog
            <PenTool className="w-5 h-5 ml-2 group-hover:rotate-12 transition-transform" />
          </Button>
          <Button
            size="lg"
            variant="glass-ghost"
            className="w-full sm:w-auto h-14 px-8 text-lg font-medium"
          >
            <Play className="w-5 h-5 mr-2 text-pink-400" />
            Watch Demo
          </Button>
        </div>

        {/* Floating Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8 w-full max-w-4xl mx-auto px-4 animate-fade-up" style={{ animationDelay: '800ms' }}>

          <div className="flex flex-col items-center justify-center p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl">
            <TrendingUp className="w-6 h-6 text-indigo-400 mb-2" />
            <span className="text-sm font-medium text-gray-300">7-Step Pipeline</span>
          </div>

          <div className="flex flex-col items-center justify-center p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl">
            <PenTool className="w-6 h-6 text-pink-400 mb-2" />
            <span className="text-sm font-medium text-gray-300">1,500-2,000 Words</span>
          </div>

          <div className="flex flex-col items-center justify-center p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl">
            <BarChart3 className="w-6 h-6 text-green-400 mb-2" />
            <span className="text-sm font-medium text-gray-300">Real SEO Scores</span>
          </div>

          <div className="flex flex-col items-center justify-center p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl">
            <Search className="w-6 h-6 text-cyan-400 mb-2" />
            <span className="text-sm font-medium text-gray-300">GEO Optimized</span>
          </div>

        </div>

      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 animate-bounce z-20">
        <Button variant="ghost" size="icon" className="rounded-full text-gray-400 hover:text-white" onClick={scrollToDemo}>
          <ChevronDown className="w-6 h-6" />
        </Button>
      </div>

    </section>
  );
}
