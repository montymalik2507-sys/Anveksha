import React from 'react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { House, CirclePlus, ChartColumn, History, Settings } from 'lucide-react';

export const MobileTabBar: React.FC = () => {
  const { t } = useTranslation();

  return (
    <nav className="mobile-tab-bar" aria-label="Mobile Navigation">
      <NavLink
        to="/"
        end
        className={({ isActive }) => `mobile-tab-item ${isActive ? 'active' : ''}`}
        aria-label={t('nav.home')}
      >
        <House size={20} strokeWidth={2} aria-hidden="true" />
        <span>{t('nav.home')}</span>
      </NavLink>

      <NavLink
        to="/new-test"
        className={({ isActive }) => `mobile-tab-item ${isActive ? 'active' : ''}`}
        aria-label={t('nav.new_test')}
      >
        <CirclePlus size={20} strokeWidth={2} aria-hidden="true" />
        <span>{t('nav.new_test')}</span>
      </NavLink>

      <NavLink
        to="/results"
        className={({ isActive }) => `mobile-tab-item ${isActive ? 'active' : ''}`}
        aria-label={t('nav.results')}
      >
        <ChartColumn size={20} strokeWidth={2} aria-hidden="true" />
        <span>{t('nav.results')}</span>
      </NavLink>

      <NavLink
        to="/history"
        className={({ isActive }) => `mobile-tab-item ${isActive ? 'active' : ''}`}
        aria-label={t('nav.history')}
      >
        <History size={20} strokeWidth={2} aria-hidden="true" />
        <span>{t('nav.history')}</span>
      </NavLink>

      <NavLink
        to="/settings"
        className={({ isActive }) => `mobile-tab-item ${isActive ? 'active' : ''}`}
        aria-label={t('nav.settings')}
      >
        <Settings size={20} strokeWidth={2} aria-hidden="true" />
        <span>{t('nav.settings')}</span>
      </NavLink>
    </nav>
  );
};
