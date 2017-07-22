const _ = require('../lib/verify')
const log = require("../lib/reporter")

module.exports = {
    unarrize (seed = {}) {
        if (Object.keys(seed)) {
            let obj = Object.assign({}, seed)
            
            Object.keys(obj).forEach(
                (key) => {
                    if (_.is_object(obj[key])) {
                        obj[key] = this.unarrize(obj[key])
                    }
                    else if (Array.isArray(obj[key])) {
                        obj[key] = obj[key].join(" ")
                    }
                }
            )
            
            return obj
        }

        return seed
    },

    arrize (seed = {}) {
        if (Object.keys(seed)) {
            
            let obj = Object.assign({}, seed)
            
            Object.keys(obj).forEach(
                (key) => {
                    if (_.is_object(obj[key]) ) {
                        obj[key] = this.arrize(obj[key])
                    }
                    else {
                        obj[key] = obj[key].split(" ")
                    }
                }
            )

            return obj
        }
        return seed
    }

}
