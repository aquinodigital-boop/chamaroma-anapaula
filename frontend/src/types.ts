export interface PiramideOlfativa {
  saida: string;
  corpo: string;
  fundo: string;
}

export interface CopyRaioX {
  titulo_seo_ml: string;
  bullets_matadores: string[];
  gancho_emocional: string;
  descricao_sensorial: string;
  cta_fechamento: string;
}

export interface MockupVisual {
  cor_cera: string;
  hex_cera: string;
  gradiente_secundario?: string;
}

export interface Aroma {
  id: string;
  nome: string;
  emoji: string;
  categoria: 'frescos' | 'florais' | 'doces' | 'especiais';
  descricao: string;
  notas_sensoriais: string[];
  mood: string[];
  ocasioes: string[];
  piramide: PiramideOlfativa;
  copy_raio_x: CopyRaioX;
  mockup: MockupVisual;
}

export const AROMA_CATEGORIES: { id: string; label: string; emoji: string; color: string }[] = [
  { id: 'todos', label: 'Todos', emoji: '🕯️', color: 'from-studio-500 to-studio-400' },
  { id: 'frescos', label: 'Frescos', emoji: '🍋', color: 'from-lime-500 to-emerald-500' },
  { id: 'florais', label: 'Florais', emoji: '🌸', color: 'from-pink-500 to-rose-500' },
  { id: 'doces', label: 'Doces', emoji: '🍪', color: 'from-amber-500 to-orange-500' },
  { id: 'especiais', label: 'Especiais', emoji: '✨', color: 'from-violet-500 to-purple-500' },
];

export interface GeneratedPrompts {
  analysis?: string;
  creative_concept?: string;
  visual_intention?: string;
  avoided?: string;
  hero_shot: string;
  dark_moody: string;
  ingredient_story: string;
  lifestyle: string;
  anti_cliche: string;
  ambience: string;
  close_up: string;
  social_media: string;
  smoke_aroma: string;
  premium_context: string;
}

export type PromptKey = keyof Omit<GeneratedPrompts, 'analysis' | 'creative_concept' | 'visual_intention' | 'avoided'>;

export const PROMPT_KEYS: PromptKey[] = [
  'hero_shot', 'dark_moody', 'ingredient_story', 'lifestyle', 'anti_cliche',
  'ambience', 'close_up', 'social_media', 'smoke_aroma', 'premium_context'
];

export const PROMPT_LABELS: Record<PromptKey, string> = {
  hero_shot: 'Hero Shot',
  dark_moody: 'Dark & Moody',
  ingredient_story: 'Ingredient Story',
  lifestyle: 'Lifestyle',
  anti_cliche: 'Anti-Clichê',
  ambience: 'Ambience',
  close_up: 'Close-Up Macro',
  social_media: 'Social Media',
  smoke_aroma: 'Smoke & Aroma',
  premium_context: 'Premium Context',
};

export type Category = 'velas' | 'home_spray';

export interface VideoScripts {
  clips_ml: any[];
  instagram_feed: any[];
  instagram_stories: any[];
}

export interface InstagramPost {
  post_type: string;
  caption: string;
  hashtags: string[];
  slides: any[];
  best_posting_time: string;
  content_pillar: string;
  cta_type: string;
  alt_text: string;
}
