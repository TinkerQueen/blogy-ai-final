import { Button } from '../components/ui/button';

export function Footer() {
  return (
    <footer className="relative bg-[#050508] pt-24 pb-12 overflow-hidden border-t border-white/10">
      
      {/* Subtle top gradient */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent"></div>

      <div className="container mx-auto px-4 relative z-10">
        
        {/* Hackathon Callout */}
        <div className="max-w-4xl mx-auto mb-20 p-8 rounded-3xl bg-indigo-900/10 border border-indigo-500/20 text-center relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <h3 className="text-2xl md:text-3xl font-bold text-white mb-3 font-serif relative z-10">
            Built for Blogy
          </h3>
          <p className="text-indigo-200/80 mb-6 relative z-10">
            AI-powered blog automation platform with a 7-step SEO pipeline — generating high-ranking, structured content in seconds.
          </p>
          <Button variant="outline" className="border-indigo-500/30 text-indigo-300 hover:text-white hover:bg-indigo-500/20 relative z-10">
            View Architecture →
          </Button>
        </div>

        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 md:gap-8 mb-16">
          
          {/* Brand Column */}
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">✍️</span>
              <span className="font-bold text-xl tracking-tight text-white font-serif">
                Blogy
              </span>
            </div>
            <p className="text-sm text-gray-500 leading-relaxed mb-6">
              India's most powerful AI blog automation platform. From keyword to ranked content in 60 seconds.
            </p>
          </div>

          {/* Links Columns */}
          <div>
            <h4 className="font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-3">
              <li><a href="#features" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">Features</a></li>
              <li><a href="#pipeline" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">7-Step Pipeline</a></li>
              <li><a href="#demo" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">Live Demo</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">Resources</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">Blog Examples</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">API Documentation</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">SEO Guides</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">Company</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">About Us</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">Contact</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-indigo-400 transition-colors">DTU Hackathon</a></li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-600">
            © 2026 Blogy. Powered by <span className="text-pink-500/80">Groq</span> & <span className="text-indigo-500/80">LLaMA 3.3</span>
          </p>
          <div className="flex gap-4">
            <a href="#" className="text-sm text-gray-600 hover:text-white transition-colors">Terms</a>
            <a href="#" className="text-sm text-gray-600 hover:text-white transition-colors">Privacy</a>
          </div>
        </div>

      </div>
    </footer>
  );
}
