export function PerspectiveField({ medium }: { medium: boolean }) {
  return <group position={[0, -2.15, -1.35]}>
    <gridHelper args={[22, medium ? 20 : 28, "#315c4b", "#234134"]} material-transparent material-opacity={.13} />
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -.08, 0]}>
      <planeGeometry args={[22, 22]} />
      <meshBasicMaterial color="#07120f" transparent opacity={.24} depthWrite={false} />
    </mesh>
  </group>;
}
