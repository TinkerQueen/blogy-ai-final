import React, { useState } from 'react';
import { Settings, Sparkles, MapPin, MessageSquare, Terminal, Key } from 'lucide-react';
import { Button } from './button';
import { Textarea } from './textarea';

interface PromptInputBoxProps {
  onGenerate: (keyword: string, config: any) => void;
  isLoading: boolean;
}

export function PromptInputBox({ onGenerate, isLoading }: PromptInputBoxProps) {
  const [keyword, setKeyword] = useState('');
  const [showConfig, setShowConfig] = useState(true);
  
  const [config, setConfig] = useState({
    location: 'India',
    tone: 'Professional',
    model: 'llama-3.3-70b-versatile',
    apiKey: ''
  });

  const wordCount = keyword.trim().split(/\s+/).filter(w => w.length > 0).length;

  const handleGenerate = () => {
    if (!keyword.trim() || isLoading) return;
    onGenerate(keyword, config);
  };

  return (
    <div className="w-full max-w-3xl mx-auto rounded-3xl p-6 bg-card/60 backdrop-blur-xl border border-white/10 shadow-[0_8px_30px_rgba(0,0,0,0.5)]">
      <div className="relative group">
        <div className="absolute -inset-0.5 bg-gradient-primary rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
        <div className="relative bg-background/80 rounded-2xl border border-white/10 overflow-hidden flex flex-col">
          <Textarea 
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="Enter your primary keyword..."
            className="min-h-[120px] resize-none border-0 focus-visible:ring-0 bg-transparent text-lg p-6 font-medium text-white"
          />
          <div className="flex items-center justify-between p-4 border-t border-white/5 bg-black/40">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-white" onClick={() => setShowConfig(!showConfig)}>
                <Settings className="w-4 h-4 mr-2" />
                {showConfig ? 'Hide Config' : 'Show Config'}
              </Button>
              <span className="text-xs text-muted-foreground/60">
                {wordCount} {wordCount === 1 ? 'word' : 'words'}
              </span>
            </div>
            <Button 
              onClick={handleGenerate}
              disabled={!keyword.trim() || isLoading}
              className="bg-gradient-primary text-white rounded-full px-6 transition-all transform active:scale-95 shadow-lg shadow-indigo-500/20"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              Generate Blog 🚀
            </Button>
          </div>
        </div>
      </div>

      <div className={`mt-6 space-y-4 transition-all duration-500 overflow-hidden ${showConfig ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white/5 border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <MapPin className="w-4 h-4 text-indigo-400" />
            <div className="flex-1">
              <label className="text-xs text-muted-foreground block">Target Location</label>
              <input value={config.location} onChange={e => setConfig({...config, location: e.target.value})} className="w-full bg-transparent border-0 p-0 text-sm text-white focus:ring-0" />
            </div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <MessageSquare className="w-4 h-4 text-pink-400" />
            <div className="flex-1">
              <label className="text-xs text-muted-foreground block">Blog Tone</label>
              <select value={config.tone} onChange={e => setConfig({...config, tone: e.target.value})} className="w-full bg-transparent border-0 p-0 text-sm text-white focus:ring-0">
                <option>Professional</option>
                <option>Conversational</option>
                <option>Authoritative</option>
              </select>
            </div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <Terminal className="w-4 h-4 text-cyan-400" />
            <div className="flex-1">
              <label className="text-xs text-muted-foreground block">Groq Model</label>
              <select value={config.model} onChange={e => setConfig({...config, model: e.target.value})} className="w-full bg-transparent border-0 p-0 text-sm text-cyan-50 focus:ring-0">
                <option value="llama-3.3-70b-versatile">LLaMA 3.3 70B (Recommended)</option>
                <option value="llama-3.1-8b-instant">LLaMA 3.1 8B (Fastest)</option>
                <option value="mixtral-8x7b-32768">Mixtral 8x7B</option>
              </select>
            </div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <Key className="w-4 h-4 text-purple-400" />
            <div className="flex-1">
              <label className="text-xs text-muted-foreground block">Groq API Key (Optional)</label>
              <input type="password" value={config.apiKey} onChange={e => setConfig({...config, apiKey: e.target.value})} className="w-full bg-transparent border-0 p-0 text-sm text-white focus:ring-0 placeholder:text-white/20" placeholder="gsk_..." />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
