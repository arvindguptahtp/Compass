const reporter = require("./reporter.js")

const common = require("./vefa-html/common.js")()
const Vefa = require("./vefa-html/framework")

module.exports = (config, locals) => {

    locals = Object.assign(
        locals, 
        require("./vefa-html/structure")(locals)
    )


    locals = Object.assign(
        locals, 
        {
            Vefa
        }
    )

    
    return {
        test: /\.pug$/,
        use: [
            {
                loader: "vefa-export-loader",
                options: config.templates
            },
            {
                loader: "vefa-html-loader",
                options: {
                    locals: locals,
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
