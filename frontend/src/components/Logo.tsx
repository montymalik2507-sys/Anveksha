import React from 'react';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'intro';
  showText?: boolean;
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({ size = 'sm', showText = true, className = '' }) => {
  // Sizes according to spec:
  // bar: ~40px, home: 84px, intro: 160px
  let hexSize = 40;
  let wordmarkSize = '20px';
  let taglineSize = '12px';

  if (size === 'md') {
    hexSize = 56;
    wordmarkSize = '24px';
    taglineSize = '13px';
  } else if (size === 'lg') {
    hexSize = 84;
    wordmarkSize = '32px';
    taglineSize = '15px';
  } else if (size === 'intro') {
    hexSize = 160;
    wordmarkSize = '42px';
    taglineSize = '18px';
  }

  return (
    <div
      className={`logo-container flex items-center ${className}`}
      style={{ display: 'inline-flex', alignItems: 'center', gap: '12px', userSelect: 'none' }}
    >
      {/* Navy Hexagon SVG with teal & orange 'A', pulse line, and two small bars */}
      <svg
        width={hexSize}
        height={hexSize}
        viewBox="0 0 200 200"
        role="img"
        aria-label="ANVEKSHA logo"
        style={{ flexShrink: 0 }}
      >
        <defs>
          <linearGradient id={`navyHexGrad-${size}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#15365A" />
            <stop offset="100%" stopColor="#0A1828" />
          </linearGradient>
          <linearGradient id={`hexBorderGrad-${size}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3EF0DC" stopOpacity="0.7" />
            <stop offset="50%" stopColor="#5AA9FF" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#F28C1E" stopOpacity="0.7" />
          </linearGradient>
          <linearGradient id={`tealGrad-${size}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3EF0DC" />
            <stop offset="100%" stopColor="#14B8A6" />
          </linearGradient>
          <linearGradient id={`saffronGrad-${size}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#F28C1E" />
            <stop offset="100%" stopColor="#EA580C" />
          </linearGradient>
          <filter id={`softGlow-${size}`} x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3.5" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Outer navy hexagon */}
        <polygon
          points="100,12 178,57 178,143 100,188 22,143 22,57"
          fill={`url(#navyHexGrad-${size})`}
          stroke={`url(#hexBorderGrad-${size})`}
          strokeWidth="3.5"
          strokeLinejoin="round"
        />

        {/* Inner subtle hexagon line */}
        <polygon
          points="100,22 168,61 168,139 100,178 32,139 32,61"
          fill="none"
          stroke="#1E3E65"
          strokeWidth="1.5"
          strokeOpacity="0.4"
          strokeLinejoin="round"
        />

        {/* Teal left leg of 'A' */}
        <path d="M 64 148 L 94 54 L 102 54 L 82 148 Z" fill={`url(#tealGrad-${size})`} />

        {/* Orange / Saffron right leg of 'A' */}
        <path d="M 98 54 L 106 54 L 136 148 L 118 148 L 100 86 Z" fill={`url(#saffronGrad-${size})`} />

        {/* Peak apex of A */}
        <polygon points="94,54 106,54 100,42" fill="#3EF0DC" />

        {/* Medical ECG Pulse Line */}
        <path
          d="M 44 116 L 72 116 L 82 128 L 96 78 L 108 136 L 118 108 L 126 116 L 156 116"
          fill="none"
          stroke="#FFFFFF"
          strokeWidth="4"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter={`url(#softGlow-${size})`}
        />

        {/* Two small bars at bottom center representing dataset comparison */}
        <rect x="88" y="156" width="9" height="18" rx="2" fill="#3EF0DC" opacity="0.95" />
        <rect x="103" y="150" width="9" height="24" rx="2" fill="#F28C1E" opacity="0.95" />
      </svg>

      {/* Live text wordmark and tagline */}
      {showText && (
        <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.1 }}>
          <span
            style={{
              fontWeight: 800,
              fontSize: wordmarkSize,
              letterSpacing: '0.14em',
              color: 'var(--text)',
              fontFamily: 'var(--font-family)',
            }}
          >
            ANVEKSHA
          </span>
          <span
            style={{
              fontSize: taglineSize,
              fontWeight: 600,
              letterSpacing: '0.02em',
              marginTop: '2px',
              fontFamily: 'var(--font-family)',
            }}
          >
            <span style={{ color: 'var(--accent-teal)' }}>Beyond Accuracy. </span>
            <span style={{ color: 'var(--accent-saffron)' }}>Across Population.</span>
          </span>
        </div>
      )}
    </div>
  );
};
