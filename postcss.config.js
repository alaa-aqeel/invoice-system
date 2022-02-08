module.exports = {
    plugins: [
        require('tailwindcss'),
        require('autoprefixer')
    ],
    purge: {
        enabled: true,
        content: ['./templates/**/*.html'],
    },
}