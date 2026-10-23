import React from 'react';
import { Check, TriangleAlert, X, CircleHelp } from 'lucide-react';

export type StatusType = 'Pass' | 'Warning' | 'Fail' | 'Not verified';

interface StatusBadgeProps {
  status: StatusType;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md', className = '' }) => {
  let iconSize = 16;
  let fontSize = '13px';
  let padding = '4px 10px';

  if (size === 'sm') {
    iconSize = 14;
    fontSize = '12px';
    padding = '2px 8px';
  } else if (size === 'lg') {
    iconSize = 18;
    fontSize = '14px';
    padding = '6px 14px';
  }

  const renderContent = () => {
    switch (status) {
      case 'Pass':
        return (
          <span
            className={`status-badge pass ${className}`}
            style={{ fontSize, padding }}
            role="status"
            aria-label="Status: Pass"
          >
            <Check size={iconSize} strokeWidth={2.5} aria-hidden="true" />
            <span>Pass</span>
          </span>
        );
      case 'Warning':
        return (
          <span
            className={`status-badge warning ${className}`}
            style={{ fontSize, padding }}
            role="status"
            aria-label="Status: Warning"
          >
            <TriangleAlert size={iconSize} strokeWidth={2.5} aria-hidden="true" />
            <span>Warning</span>
          </span>
        );
      case 'Fail':
        return (
          <span
            className={`status-badge fail ${className}`}
            style={{ fontSize, padding }}
            role="status"
            aria-label="Status: Fail"
          >
            <X size={iconSize} strokeWidth={2.5} aria-hidden="true" />
            <span>Fail</span>
          </span>
        );
      case 'Not verified':
      default:
        return (
          <span
            className={`status-badge not-verified ${className}`}
            style={{ fontSize, padding }}
            role="status"
            aria-label="Status: Not verified"
          >
            <CircleHelp size={iconSize} strokeWidth={2.5} aria-hidden="true" />
            <span>Not verified</span>
          </span>
        );
    }
  };

  return renderContent();
};
