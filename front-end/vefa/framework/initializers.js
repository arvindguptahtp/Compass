const teardowns = require('./teardowns')
const log = require("../lib/reporter")
const convert = require("../lib/convert")

module.exports = {
    initialize_$members (vefa_obj, obj) {
        let seed = Object.assign({}, obj)
        
        // if (seed.provide) {
        //     seed.provide.forEach(
        //         (tuple) => {
        //             if (typeof tuple[1] == "function" ) {
        //                 injector.set(        
        //                     tuple[0], 
        //                     tuple[1].call(seed)
        //                 )
        //             }
        //             else {
        //                 injector.set(
        //                     tuple[0], 
        //                     tuple[1]
        //                 )
        //             }
        //         }
        //     )
        // }

        Object.defineProperty(
            vefa_obj,
            '$data',
            {
                value: seed.data || {},
                writable: true,
                configurable: false,
                enumerable: true
            }
        )
        
        Object.defineProperty(
            vefa_obj,
            '$methods',
            {
                value: seed.methods || {},
                writable: true,
                configurable: false,
                enumerable: true
            }
        )
        
        Object.defineProperty(
            vefa_obj,
            '$computed',
            {
                value: seed.computed || {},
                writable: true,
                configurable: false,
                enumerable: true
            }
        )


        Object.defineProperty(
            vefa_obj,
            '$dom',
            {
                value: convert.arrize(seed.dom),
                writable: true,
                configurable: false,
                enumerable: true
            }
        )

        // Object.defineProperty(
        //     vefa_obj,
        //     '$inject',
        //     {
        //         value: seed.inject || [],
        //         writable: true,
        //         configurable: false,
        //         enumerable: true
        //     }
        // )

        teardowns.clean_seed(seed)
        
        // set the remainder items to $options for later weaving
        Object.defineProperty(
            vefa_obj,
            '$options',
            {
                value: seed || {},
                writable: true,
                configurable: false,
                enumerable: true
            }
        )

        seed = {}
    }
}
