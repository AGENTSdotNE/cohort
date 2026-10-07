import js from '@eslint/js'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import storybook from 'eslint-plugin-storybook'
import { globalIgnores } from 'eslint/config'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs['recommended-latest'],
      reactRefresh.configs.vite,
    ],
    plugins: { 'simple-import-sort': simpleImportSort },
    rules: {
      'simple-import-sort/imports': 'error',
      'simple-import-sort/exports': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
    },
  },
  {
    // Written by `npx shadcn@latest add`. Reformatting them on every add is churn, and they
    // deliberately export variant helpers next to the component.
    files: ['src/components/ui/**/*.{ts,tsx}'],
    rules: {
      'simple-import-sort/imports': 'off',
      'simple-import-sort/exports': 'off',
      'react-refresh/only-export-components': 'off',
    },
  },
  storybook.configs['flat/recommended'],
)
