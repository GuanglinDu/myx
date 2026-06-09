# Organize Tailwind CSS utilities

- What are the best practices to group the Tailwind utilities? - Google AI Overview
- Group related properties together logically (Layout → Spacing → Sizing → Typography → Colors → States). Use the official Prettier Plugin for Tailwind CSS to automate this sorting process.

## Standardized Class Order

When writing multiple classes, always follow a predictable, sequential pattern. This makes your code instantly readable across your team.

- Layout & Display: flex, grid, hidden, absolute, relative
- Spacing & Positioning: m-, p-, top-, left
- Dimensions: w-, h-, max-w-, max-h
- Typography: font-, text-, leading-, tracking
- Visuals & Effects: bg-, border-, shadow-, rounded-, opacity
- Variants & States: hover:, focus:, dark:, disabled:

## Tailwind class sorter (prettier-plugin-tailwindcss)

- [prettier-plugin-tailwindcss](https://github.com/tailwindlabs/prettier-plugin-tailwindcss)
- [Automatic Class Sorting with Prettier](https://tailwindcss.com/blog/automatic-class-sorting-with-prettier)

### Configure Prettier

```shell
npm install -D prettier prettier-plugin-tailwindcss
```

Create or update your Prettier configuration file (such as `.prettierrc` or `prettier.config.js`) in the root directory of your project. Add the plugin to your configurations (Tailwind CSS v3):

```json
{
  "plugins": ["prettier-plugin-tailwindcss"],
  "tailwindConfig": "./tailwind.config.js"
}
```

- Note: For Tailwind CSS v4+ environments, you may also want to specify your main CSS entry point using the tailwindStylesheet property so that the plugin can accurately group custom utilities:

```json
{
  "plugins": ["prettier-plugin-tailwindcss"],
  "tailwindStylesheet": "./src/styles/global.css"
}
```

### Set Up Auto-Format on Save (Optional)

If you are using Visual Studio Code, you can automate this grouping behavior so that classes sort every time you save a file. Install the official Prettier - Code formatter extension and add the following settings to your VS Code settings.json:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```
