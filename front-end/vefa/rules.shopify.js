const reporter = require("./reporter.js")

const common = require("./vefa-html/common.js")()

module.exports = (config, locals) => {

    locals = Object.assign(
        locals, 
        require("./vefa-html/structure")(locals)
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
                    filters: {
                        md ( block, opts ) {
                           return locals.markdown(block);
                        },
                        v (block, expression) {
                            expression = common.get_expression(expression)
                            return `{{ ${ expression } }}`
                        }
                    }
                }
            },
        ]
    }
}


// filters: Object.assign(
//     require(`${CFG.src}/vefa-html/pug.js`)(locals)
// )
