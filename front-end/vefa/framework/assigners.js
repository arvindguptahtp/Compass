const _ = require('../lib/verify')
const log = require("../lib/reporter")
const convert = require("../lib/convert")


module.exports = {
    $data (vefa_obj) {
        if (_.has_props(vefa_obj.$data)) {
            
            Object.keys(vefa_obj.$data).forEach( (key) => {
                // will aways override

                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        get: () => {
                            return vefa_obj.$data[key]
                        },
                        set: (val) => {
                            vefa_obj.$data[key] = val
                            this.$computed(vefa_obj)
                        },
                        configurable: true,
                        enumerable: true
                    }
                )
            })
        }
    },
    
    $methods (vefa_obj) {
        if (_.has_props(vefa_obj.$methods)) {
            Object.keys(vefa_obj.$methods).forEach( (key) => {
                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        value: vefa_obj.$methods[key],
                        writeable: true,
                        configurable: true,
                        enumerable: true
                    }
                )
            })
        }
    },

    $options (vefa_obj) {
        if (_.has_props(vefa_obj.$options)) {
            Object.keys(vefa_obj.$options).forEach( (key) => {
                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        get: () => {
                            return vefa_obj.$options[key]
                        },
                        set: (val) => {
                            vefa_obj.$options[key] = val
                            assign_$computed(vefa_obj)
                        },
                        configurable: true,
                        enumerable: true
                    }
                )
            })
        }
    },

    $computed (vefa_obj) {
        if (_.has_props(vefa_obj.$computed)) {
            Object.keys(vefa_obj.$computed).forEach( (key) => {
                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        value: vefa_obj.$computed[key].call(vefa_obj),
                        writeable: true,
                        configurable: true,
                        enumerable: true
                    }
                )
            })
        }
    },

    $dom (vefa_obj) {
        if (_.has_props(vefa_obj.$dom)) {
            let dom  = convert.unarrize(vefa_obj.$dom)
            Object.keys(dom).forEach( (key) => {
                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        value: dom[key],
                        writeable: true,
                        configurable: true,
                        enumerable: true
                    }
                )
            })
        }
    }
}
