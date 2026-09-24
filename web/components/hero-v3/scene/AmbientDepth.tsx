import * as THREE from "three";

export function AmbientDepth({ medium }: { medium: boolean }) {
  const planes = medium ? [[-2.9, .45, -4], [3, 1.2, -3.5]] : [
    [-3.4, .6, -4], [-1.7, 1.8, -5.4], [2.8, 1.3, -4.2], [3.7, -.25, -5]
  ];
  return <group>
    {planes.map(([x,y,z], index) => <mesh key={index} position={[x,y,z]} rotation={[0, index % 2 ? -.25 : .3, 0]}>
      <planeGeometry args={[1.25, 1.9]} />
      <meshPhysicalMaterial color="#2e6d51" transparent opacity={.075} side={THREE.DoubleSide}
        depthWrite={false} roughness={.25} metalness={0} />
    </mesh>)}
  </group>;
}
