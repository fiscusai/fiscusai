type Props = { title?: string; description?: string; action?: React.ReactNode }
export default function EmptyState({ title = 'Kayıt yok', description = 'Henüz veri eklenmemiş görünüyor.', action }: Props) {
  return (
    <div className="rounded-xl border border-zinc-200/60 bg-white p-8 text-center shadow-sm">
      <div className="mx-auto mb-3 h-10 w-10 rounded-full border border-amber-500/40 grid place-items-center">∅</div>
      <h3 className="font-display text-lg">{title}</h3>
      <p className="text-zinc-600 mt-1">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
