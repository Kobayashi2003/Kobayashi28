"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { VNDetailsPanel } from "@/components/panel/VNDetails/VNDetailsPanel"

import type {
  VN, Release, Character, Producer, Staff, Tag, Trait
} from "@/lib/types"
import { api } from "@/lib/api"

export default function ItemPage() {

  const params = useParams()
  const type = params.type as string
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [notFound, setNotFound] = useState(false)

  const [vn, setVN] = useState<VN | null>(null)
  const [release, setRelease] = useState<Release | null>(null)
  const [character, setCharacter] = useState<Character | null>(null)
  const [producer, setProducer] = useState<Producer | null>(null)
  const [staff, setStaff] = useState<Staff | null>(null)
  const [tag, setTag] = useState<Tag | null>(null)
  const [trait, setTrait] = useState<Trait | null>(null)

  const [abortController, setAbortController] = useState<AbortController | null>(null)

  const clearItems = () => {
    setVN(null)
    setRelease(null)
    setCharacter(null)
    setProducer(null)
    setStaff(null)
    setTag(null)
    setTrait(null)
  }

  const fetchItem = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      setLoading(true)
      setError(null)
      setNotFound(false)

      switch (type) {
        case "v":
          const vn = await api.by_id.vn(id, newController.signal)
          if (!vn) {
            setNotFound(true)
            break;
          }
          setVN(vn)
          break;
        case "r":
          const release = await api.by_id.release(id, newController.signal)
          if (!release) {
            setNotFound(true)
            break;
          }
          setRelease(release)
          break;
        case "c":
          const character = await api.by_id.character(id, newController.signal)
          if (!character) {
            setNotFound(true)
            break;
          }
          setCharacter(character)
          break;
        case "p":
          const producer = await api.by_id.producer(id, newController.signal)
          if (!producer) {
            setNotFound(true)
            break;
          }
          setProducer(producer)
          break;
        case "s":
          const staff = await api.by_id.staff(id, newController.signal)
          if (!staff) {
            setNotFound(true)
            break;
          }
          setStaff(staff)
          break;
        case "g":
          const tag = await api.by_id.tag(id, newController.signal)
          if (!tag) {
            setNotFound(true)
            break;
          }
          setTag(tag)
          break;
        case "i":
          const trait = await api.by_id.trait(id, newController.signal)
          if (!trait) {
            setNotFound(true)
            break;
          }
          setTrait(trait)
          break;
        default:
          setNotFound(true)
          break;
      }
    } catch (error) {
      setError(error as string)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchItem()
    return () => {
      abortController?.abort()
    }
  }, [])

  const fadeInAnimation = {
    initial: { filter: "blur(20px)", opacity: 0 },
    animate: { filter: "blur(0px)", opacity: 1 },
    exit: { filter: "blur(20px)", opacity: 0 },
    transition: { duration: 0.4, ease: "easeInOut" }
  }
  const statusStyle = "flex-grow flex justify-center items-center"

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      <AnimatePresence mode="wait">
        {/* Loading */}
        {loading && (
          <motion.div
            key="loading"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <Loading message="Loading..." />
          </motion.div>
        )}
        {/* Error */}
        {error && (
          <motion.div
            key="error"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <Error message={`Error: ${error}`} />
          </motion.div>
        )}
        {/* Not Found */}
        {notFound && (
          <motion.div
            key="notfound"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <NotFound message="No items found" />
          </motion.div>
        )}
        {/* Item Test */}
        {!loading && !error && !notFound && (
          <motion.div>
            {type === "v" && vn && <VNDetailsPanel vn={vn} />}
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  )
}