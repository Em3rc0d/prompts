"use client";

import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

function roundedSlab() {
  const w = 3.35, h = 2.5, r = .2;
  const s = new THREE.Shape();
  s.moveTo(-w / 2 + r, -h / 2);
  s.lineTo(w / 2 - r, -h / 2);
  s.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r);
  s.lineTo(w / 2, h / 2 - r);
  s.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2);
  s.lineTo(-w / 2 + r, h / 2);
  s.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r);
  s.lineTo(-w / 2, -h / 2 + r);
  s.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
  return s;
}

const heights = [-1.02, -.38, .26, .9];

export function CentralStack() {
  const geometry = useMemo(() => new THREE.ExtrudeGeometry(roundedSlab(), {
    depth: .15, bevelEnabled: true, bevelSize: .065, bevelThickness: .045,
    bevelSegments: 3, curveSegments: 10, steps: 1
  }), []);
  const group = useRef<THREE.Group>(null);
  const start = useRef<number | null>(null);
  useFrame(({ clock, invalidate }) => {
    if (!group.current) return;
    if (start.current === null) start.current = clock.elapsedTime;
    const t = Math.min((clock.elapsedTime - start.current) / .46, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    group.current.position.y = (ease - 1) * .35;
    group.current.scale.setScalar(1.04 + ease * .08);
    if (t < 1) invalidate();
  });
  return <group ref={group} rotation={[-.94, 0, -.36]} position={[0, .12, 0]}>
    {heights.map((z, index) => <group key={z} position={[0, 0, z]}>
      <mesh geometry={geometry}>
        <meshPhysicalMaterial attach="material-0" color={index === 3 ? "#273731" : "#192a27"}
          transparent opacity={index === 3 ? .64 : .48} roughness={index === 3 ? .18 : .3}
          metalness={.045} clearcoat={1} clearcoatRoughness={.075} depthWrite={false} side={THREE.DoubleSide} />
        <meshPhysicalMaterial attach="material-1" color="#3e6154" transparent opacity={.58}
          roughness={.22} metalness={.06} emissive="#267f58" emissiveIntensity={.07} depthWrite={false} />
      </mesh>
      <lineLoop position={[0, 0, .198]}>
        <bufferGeometry attach="geometry" onUpdate={(self) => self.setFromPoints([
          new THREE.Vector3(-1.48, -1.18, 0), new THREE.Vector3(1.48, -1.18, 0),
          new THREE.Vector3(1.61, -.99, 0), new THREE.Vector3(1.61, .99, 0),
          new THREE.Vector3(1.48, 1.18, 0), new THREE.Vector3(-1.48, 1.18, 0),
          new THREE.Vector3(-1.61, .99, 0), new THREE.Vector3(-1.61, -.99, 0)
        ])} />
        <lineBasicMaterial color={index === 3 ? "#e1fff1" : "#8fdfb4"} transparent opacity={index === 3 ? .84 : .4} />
      </lineLoop>
    </group>)}
    <mesh position={[0, 0, 1.18]} rotation={[Math.PI / 2, 0, 0]}>
      <cylinderGeometry args={[.49, .49, .075, 64]} />
      <meshPhysicalMaterial color="#091f19" roughness={.2} metalness={.16} clearcoat={1} />
    </mesh>
    <mesh position={[0, 0, 1.24]}>
      <torusGeometry args={[.41, .019, 8, 64]} />
      <meshBasicMaterial color="#adffd7" />
    </mesh>
    <group position={[0, 0, 1.256]}>
      <mesh position={[-.145, 0, 0]} rotation={[0, 0, .5]}>
        <boxGeometry args={[.055, .6, .028]} /><meshBasicMaterial color="#b6ffdc" />
      </mesh>
      <mesh position={[.145, 0, 0]} rotation={[0, 0, -.5]}>
        <boxGeometry args={[.055, .6, .028]} /><meshBasicMaterial color="#b6ffdc" />
      </mesh>
    </group>
  </group>;
}
