const chalk = require('chalk')

module.exports = {
    warn (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgYellowBright.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    },
    err (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgRedBright.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    },
    impt (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgGreenBright.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    },
    info (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgWhite.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    }
}
