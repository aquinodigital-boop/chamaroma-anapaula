import React, { useState, useCallback, useRef } from 'react'
import { Flame, SprayCan, Upload, Loader2, Copy, Check, Download, ImageIcon, Video, Instagram, BookOpen, Zap, Crown, ChevronDown, ChevronUp, Sparkles, Eye, X, RefreshCw } from 'lucide-react'
import { Aroma, AROMA_CATEGORIES, GeneratedPrompts, PROMPT_KEYS, PROMPT_LABELS, Category, VideoScripts, InstagramPost } from './types'

const API = '/api'

// Category config
const CATEGORY_CONFIG: Record<Category, { label: string; emoji: string; icon: React.ReactNode; color: string }> = {
  velas: { label: 'Velas', emoji: '🕯️', icon: <Flame size={20} />, color: 'from-flame to-orange-600' },
  home_spray: { label: 'Home Spray', emoji: '💨', icon: <SprayCan size={20} />, color: 'from-cyan-500 to-blue-500' },
}

// PromptCard Component
const PromptCard = ({
  promptKey,
  prompt,
  mode,
  onModeChange,
  onGenerate,
  loading,
  imageSrc,
  onDownload,
  watermark
}: {
  promptKey: string
  prompt: string
  mode: 'flash' | 'pro'
  onModeChange: (key: string, mode: 'flash' | 'pro') => void
  onGenerate: (key: string, mode: 'flash' | 'pro') => void
  loading: boolean
  imageSrc?: string
  onDownload: (key: string) => void
  watermark: string
}) => {
  const [expanded, setExpanded] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(prompt)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="card animate-fade-in-up">
      <div className="flex justify-between items-start mb-4">
        <h3 className="font-semibold text-studio-100">{PROMPT_LABELS[promptKey as any]}</h3>
        <button onClick={() => setExpanded(!expanded)} className="text-studio-400 hover:text-studio-200">
          {expanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>
      </div>

      {expanded && (
        <div className="mb-4 p-3 bg-studio-900 rounded-lg border border-studio-700">
          <p className="text-sm text-studio-200 leading-relaxed whitespace-pre-wrap">{prompt}</p>
          <button onClick={handleCopy} className="mt-3 text-xs text-accent hover:text-accent-light flex items-center gap-2">
            {copied ? <Check size={14} /> : <Copy size={14} />}
            {copied ? 'Copiado!' : 'Copiar'}
          </button>
        </div>
      )}

      <div className="flex gap-2 mb-4">
        {(['flash', 'pro'] as const).map(m => (
          <button
            key={m}
            onClick={() => onModeChange(promptKey, m)}
            className={`flex-1 py-2 rounded-lg text-xs font-medium transition-all ${
              mode === m
                ? 'bg-accent text-white shadow-lg shadow-accent/30'
                : 'bg-studio-700 text-studio-300 hover:bg-studio-600'
            }`}
          >
            {m === 'flash' ? <Zap className="inline mr-1" size={12} /> : <Crown className="inline mr-1" size={12} />}
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {imageSrc && (
        <div className="mb-4">
          <img src={imageSrc} alt="Generated" className="w-full rounded-lg mb-2 max-h-48 object-cover" />
          <button onClick={() => onDownload(promptKey)} className="w-full btn-secondary flex items-center justify-center gap-2">
            <Download size={14} /> Download
          </button>
        </div>
      )}

      <button
        onClick={() => onGenerate(promptKey, mode)}
        disabled={loading}
        className="w-full btn-primary flex items-center justify-center gap-2"
      >
        {loading ? <Loader2 size={16} className="animate-spin" /> : <ImageIcon size={16} />}
        Gerar Imagem
      </button>
    </div>
  )
}

// AromaCard Component
const AromaCard = ({
  aroma,
  onSelect
}: {
  aroma: Aroma
  onSelect: (aroma: Aroma) => void
}) => {
  return (
    <button
      onClick={() => onSelect(aroma)}
      className="card hover:border-accent/50 cursor-pointer text-left transform hover:scale-105 transition-all"
    >
      <div className="text-4xl mb-3">{aroma.emoji}</div>
      <div className="flex items-center gap-2 mb-2">
        <h3 className="font-semibold text-studio-100">{aroma.nome}</h3>
        <span className="text-xs px-2 py-1 rounded-full bg-studio-700 text-studio-300">
          {aroma.categoria}
        </span>
      </div>
      <p className="text-sm text-studio-300 mb-3 line-clamp-2">{aroma.descricao}</p>
      <div
        className="w-full h-12 rounded-lg border border-studio-600 mb-3"
        style={{ backgroundColor: aroma.mockup.hex_cera }}
      />
      <div className="flex flex-wrap gap-1">
        {aroma.notas_sensoriais.slice(0, 2).map((nota, i) => (
          <span key={i} className="text-xs bg-studio-700 text-studio-300 px-2 py-1 rounded">
            {nota}
          </span>
        ))}
      </div>
    </button>
  )
}

// AromaDetail Modal Component
const AromaDetail = ({
  aroma,
  onClose
}: {
  aroma: Aroma | null
  onClose: () => void
}) => {
  const [copiedSeo, setCopiedSeo] = useState(false)

  if (!aroma) return null

  const handleCopySeo = () => {
    navigator.clipboard.writeText(aroma.copy_raio_x.titulo_seo_ml)
    setCopiedSeo(true)
    setTimeout(() => setCopiedSeo(false), 2000)
  }

  const handleCopyAll = () => {
    const all = `
${aroma.copy_raio_x.titulo_seo_ml}

${aroma.copy_raio_x.bullets_matadores.map(b => `• ${b}`).join('\n')}

${aroma.copy_raio_x.gancho_emocional}

${aroma.copy_raio_x.descricao_sensorial}

${aroma.copy_raio_x.cta_fechamento}
    `.trim()
    navigator.clipboard.writeText(all)
  }

  return (
    <div className="modal-overlay flex items-center justify-center p-4 z-50" onClick={onClose}>
      <div className="card w-full max-w-2xl max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <button onClick={onClose} className="float-right mb-4">
          <X size={24} />
        </button>

        <div className="flex items-center gap-3 mb-6">
          <span className="text-5xl">{aroma.emoji}</span>
          <div>
            <h2 className="text-2xl font-bold">{aroma.nome}</h2>
            <span className="text-xs px-2 py-1 rounded-full bg-studio-700 text-studio-300">
              {aroma.categoria}
            </span>
          </div>
        </div>

        <p className="text-studio-200 mb-6">{aroma.descricao}</p>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-studio-900 rounded-lg p-4">
            <h4 className="text-xs font-semibold text-studio-400 mb-2">NOTAS</h4>
            <div className="flex flex-col gap-2">
              {aroma.notas_sensoriais.map((nota, i) => (
                <span key={i} className="text-sm text-studio-200">{nota}</span>
              ))}
            </div>
          </div>

          <div className="bg-studio-900 rounded-lg p-4">
            <h4 className="text-xs font-semibold text-studio-400 mb-2">MOOD</h4>
            <div className="flex flex-col gap-2">
              {aroma.mood.map((m, i) => (
                <span key={i} className="text-sm text-studio-200">{m}</span>
              ))}
            </div>
          </div>

          <div className="bg-studio-900 rounded-lg p-4">
            <h4 className="text-xs font-semibold text-studio-400 mb-2">OCASIÕES</h4>
            <div className="flex flex-col gap-2">
              {aroma.ocasioes.map((oc, i) => (
                <span key={i} className="text-sm text-studio-200">{oc}</span>
              ))}
            </div>
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Pirâmide Olfativa</h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-studio-700 rounded-lg p-4 text-center">
              <div className="text-sm text-studio-400 mb-2">SAÍDA</div>
              <div className="font-semibold text-studio-100">{aroma.piramide.saida}</div>
            </div>
            <div className="bg-studio-700 rounded-lg p-4 text-center">
              <div className="text-sm text-studio-400 mb-2">CORPO</div>
              <div className="font-semibold text-studio-100">{aroma.piramide.corpo}</div>
            </div>
            <div className="bg-studio-700 rounded-lg p-4 text-center">
              <div className="text-sm text-studio-400 mb-2">FUNDO</div>
              <div className="font-semibold text-studio-100">{aroma.piramide.fundo}</div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Copy Raio-X</h3>

          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs text-studio-400">TÍTULO SEO</label>
              <span className="text-xs text-studio-400">{aroma.copy_raio_x.titulo_seo_ml.length} chars</span>
            </div>
            <div className="bg-studio-900 rounded-lg p-3 text-studio-200 flex justify-between items-start">
              <span className="text-sm">{aroma.copy_raio_x.titulo_seo_ml}</span>
              <button onClick={handleCopySeo} className="ml-2 text-accent hover:text-accent-light">
                {copiedSeo ? <Check size={14} /> : <Copy size={14} />}
              </button>
            </div>
          </div>

          <div className="mb-4">
            <label className="text-xs text-studio-400 mb-2 block">BULLETS MATADORES</label>
            <ul className="space-y-2">
              {aroma.copy_raio_x.bullets_matadores.map((bullet, i) => (
                <li key={i} className="text-sm text-studio-200 flex gap-2">
                  <span className="text-accent">•</span> {bullet}
                </li>
              ))}
            </ul>
          </div>

          <div className="mb-4">
            <label className="text-xs text-studio-400 mb-2 block">GANCHO EMOCIONAL</label>
            <p className="bg-studio-900 rounded-lg p-3 text-sm text-studio-200">{aroma.copy_raio_x.gancho_emocional}</p>
          </div>

          <div className="mb-4">
            <label className="text-xs text-studio-400 mb-2 block">DESCRIÇÃO SENSORIAL</label>
            <p className="bg-studio-900 rounded-lg p-3 text-sm text-studio-200">{aroma.copy_raio_x.descricao_sensorial}</p>
          </div>

          <div className="mb-4">
            <label className="text-xs text-studio-400 mb-2 block">CTA FECHAMENTO</label>
            <p className="bg-studio-900 rounded-lg p-3 text-sm text-studio-200">{aroma.copy_raio_x.cta_fechamento}</p>
          </div>

          <button onClick={handleCopyAll} className="w-full btn-primary flex items-center justify-center gap-2">
            <Copy size={16} /> Copiar Tudo
          </button>
        </div>
      </div>
    </div>
  )
}

// Header Component
const Header = ({ activeTab, onTabChange }: { activeTab: string; onTabChange: (tab: string) => void }) => {
  const tabs = [
    { id: 'editor', label: 'Editor', icon: <Sparkles size={18} /> },
    { id: 'catalog', label: 'Catálogo', icon: <BookOpen size={18} /> },
    { id: 'video', label: 'Vídeo', icon: <Video size={18} /> },
    { id: 'instagram', label: 'Instagram', icon: <Instagram size={18} /> },
  ]

  return (
    <div className="sticky top-0 z-40 border-b border-studio-700 bg-studio-900/95 backdrop-blur">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="text-3xl">🕯️</div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-flame to-orange-600 bg-clip-text text-transparent">
                Chamaroma Studio
              </h1>
              <p className="text-xs text-studio-400">Content & Creative Suite</p>
            </div>
          </div>
        </div>

        <div className="flex gap-2 overflow-x-auto pb-2">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-accent text-white shadow-lg shadow-accent/30'
                  : 'bg-studio-800 text-studio-300 hover:bg-studio-700'
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// CategorySelector Component
const CategorySelector = ({
  selectedCategory,
  onSelect
}: {
  selectedCategory: Category | null
  onSelect: (cat: Category) => void
}) => {
  const categories: Category[] = ['velas', 'home_spray']

  return (
    <div className="grid grid-cols-2 gap-3">
      {categories.map(cat => {
        const config = CATEGORY_CONFIG[cat]
        return (
          <button
            key={cat}
            onClick={() => onSelect(cat)}
            className={`p-4 rounded-xl border-2 transition-all ${
              selectedCategory === cat
                ? `border-accent bg-gradient-to-br ${config.color}`
                : 'border-studio-700 bg-studio-800 hover:border-studio-600'
            }`}
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">{config.emoji}</span>
            </div>
            <div className={selectedCategory === cat ? 'text-white font-semibold' : 'text-studio-200 font-semibold'}>
              {config.label}
            </div>
          </button>
        )
      })}
    </div>
  )
}

// Main App
export default function App() {
  const [activeTab, setActiveTab] = useState('editor')

  // Editor state
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null)
  const [productName, setProductName] = useState('')
  const [hexCode, setHexCode] = useState('#f59e0b')
  const [selectedAroma, setSelectedAroma] = useState<string>('')
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [promptMode, setPromptMode] = useState<Record<string, 'flash' | 'pro'>>({})
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<GeneratedPrompts | null>(null)
  const [editedPrompts, setEditedPrompts] = useState<Record<string, string>>({})
  const [watermark, setWatermark] = useState('chamaroma')
  const [generatingImages, setGeneratingImages] = useState<Record<string, boolean>>({})
  const [generatedImages, setGeneratedImages] = useState<Record<string, string>>({})
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Catalog state
  const [aromas, setAromas] = useState<Aroma[]>([])
  const [aromasLoaded, setAromasLoaded] = useState(false)
  const [selectedAromaDetail, setSelectedAromaDetail] = useState<Aroma | null>(null)
  const [aromaFilter, setAromaFilter] = useState('todos')

  // Video state
  const [videoLoading, setVideoLoading] = useState(false)
  const [videoScripts, setVideoScripts] = useState<VideoScripts | null>(null)
  const [narrationLoading, setNarrationLoading] = useState(false)
  const [narrationText, setNarrationText] = useState('')
  const [productBrand, setProductBrand] = useState('')

  // Instagram state
  const [igLoading, setIgLoading] = useState(false)
  const [igPost, setIgPost] = useState<InstagramPost | null>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result as string)
    }
    reader.readAsDataURL(file)
  }

  const handleDragDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result as string)
    }
    reader.readAsDataURL(file)
  }

  const generatePrompts = async () => {
    if (!selectedCategory || !productName) {
      setError('Preencha categoria e nome do produto')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API}/prompts/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: selectedCategory,
          product_name: productName,
          hex_code: hexCode,
          aroma_id: selectedAroma || null,
          image_base64: imagePreview,
        }),
      })

      if (!response.ok) throw new Error('Erro ao gerar prompts')
      const data = await response.json()
      setResults(data)

      const initialModes: Record<string, 'flash' | 'pro'> = {}
      PROMPT_KEYS.forEach(key => {
        initialModes[key] = 'flash'
      })
      setPromptMode(initialModes)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido')
    } finally {
      setLoading(false)
    }
  }

  const generateImage = async (promptKey: string, mode: 'flash' | 'pro') => {
    if (!results) return

    const prompt = editedPrompts[promptKey] || results[promptKey as keyof GeneratedPrompts] as string
    setGeneratingImages(prev => ({ ...prev, [promptKey]: true }))

    try {
      const response = await fetch(`${API}/images/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          mode,
          watermark,
        }),
      })

      if (!response.ok) throw new Error('Erro ao gerar imagem')
      const data = await response.json()
      setGeneratedImages(prev => ({ ...prev, [promptKey]: data.image_url }))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao gerar imagem')
    } finally {
      setGeneratingImages(prev => ({ ...prev, [promptKey]: false }))
    }
  }

  const downloadImage = (promptKey: string) => {
    const url = generatedImages[promptKey]
    if (!url) return

    const a = document.createElement('a')
    a.href = url
    a.download = `${productName}-${promptKey}-${Date.now()}.png`
    a.click()
  }

  const loadAromas = async () => {
    if (aromasLoaded) return

    try {
      const response = await fetch(`${API}/aromas`)
      if (!response.ok) throw new Error('Erro ao carregar aromas')
      const data = await response.json()
      setAromas(data)
      setAromasLoaded(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar aromas')
    }
  }

  const generateVideoScripts = async () => {
    if (!selectedCategory || !productName) {
      setError('Preencha categoria e nome do produto')
      return
    }

    setVideoLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API}/videos/scripts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: selectedCategory,
          product_name: productName,
          aroma_id: selectedAroma || null,
        }),
      })

      if (!response.ok) throw new Error('Erro ao gerar scripts')
      const data = await response.json()
      setVideoScripts(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao gerar scripts')
    } finally {
      setVideoLoading(false)
    }
  }

  const generateNarration = async () => {
    if (!videoScripts) return

    setNarrationLoading(true)

    try {
      const response = await fetch(`${API}/videos/narration`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scripts: videoScripts,
          brand_name: productBrand,
        }),
      })

      if (!response.ok) throw new Error('Erro ao gerar narração')
      const data = await response.json()
      setNarrationText(data.narration)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao gerar narração')
    } finally {
      setNarrationLoading(false)
    }
  }

  const generateIgPost = async () => {
    if (!selectedCategory || !productName) {
      setError('Preencha categoria e nome do produto')
      return
    }

    setIgLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API}/instagram/post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: selectedCategory,
          product_name: productName,
          aroma_id: selectedAroma || null,
          hex_code: hexCode,
        }),
      })

      if (!response.ok) throw new Error('Erro ao gerar post')
      const data = await response.json()
      setIgPost(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao gerar post')
    } finally {
      setIgLoading(false)
    }
  }

  const filteredAromas = aromaFilter === 'todos'
    ? aromas
    : aromas.filter(a => a.categoria === aromaFilter)

  return (
    <div className="min-h-screen bg-studio-900 text-white">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {activeTab === 'editor' && (
          <div className="space-y-6">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Sparkles size={20} className="text-accent" />
                Configurar Produto
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-studio-300 mb-2">Categoria</label>
                  <CategorySelector selectedCategory={selectedCategory} onSelect={setSelectedCategory} />
                </div>

                <div>
                  <label className="block text-sm font-medium text-studio-300 mb-2">Nome do Produto</label>
                  <input
                    type="text"
                    value={productName}
                    onChange={e => setProductName(e.target.value)}
                    placeholder="Ex: Vela de Lavanda"
                    className="input-field w-full"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-studio-300 mb-2">Cor (HEX)</label>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={hexCode}
                        onChange={e => setHexCode(e.target.value)}
                        placeholder="#f59e0b"
                        className="input-field flex-1"
                      />
                      <div
                        className="w-12 h-12 rounded-lg border-2 border-studio-600"
                        style={{ backgroundColor: hexCode }}
                      />
                    </div>
                  </div>

                  {selectedCategory && ['velas', 'home_spray'].includes(selectedCategory) && (
                    <div>
                      <label className="block text-sm font-medium text-studio-300 mb-2">Aroma (opcional)</label>
                      <select
                        value={selectedAroma}
                        onChange={e => setSelectedAroma(e.target.value)}
                        className="input-field w-full"
                      >
                        <option value="">Selecionar aroma...</option>
                        {aromas.map(a => (
                          <option key={a.id} value={a.id}>{a.nome}</option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-studio-300 mb-2">Imagem Referência (opcional)</label>
                  <div
                    onDragOver={e => e.preventDefault()}
                    onDrop={handleDragDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className="border-2 border-dashed border-studio-600 rounded-xl p-8 text-center cursor-pointer hover:border-accent transition-colors"
                  >
                    {imagePreview ? (
                      <div>
                        <img src={imagePreview} alt="Preview" className="w-full max-h-32 object-cover rounded-lg mb-3 mx-auto" />
                        <button
                          type="button"
                          onClick={e => {
                            e.stopPropagation()
                            setImagePreview(null)
                          }}
                          className="text-sm text-accent hover:text-accent-light"
                        >
                          Remover imagem
                        </button>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center gap-2">
                        <Upload size={24} className="text-studio-400" />
                        <div className="text-sm text-studio-300">Arraste uma imagem aqui ou clique</div>
                      </div>
                    )}
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-studio-300 mb-2">Modo Padrão</label>
                    <div className="flex gap-2">
                      {(['flash', 'pro'] as const).map(m => (
                        <button
                          key={m}
                          onClick={() => {
                            const newModes: Record<string, 'flash' | 'pro'> = {}
                            PROMPT_KEYS.forEach(key => {
                              newModes[key] = m
                            })
                            setPromptMode(newModes)
                          }}
                          className={`flex-1 py-2 rounded-lg text-xs font-medium ${
                            Object.values(promptMode).every(mode => mode === m)
                              ? 'bg-accent text-white'
                              : 'bg-studio-700 text-studio-300'
                          }`}
                        >
                          {m.toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-studio-300 mb-2">Marca d'água</label>
                    <select
                      value={watermark}
                      onChange={e => setWatermark(e.target.value)}
                      className="input-field w-full"
                    >
                      <option value="chamaroma">Chamaroma Studio</option>
                      <option value="aquinobrasil">Aquino Brasil</option>
                      <option value="gama">Gama</option>
                      <option value="labor">Labor</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={generatePrompts}
                  disabled={loading || !selectedCategory || !productName}
                  className="w-full btn-primary flex items-center justify-center gap-2"
                >
                  {loading ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}
                  {loading ? 'Gerando Prompts...' : 'Gerar Prompts'}
                </button>
              </div>
            </div>

            {results && (
              <div className="space-y-4">
                <div className="card">
                  <h3 className="text-lg font-semibold mb-3">Análise</h3>
                  <p className="text-studio-200 mb-3">{results.analysis}</p>
                  <p className="text-sm text-studio-400 mb-4"><strong>Conceito:</strong> {results.creative_concept}</p>
                  <p className="text-sm text-studio-400"><strong>Intenção Visual:</strong> {results.visual_intention}</p>
                </div>

                <div>
                  <h2 className="text-xl font-semibold mb-4">Prompts Gerados</h2>
                  <div className="grid grid-cols-2 gap-4">
                    {PROMPT_KEYS.map(key => (
                      <PromptCard
                        key={key}
                        promptKey={key}
                        prompt={editedPrompts[key] || (results[key as keyof GeneratedPrompts] as string) || ''}
                        mode={promptMode[key] || 'flash'}
                        onModeChange={(k, m) => setPromptMode(prev => ({ ...prev, [k]: m }))}
                        onGenerate={generateImage}
                        loading={generatingImages[key] || false}
                        imageSrc={generatedImages[key]}
                        onDownload={downloadImage}
                        watermark={watermark}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'catalog' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  <BookOpen size={24} className="text-accent" />
                  Catálogo de Aromas
                </h2>
                <p className="text-studio-400 text-sm">Explore {filteredAromas.length} aromas disponíveis</p>
              </div>
            </div>

            <div className="flex gap-2 overflow-x-auto pb-2">
              {AROMA_CATEGORIES.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => setAromaFilter(cat.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
                    aromaFilter === cat.id
                      ? `bg-gradient-to-r ${cat.color} text-white shadow-lg`
                      : 'bg-studio-800 text-studio-300 hover:bg-studio-700'
                  }`}
                >
                  <span className="text-lg">{cat.emoji}</span>
                  {cat.label}
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    aromaFilter === cat.id ? 'bg-black/20' : 'bg-studio-700'
                  }`}>
                    {aromaFilter === cat.id ? filteredAromas.length : aromas.filter(a => a.categoria === cat.id).length}
                  </span>
                </button>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-4">
              {filteredAromas.map(aroma => (
                <AromaCard
                  key={aroma.id}
                  aroma={aroma}
                  onSelect={setSelectedAromaDetail}
                />
              ))}
            </div>

            <AromaDetail aroma={selectedAromaDetail} onClose={() => setSelectedAromaDetail(null)} />
          </div>
        )}

        {activeTab === 'video' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Video size={24} className="text-accent" />
              Gerador de Vídeos
            </h2>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Configuração</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-studio-300 mb-2">Nome da Marca</label>
                  <input
                    type="text"
                    value={productBrand}
                    onChange={e => setProductBrand(e.target.value)}
                    placeholder="Ex: Chamaroma"
                    className="input-field w-full"
                  />
                </div>

                <button
                  onClick={generateVideoScripts}
                  disabled={videoLoading || !selectedCategory || !productName}
                  className="btn-primary flex items-center justify-center gap-2"
                >
                  {videoLoading ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}
                  Gerar Scripts
                </button>

                {videoScripts && (
                  <button
                    onClick={generateNarration}
                    disabled={narrationLoading}
                    className="w-full btn-secondary flex items-center justify-center gap-2"
                  >
                    {narrationLoading ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}
                    Gerar Narração
                  </button>
                )}
              </div>
            </div>

            {videoScripts && (
              <div className="space-y-4">
                <div className="card">
                  <h3 className="font-semibold mb-3">Clips MercadoLivre</h3>
                  <div className="space-y-2">
                    {videoScripts.clips_ml?.map((clip, i) => (
                      <div key={i} className="bg-studio-900 rounded-lg p-3 text-sm text-studio-200">
                        {clip}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="card">
                  <h3 className="font-semibold mb-3">Instagram Feed</h3>
                  <div className="space-y-2">
                    {videoScripts.instagram_feed?.map((clip, i) => (
                      <div key={i} className="bg-studio-900 rounded-lg p-3 text-sm text-studio-200">
                        {clip}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="card">
                  <h3 className="font-semibold mb-3">Instagram Stories</h3>
                  <div className="space-y-2">
                    {videoScripts.instagram_stories?.map((clip, i) => (
                      <div key={i} className="bg-studio-900 rounded-lg p-3 text-sm text-studio-200">
                        {clip}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {narrationText && (
              <div className="card">
                <h3 className="font-semibold mb-3">Narração Gerada</h3>
                <p className="text-studio-200 mb-4 whitespace-pre-wrap">{narrationText}</p>
                <button
                  onClick={() => navigator.clipboard.writeText(narrationText)}
                  className="btn-secondary flex items-center justify-center gap-2"
                >
                  <Copy size={16} /> Copiar Narração
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === 'instagram' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Instagram size={24} className="text-accent" />
              Gerador Instagram
            </h2>

            <button
              onClick={generateIgPost}
              disabled={igLoading || !selectedCategory || !productName}
              className="btn-primary flex items-center justify-center gap-2"
            >
              {igLoading ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}
              Gerar Post
            </button>

            {igPost && (
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">{igPost.post_type}</h3>
                  <span className="text-xs px-3 py-1 bg-accent text-white rounded-full">
                    {igPost.content_pillar}
                  </span>
                </div>

                <div className="mb-6 p-4 bg-studio-900 rounded-lg">
                  <p className="text-studio-200 mb-3">{igPost.caption}</p>
                  <div className="flex flex-wrap gap-2">
                    {igPost.hashtags.map((tag, i) => (
                      <span key={i} className="text-sm text-accent">#{tag}</span>
                    ))}
                  </div>
                  <button
                    onClick={() => navigator.clipboard.writeText(igPost.caption)}
                    className="mt-3 text-xs text-accent hover:text-accent-light flex items-center gap-2"
                  >
                    <Copy size={14} /> Copiar Caption
                  </button>
                </div>

                <div className="mb-6">
                  <h4 className="font-semibold mb-3">Slides do Carrossel</h4>
                  <div className="grid grid-cols-2 gap-3">
                    {igPost.slides?.map((slide, i) => (
                      <div key={i} className="bg-studio-900 rounded-lg p-3">
                        <div className="text-sm text-studio-300">{slide}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="text-xs text-studio-400 space-y-1">
                  <p><strong>Melhor hora:</strong> {igPost.best_posting_time}</p>
                  <p><strong>CTA:</strong> {igPost.cta_type}</p>
                  <p><strong>Alt Text:</strong> {igPost.alt_text}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <footer className="border-t border-studio-700 bg-studio-800/50 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-studio-400">
          Chamaroma Studio v1.0 · Powered by Google Gemini · 17 Aromas · 10 Prompts Ultimate
        </div>
      </footer>
    </div>
  )
}
