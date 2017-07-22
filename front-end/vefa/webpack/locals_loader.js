const reporter = require("../lib/reporter.js")
const fs = require('fs')

class LocalsLoader {
    constructor (options, locals) { 
        this.opts = options
        this.locals = locals
        this.locals.load = false
    }

    file_to_locals (load_obj, compilation) {
        let refs = fs.readdirSync (load_obj.dir)

        refs.forEach(
            (file) => {
                if (file.includes('.yaml') || file.includes('.yml')) {
                    let data = path.resolve(`${load_obj.dir}/${file}`)
                    let file_name = file.split(".")[0]
                    
                    if (file_name) {
                        this.locals[file_name] = yaml.safeLoad( fs.readFileSync(data, 'utf8') );
                    }
                }
            }
        )
    }

    file_to_json (load_obj) {
        if (load_obj.output) {
            let output = load_obj.output
            let refs = fs.readdirSync(load_obj.dir)
            
            if (!fs.existsSync(output.dir)) {
                fs.mkdirSync (output.dir)
            }

            refs.forEach(
                (file) => {
                    if (file.includes('.yaml') || file.includes('.yml')) {
                        let file_name = file.split(".")[0]
                        let file_name_path = `${output.dir}/${file_name}.json`

                        if (!output.files || output.files.includes(file_name)) {
                            fs.writeFileSync(
                                file_name_path, 
                                JSON.stringify(this.locals[file_name])
                            )
                        }
                    }
                }
            )
        }
    }
    
    apply (compiler) {
        compiler.plugin(
            'compilation', 
            (compilation) => {
                if (this.opts) {
                    this.opts.forEach(
                        (local) => {
                            this.file_to_locals(local, compilation)
                            this.file_to_json(local)
                        }
                    )
                }
            }
        )

        compiler.plugin(
            'watch-run', 
            (watching, callback) => {
                watching.compiler.plugin(
                    'compilation',
                    (compilation) => {
                        if (this.opts) {
                            this.opts.forEach(
                                (local) => {
                                    this.file_to_locals(local, compilation)
                                    this.file_to_json(local)
                                }
                            )
                        }
                    }
                )
                
                callback()
            }
        )

        return
    }

}

module.exports = LocalsLoader
