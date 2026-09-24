import * as THREE from "three";

const panels = [
  [-3.6, .8, -3.6, 1.3, 2.5, .22],
  [-1.9, 1.6, -5.1, .8, 3.7, .15],
  [2.85, .6, -3.8, 1.35, 2.7, .23],
  [4.2, -.3, -5.8, 1.2, 3.2, .13],
  [.75, 1.9, -6.8, .72, 3.9, .12]
] as const;

const traces = [
  [-3.7, 1.25, -3.4], [-2.75, .1, -4.8], [-1.2, 2.2, -5.7],
  [2.4, 1.65, -4.9], [3.65, .35, -3.9], [4.4, 1.6, -6.2]
] as const;

export function AmbientDepth({ medium }: { medium: boolean }) {
  return <group>
    {panels.slice(0, medium ? 3 : 5).map(([x, y, z, w, h, opacity], index) =>
      <group key={index} position={[x, y, z]} rotation={[0, index % 2 ? -.34 : .25, 0]}>
        <mesh>
          <planeGeometry args={[w, h]} />
          <meshPhysicalMaterial color="#244d3f" transparent opacity={opacity}
            side={THREE.DoubleSide} depthWrite={false} roughness={.22} metalness={.2} clearcoat={1} />
        </mesh>
        <mesh position={[-w / 2, 0, .01]}>
          <planeGeometry args={[.012, h]} />
          <meshBasicMaterial color="#77e9b2" transparent opacity={opacity * 1.7} depthWrite={false} />
        </mesh>
      </group>)}
    {traces.slice(0, medium ? 3 : 6).map(([x, y, z], index) => <group key={index} position={[x, y, z]}>
      <mesh>
        <cylinderGeometry args={[.006, .006, index % 2 ? 1.6 : 2.8, 6]} />
        <meshBasicMaterial color="#64cfa0" transparent opacity={index % 2 ? .14 : .23} depthWrite={false} />
      </mesh>
      <mesh position={[0, index % 2 ? .15 : -.3, .03]}>
        <sphereGeometry args={[index % 2 ? .025 : .045, 12, 12]} />
        <meshBasicMaterial color="#b0ffda" toneMapped={false} />
      </mesh>
    </group>)}
    {!medium && Array.from({ length: 18 }, (_, i) => {
      const x = Math.sin(i * 12.7) * 4.7;
      const y = Math.cos(i * 4.3) * 2.3;
      const z = -2.5 - i % 5;
      return <mesh key={i} position={[x, y, z]}>
        <sphereGeometry args={[i % 4 ? .013 : .027, 6, 6]} />
        <meshBasicMaterial color="#a2eec8" transparent opacity={i % 4 ? .25 : .45} depthWrite={false} />
      </mesh>;
    })}
  </group>;
}
