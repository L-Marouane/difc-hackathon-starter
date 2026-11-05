import { GenieChat } from '@databricks/appkit-ui/react';

const SAMPLE_QUESTIONS = [
  'Which accounts are at risk right now and how much MRR is at stake?',
  'Which acquisition channel gives the best return on marketing spend?',
  'What happened in Saudi Arabia in summer 2026?',
];

export function GeniePage() {
  return (
    <div className="space-y-6 w-full max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Ask Genie</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Ask anything about Falak&apos;s customers, revenue, marketing and support. Try:
        </p>
        <ul className="text-sm text-muted-foreground mt-2 list-disc list-inside">
          {SAMPLE_QUESTIONS.map((q) => (
            <li key={q}>{q}</li>
          ))}
        </ul>
      </div>
      <div className="h-[min(640px,70vh)] border rounded-lg overflow-hidden">
        <GenieChat alias="default" />
      </div>
    </div>
  );
}
