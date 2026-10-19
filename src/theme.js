import { createElement, useEffect, useState } from 'react';

const THEME_KEY = 'importaciones-ebc-theme';
const DARK = 'dark';
const LIGHT = 'light';

function systemTheme() {
  return typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: dark)').matches ? DARK : LIGHT;
}

function storedTheme() {
  if (typeof window === 'undefined') return null;
  const value = window.localStorage.getItem(THEME_KEY);
  return value === DARK || value === LIGHT ? value : null;
}

export function resolveTheme() {
  return storedTheme() || systemTheme();
}

export function applyTheme(theme) {
  if (typeof document === 'undefined') return;
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
}

export function initializeTheme() {
  const theme = resolveTheme();
  applyTheme(theme);
  return theme;
}

export function useThemePreference() {
  const [theme, setTheme] = useState(initializeTheme);

  useEffect(() => {
    applyTheme(theme);
    window.localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  return [theme, () => setTheme(current => current === DARK ? LIGHT : DARK)];
}

export function ThemeToggle({ className = '' }) {
  const [theme, toggleTheme] = useThemePreference();
  const dark = theme === DARK;
  return createElement('button', {
    type: 'button',
    className: `theme-toggle ${className}`.trim(),
    onClick: toggleTheme,
    'aria-pressed': dark,
    'aria-label': dark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro',
    title: dark ? 'Modo claro' : 'Modo oscuro',
  }, createElement('span', { 'aria-hidden': 'true' }, dark ? '☼' : '☾'), createElement('strong', null, dark ? 'Claro' : 'Oscuro'));
}
