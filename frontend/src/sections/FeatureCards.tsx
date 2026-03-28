import React from 'react';
import { Target, Zap, LayoutTemplate, Activity, Link as LinkIcon, Layers } from 'lucide-react';
import { Card } from '../components/ui/card';

const features = [
  {
    icon: <Target className="w-6 h-6 text-indigo-400" />,
    title: "GEO-Optimized Content",
    description: "India-specific signals, local statistics, and regional context built natively into the generated content.",
    bgClass: "bg-indigo-500/10"
  },
  {
    icon: <Zap className="w-6 h-6 text-pink-400" />,
    title: "Groq-Powered Speed",
    description: "Generate comprehensive 2,000-word blogs in under 60 seconds leveraging LLaMA 3.3 inferencing.",
    bgClass: "bg-pink-500/10"
  },
  {
    icon: <LayoutTemplate className="w-6 h-6 text-cyan-400" />,
    title: "SERP Gap Intelligence",
    description: "Simulates competitor H2 structures to identify what top-ranking posts miss, filling critical content gaps.",
    bgClass: "bg-cyan-500/10"
  },
  {
    icon: <Activity className="w-6 h-6 text-green-400" />,
    title: "Live SEO Scoring",
    description: "Keyword density, naturalness score, and snippet readiness—computed and validated instantly.",
    bgClass: "bg-green-500/10"
  },
  {
    icon: <LinkIcon className="w-6 h-6 text-purple-400" />,
    title: "FAQ + Schema Markup",
    description: "Auto-generates JSON-LD FAQ schema precisely formatted for Google's 'People Also Ask' box.",
    bgClass: "bg-purple-500/10"
  },
  {
    icon: <Layers className="w-6 h-6 text-yellow-400" />,
    title: "Scalable Pipeline",
    description: "One keyword produces a full blog. Repeat for 1,000 keywords with identical logic and uncompromised quality.",
    bgClass: "bg-yellow-500/10"
  }
];

export function FeatureCards() {
  return (
    <section id="features" className="py-24 relative overflow-hidden bg-background">
      <div className="container mx-auto px-4 z-10 relative">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 font-serif">
            Built for Ranking. <span className="text-gradient">Built for India.</span>
          </h2>
          <p className="text-xl text-muted-foreground w-full max-w-2xl mx-auto">
            Our architecture is specifically tuned to generate content that fulfills search intent and outranks generic alternatives.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="p-8 border-white/5 bg-white/5 hover:bg-card/80 transition-all duration-300 animate-fade-up group overflow-hidden relative"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Subtle hover gradient background */}
              <div className={`absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-500 ${feature.bgClass}`}></div>
              
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 border border-white/5 relative z-10 transition-transform group-hover:-translate-y-1 ${feature.bgClass}`}>
                {feature.icon}
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 font-serif relative z-10">
                {feature.title}
              </h3>
              
              <p className="text-gray-400 leading-relaxed relative z-10">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
