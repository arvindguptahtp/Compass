const reporter = require("../lib/reporter.js")

module.exports = (locals) => ({
    test: /\.js$/,
    exclude: /(node_modules|bower_components)/,
    use: [
        {
            loader: 'babel-loader',
            // options: {
            //     presets: ['env', 'stage-2']
            // }
        }    
    ]
})
