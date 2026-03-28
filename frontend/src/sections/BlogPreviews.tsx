import { ExternalLink, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ScrollArea } from '../components/ui/scroll-area';
import { Button } from '../components/ui/button';

const blogExamples = [
  {
    title: "Blogy – Best AI Blog Automation Tool in India",
    score: 91,
    platforms: "Medium • LinkedIn • WordPress",
    content: `# Blogy – Best AI Blog Automation Tool in India

If you're tired of spending 4+ hours researching keywords, finding H2 gaps, and trying to write content that actually ranks on Google India, you're not alone. The digital marketing landscape here is crowded, and generic AI tools just don't cut it anymore.

Enter **Blogy**, an SEO automation powerhouse that takes a single keyword and turns it into a fully optimized, 2,000-word blog post in under 60 seconds.

## Why Indian Marketers Need Specialized Tools
Most generative AI lacks the regional context needed for the Indian market. Local pricing, tier-specific audience understanding, and proper semantic SEO structures are crucial. 

With Blogy's pipeline, you aren't just generating text; you are generating an SEO asset designed specifically to capture organic traffic...`
  },
  {
    title: "How Blogy is Disrupting Martech – Organic Traffic on Autopilot",
    score: 94,
    platforms: "Substack • Dev.to • Blogger",
    content: `# How Blogy is Disrupting Martech – Organic Traffic on Autopilot

The traditional content marketing playbook is broken. Paying agencies exorbitant fees for 4 blogs a month is no longer a viable strategy for startups looking to scale rapidly. The new strategy? AI-driven SEO automation.

## The 7-Step Pipeline Advantage
What makes Blogy different isn't the AI model itself—it's the automated rigor applied *before* and *after* the generation step.

1. **Keyword Clustering:** Finding the exact LSI terms your competitors rank for.
2. **SERP Gap Analysis:** Extracting H2 structures from the top 5 ranking pages on Google India.
3. **Structured Outlines:** Ensuring the semantic flow tells a complete story.

By mechanizing these steps, Blogy guarantees a baseline of quality that most human writers struggle to maintain consistently...`
  }
];

export function BlogPreviews() {
  return (
    <section id="examples" className="py-24 relative overflow-hidden bg-black/40">
      <div className="container mx-auto px-4 z-10 relative">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 font-serif">
            Blogs That <span className="text-gradient">Rank</span>
          </h2>
          <p className="text-xl text-muted-foreground w-full max-w-2xl mx-auto">
            Examples of long-form, optimized content generated entirely by the pipeline.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {blogExamples.map((blog, index) => (
            <Card 
              key={index} 
              className="group overflow-hidden border-white/10 bg-card/60 backdrop-blur-xl animate-fade-up flex flex-col h-[500px]"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <CardHeader className="bg-white/5 border-b border-white/5 relative">
                
                <div className="flex justify-between items-start mb-2 gap-4">
                  <CardTitle className="text-xl md:text-2xl font-serif text-white group-hover:text-indigo-300 transition-colors leading-tight">
                    {blog.title}
                  </CardTitle>
                  <Badge variant="success" className="shrink-0 font-mono">
                    <CheckCircle className="w-3 h-3 mr-1" />
                    SEO: {blog.score}/100
                  </Badge>
                </div>
                
                <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">
                  Published on: <span className="text-gray-300">{blog.platforms}</span>
                </p>
              </CardHeader>

              <CardContent className="p-0 flex-1 relative">
                <ScrollArea className="h-full w-full">
                  <div className="p-6 prose prose-invert prose-p:text-gray-400 prose-headings:text-gray-200">
                    <div dangerouslySetInnerHTML={{ 
                      __html: blog.content
                        .replace(/# (.*)/g, '<h1 class="text-xl font-bold text-white mb-4">$1</h1>')
                        .replace(/## (.*)/g, '<h2 class="text-lg font-semibold text-indigo-300 mt-6 mb-3">$1</h2>')
                        .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-pink-400/90 font-semibold">$1</strong>')
                        .replace(/\n\n/g, '<br/><br/>')
                    }} />
                    
                    {/* Fade out text at the bottom to indicate more content */}
                    <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-card via-card/80 to-transparent pointer-events-none"></div>
                  </div>
                </ScrollArea>
              </CardContent>

              <div className="p-4 border-t border-white/5 bg-black/40 mt-auto flex justify-between items-center relative z-10">
                <p className="text-xs text-gray-500 font-mono group-hover:text-indigo-400 transition-colors">
                  ~1,840 words • 8 min read
                </p>
                <Button variant="ghost" className="text-indigo-400 hover:text-indigo-300 hover:bg-white/5">
                  Read Full Blog <ExternalLink className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
