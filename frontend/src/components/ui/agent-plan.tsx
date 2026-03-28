import { CheckCircle2, Circle, Loader2 } from 'lucide-react';
import { Card } from './card';

export type TaskStatus = 'pending' | 'in-progress' | 'completed';

export interface Task {
  id: string;
  title: string;
  status: TaskStatus;
}

interface AgentPlanProps {
  tasks: Task[];
}

export function AgentPlan({ tasks }: AgentPlanProps) {
  const completedCount = tasks.filter(t => t.status === 'completed').length;
  const progress = tasks.length > 0 ? (completedCount / tasks.length) * 100 : 0;

  return (
    <Card className="w-full max-w-2xl mx-auto p-6 bg-card/80 backdrop-blur-xl border-white/10 shadow-[0_8px_30px_rgba(0,0,0,0.6)] animate-fade-in relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-1 bg-white/5">
        <div 
          className="h-full bg-gradient-to-r from-indigo-500 to-pink-500 transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
      
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30">
          {progress < 100 ? (
            <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-green-400" />
          )}
        </div>
        <div>
          <h3 className="font-semibold text-lg text-white font-serif">
            {progress < 100 ? 'AI Agent Working' : 'Pipeline Complete'}
          </h3>
          <p className="text-sm text-indigo-300">
            {completedCount}/{tasks.length} steps completed
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {tasks.map((task) => {
          const isPending = task.status === 'pending';
          const isInProgress = task.status === 'in-progress';
          const isCompleted = task.status === 'completed';

          return (
            <div 
              key={task.id}
              className={`flex items-center gap-4 p-3 rounded-lg transition-all duration-300 ${
                isInProgress ? 'bg-indigo-500/10 border border-indigo-500/20 translate-x-2' : 
                isCompleted ? 'bg-white/5 opacity-80' : 
                'opacity-40 grayscale'
              }`}
            >
              <div className="shrink-0">
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5 text-green-400" />
                ) : isInProgress ? (
                  <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-500" />
                )}
              </div>
              <span className={`text-sm font-medium ${isCompleted ? 'text-gray-300 line-through' : isInProgress ? 'text-white' : 'text-gray-500'}`}>
                {task.title}
              </span>
              {isInProgress && (
                <span className="ml-auto text-[10px] uppercase tracking-widest text-indigo-400 font-bold animate-pulse">
                  Processing...
                </span>
              )}
            </div>
          );
        })}
      </div>
    </Card>
  );
}
