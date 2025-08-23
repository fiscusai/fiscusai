type Props = { title?: string; description?: string; retry?: () => void }
export default function ErrorState({ title = 'Bir şeyler ters gitti', description = 'Lütfen tekrar deneyin.', retry }: Props) {
  return (
    <div className="rounded-xl border border-red-200/60 bg-white p-8 text-center shadow-sm">
      <div className="mx-auto mb-3 h-10 w-10 rounded-full border border-red-500/50 grid place-items-center">!</div>
      <h3 className="font-display text-lg text-red-700">{title}</h3>
      <p className="text-zinc-700 mt-1">{description}</p>
      {retry && <button onClick={retry} className="mt-4 px-4 py-2 border border-zinc-300 rounded-md hover:shadow-sm">Tekrar Dene</button>}
    </div>
  )
}
