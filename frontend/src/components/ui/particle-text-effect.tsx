import React, { useEffect, useRef, useState } from 'react';

interface Particle {
  x: number;
  y: number;
  originX: number;
  originY: number;
  vx: number;
  vy: number;
  color: string;
}

interface ParticleTextEffectProps {
  words: string[];
  particleColor1?: string;
  particleColor2?: string;
}

export function ParticleTextEffect({ 
  words, 
  particleColor1 = "#6366f1", // indigo
  particleColor2 = "#ec4899"  // pink
}: ParticleTextEffectProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    if (!ctx) return;

    let particles: Particle[] = [];
    let animationFrameId: number;
    let width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
    let height = canvas.height = 300; // Fixed height for hero section part

    const handleResize = () => {
      width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      height = canvas.height = 300;
      createParticles(words[currentWordIndex]);
    };

    window.addEventListener('resize', handleResize);

    const createParticles = (text: string) => {
      // Clear for new text reading
      ctx.clearRect(0, 0, width, height);
      
      // Calculate font size relative to width
      const fontSize = Math.min(width * 0.15, 120);
      ctx.font = `bold ${fontSize}px Inter, sans-serif`;
      ctx.fillStyle = 'white';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Draw text
      ctx.fillText(text, width / 2, height / 2);
      
      // Get image data
      const imageData = ctx.getImageData(0, 0, width, height);
      const data = imageData.data;
      
      const newParticles: Particle[] = [];
      const step = Math.max(Math.floor(width / 150), 3); // Particle density
      
      for (let y = 0; y < height; y += step) {
        for (let x = 0; x < width; x += step) {
          const index = (y * width + x) * 4;
          // If pixel has alpha
          if (data[index + 3] > 128) {
            // Randomly assign one of the two colors, with slight variations
            const isColor1 = Math.random() > 0.5;
            const baseColor = isColor1 ? particleColor1 : particleColor2;
            
            // Re-use existing particles if possible to avoid recreating objects
            const existingParticle = particles.find(p => p.x === -9999);
            
            if (existingParticle) {
              existingParticle.originX = x;
              existingParticle.originY = y;
              existingParticle.color = baseColor;
              existingParticle.x = existingParticle.x === -9999 ? Math.random() * width : existingParticle.x;
              existingParticle.y = existingParticle.y === -9999 ? Math.random() * height : existingParticle.y;
              newParticles.push(existingParticle);
            } else {
              newParticles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                originX: x,
                originY: y,
                vx: 0,
                vy: 0,
                color: baseColor
              });
            }
          }
        }
      }
      
      particles = newParticles;
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);
      
      particles.forEach(p => {
        // Friction and easing towards origin
        p.vx += (p.originX - p.x) * 0.05;
        p.vy += (p.originY - p.y) * 0.05;
        p.vx *= 0.85; // friction
        p.vy *= 0.85; // friction
        
        p.x += p.vx;
        p.y += p.vy;
        
        // Jiggle slightly when near origin
        const dist = Math.hypot(p.originX - p.x, p.originY - p.y);
        if (dist < 1) {
          p.x += (Math.random() - 0.5) * 0.5;
          p.y += (Math.random() - 0.5) * 0.5;
        }

        ctx.fillStyle = p.color;
        ctx.beginPath();
        // Slightly glowing circles
        ctx.arc(p.x, p.y, Math.random() * 0.5 + 1.2, 0, Math.PI * 2);
        ctx.fill();
        
        // Add faint connection lines to close particles occasionally
        if (Math.random() > 0.98) {
           ctx.shadowBlur = 10;
           ctx.shadowColor = p.color;
        } else {
          ctx.shadowBlur = 0;
        }
      });
      
      animationFrameId = requestAnimationFrame(animate);
    };

    createParticles(words[currentWordIndex]);
    animate();

    const interval = setInterval(() => {
      setCurrentWordIndex((prev) => (prev + 1) % words.length);
    }, 4000); // Change word every 4s

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      clearInterval(interval);
    };
  }, [words, currentWordIndex, particleColor1, particleColor2]);

  return (
    <div className="w-full flex justify-center items-center pointer-events-none">
      <canvas 
        ref={canvasRef} 
        className="max-w-full"
        style={{ filter: 'drop-shadow(0 0 15px rgba(99, 102, 241, 0.3))' }}
      />
    </div>
  );
}
