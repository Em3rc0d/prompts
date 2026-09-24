"use client";

import { useMemo } from "react";
import * as THREE from "three";

export function OrbitSystem({ medium }: { medium: boolean }) {
  const paths = useMemo(() => [
    { rx: 4.3, ry: 1.8, z: -.55, color: "#72dba8", opacity: .35 },
    { rx: 3.05, ry: 1.32, z: -1.3, color: "#a9e9ca", opacity: .2 },
    { rx: 5.4, ry: 2.15, z: -2.5, color: "#60c793", opacity: .1 }
  ].map((item, index) => ({ ...item, geometry: new THREE.BufferGeometry().setFromPoints(
    Array.from({ length: 129 }, (_, i) => {
      const theta = i / 128 * Math.PI * 2;
      return new THREE.Vector3(Math.cos(theta) * item.rx + index * .32,
        Math.sin(theta) * item.ry * .34 - .22 - index * .18,
        Math.sin(theta) * item.ry * .95 + item.z);
    })
  ) })), []);
  return <group>
    {paths.slice(0, medium ? 2 : 3).map((path, index) => <lineLoop key={index} geometry={path.geometry}>
      <lineBasicMaterial color={path.color} transparent opacity={path.opacity} depthWrite={false} />
    </lineLoop>)}
    {[[ -4.07, -.3, -.28 ], [3.8, -.12, -.18], [-2.7, -1.12, -.42], [3.14, -1.03, .08]].map((pos, i) => <group key={i} position={pos as [number, number, number]}>
      <mesh>
        <sphereGeometry args={[i === 3 ? .078 : .05, 12, 12]} />
        <meshBasicMaterial color="#b5ffdf" toneMapped={false} />
      </mesh>
      <mesh>
        <sphereGeometry args={[i === 3 ? .14 : .1, 12, 12]} />
        <meshBasicMaterial color="#45ca8d" transparent opacity={.14} depthWrite={false} />
      </mesh>
    </group>)}
  </group>;
}
