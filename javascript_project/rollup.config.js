import resolve from "@rollup/plugin-node-resolve";

export default {
  input: "C:\Users\Isak\Documents\Programmeringsfiler\javascript_project\app.js",
  output: [
    {
      format: "esm",
      file: "C:\Users\Isak\Documents\Programmeringsfiler\javascript_project\bundle.js",
    },
  ],
  plugins: [resolve()],
};