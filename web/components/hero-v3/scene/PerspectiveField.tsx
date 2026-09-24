export function PerspectiveField({ medium }: { medium: boolean }) {
  return <group position={[0, -2.35, -1.9]}>
    <gridHelper args={[24, medium ? 20 : 32, "#47735d", "#284838"]} material-transparent material-opacity={.31} />
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[.2, -.06, .6]}>
      <circleGeometry args={[3.6, 64]} />
      <meshBasicMaterial color="#46c48b" transparent opacity={.045} depthWrite={false} />
    </mesh>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -.08, 0]}>
      <planeGeometry args={[24, 24]} />
      <meshBasicMaterial color="#07120f" transparent opacity={.16} depthWrite={false} />
    </mesh>
  </group>;
}
