const reporter = require("../lib/reporter.js")
const Vefa = require("../vefa")

module.exports = (config, locals) => {

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
        test: /\.pug$/,
        use: [
            {
                loader: "vefa-export-loader",
                options: config.templates
            },
            {
                loader: "vefa-html-loader",
                options: {
                    context: config.templates.context || true,
                    emit: config.templates.emit || false,
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
