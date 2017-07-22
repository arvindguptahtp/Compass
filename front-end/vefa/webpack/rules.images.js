const reporter = require("../lib/reporter.js")

module.exports = (config) => {
    
    let img_opts = {
        imagemin: {
            gifsicle: { interlaced: false },
            jpegtran: {
                progressive: true,
                arithmetic: false
            },
            optipng: { optimizationLevel: 5 }
        }
    }
    img_opts = config.images.options
        ? Object.assign(img_opts, config.images.options)
        : img_opts


    let webp_opts = {
        quality: 80
    }
    img_opts = config.webp.options 
        ? Object.assign(webp_opts, config.webp.options)
        : webp_opts

    let img_io = {
        passSource: true
    }
    img_io = config.images.io
        ? Object.assign(img_io, config.images.io)
        : img_io
    

    return {
        test: /\.(jpe?g|png|gif)$/i,
        use: [
            {
                loader: "vefa-asset-loader",
                options: config.webp.io
            },
            {
                loader: "webp-loader",
                options: webp_opts
            },
            {
                loader: "vefa-asset-loader",
                options: img_io
            },
            {
                loader: "image-webpack-loader",
                options: img_opts
            }
        ]        
    }
}
