import React, { useState } from 'react';
import { PromptInputBox } from '../components/ui/ai-prompt-box';
import { AgentPlan } from '../components/ui/agent-plan';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Card } from '../components/ui/card';
import { ScrollArea } from '../components/ui/scroll-area';
import { CheckCircle2, AlertCircle, RefreshCw, Loader2 } from 'lucide-react';
import { Button } from '../components/ui/button';

const API_BASE_URL = "http://localhost:8000/api";

export function DemoSection() {
  const [appState, setAppState] = useState<'idle' | 'generating' | 'complete'>('idle');
  const [blogData, setBlogData] = useState<{
    markdown: string;
    schema: string;
    report: any;
    meta: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [tasks, setTasks] = useState([
    { id: "1", title: "Keyword Cluster Research", status: "pending" as const },
    { id: "2", title: "SERP Gap Analysis", status: "pending" as const },
    { id: "3", title: "Blog Outline Generation", status: "pending" as const },
    { id: "4", title: "Full Blog Writing", status: "pending" as const },
    { id: "5", title: "FAQ + JSON-LD Schema", status: "pending" as const },
    { id: "6", title: "CTA Section", status: "pending" as const },
    { id: "7", title: "SEO Validation Report", status: "pending" as const }
  ]);

  const updateTaskStatus = (id: string, status: 'pending' | 'in-progress' | 'completed') => {
    setTasks(prev => prev.map(t => t.id === id ? { ...t, status } : t));
  };

  const handleGenerate = async (keyword: string, config: any) => {
    setAppState('generating');
    setError(null);
    setTasks(prev => prev.map(t => ({ ...t, status: 'pending' })));
    
    try {
      const payload = { 
        keyword: keyword || "", 
        location: config?.location || "India", 
        tone: config?.tone || "Professional",
        model: config?.model || "llama-3.3-70b-versatile"
      };

      const callStep = async (stepId: string, endpoint: string, bodyObj: any) => {
        updateTaskStatus(stepId, "in-progress");
        const res = await fetch(`${API_BASE_URL}/${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(bodyObj)
        });
        if (!res.ok) {
           const errJson = await res.json().catch(() => ({ detail: res.statusText }));
           throw new Error(errJson.detail || res.statusText);
        }
        const data = await res.json();
        updateTaskStatus(stepId, "completed");
        return data;
      };

      const clusterData = await callStep("1", "keyword-cluster", payload);
      const serpData = await callStep("2", "serp-gap", payload);
      const outlineData = await callStep("3", "outline", { ...payload, cluster: clusterData?.result || "", serp: serpData?.result || "" });
      const blogBodyData = await callStep("4", "full-blog", { ...payload, outline: outlineData?.result || "", cluster: clusterData?.result || "" });
      const faqData = await callStep("5", "faq", { ...payload, title: keyword });
      const ctaData = await callStep("6", "cta", payload);
      const finalContent = `${blogBodyData?.result || ""}\n\n${faqData?.result || ""}\n\n${ctaData?.result || ""}`;
      const reportData = await callStep("7", "seo-report", { ...payload, blog_text: finalContent, cluster: clusterData?.result || "" });

      let extractedSchema = "{}";
      const rawFaq = faqData?.result || "";
      if (typeof rawFaq === 'string' && rawFaq.includes("```json")) {
         try {
           const parts = rawFaq.split("```json")[1].split("```");
           if (parts.length > 0) extractedSchema = parts[0].trim();
         } catch (e) {
           console.error("Schema extraction failed", e);
         }
      }

      setBlogData({
        markdown: finalContent,
        schema: extractedSchema,
        report: reportData,
        meta: "SEO Optimized"
      });
      setAppState('complete');
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Something went wrong.");
      setAppState('idle');
    }
  };

  return (
    <section id="demo" className="py-24 relative overflow-hidden bg-background">
      <div className="container mx-auto px-4 z-10 relative">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-6 font-serif tracking-tight">Try It <span className="text-gradient">Live</span></h2>
          <p className="text-muted-foreground">The Groq-powered AI pipeline is fully integrated and ready for the hackathon.</p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start max-w-7xl mx-auto">
          <div className="lg:col-span-4 flex flex-col gap-6">
            {appState === 'idle' ? <PromptInputBox onGenerate={handleGenerate} isLoading={false} /> : <AgentPlan tasks={tasks} />}
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500 text-sm flex items-start gap-3">
                <AlertCircle className="w-5 h-5 shrink-0" />
                <p className="font-medium">{error}</p>
              </div>
            )}
            {appState === 'complete' && (
               <Button variant="outline" className="w-full mt-2 border-white/10 text-white" onClick={() => setAppState('idle')}>
                 <RefreshCw className="w-4 h-4 mr-2" /> Start New Generation
               </Button>
            )}
          </div>
          <div className="lg:col-span-8 w-full h-[700px]">
            {appState === 'idle' ? (
              <div className="w-full h-full rounded-2xl border border-white/10 bg-card/30 backdrop-blur-md flex flex-col items-center justify-center p-8 text-center border-dashed">
                <h3 className="text-xl font-semibold text-white/50 mb-2">Awaiting Instructions</h3>
              </div>
            ) : appState === 'generating' ? (
              <div className="w-full h-full rounded-2xl border border-white/10 bg-card/30 backdrop-blur-md flex flex-col items-center justify-center p-8 text-center">
                <Loader2 className="w-12 h-12 text-indigo-500 animate-spin mb-4" />
                <h3 className="text-2xl font-semibold text-white mb-4 animate-pulse">Groq-70B Pipeline Active</h3>
              </div>
            ) : (
              blogData && (
                <Card className="w-full h-full flex flex-col overflow-hidden animate-fade-in bg-card/90">
                  <Tabs defaultValue="blog" className="w-full h-full flex flex-col">
                    <div className="px-6 border-b border-white/10 bg-black/40 pt-4">
                      <TabsList className="bg-transparent border-0 mb-[-1px] space-x-2">
                        <TabsTrigger value="blog">Blog</TabsTrigger>
                        <TabsTrigger value="seo">SEO Audit</TabsTrigger>
                        <TabsTrigger value="schema">JSON-LD</TabsTrigger>
                      </TabsList>
                    </div>
                    <div className="flex-1 overflow-hidden">
                      <TabsContent value="blog" className="h-full m-0 p-0 outline-none">
                        <ScrollArea className="h-full w-full">
                          <div className="p-8 prose prose-invert prose-indigo max-w-none" dangerouslySetInnerHTML={{ 
                              __html: (blogData.markdown || "")
                                .replace(/# (.*)/g, '<h1 class="text-3xl font-bold font-serif text-gradient mb-6 pb-4 border-b border-white/10">$1</h1>')
                                .replace(/## (.*)/g, '<h2 class="text-2xl font-semibold mt-8 mb-4 text-indigo-300 font-serif">$1</h2>')
                                .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-pink-400/90 font-semibold">$1</strong>')
                                .replace(/\n\n/g, '<br/><br/>')
                            }} />
                        </ScrollArea>
                      </TabsContent>
                      <TabsContent value="seo" className="h-full m-0 p-6">
                        <div className="flex flex-col gap-6">
                           <div className="p-6 bg-green-500/10 rounded-2xl border border-green-500/20 flex justify-between items-center">
                               <h3 className="text-2xl font-bold text-white">Score: {blogData.report?.score || 0}/100</h3>
                               <CheckCircle2 className="w-12 h-12 text-green-500" />
                           </div>
                           <div className="grid grid-cols-2 gap-4">
                               <div className="p-4 bg-white/5 rounded-xl border border-white/10">
                                   <p className="text-gray-400 text-xs mb-1 uppercase tracking-wider">Words</p>
                                   <p className="text-xl font-bold text-white">{blogData.report?.word_count || 0}</p>
                               </div>
                               <div className="p-4 bg-white/5 rounded-xl border border-white/10">
                                   <p className="text-gray-400 text-xs mb-1 uppercase tracking-wider">Density</p>
                                   <p className="text-xl font-bold text-white">{blogData.report?.density || 0}%</p>
                               </div>
                           </div>
                           <div className="space-y-3">
                               <h4 className="text-sm font-semibold text-white/50 uppercase tracking-widest">Suggestions</h4>
                               {blogData.report?.suggestions?.map((s: string, i: number) => (
                                 <div key={i} className="flex gap-2 items-start text-sm text-indigo-300/80">
                                   <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                                   <p>{s}</p>
                                 </div>
                               ))}
                           </div>
                        </div>
                      </TabsContent>
                      <TabsContent value="schema" className="h-full m-0 p-6">
                         <ScrollArea className="h-full w-full">
                            <pre className="bg-black/50 p-6 rounded-xl border border-white/10 font-mono text-xs text-pink-300 overflow-x-auto">{blogData.schema || "{}"}</pre>
                         </ScrollArea>
                      </TabsContent>
                    </div>
                  </Tabs>
                </Card>
              )
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
