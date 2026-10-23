import React from 'react';
import { TriangleAlert } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface DemoBannerProps {
  isDemo?: boolean;
}

export const DemoBanner: React.FC<DemoBannerProps> = ({ isDemo = false }) => {
  const { t } = useTranslation();

  if (!isDemo) return null;

  return (
    <div
      className="demo-banner"
      role="alert"
      aria-live="polite"
      id="anveksha-demo-banner"
    >
      <TriangleAlert size={16} strokeWidth={2.5} aria-hidden="true" />
      <span>{t('demo.banner', 'Demo data. Numbers on this screen are examples, not an actual evaluation.')}</span>
    </div>
  );
};
