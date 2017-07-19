const reporter = require("../reporter.js")

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
