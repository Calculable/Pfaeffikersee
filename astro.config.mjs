import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import figures from "./scripts/rehype-figures.mjs";
export default defineConfig({
  site: "https://www.pfäffikersee.org",
  output: "static",
  devToolbar: { enabled: false },
  markdown: {
    processor: unified({ rehypePlugins: [figures], smartypants: false }),
  },
});
