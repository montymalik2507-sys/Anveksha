import React from 'react';
import { Check } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export interface WorkflowStep {
  number: number;
  id: string;
  label: string;
  path: string;
}

export const WORKFLOW_STEPS: WorkflowStep[] = [
  { number: 1, id: 'add_data', label: 'Add data', path: '/new-test' },
  { number: 2, id: 'check_data', label: 'Check data', path: '/check-data' },
  { number: 3, id: 'compatibility', label: 'Compatibility', path: '/compatibility' },
  { number: 4, id: 'run_model', label: 'Run model', path: '/check-model' },
  { number: 5, id: 'results', label: 'Results', path: '/results' },
];

interface WorkflowStepperProps {
  currentStep: number; // 1 to 5
}

export const WorkflowStepper: React.FC<WorkflowStepperProps> = ({ currentStep }) => {
  const navigate = useNavigate();
  const currentStepObj = WORKFLOW_STEPS.find(s => s.number === currentStep) || WORKFLOW_STEPS[0];

  return (
    <nav aria-label="Workflow Stepper" style={{ marginBottom: '24px' }}>
      {/* Desktop & Tablet Stepper Bar */}
      <div className="stepper-nav" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        {WORKFLOW_STEPS.map((step) => {
          const isDone = step.number < currentStep;
          const isCurrent = step.number === currentStep;
          const isNext = step.number > currentStep;

          let statusClass = 'next';
          if (isDone) statusClass = 'done';
          if (isCurrent) statusClass = 'current';

          return (
            <button
              key={step.id}
              type="button"
              className={`step-item ${statusClass}`}
              disabled={!isDone}
              onClick={() => {
                if (isDone) {
                  navigate(step.path);
                }
              }}
              title={isDone ? `Go back to ${step.label}` : step.label}
              aria-current={isCurrent ? 'step' : undefined}
            >
              <div className="step-circle">
                {isDone ? (
                  <Check size={14} strokeWidth={3} aria-hidden="true" />
                ) : (
                  <span>{step.number}</span>
                )}
              </div>
              <span className="step-label-text" style={{ fontSize: '13px' }}>
                {step.label}
              </span>
            </button>
          );
        })}
      </div>

      {/* Mobile Step Summary (<700px): "Step 2 of 5: Check data" */}
      <div
        style={{
          display: 'none',
          padding: '8px 12px',
          background: 'var(--card)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--line)',
          fontSize: '13px',
          fontWeight: 600,
          color: 'var(--accent-teal)',
          marginBottom: '16px',
        }}
        className="mobile-stepper-summary"
      >
        Step {currentStep} of 5: {currentStepObj.label}
      </div>

      <style>{`
        @media (max-width: 700px) {
          .step-label-text {
            display: none !important;
          }
          .mobile-stepper-summary {
            display: block !important;
          }
        }
      `}</style>
    </nav>
  );
};
