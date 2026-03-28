import React, { useEffect, useState, useRef } from 'react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { TrendingUp, Target, Zap } from 'lucide-react';
import { Card } from '../components/ui/card';

const AnimatedCounter = ({ end, duration = 2000, suffix = "", prefix = "" }: { end: number, duration?: number, suffix?: string, prefix?: string }) => {
  const [count, setCount] = useState(0);
  const nodeRef = useRef<HTMLSpanElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) setIsVisible(true);
      },
      { threshold: 0.1 }
    );
    if (nodeRef.current) observer.observe(nodeRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isVisible) return;
    let startTime: number | null = null;
    const step = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const easing = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      setCount(Math.floor(easing * end));
      if (progress < 1) window.requestAnimationFrame(step);
      else setCount(end);
    };
    window.requestAnimationFrame(step);
  }, [end, duration, isVisible]);

  return <span ref={nodeRef}>{prefix}{count}{suffix}</span>;
};

const chartData = [
  { step: '1. Keywords', score: 20 },
  { step: '2. SERP Gap', score: 45 },
  { step: '3. Outline', score: 60 },
  { step: '4. Content', score: 72 },
  { step: '5. Schema', score: 81 },
  { step: '6. CTA', score: 88 },
  { step: '7. Validation', score: 94 },
];

export function MetricsDashboard() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsMounted(true), 150);
    return () => clearTimeout(timer);
  }, []);

  return (
    <section id="dashboard" className="py-24 relative overflow-hidden bg-background">
      <div className="container mx-auto px-4 z-10 relative">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 font-serif">
            Real-Time <span className="text-gradient">SEO Intelligence</span>
          </h2>
          <p className="text-xl text-muted-foreground">Watch your content quality improve objectively across the pipeline.</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-16">
          {[
            { label: "Avg SEO Score", value: 94, suffix: "%", icon: <TrendingUp className="text-indigo-400" /> },
            { label: "Avg Word Count", value: 1847, suffix: "", icon: <AlignLeft className="text-pink-400" /> },
            { label: "Keyword Density", value: 4, suffix: ".2%", icon: <Target className="text-cyan-400" /> },
            { label: "Snippet Eligibility", value: 87, suffix: "%", icon: <Zap className="text-purple-400" /> }
          ].map((metric, i) => (
            <Card key={i} className="p-6 text-center border-white/5 bg-white/5 hover:bg-white/10 transition-colors animate-fade-up group" style={{ animationDelay: `${i * 100}ms` }}>
              <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                {metric.icon}
              </div>
              <h4 className="text-4xl font-bold text-white mb-2 font-serif tracking-tight">
                <AnimatedCounter end={metric.value} suffix={metric.suffix} />
              </h4>
              <p className="text-sm font-medium text-gray-400">{metric.label}</p>
            </Card>
          ))}
        </div>

        <Card className="p-6 md:p-8 border-white/10 bg-black/60 backdrop-blur-xl animate-fade-up relative">
          <div className="mb-6">
            <h3 className="text-2xl font-bold text-white font-serif">SEO Score Progression Over Pipeline Steps</h3>
            <p className="text-sm text-gray-400 mt-1">Simulated impact of each AI agent step on the final ranking probability.</p>
          </div>
          <div className="h-[400px] w-full min-h-[400px] relative overflow-hidden flex items-center justify-center">
            {isMounted ? (
              <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
                <AreaChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="step" stroke="rgba(255,255,255,0.2)" tick={{fill: 'rgba(255,255,255,0.5)', fontSize: 12}} tickMargin={10} />
                  <YAxis stroke="rgba(255,255,255,0.2)" tick={{fill: 'rgba(255,255,255,0.5)', fontSize: 12}} domain={[0, 100]} />
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(10,10,15,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }} itemStyle={{ color: '#6366f1', fontWeight: 'bold' }} />
                  <Area type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" activeDot={{ r: 8, fill: '#ec4899', stroke: '#fff', strokeWidth: 2 }} animationDuration={2000} />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
                <p className="text-sm text-gray-500">Preparing Analytics...</p>
              </div>
            )}
          </div>
        </Card>
      </div>
    </section>
  );
}

const AlignLeft = (props: any) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <line x1="21" x2="3" y1="6" y2="6"/><line x1="15" x2="3" y1="12" y2="12"/><line x1="17" x2="3" y1="18" y2="18"/>
  </svg>
);
