"use client"
import { useState, useEffect, useRef } from 'react';

interface UseOnVisibleParams {
  /** Threshold ratio (0-1) for visibility changes */
  threshold?: number | number[];
  /** Root element for the observer */
  root?: Element | null;
  /** Margin around the root element */
  rootMargin?: string;
}

interface VisibilityState {
  /** Whether the element is visible */
  isVisible: boolean;
  /** Current visible ratio (0-1) */
  intersectionRatio: number;
}

export const useOnVisible = (
  elementId: string,
  {
    threshold = 0.1,
    root = null,
    rootMargin = '0px'
  }: UseOnVisibleParams = {}
): VisibilityState => {
  const [visibility, setVisibility] = useState<VisibilityState>({
    isVisible: false,
    intersectionRatio: 0
  });

  const observerRef = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    // Find target element by ID
    const targetElement = document.getElementById(elementId);

    if (!targetElement) {
      console.warn(`Element with id ${elementId} not found`);
      return;
    }

    // IntersectionObserver callback handler
    const handleIntersect: IntersectionObserverCallback = (entries) => {
      entries.forEach(entry => {
        setVisibility({
          isVisible: entry.isIntersecting,
          intersectionRatio: entry.intersectionRatio
        });
      });
    };

    // Clean up previous observer
    if (observerRef.current) {
      observerRef.current.disconnect();
    }

    // Create new observer instance
    observerRef.current = new IntersectionObserver(handleIntersect, {
      threshold,
      root,
      rootMargin
    });

    // Start observing the target element
    observerRef.current.observe(targetElement);

    // Cleanup function for effect
    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, [elementId, threshold, root, rootMargin]);

  return visibility;
};