/**
 * @file This file exports a VisuallyHidden component, which hides content visually but keeps it accessible to screen readers.
 */

import { cn } from "@/lib/utils"

/**
 * VisuallyHidden component hides content visually but keeps it accessible to screen readers.
 * @param props - The props for the component.
 * @returns The VisuallyHidden component.
 */
export const VisuallyHidden = ({ children, ...props }: { children: React.ReactNode; [x: string]: any }) => (
  <span className={cn("sr-only", props.className)} {...props}>
    {children}
  </span>
)