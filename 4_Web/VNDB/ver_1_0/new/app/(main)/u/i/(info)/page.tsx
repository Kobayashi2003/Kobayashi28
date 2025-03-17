"use client"

import { useState, useEffect } from "react"
import { useUserContext } from "@/context/UserContext"

export default function UserInfoPage() {
  const { user } = useUserContext()

  const fontSizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
  const textColors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "gray", "black", "white"]
  const [currentFontSize, setCurrentFontSize] = useState<number>(fontSizes[0])
  const [currentTextColor, setCurrentTextColor] = useState<string>(textColors[0])
  const [opacity, setOpacity] = useState<number>(1)
  const [transform, setTransform] = useState<string>("scale(1) rotate(0deg)")

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFontSize(fontSizes[Math.floor(Math.random() * fontSizes.length)])
      setCurrentTextColor(textColors[Math.floor(Math.random() * textColors.length)])
      setTransform(`scale(${Math.random() * (1.5 - 0.8) + 0.8}) rotate(${Math.random() * 360}deg)`)
      setOpacity(Math.random() * (1 - 0.5) + 0.5)
    }, 100)
    return () => clearInterval(interval)
  }, [user])

  return (
    <div className="w-full min-h-screen flex flex-col md:flex-row justify-center items-center overflow-hidden">
      <div className="font-bold transition-transform duration-300 ease-in-out"
        style={{
          fontSize: `${currentFontSize}px`,
          color: currentTextColor,
          transform: transform,
          opacity: opacity,
        }}
      >
        {user?.username}
      </div>
    </div>
  )
}