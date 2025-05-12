/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [ './templates/**/*.{html,js}', // Assurez-vous que le chemin correspond à celui de vos fichiers templates
    './path/to/other/templates/*.html', // Ajoutez d'autres chemins si nécessaire
    // Ajoutez d'autres extensions si vous utilisez des formats spécifiques comme jsx, vue, etc.
    // ],
  theme: {
    extend: {
      colors: {
        primary: '#4F46E5', // Couleur principale
        secondary: '#10B981', // Couleur secondaire
      },
    },
  },
  plugins: [],

  
}

