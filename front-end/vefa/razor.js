const razor = require("css-razor").default
const fs = require('fs')
const yargs = require('yargs').argv
const yaml = require('js-yaml')

const postcss = require('postcss')

let config = yaml.safeLoad( fs.readFileSync(`${__dirname}/../${ yargs.config }`, 'utf8') )

let files = config.styles.emit.forEach( (file) => {
    let file_expect = `./${ config.build }${ config.styles.build }${file.replace("styl", "css")}`
    let file_mid = `./${ config.build }${ config.styles.build }${file.replace("styl", "mid.css")}`
    let file_min = `./${ config.build }${ config.styles.build }${file.replace("styl", "min.css")}`
    
    console.log(`Razoring: ${file_expect}`)

    razor({
        html: [`./${ config.build }/**/*.html`],
        css: file_expect,
        ignore: [],
        outputFile: file_mid,
        stdout: true,
        report: true,
    })

    fs.readFile(file_expect, (err, css) => {
        postcss()
            .use(
                require('cssnano')({
                    discardUnused: {
                        fontFace: false
                    },
                    autoprefixer: false, 
                })
            )
            .process(css, { from: file_mid, to: file_min })
            .then(result => {
                fs.writeFile(file_min, result.css)
            })
    })
            
})
