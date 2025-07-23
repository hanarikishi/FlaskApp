// 使用する環境
module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
// ルールセット
extends: [
    'eslint:recommended',
    'plugin:vue/recommended',
  ],
// Js構文のバージョンや形式
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module',
  },
// ルールの個別設定・無効か
  rules: {
    'vue/multi-word-component-names': 'off', // 単語1つのコンポーネント名でもOKに
  },
};

