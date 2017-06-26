const reporter = require("../reporter.js")

module.exports = (locals) => {
    return {
        get_expression (values) {
            if (values) {
                delete values.filename
                
                values = Object.keys(values).join(" ")
                
                if ((values.match(/\"/g) || []).length % 2) {
                    values = `${ values }"`
                }
                
                return values
            }

            return null
        }
    }
}
