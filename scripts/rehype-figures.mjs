// Markdown-Bilder und eine optionale kursiv gesetzte Bildunterschrift.
export default function figures() {
  return (tree) => {
    function walk(parent) {
      if (!parent.children) return;
      for (let i = 0; i < parent.children.length; i++) {
        const node = parent.children[i];
        if (node.tagName === "img") {
          node.properties ||= {};
          node.properties.loading = "lazy";
          node.properties.decoding = "async";
        }
        const image =
          node.tagName === "p" &&
          node.children?.length === 1 &&
          (node.children[0].tagName === "img" ||
            (node.children[0].tagName === "a" &&
              node.children[0].children?.[0]?.tagName === "img"));
        if (image) {
          node.tagName = "figure";
          let j = i + 1;
          while (
            parent.children[j]?.type === "text" &&
            !parent.children[j].value.trim()
          )
            j++;
          const caption = parent.children[j];
          if (
            caption?.tagName === "p" &&
            caption.children?.length === 1 &&
            caption.children[0].tagName === "em"
          ) {
            node.children.push({
              type: "element",
              tagName: "figcaption",
              properties: {},
              children: caption.children[0].children,
            });
            parent.children.splice(i + 1, j - i);
          }
        }
        walk(node);
      }
    }
    walk(tree);
  };
}
