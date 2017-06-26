const reporter = require("./reporter.js")

module.exports = (config) => {
    let postcss_opts = {
        mq: {
            sort: true
        },
        pxtorem: {
            rootValue: 16,
            unitPrecision: 3,
            replace: true,
            propWhiteList: [],
            mediaQuery: true
        },
        cssnext: {
            features: {
                rem: false,
                customProperties: false
            }
        },
        cssnano: {
            discardUnused: {
                fontFace: false
            },
            autoprefixer: false
        }
    }
    postcss_opts = config.styles.postcss
        ? Object.assign(postcss_opts, config.styles.postcss)
        : postcss_opts
    postcss_opts.cssnext = config.styles.browsers
        ? Object.assign(postcss_opts.cssnext, config.styles.browsers)
        : {}
    
    let library_opts =config.styles.libraries 
        ? config.styles.libraries
        : ['../vefa/vefa-css/*']

    return {
        test: /\.styl$/,
        use: [
            {
                loader: "vefa-export-loader",
                options: config.styles
            },
            {
                loader: "postcss-loader",
                options: {
                    sourceMap: true,
                    plugins: () => {
                        let pcss_arr = [
                            // require('postcss-write-svg'), 
                            // require('postcss-brand-colors'), 
                            require('rucksack-css'), 
                            // require('postcss-pxtorem')(postcss_opts.pxtorem), 
                            require('postcss-cssnext')(postcss_opts.cssnext), 
                            require('css-mqpacker')(postcss_opts.mq), 
                        ]

                        // if (config.PROD) {
                        //     pcss_arr.push (require('cssnano')(postcss_opts.cssnano))
                        // }

                        return pcss_arr

                    }
                }
            },
            {
                loader: "stylus-loader",
                options: {
                    import: library_opts,
                    define: config.styles.define
                }
            }
        ]
    }
}
