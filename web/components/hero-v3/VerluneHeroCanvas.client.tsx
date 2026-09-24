"use client";

import { Canvas } from "@react-three/fiber";
import { CentralStack } from "./scene/CentralStack";
import { SceneLighting } from "./scene/SceneLighting";
import { PerspectiveField } from "./scene/PerspectiveField";
import { AmbientDepth } from "./scene/AmbientDepth";
import { OrbitSystem } from "./scene/OrbitSystem";

export default function VerluneHeroCanvas({ medium, onReady }: { medium: boolean; onReady: () => void }) {
  return <Canvas
    className="vHero3Canvas"
    camera={{ position: [0, 1.6, 9.8], fov: 44, near: .1, far: 70 }}
    dpr={medium ? [1, 1.25] : [1, 1.6]}
    frameloop="demand"
    gl={{ alpha: true, antialias: true, powerPreference: "high-performance" }}
    onCreated={({ gl }) => { gl.setClearColor("#090d0f", 0); onReady(); }}
  >
    <SceneLighting />
    <AmbientDepth medium={medium} />
    <PerspectiveField medium={medium} />
    <OrbitSystem medium={medium} />
    <CentralStack />
  </Canvas>;
}
