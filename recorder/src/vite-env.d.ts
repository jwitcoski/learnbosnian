/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_AUDIO_API_URL: string;
  readonly VITE_AUDIO_PUBLIC_BASE: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
