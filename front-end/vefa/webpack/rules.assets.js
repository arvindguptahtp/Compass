const reporter = require("../lib/reporter.js")

module.exports = (config) => {
    return {
        test: /\.(eot|woff|ttf|otf|pdf|ico|xml|woff2|json|svg|)$/i,
        use: [
            {
                loader: "vefa-asset-loader",
                options: config.assets.io
            }
        ]
    }
}
