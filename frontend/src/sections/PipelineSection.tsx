import React, { useEffect, useRef } from 'react';
import { Search, Map, AlignLeft, PenBox, HelpCircle, Megaphone, CheckCircle } from 'lucide-react';

const steps = [
  {
    icon: <Search className="w-6 h-6 text-indigo-400" />,
    title: "Keyword Cluster",
    description: "6-8 LSI & long-tail keywords extracted from your seed keyword"
  },
  {
    icon: <Map className="w-6 h-6 text-pink-400" />,
    title: "SERP Gap Analysis",
    description: "We simulate competitor H2 structures and find the content gaps they miss"
  },
  {
    icon: <AlignLeft className="w-6 h-6 text-cyan-400" />,
    title: "Blog Outline",
    description: "SEO title (≤65 chars), meta description (≤155 chars), 7 structured H2 headings"
  },
  {
    icon: <PenBox className="w-6 h-6 text-purple-400" />,
    title: "Full Blog Post",
    description: "1,500-2,000 word GEO-optimized post with featured snippet paragraph"
  },
  {
    icon: <HelpCircle className="w-6 h-6 text-green-400" />,
    title: "FAQ + JSON-LD",
    description: "5 Q&A pairs + Schema markup for Google's People Also Ask"
  },
  {
    icon: <Megaphone className="w-6 h-6 text-yellow-400" />,
    title: "CTA Section",
    description: "Conversion-focused closing powered by Blogy's copywriting engine"
  },
  {
    icon: <CheckCircle className="w-6 h-6 text-indigo-400" />,
    title: "SEO Validation",
    description: "Live score card: keyword density, snippet readiness, naturalness score, GEO signal"
  }
];

export function PipelineSection() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('opacity-100', 'translate-y-0', 'scale-100');
            entry.target.classList.remove('opacity-0', 'translate-y-8', 'scale-95');
            // Check if it's the line
            if (entry.target.classList.contains('draw-line')) {
               entry.target.classList.add('h-full');
               entry.target.classList.remove('h-0');
            }
          }
        });
      },
      { threshold: 0.2, rootMargin: '0px 0px -100px 0px' }
    );

    const elements = containerRef.current?.querySelectorAll('.animate-on-scroll');
    elements?.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  return (
    <section id="pipeline" className="py-24 relative overflow-hidden bg-black/40">
      <div className="container mx-auto px-4" ref={containerRef}>
        
        <div className="text-center mb-20 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700 ease-out">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 font-serif">
            How Blogy <span className="text-gradient">Works</span>
          </h2>
          <p className="text-xl text-muted-foreground w-full max-w-2xl mx-auto">
            A repeatable, stress-tested 7-step SEO pipeline.
          </p>
        </div>

        <div className="relative max-w-4xl mx-auto">
          {/* Central Line */}
          <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-[2px] bg-white/10 -translate-x-1/2">
            <div className="w-full bg-gradient-to-b from-indigo-500 via-pink-500 to-indigo-500 transition-all duration-1000 ease-out animate-on-scroll draw-line h-0 origin-top"></div>
          </div>

          <div className="space-y-12 relative px-2">
            {steps.map((step, index) => {
              const isEven = index % 2 === 0;
              
              return (
                <div 
                  key={index}
                  className={`flex flex-col md:flex-row items-start md:items-center relative animate-on-scroll opacity-0 scale-95 transition-all duration-700 ease-out
                    ${isEven ? 'md:flex-row-reverse' : ''}`}
                  style={{ transitionDelay: `${index * 150}ms` }}
                >
                  
                  {/* Timeline Badge/Dot */}
                  <div className="absolute left-4 md:left-1/2 w-10 h-10 rounded-full bg-background border-4 border-[#1F2023] shadow-lg flex items-center justify-center -translate-x-1/2 z-10 shrink-0">
                    <div className="w-full h-full rounded-full bg-gradient-primary flex items-center justify-center text-white font-bold text-sm">
                      {index + 1}
                    </div>
                  </div>

                  {/* Content Box */}
                  <div className={`w-full md:w-1/2 pl-12 md:p-0 ${isEven ? 'md:pr-16 text-left md:text-right' : 'md:pl-16 text-left'}`}>
                    <div className={`glass-panel p-6 relative group transition-all duration-300 hover:scale-105
                      ${isEven ? 'hover:shadow-pink-500/20' : 'hover:shadow-indigo-500/20'}`}>
                      
                      <div className={`w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-4
                        ${isEven ? 'md:ml-auto' : ''}`}>
                        {step.icon}
                      </div>
                      
                      <h3 className="text-xl font-bold text-white mb-2 font-serif group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-indigo-400 group-hover:to-pink-400 transition-all">
                        {step.title}
                      </h3>
                      
                      <p className="text-gray-400 leading-relaxed text-sm">
                        {step.description}
                      </p>

                    </div>
                  </div>

                </div>
              );
            })}
          </div>
        </div>
        
      </div>
    </section>
  );
}
