
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // 啟用 React Plugin
  plugins: [react()],

  // 開發伺服器設定
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,

    // API Proxy
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
