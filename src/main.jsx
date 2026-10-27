import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

const preventPinchZoom = event => {
  const hasMultipleTouches = event.touches?.length > 1;
  const isGestureZoom = typeof event.scale === 'number' && event.scale !== 1;
  if (hasMultipleTouches || isGestureZoom) event.preventDefault();
};

['touchstart', 'touchmove', 'gesturestart', 'gesturechange'].forEach(type => {
  document.addEventListener(type, preventPinchZoom, { passive: false });
});

createRoot(document.getElementById('root')).render(<App />);
