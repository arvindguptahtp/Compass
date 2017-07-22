const reporter = require("../lib/reporter.js")
const Vefa = require("../vefa")

module.exports = (cfg, locals) => {
    locals = Object.assign(
        locals, 
        require("../lib/django")(locals)
    )


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
                        "js": [{
                            loader: 'babel-loader',
                            options: {
                                presets: ["env"]
                            }
                        }], 
                        "pug": [
                            {
                                loader: "vefa-html-loader",
                                options: {
                                    locals,
                                    pretty: true,
                                    cache: true,
                                    filters: {
                                        md ( block, opts ) {
                                        return locals.markdown(block);
                                        }
                                    }
                                }
                            },
                        ]
                    }
                }
            }
        ]
    }
}
