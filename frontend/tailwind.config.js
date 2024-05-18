module.exports = {
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                "primary": "#ffe18c",
                "c-orange": "#ffc071",
                "c-light-orange": "#ffdaa8",
                "c-pink": "#ffb899",

                "c-selected": "#ffedba",
                "c-selected-text": "#be8208",

                "c-assets-padding": "#f6f4f0",

                "c-black": "#313131",
                "c-title": "#5f5f5f",
                "c-text": "#8b8b8b",
            }
        },

    },
    variants: {
        extend: {},
    },
    plugins: [],
    darkMode: 'false',
}