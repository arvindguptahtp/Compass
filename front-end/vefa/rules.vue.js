const Vefa = require("./vefa-html/framework")

module.exports = (cfg, locals) => {
    locals = Object.assign(
        locals, 
        {
            Vefa
        }
    )

    return {
        test: /\.vue?$/,
        use: [
            {
                loader: 'vue-loader',
                options: {
                    loaders: {
                        "pug": [
                            {
                                loader: "vefa-html-loader",
                                options: {
                                    locals: locals,
                                }
                            },
                        ]
                    }
                }
            }
        ]
    }
}
