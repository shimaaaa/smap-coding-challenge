const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');


module.exports = {
    context: __dirname,
    entry: './consumption/assets/js/app.js',

    output: {
        filename: "[name]-[hash].js",
        path: path.resolve('./consumption/assets/bundles/'),
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new VueLoaderPlugin(),
    ],

    module: {
        rules:  [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
              test: /\.css/,
              use: ['vue-style-loader', 'css-loader']
            }
        ],
    },
    resolve: {
        alias: {
            vue: 'vue/dist/vue.js',
            '@': path.resolve('./consumption/assets/js/')
        },
    },
}