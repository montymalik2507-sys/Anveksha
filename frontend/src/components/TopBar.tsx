import React, { useState, useRef, useEffect } from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { 
  House, 
  CirclePlus, 
  ChartColumn, 
  History, 
  BookOpen, 
  Settings, 
  Globe, 
  Check, 
  Library as LibraryIcon,
  User
} from 'lucide-react';
import { Logo } from './Logo';
import { SUPPORTED_LANGUAGES } from '../i18n/config';

interface TopBarProps {
  onOpenSettings?: () => void;
}

export const TopBar: React.FC<TopBarProps> = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [langDropdownOpen, setLangDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click or Escape
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setLangDropdownOpen(false);
      }
    };
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setLangDropdownOpen(false);
      }
    };

    if (langDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [langDropdownOpen]);

  const handleSelectLanguage = (code: string) => {
    i18n.changeLanguage(code);
    localStorage.setItem('anveksha_lang', code);
    setLangDropdownOpen(false);
  };

  const currentLang = SUPPORTED_LANGUAGES.find(l => l.code === i18n.language) || SUPPORTED_LANGUAGES[0];

  return (
    <header className="top-bar" role="banner">
      {/* Left: Logo, wordmark, tagline */}
      <Link to="/" style={{ textDecoration: 'none' }} aria-label="ANVEKSHA Home">
        <Logo size="sm" showText={true} />
      </Link>

      {/* Middle: Desktop Nav Links (Section 5) */}
      <nav className="desktop-nav-links" style={{ display: 'flex', alignItems: 'center', gap: '8px' }} aria-label="Main Navigation">
        <NavLink
          to="/"
          end
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <House className="nav-icon" size={18} strokeWidth={2} aria-hidden="true" />
          <span>{t('nav.home')}</span>
        </NavLink>

        <NavLink
          to="/new-test"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <CirclePlus className="nav-icon" size={18} strokeWidth={2} aria-hidden="true" />
          <span>{t('nav.new_test')}</span>
        </NavLink>

        <NavLink
          to="/results"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <ChartColumn className="nav-icon" size={18} strokeWidth={2} aria-hidden="true" />
          <span>{t('nav.results')}</span>
        </NavLink>

        <NavLink
          to="/history"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <History className="nav-icon" size={18} strokeWidth={2} aria-hidden="true" />
          <span>{t('nav.history')}</span>
        </NavLink>

        <NavLink
          to="/library"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <LibraryIcon className="nav-icon" size={18} strokeWidth={2} aria-hidden="true" />
          <span>{t('nav.library')}</span>
        </NavLink>

        <NavLink
          to="/learn"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <BookOpen className="nav-icon" size={18} strokeWidth={2} aria-hidden="true" />
          <span>{t('nav.learn')}</span>
        </NavLink>
      </nav>

      {/* Right: Language Dropdown, Settings Gear, Profile Circle */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', position: 'relative' }}>
        {/* Language selector dropdown */}
        <div ref={dropdownRef} style={{ position: 'relative' }}>
          <button
            type="button"
            className="btn-ghost"
            style={{ padding: '6px 10px', height: '36px', minHeight: '36px', borderRadius: '8px', fontSize: '13px' }}
            onClick={() => setLangDropdownOpen(!langDropdownOpen)}
            aria-expanded={langDropdownOpen}
            aria-haspopup="true"
            aria-label={`Select language. Current: ${currentLang.name}`}
          >
            <Globe size={18} strokeWidth={2} aria-hidden="true" />
            <span style={{ fontWeight: 600 }}>{currentLang.code.toUpperCase()}</span>
          </button>

          {langDropdownOpen && (
            <div
              style={{
                position: 'absolute',
                top: '46px',
                right: 0,
                width: '210px',
                background: 'var(--card)',
                border: '1px solid var(--line)',
                borderRadius: 'var(--radius-md)',
                boxShadow: 'var(--shadow-lg)',
                padding: '6px',
                zIndex: 2000,
              }}
              role="menu"
              aria-orientation="vertical"
            >
              <div style={{ padding: '6px 10px', fontSize: '12px', color: 'var(--muted)', fontWeight: 600, borderBottom: '1px solid var(--line-2)' }}>
                Select Language
              </div>
              <div style={{ maxHeight: '280px', overflowY: 'auto' }}>
                {SUPPORTED_LANGUAGES.map((lang) => {
                  const isSelected = i18n.language === lang.code;
                  return (
                    <button
                      key={lang.code}
                      type="button"
                      role="menuitem"
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        width: '100%',
                        padding: '8px 10px',
                        background: isSelected ? 'rgba(62, 240, 220, 0.1)' : 'transparent',
                        color: isSelected ? 'var(--accent-teal)' : 'var(--text)',
                        border: 'none',
                        borderRadius: 'var(--radius-sm)',
                        cursor: 'pointer',
                        textAlign: 'left',
                        fontSize: '14px',
                        fontWeight: isSelected ? 600 : 400,
                      }}
                      onClick={() => handleSelectLanguage(lang.code)}
                    >
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span>{lang.nativeName}</span>
                        <span style={{ fontSize: '11px', color: 'var(--muted)' }}>{lang.name}</span>
                      </div>
                      {isSelected && <Check size={16} strokeWidth={2.5} color="var(--accent-teal)" />}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Settings gear with rotate on hover */}
        <button
          type="button"
          onClick={() => navigate('/settings')}
          className="btn-ghost settings-gear"
          style={{ width: '40px', height: '40px', minHeight: '40px', padding: 0, borderRadius: '50%' }}
          aria-label="Open Settings"
          title="Settings"
        >
          <Settings size={20} strokeWidth={2} />
        </button>

        {/* Profile Avatar circle */}
        <Link
          to="/signin"
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--line-3), var(--header))',
            border: '2px solid var(--line)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text)',
            textDecoration: 'none',
          }}
          aria-label="User Profile and Account"
          title="Account / Sign in"
        >
          <User size={18} strokeWidth={2} />
        </Link>
      </div>
    </header>
  );
};
