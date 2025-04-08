"use client"
import { useState, useEffect, useCallback, useRef } from 'react';

interface UseOnScrollParams {
  /** Minimum scroll distance to trigger the hide/show effect */
  scrollThreshold?: number;
  /** Time to wait after the last scroll event before updating state */
  debounceTime?: number;
  /** Minimum time between scroll event handling */
  throttleTime?: number;
}

interface ScrollState {
  /** Whether to trigger the hide effect */
  trigger: boolean;
  /** Current scroll position */
  scrollY: number;
  /** Current scroll direction */
  scrollDirection: 'up' | 'down' | null;
}

export const useOnScroll = ({
  scrollThreshold = 50,
  debounceTime = 100,
  throttleTime = 100,
}: UseOnScrollParams = {}): ScrollState => {
  // Initialize scroll state
  const [scrollState, setScrollState] = useState<ScrollState>({
    trigger: false,
    scrollY: 0,
    scrollDirection: null,
  });

  // Refs for tracking scroll position and timers
  const lastScrollY = useRef(0);
  const throttleTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const debounceTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Main scroll handler logic
  const handleScroll = useCallback(() => {
    const currentScrollY = window.scrollY;
    const direction = currentScrollY > lastScrollY.current ? 'down' : 'up';
    const scrollDifference = Math.abs(currentScrollY - lastScrollY.current);

    if (scrollDifference >= 5) {
      setScrollState(prev => ({
        trigger: direction === 'down'
          ? (currentScrollY > scrollThreshold || prev.trigger)
          : false,
        scrollY: currentScrollY,
        scrollDirection: direction,
      }));
      lastScrollY.current = currentScrollY;
    }

  }, [scrollThreshold]);

  // Throttle scroll events to improve performance
  const throttledScrollHandler = useCallback(() => {
    if (!throttleTimeout.current) {
      throttleTimeout.current = setTimeout(() => {
        handleScroll();
        throttleTimeout.current = null;
      }, throttleTime);
    }
  }, [handleScroll, throttleTime]);

  // Debounce scroll events for smoother state updates
  const debouncedScrollHandler = useCallback(() => {
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }

    debounceTimeout.current = setTimeout(() => {
      handleScroll();
      debounceTimeout.current = null;
    }, debounceTime);
  }, [handleScroll, debounceTime]);

  // Combine throttle and debounce for optimal performance
  const combinedScrollHandler = useCallback(() => {
    throttledScrollHandler(); // For immediate visual feedback
    debouncedScrollHandler(); // For accurate final position
  }, [throttledScrollHandler, debouncedScrollHandler]);

  // Set up scroll event listener
  useEffect(() => {
    window.addEventListener('scroll', combinedScrollHandler);

    // Cleanup function
    return () => {
      window.removeEventListener('scroll', combinedScrollHandler);
      // Clear any pending timeouts
      if (throttleTimeout.current) {
        clearTimeout(throttleTimeout.current);
      }
      if (debounceTimeout.current) {
        clearTimeout(debounceTimeout.current);
      }
    };
  }, [combinedScrollHandler]);

  return scrollState;
};