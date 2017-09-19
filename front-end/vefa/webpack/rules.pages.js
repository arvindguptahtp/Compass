const reporter = require("../lib/reporter.js")
const Vefa = require("../vefa")

module.exports = (config, locals) => {
    locals = Object.assign(
        locals, 
        {
            Vefa
        }
    )

    return {
        test: /\.md$/,
        use: [
            {
                loader: "vefa-export-loader",
                options: config.pages
            },
            {
                loader: "vefa-html-loader",
                options: {
                    context: config.templates.context || true,
                    emit: config.templates.emit || false,
                    pretty: true,
                    cache: true,
                    locals,
                    filters: {
                        md ( block, opts ) {
                           return locals.markdown(block);
                        }
                    }
                }
            },
            {
                loader: "vefa-pages-loader",
                options: {
                    locals,
                    config: config.pages
                }
            }
            // {
            //     loader: "vefa-import-loader",
            //     options: {
            //         import: config.import,
            //         locals: locals
            //     }
            // },
        ]
    }
}
