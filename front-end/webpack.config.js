'use strict'
require('yamlify/register')

// file system funcions
const path = require('path')
const fs = require('fs')

// processor functionalities
const webpack = require('webpack')

const locals_loader = require("./vefa/locals_loader")
const notifier = require("webpack-notifier")
const browser_sync = require('browser-sync-webpack-plugin')
const friendly_errors = require('friendly-errors-webpack-plugin')
const yaml = require('js-yaml')
const reporter = require("./vefa/reporter")

const typogr = require('typogr')
const md = require('markdown-it')({
    html: true,
    linkify: true,
    typographer: true
})

module.exports = (env) => {
    // important environment flags
    let CFG = env.init ? require(`${__dirname}/${env.init}`) : null
    let PROD = CFG.PROD = env.production ? true : false
    let DJANGO = CFG.DJANGO = env.django ? true : false
    
    let locals = {
        prod: PROD,
        django: DJANGO,
        basedir: (function(){
            let base_dir_arr = [__dirname, CFG.components]
            return base_dir_arr.join("/")
        })(),
        markdown: function(prerender){
            md
                .use(require('markdown-it-attrs'))
                .use(require('markdown-it-abbr'))
                .use(require('markdown-it-deflist'))
                .use(require('markdown-it-footnote'))
                .use(require("markdown-it-block-image"))
                .use(require('markdown-it-anchor'))

            return typogr(md.render(prerender)).typogrify()
        },
    }

    let config = {
        entry: CFG.entries,
        output: {
            filename: `${CFG.publicPath}[name].js`,
            path: path.resolve(__dirname, CFG.build),
            publicPath: CFG.publicPath,
        },
        module: {
            rules: [
                require('./vefa/rules.babel')(CFG),
                require('./vefa/rules.vue')(CFG, locals),
                require('./vefa/rules.styles')(CFG),
                require('./vefa/rules.django')(CFG, locals),
                require('./vefa/rules.images')(CFG),
                require('./vefa/rules.assets')(CFG)
            ]
        },
        context: path.resolve(CFG.src),
        cache: !PROD,
        target: 'web',
        devtool: 'inline-eval-cheap-source-map',
        resolve: {
            extensions: [".js", ".json", '.yaml', '.yml', '.vue', '.styl', '.pug'],
        },
        plugins: [
            new locals_loader(CFG.locals, locals),
            new webpack.DefinePlugin({
                'process.env': {
                    NODE_ENV: PROD ? '"production"' : '"development"'
                }
            }),
            new notifier({
                title: CFG.project,
                alwaysNotify: false,
                skipFirstNotification: false
            }),
            new friendly_errors(),
            new browser_sync({
                server: DJANGO ? false : CFG.build,
                proxy: DJANGO ? "localhost:8000" : false,
                port: 1515,
                ui: {
                    port: 8002,
                    weinre: 8003,
                },
                reloadDelay: 500,
                // reloadDebounce: 2000,
                ghostMode: {
                    clicks: true,
                    forms: true,
                    scroll: true,
                },
                logPrefix: CFG.project + " -- DEV",
                open: false,
                reloadOnRestart: true,
                injectChange: false,
                notify: false,
            }),
        ]
    }

    return config
}
