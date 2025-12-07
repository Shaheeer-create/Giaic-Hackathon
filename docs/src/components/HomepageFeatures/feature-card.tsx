"use client"

import { motion } from "framer-motion"
import type { LucideIcon } from "lucide-react"

interface FeatureCardProps {
  title: string
  description: string
  icon: LucideIcon
  color: string
  delay: number
  isInView: boolean
}

export default function FeatureCard({ title, description, icon: Icon, color, delay, isInView }: FeatureCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
      transition={{ duration: 0.7, delay: delay * 0.1, ease: "easeOut" }}
      whileHover={{ y: -8, transition: { duration: 0.3 } }}
      className="group relative"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-accent/20 via-transparent to-primary/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur" />

      <div className="relative p-8 rounded-2xl bg-card border border-border/50 hover:border-accent/50 transition-all duration-300 backdrop-blur-sm">
        {/* Icon container with gradient background */}
        <div className={`mb-6 inline-flex p-4 rounded-xl bg-gradient-to-br ${color} bg-opacity-15`}>
          <Icon className={`w-6 h-6 text-${color.split(" ")[0]} text-accent`} />
        </div>

        {/* Animated line accent */}
        <motion.div
          initial={{ width: 0 }}
          animate={isInView ? { width: 40 } : { width: 0 }}
          transition={{ duration: 0.8, delay: delay * 0.1 + 0.2 }}
          className={`mb-4 h-1 bg-gradient-to-r ${color} rounded-full`}
        />

        {/* Content */}
        <h3 className="text-xl font-semibold mb-3 text-foreground">{title}</h3>
        <p className="text-muted-foreground leading-relaxed text-sm md:text-base">{description}</p>

        {/* Hover arrow indicator */}
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          whileHover={{ opacity: 1, x: 0 }}
          className="mt-6 flex items-center text-accent text-sm font-medium"
        >
          Learn more <span className="ml-2">→</span>
        </motion.div>
      </div>
    </motion.div>
  )
}
