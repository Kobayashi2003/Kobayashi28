"use client"

import { useEffect, useRef, useState } from "react"
import { IMGSERVE_BASE_URL } from "@/lib/constants"

// Animation frame loop optimization
const useAnimationFrame = (callback: () => void) => {
  const requestRef = useRef<number>(undefined)

  const animate = () => {
    callback()
    requestRef.current = requestAnimationFrame(animate)
  }

  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate)
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current)
    }
  }, [])
}

export default function VNDBBackground() {
  // Background states
  const [bgUrls, setBgUrls] = useState([`url(${IMGSERVE_BASE_URL}/bg)`, `url(${IMGSERVE_BASE_URL}/bg)`])
  const [activeBgIndex, setActiveBgIndex] = useState(0)
  
  // Cursor and animation refs
  const mouse = useRef({ x: 0, y: 0, smoothX: 0, smoothY: 0 })
  const lightRef = useRef<SVGFEPointLightElement>(null)
  const turbulenceRef = useRef<SVGFETurbulenceElement>(null)
  const cursorPointRef = useRef<HTMLDivElement>(null)
  const cursorLightRef = useRef<HTMLDivElement>(null)
  const noise = useRef(0)
  
  // UI states
  const [gradientPos, setGradientPos] = useState({ x: 50, y: 50 })
  const [mounted, setMounted] = useState(false)

  // Background image preloader
  const preloadBackground = (index: number) => {
    const img = new Image()
    const timestamp = Date.now()
    img.src = `${IMGSERVE_BASE_URL}/bg?t=${timestamp}`
    img.onload = () => {
      setBgUrls(prev => {
        const newUrls = [...prev]
        newUrls[index] = `url(${img.src})`
        return newUrls
      })
    }
  }

  // Mount initialization
  useEffect(() => {
    setMounted(true)
    preloadBackground(1) // Preload second background
  }, [])

  // Mouse movement handler
  useEffect(() => {
    if (!mounted) return

    const handleMouseMove = (e: MouseEvent) => {
      mouse.current.x = e.pageX
      mouse.current.y = e.pageY
      setGradientPos({
        x: (mouse.current.x / window.innerWidth) * 100,
        y: (mouse.current.y / window.innerHeight) * 100
      })
    }

    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [mounted])

  // Animation logic
  useAnimationFrame(() => {
    if (!lightRef.current || !turbulenceRef.current || !cursorPointRef.current || !cursorLightRef.current) return

    // Smooth cursor interpolation
    mouse.current.smoothX += (mouse.current.x - mouse.current.smoothX) * 0.1
    mouse.current.smoothY += (mouse.current.y - mouse.current.smoothY) * 0.1

    // Update light position
    lightRef.current.setAttribute("x", `${mouse.current.smoothX}`)
    lightRef.current.setAttribute("y", `${mouse.current.smoothY}`)

    // Get dynamic cursor element sizes
    const pointRect = cursorPointRef.current.getBoundingClientRect()
    const lightRect = cursorLightRef.current.getBoundingClientRect()

    // Update cursor positions (centered)
    cursorPointRef.current.style.transform = `translate(
      ${mouse.current.smoothX - pointRect.width / 2}px,
      ${mouse.current.smoothY - pointRect.height / 2}px
    )`

    cursorLightRef.current.style.transform = `translate(
      ${mouse.current.smoothX - lightRect.width / 2}px,
      ${mouse.current.smoothY - lightRect.height / 2}px
    )`

    // Update noise effect
    noise.current += 0.5
    turbulenceRef.current.setAttribute("seed", `${Math.round(noise.current)}`)
  })

  // Background rotation logic
  useEffect(() => {
    const interval = setInterval(() => {
      const nextIndex = activeBgIndex === 0 ? 1 : 0
      setActiveBgIndex(nextIndex)
      preloadBackground(nextIndex)
    }, 1000 * 4)

    return () => clearInterval(interval)
  }, [activeBgIndex])

  return (
    <div className="relative min-h-screen cursor-none">
      {/* Background layers */}
      <div className="absolute inset-0 z-0">
        {bgUrls.map((url, index) => (
          <div
            key={index}
            className={`absolute inset-0 h-full w-full transition-opacity duration-3000`}
            style={{
              backgroundImage: url,
              backgroundSize: "cover",
              backgroundPosition: "center",
              opacity: index === activeBgIndex ? 1 : 0,
            }}
          />
        ))}
        
        {/* Dynamic gradient overlay */}
        <div
          className="absolute inset-0"
          style={{
            background: `radial-gradient(
              circle at ${gradientPos.x}% ${gradientPos.y}%,
              rgba(0, 0, 0, 0.6) 0%,
              rgba(0, 0, 0, 0.98) 100%
            )`,
          }}
        />
      </div>

      {/* Main content */}
      <div className="content-container relative z-10 h-screen w-full">
        <h1 className="title">VNDB</h1>
        <div className="subtitle">Visual Novel Database -- By KOBAYASHI</div>
        <button 
          className="frosted-glass-button"
          onClick={() => window.location.href = '/'}
        >
          Go To Home -&gt;
        </button>
      </div>

      {/* Cursor elements */}
      <div ref={cursorPointRef} className="cursor-point" />
      <div ref={cursorLightRef} className="cursor-light" />

      {/* SVG filters */}
      <svg className="svg-filters" xmlns="http://www.w3.org/2000/svg">
        <filter id="light">
          <feSpecularLighting
            result="specOut"
            surfaceScale="1"
            specularConstant="1.2"
            specularExponent="10"
            lightingColor="#666"
          >
            <fePointLight ref={lightRef} x="50" y="75" z="100" />
          </feSpecularLighting>
        </filter>
        <filter id="noise">
          <feTurbulence ref={turbulenceRef} type="fractalNoise" baseFrequency="0.999 0.999" seed="1" numOctaves="10" />
          <feColorMatrix type="saturate" values="0" />
          <feComponentTransfer result="noise">
            <feFuncA type="linear" slope="1" />
          </feComponentTransfer>
          <feBlend in="noise" in2="SourceGraphic" mode="multiply" />
        </filter>
      </svg>

      {/* Global styles */}
      <style jsx global>{`
        .content-container {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          filter: url('#noise') url('#light');
          color: white;
          pointer-events: none;
        }

        .title {
          font-family: 'Arial', sans-serif;
          font-size: 10vw;
          letter-spacing: 0.2em;
          margin: 0;
          text-transform: uppercase;
          text-shadow: 0 0 20px rgba(255,255,255,0.2);
          white-space: nowrap;
        }

        .subtitle {
          font-family: 'Arial', sans-serif;
          font-size: 1.5rem;
          letter-spacing: 0.3em;
          margin-top: 1.5em;
          opacity: 0.8;
        }

        .frosted-glass-button {
          margin-top: 2rem;
          padding: 1rem 2.5rem;
          font-size: 1.2rem;
          font-weight: 500;
          letter-spacing: 0.1em;
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 50px;
          color: white;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
          pointer-events: auto !important;
        }

        .frosted-glass-button:hover {
          background: rgba(255, 255, 255, 0.15);
          transform: scale(1.05);
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .frosted-glass-button:active {
          transform: scale(0.95);
        }

        .frosted-glass-button::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.05);
          z-index: -1;
          border-radius: 50px;
        }

        .cursor-point {
          position: fixed;
          width: 6px;
          height: 6px;
          background: white;
          border-radius: 50%;
          pointer-events: none;
          z-index: 999;
          transition: transform 0.1s linear;
        }

        .cursor-light {
          position: fixed;
          width: 48px;
          height: 48px;
          background: white;
          border-radius: 50%;
          opacity: 0.08;
          pointer-events: none;
          z-index: 998;
          transition: transform 0.2s ease-out;
        }

        .svg-filters {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: -1;
        }
        
        @media (max-width: 768px) {
          .subtitle {
            font-size: 1rem;
            letter-spacing: 0.2em;
          }

          .frosted-glass-button {
            padding: 0.8rem 2rem;
            font-size: 1rem;
          }
          
          .cursor-light {
            width: 24px;
            height: 24px;
          }
        }
      `}</style>
    </div>
  )
}