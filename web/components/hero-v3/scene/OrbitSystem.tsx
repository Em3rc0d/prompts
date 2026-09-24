"use client";

import { useMemo } from "react";
import * as THREE from "three";

export function OrbitSystem({ medium }: { medium: boolean }) {
  const paths = useMemo(() => [
    { rx: 3.5, ry: 1.35, z: -.6, color: "#72dba8", opacity: .42 },
    { rx: 2.85, ry: 1.02, z: -.95, color: "#a9e9ca", opacity: .21 },
    { rx: 4.15, ry: 1.7, z: -1.15, color: "#60c793", opacity: .14 }
  ].map((item, index) => ({ ...item, geometry: new THREE.BufferGeometry().setFromPoints(
    Array.from({ length: 129 }, (_, i) => {
      const theta = i / 128 * Math.PI * 2;
      return new THREE.Vector3(Math.cos(theta) * item.rx, Math.sin(theta) * item.ry * .48 - .08,
        Math.sin(theta) * item.ry * .88 + item.z - index * .08);
    })
  ) })), []);
  return <group>
    {paths.slice(0, medium ? 2 : 3).map((path, index) => <lineLoop key={index} geometry={path.geometry}>
      <lineBasicMaterial color={path.color} transparent opacity={path.opacity} depthWrite={false} />
    </lineLoop>)}
    {[[ -3.22, .21, -.15 ], [3.1, .22, -.1], [-2.63, -1.04, -.25], [2.76, -.94, -.3]].map((pos, i) => <mesh key={i} position={pos as [number, number, number]}>
      <sphereGeometry args={[i === 3 ? .053 : .038, 10, 10]} />
      <meshBasicMaterial color="#acffcf" />
    </mesh>)}
  </group>;
}
