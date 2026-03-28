import React, { useState, useEffect } from 'react';
import { ExternalLink, CheckCircle, X, ChevronDown, ChevronUp, BarChart3, Target, FileText, Hash, Link2, Globe, ArrowRight, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ScrollArea } from '../components/ui/scroll-area';
import { Button } from '../components/ui/button';

interface BlogExample {
  title: string;
  score: number;
  platforms: string;
  content: string;
  faq: { question: string; answer: string }[];
  cta: { headline: string; description: string; buttonText: string };
  seoBreakdown: { label: string; score: number; icon: React.ReactNode }[];
}

const blogExamples: BlogExample[] = [
  {
    title: "Blogy – Best AI Blog Automation Tool in India",
    score: 91,
    platforms: "Medium • LinkedIn • WordPress",
    content: `# Blogy – Best AI Blog Automation Tool in India

If you're tired of spending 4+ hours researching keywords, finding H2 gaps, and trying to write content that actually ranks on Google India, you're not alone. The digital marketing landscape here is crowded, and generic AI tools just don't cut it anymore.

Enter **Blogy**, an SEO automation powerhouse that takes a single keyword and turns it into a fully optimized, 2,000-word blog post in under 60 seconds.

## Why Indian Marketers Need Specialized Tools
Most generative AI lacks the regional context needed for the Indian market. Local pricing, tier-specific audience understanding, and proper semantic SEO structures are crucial. 

With Blogy's pipeline, you aren't just generating text; you are generating an SEO asset designed specifically to capture organic traffic in your target locale. It automatically structures your meta descriptions, generates internal linking suggestions, and formats schema markup right out of the box.

## The Problem with Generic AI Writers
When you use a standard LLM to write a blog post, you often end up with:
1. Fluffy, repetitive introductions.
2. Poor keyword density leading to cannibalization.
3. Lack of proper H2/H3 tag hierarchies.
4. Hallucinated facts that hurt domain authority.

**Blogy fixes this** by applying a multi-agent workflow. The first agent acts as an SEO analyst, scraping the top 10 search results for your keyword. The second acts as an outline constructor, building a framework that explicitly targets PAA (People Also Ask) queries.

## Conclusion
If you want to scale your organic presence without scaling your headcount, Blogy is the definitive solution for Indian enterprises and indie-hackers alike. Try it today and watch your impressions skyrocket.`,
    faq: [
      { question: "What makes Blogy different from ChatGPT for blog writing?", answer: "Blogy uses a 7-step SEO pipeline that includes keyword clustering, SERP gap analysis, and structured outlines — not just raw text generation. Every output is optimized for Google India rankings." },
      { question: "How long does it take to generate a blog?", answer: "Under 60 seconds. From a single keyword input, Blogy produces a fully structured, SEO-optimized 1,500–2,000 word blog post with meta tags, FAQs, and schema markup." },
      { question: "Can I use Blogy for my WordPress site?", answer: "Absolutely. Blogy outputs clean Markdown and HTML that can be pasted directly into WordPress, Medium, LinkedIn, or any CMS without additional formatting." },
      { question: "Is Blogy suitable for the Indian market?", answer: "Yes — Blogy is specifically designed with GEO-optimization for India, including local keyword targeting, regional context awareness, and tier-specific audience understanding." },
    ],
    cta: {
      headline: "Ready to 10x Your Organic Traffic?",
      description: "Stop spending hours on content that doesn't rank. Let Blogy's AI pipeline generate high-ranking blogs in seconds.",
      buttonText: "Try Blogy Free →"
    },
    seoBreakdown: [
      { label: "Keyword Density", score: 94, icon: <Target className="w-4 h-4" /> },
      { label: "Content Length", score: 88, icon: <FileText className="w-4 h-4" /> },
      { label: "Heading Structure", score: 96, icon: <Hash className="w-4 h-4" /> },
      { label: "Internal Links", score: 82, icon: <Link2 className="w-4 h-4" /> },
      { label: "Meta Optimization", score: 93, icon: <Globe className="w-4 h-4" /> },
      { label: "Readability", score: 90, icon: <BarChart3 className="w-4 h-4" /> },
    ]
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

By mechanizing these steps, Blogy guarantees a baseline of quality that most human writers struggle to maintain consistently.

## Automating the Boring Parts
Writing the actual words is only 20% of SEO. The other 80% is formatting, keyword insertion, alt-text generation, and metadata crafting. Blogy handles all of this invisibly within its pipeline. 

You no longer have to spend an extra 30 minutes in WordPress tweaking formatting or trying to get the Yoast SEO light to turn green. Blogy natively outputs perfectly formatted Markdown and HTML, ready to be pasted directly into your CMS.

## The Future of Organic Growth
In a world where search is increasingly fragmented, publishing high-quality, long-form content consistently is the ultimate moat. Blogy empowers solo founders to output content at the velocity of a 10-person editorial team, leveling the playing field in competitive niches.`,
    faq: [
      { question: "What is Blogy's 7-step pipeline?", answer: "The pipeline includes: Keyword Clustering, SERP Gap Analysis, Outline Generation, Content Writing, SEO Scoring, Meta Tag Generation, and Final Formatting. Each step is automated for maximum quality." },
      { question: "How does Blogy compare to hiring a content agency?", answer: "A typical agency charges ₹15,000–₹50,000 per blog and takes 3–5 days. Blogy generates comparable quality in under 60 seconds at a fraction of the cost, letting you scale to 100+ blogs per month." },
      { question: "Does Blogy work for niches outside of tech?", answer: "Yes. Blogy works across all niches — health, finance, ecommerce, SaaS, education, and more. The pipeline adapts its keyword strategy and content structure based on your target industry." },
      { question: "Can Blogy generate content in regional languages?", answer: "Currently Blogy is optimized for English content targeting the Indian market. Regional language support is on the roadmap for future releases." },
    ],
    cta: {
      headline: "Scale Your Content Like a 10-Person Team",
      description: "Solo founders and lean startups are using Blogy to publish 100+ SEO-optimized blogs per month. Join them.",
      buttonText: "Start Generating →"
    },
    seoBreakdown: [
      { label: "Keyword Density", score: 96, icon: <Target className="w-4 h-4" /> },
      { label: "Content Length", score: 92, icon: <FileText className="w-4 h-4" /> },
      { label: "Heading Structure", score: 98, icon: <Hash className="w-4 h-4" /> },
      { label: "Internal Links", score: 87, icon: <Link2 className="w-4 h-4" /> },
      { label: "Meta Optimization", score: 95, icon: <Globe className="w-4 h-4" /> },
      { label: "Readability", score: 93, icon: <BarChart3 className="w-4 h-4" /> },
    ]
  }
];

function SEOScoreBar({ label, score, icon }: { label: string; score: number; icon: React.ReactNode }) {
  const getColor = (s: number) => {
    if (s >= 90) return 'bg-emerald-500';
    if (s >= 80) return 'bg-indigo-500';
    if (s >= 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="flex items-center gap-3">
      <div className="text-gray-400 shrink-0">{icon}</div>
      <div className="flex-1 min-w-0">
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm text-gray-300 font-medium">{label}</span>
          <span className="text-sm font-mono text-white font-semibold">{score}%</span>
        </div>
        <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-1000 ease-out ${getColor(score)}`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
    </div>
  );
}

function FAQItem({ question, answer }: { question: string; answer: string }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border border-white/10 rounded-xl overflow-hidden transition-all duration-300 hover:border-indigo-500/30">
      <button
        className="w-full flex items-center justify-between p-4 text-left cursor-pointer bg-white/[0.02] hover:bg-white/[0.05] transition-colors"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="text-sm md:text-base font-medium text-gray-200 pr-4">{question}</span>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-indigo-400 shrink-0" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-500 shrink-0" />
        )}
      </button>
      <div
        className={`overflow-hidden transition-all duration-300 ease-in-out ${isOpen ? 'max-h-60 opacity-100' : 'max-h-0 opacity-0'}`}
      >
        <p className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">{answer}</p>
      </div>
    </div>
  );
}

function renderMarkdown(content: string) {
  return content
    .replace(/# (.*)/g, '<h1 class="text-3xl lg:text-4xl font-bold text-white mb-6">$1</h1>')
    .replace(/## (.*)/g, '<h2 class="text-2xl font-semibold text-indigo-300 mt-10 mb-5 border-b border-white/10 pb-2">$1</h2>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-white/90 font-semibold bg-pink-500/10 px-1 rounded">$1</strong>')
    .replace(/\n\n/g, '<br/><br/>');
}

function renderPreviewMarkdown(content: string) {
  return content
    .replace(/# (.*)/g, '<h1 class="text-xl font-bold text-white mb-4">$1</h1>')
    .replace(/## (.*)/g, '<h2 class="text-lg font-semibold text-indigo-300 mt-6 mb-3">$1</h2>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-pink-400/90 font-semibold">$1</strong>')
    .replace(/\n\n/g, '<br/><br/>');
}

export function BlogPreviews() {
  const [selectedBlogIndex, setSelectedBlogIndex] = useState<number | null>(null);

  // Prevent background scrolling when modal is open
  useEffect(() => {
    if (selectedBlogIndex !== null) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [selectedBlogIndex]);

  const selectedBlog = selectedBlogIndex !== null ? blogExamples[selectedBlogIndex] : null;

  return (
    <>
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
                        __html: renderPreviewMarkdown(blog.content)
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
                  <Button
                    variant="ghost"
                    className="text-indigo-400 hover:text-indigo-300 hover:bg-white/5 cursor-pointer gap-2"
                    onClick={() => setSelectedBlogIndex(index)}
                  >
                    Read Full Blog
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Full Screen Reading Modal */}
      {selectedBlog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-md animate-fade-in transition-all duration-300">
          <div
            className="absolute inset-0 cursor-pointer"
            onClick={() => setSelectedBlogIndex(null)}
          ></div>
          <Card className="relative w-full max-w-4xl max-h-[92vh] flex flex-col bg-[#0a0a0f] border border-white/10 shadow-2xl shadow-indigo-500/5 animate-fade-up z-10 overflow-hidden rounded-2xl">

            {/* Close Button */}
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-4 right-4 z-20 text-gray-400 hover:text-white hover:bg-white/10 rounded-full cursor-pointer"
              onClick={() => setSelectedBlogIndex(null)}
            >
              <X className="w-5 h-5" />
            </Button>

            {/* Modal Header */}
            <CardHeader className="bg-white/[0.03] border-b border-white/5 pr-14 relative z-10">
              <div className="flex justify-between items-start mb-2 gap-4 flex-wrap">
                <CardTitle className="text-2xl md:text-3xl font-serif text-white leading-tight mt-2 sm:mt-0">
                  {selectedBlog.title}
                </CardTitle>
                <Badge variant="success" className="shrink-0 font-mono mt-1">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  SEO: {selectedBlog.score}/100
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground font-medium uppercase tracking-wider">
                Published on: <span className="text-gray-300">{selectedBlog.platforms}</span>
              </p>
            </CardHeader>

            {/* Scrollable Modal Content */}
            <CardContent className="p-0 flex-1 relative overflow-hidden bg-[#08080d]">
              <ScrollArea className="h-full w-full">
                <div className="p-6 md:p-8 lg:p-10">

                  {/* === Full Blog Content === */}
                  <div className="prose prose-invert prose-p:text-gray-300 prose-headings:text-gray-100 max-w-none text-base md:text-lg leading-relaxed">
                    <div dangerouslySetInnerHTML={{
                      __html: renderMarkdown(selectedBlog.content)
                    }} />
                  </div>

                  {/* === Divider === */}
                  <div className="my-12 flex items-center gap-4">
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent"></div>
                    <Sparkles className="w-5 h-5 text-indigo-400" />
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent"></div>
                  </div>

                  {/* === SEO Score Breakdown === */}
                  <div className="mb-12">
                    <div className="flex items-center gap-3 mb-6">
                      <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                        <BarChart3 className="w-5 h-5 text-emerald-400" />
                      </div>
                      <h3 className="text-xl md:text-2xl font-bold text-white font-serif">
                        SEO Score Breakdown
                      </h3>
                      <Badge variant="success" className="font-mono ml-auto">
                        Overall: {selectedBlog.score}/100
                      </Badge>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6 rounded-2xl bg-white/[0.02] border border-white/10">
                      {selectedBlog.seoBreakdown.map((item, i) => (
                        <SEOScoreBar key={i} label={item.label} score={item.score} icon={item.icon} />
                      ))}
                    </div>
                  </div>

                  {/* === FAQ Section === */}
                  <div className="mb-12">
                    <div className="flex items-center gap-3 mb-6">
                      <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
                        <ChevronDown className="w-5 h-5 text-indigo-400" />
                      </div>
                      <h3 className="text-xl md:text-2xl font-bold text-white font-serif">
                        Frequently Asked Questions
                      </h3>
                    </div>
                    <div className="space-y-3">
                      {selectedBlog.faq.map((item, i) => (
                        <FAQItem key={i} question={item.question} answer={item.answer} />
                      ))}
                    </div>
                  </div>

                  {/* === CTA Section === */}
                  <div className="relative rounded-2xl overflow-hidden p-8 md:p-10 text-center">
                    {/* CTA gradient bg */}
                    <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/20 via-purple-600/15 to-pink-600/20 border border-indigo-500/20 rounded-2xl"></div>
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(99,102,241,0.15),transparent_70%)]"></div>

                    <div className="relative z-10">
                      <Sparkles className="w-8 h-8 text-indigo-400 mx-auto mb-4" />
                      <h3 className="text-2xl md:text-3xl font-bold text-white mb-3 font-serif">
                        {selectedBlog.cta.headline}
                      </h3>
                      <p className="text-gray-300 mb-6 max-w-xl mx-auto leading-relaxed">
                        {selectedBlog.cta.description}
                      </p>
                      <Button
                        size="lg"
                        className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white px-8 h-12 text-base font-semibold shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:scale-[1.02]"
                        onClick={() => {
                          setSelectedBlogIndex(null);
                          document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' });
                        }}
                      >
                        {selectedBlog.cta.buttonText}
                      </Button>
                    </div>
                  </div>

                  {/* Bottom spacing */}
                  <div className="h-6"></div>
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  );
}
