"use client"
import { useState, useEffect, useCallback, useRef } from 'react';

interface UseHideOnScrollParams {
  /** Scroll distance threshold to trigger hide (default: 50px) */
  scrollThreshold?: number;
  /** Throttle time (default: 100ms) */
  throttleTime?: number;
}

export const useHideOnScroll = ({
  scrollThreshold = 50,
  throttleTime = 100,
}: UseHideOnScrollParams = {}): { hidden: boolean } => {
  const [hidden, setHidden] = useState(false);
  const lastScrollY = useRef(0);
  const throttleTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleScroll = useCallback(() => {
    const currentScrollY = window.scrollY;
    
    // Hide when scrolling down beyond threshold
    if (currentScrollY > lastScrollY.current + scrollThreshold) {
      setHidden(true);
    } 
    // Show when scrolling up
    else if (currentScrollY < lastScrollY.current) {
      setHidden(false);
    }
    
    lastScrollY.current = currentScrollY;
  }, [scrollThreshold]);

  const throttledScrollHandler = useCallback(() => {
    if (!throttleTimeout.current) {
      throttleTimeout.current = setTimeout(() => {
        handleScroll();
        throttleTimeout.current = null;
      }, throttleTime);
    }
  }, [handleScroll, throttleTime]);

  useEffect(() => {
    window.addEventListener('scroll', throttledScrollHandler);
    return () => {
      window.removeEventListener('scroll', throttledScrollHandler);
      if (throttleTimeout.current) {
        clearTimeout(throttleTimeout.current);
      }
    };
  }, [throttledScrollHandler]);

  return { hidden };
};