"use client";

import { useState } from "react";
import { CheckCircle2, Circle } from "lucide-react";
import { apiPatch, type Task } from "@/lib/api";

export function TaskList({ tasks }: { tasks: Task[] }) {
  const [localTasks, setLocalTasks] = useState(tasks);
  const [error, setError] = useState<string | null>(null);
  const [toggling, setToggling] = useState<string | null>(null);

  async function toggleTask(task: Task) {
    setToggling(task.id);
    setError(null);
    try {
      const updated = await apiPatch<Task>(`/tasks/${task.id}`, { is_done: !task.is_done });
      setLocalTasks((current) => current.map((item) => (item.id === updated.id ? updated : item)));
    } catch {
      setError("Failed to update task. Please try again.");
    } finally {
      setToggling(null);
    }
  }

  return (
    <div className="space-y-3">
      {error && (
        <div className="rounded border border-[#E5A39C] bg-[#FFF1EF] p-3 text-sm text-[#8B1E18]">{error}</div>
      )}
      {localTasks.map((task) => (
        <button
          key={task.id}
          onClick={() => toggleTask(task)}
          disabled={toggling === task.id}
          className="focus-ring flex w-full gap-3 rounded border border-line bg-[#fffdf9] p-4 text-left hover:border-copper disabled:opacity-70"
        >
          <span className={task.is_done ? "text-coral" : "text-[#9D8B7F]"}>
            {task.is_done ? <CheckCircle2 size={22} /> : <Circle size={22} />}
          </span>
          <span className="min-w-0">
            <span className="block font-semibold">{task.title}</span>
            <span className="mt-1 block text-sm text-[#725D50]">{task.description}</span>
            <span className="mt-3 flex flex-wrap gap-2 text-xs font-semibold">
              <span className="rounded bg-[#F2E8DC] px-2 py-1">{task.category}</span>
              <span className="rounded bg-[#FFE4DC] px-2 py-1">{task.priority}</span>
              {task.estimated_minutes ? <span>{task.estimated_minutes} min</span> : null}
            </span>
          </span>
        </button>
      ))}
    </div>
  );
}
